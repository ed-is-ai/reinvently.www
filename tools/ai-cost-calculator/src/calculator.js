const RANGE_KEYS = ["low", "base", "high"];

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function clamp(value, min, max) {
  const number = Number(value);
  if (!Number.isFinite(number)) return min;
  return Math.min(max, Math.max(min, number));
}

function getPlan(provider, planId) {
  return provider.plans.find(plan => plan.id === planId) || provider.plans[0];
}

function getMix(data, mixId) {
  return data.modelMixes.find(mix => mix.id === mixId) || data.modelMixes[0];
}

function getOperatingModel(data, modelId) {
  return data.operatingModels.find(model => model.id === modelId) || null;
}

function getRepositoryScale(data, scaleId) {
  return data.repositoryScales.find(scale => scale.id === scaleId) || data.repositoryScales[0];
}

function getChangeScope(data, scopeId) {
  return data.changeScopes.find(scope => scope.id === scopeId) || data.changeScopes[0];
}

function workloadAdjustments(data, state) {
  const repositoryScale = getRepositoryScale(data, state.repositoryScale);
  const changeScope = getChangeScope(data, state.changeScope);
  return {
    repositoryScale,
    changeScope,
    repositoryInputMultiplier: repositoryScale.inputMultiplier,
    inputMultiplier: repositoryScale.inputMultiplier * changeScope.inputMultiplier,
    outputMultiplier: changeScope.outputMultiplier
  };
}

export function applyOperatingModel(data, inputState, modelId) {
  const profile = getOperatingModel(data, modelId);
  if (!profile) return clone(inputState);

  const state = clone(inputState);
  state.operatingModel = profile.id;
  state.modelMix = profile.modelMix;
  state.scenario = clone(profile.scenario);
  return state;
}

function money(value) {
  return "$" + Math.round(value).toLocaleString("en-GB");
}

function moneyRange(low, high) {
  return Math.round(low) === Math.round(high) ? money(low) : `${money(low)}–${money(high)}`;
}

function millions(value) {
  if (value >= 1000) return `${(value / 1000).toFixed(1).replace(/\.0$/, "")}B`;
  return `${value.toFixed(value >= 100 ? 0 : 1).replace(/\.0$/, "")}M`;
}

function approximateCodeNote(tokensK, noun) {
  const characters = tokensK * 4000;
  const lowLines = Math.round(characters / 80);
  const highLines = Math.round(characters / 40);
  const format = value => value.toLocaleString("en-GB");
  return `${format(tokensK * 1000)} tokens ≈ ${format(characters)} characters; roughly ${format(lowLines)}–${format(highLines)} lines if the ${noun} were code alone`;
}

function profileTokenNote(data, state, kind) {
  const adjustments = workloadAdjustments(data, state);
  const isInput = kind === "input";
  const baseK = isInput ? state.scenario.inputKPerRun : state.scenario.outputKPerRun;
  const multiplier = isInput ? adjustments.inputMultiplier : adjustments.outputMultiplier;
  const effectiveK = baseK * multiplier;
  return `${approximateCodeNote(baseK, isInput ? "context" : "output")}; ${effectiveK.toLocaleString("en-GB")}k after workload adjustments`;
}

function workloadAdjustmentMarkup(data, state) {
  const adjustments = workloadAdjustments(data, state);
  const effectiveInputK = state.scenario.inputKPerRun * adjustments.inputMultiplier;
  const effectiveOutputK = state.scenario.outputKPerRun * adjustments.outputMultiplier;
  return `
    Applied workload adjustment: <strong>${adjustments.inputMultiplier.toFixed(2).replace(/\.?0+$/, "")}× input</strong>
    and <strong>${adjustments.outputMultiplier.toFixed(2).replace(/\.?0+$/, "")}× output</strong>.
    Effective run: ${effectiveInputK.toLocaleString("en-GB")}k input · ${effectiveOutputK.toLocaleString("en-GB")}k output.
    Assumes indexed or graph-based code search is configured.`;
}

function scenarioUsage(data, state, factor = 1) {
  const scenario = state.scenario;
  const adjustments = workloadAdjustments(data, state);
  const runs = state.seats * scenario.runsPerUserDay * scenario.workingDays * factor;
  const totalInputM = runs * scenario.inputKPerRun * adjustments.inputMultiplier / 1000;
  const readShare = clamp(scenario.cacheReadPct, 0, 95) / 100;
  const writeShare = clamp(scenario.cacheWritePct, 0, 95 - readShare * 100) / 100;

  return {
    runs,
    uncachedInputM: totalInputM * Math.max(0, 1 - readShare - writeShare),
    cacheReadM: totalInputM * readShare,
    cacheWriteM: totalInputM * writeShare,
    outputM: runs * scenario.outputKPerRun * adjustments.outputMultiplier / 1000
  };
}

function actualUsage(state) {
  return {
    runs: null,
    uncachedInputM: clamp(state.actual.uncachedInputM, 0, 1000000),
    cacheReadM: clamp(state.actual.cacheReadM, 0, 1000000),
    cacheWriteM: clamp(state.actual.cacheWriteM, 0, 1000000),
    outputM: clamp(state.actual.outputM, 0, 1000000)
  };
}

function priceUsage(provider, mix, usage, state) {
  if (provider.usagePricingMode === "unquantified") {
    return {
      cost: null,
      byModel: [],
      firstPartyShare: 0
    };
  }

  const thirdPartyShare = provider.hasFirstPartyPool
    ? 1 - clamp(state.cursorFirstPartyPct, 0, 100) / 100
    : 1;

  const byModel = provider.rates.map((rate, index) => {
    const share = mix.shares[index] * thirdPartyShare;
    const processedTokensM =
      usage.uncachedInputM + usage.cacheReadM + usage.cacheWriteM + usage.outputM;
    const cost =
      usage.uncachedInputM * share * rate.input +
      usage.cacheReadM * share * rate.cacheRead +
      usage.cacheWriteM * share * rate.cacheWrite +
      usage.outputM * share * rate.output +
      processedTokensM * share * (provider.tokenSurchargePerM || 0);
    return { rate, share, cost };
  });

  return {
    cost: byModel.reduce((sum, item) => sum + item.cost, 0),
    byModel,
    firstPartyShare: provider.hasFirstPartyPool ? 1 - thirdPartyShare : 0
  };
}

function calculatePoint(provider, plan, mix, usage, state) {
  const seatRate = state.billingTerm === "annual" ? plan.annualSeat : plan.monthlySeat;
  const usesContractInputs = Boolean(plan.requiresContractInputs);
  const contractBase = usesContractInputs
    ? clamp(state.codexContract?.monthlyBaseUsd, 0, 100000000)
    : null;
  const seatCost = usesContractInputs ? contractBase : seatRate * state.seats;
  const pricedUsage = priceUsage(provider, mix, usage, state);
  const usageKnown = pricedUsage.cost !== null;
  const contractIncluded = usesContractInputs
    ? clamp(state.codexContract?.includedCredits, 0, 1000000000) * (provider.creditUsd || 0)
    : null;
  const allowanceKnown = usageKnown && (usesContractInputs || plan.includedMeteredUsdPerSeat !== null);
  const included = usesContractInputs
    ? contractIncluded
    : allowanceKnown ? plan.includedMeteredUsdPerSeat * state.seats : null;
  const overage = !usageKnown
    ? 0
    : allowanceKnown ? Math.max(0, pricedUsage.cost - included) : pricedUsage.cost;

  return {
    seatRate,
    seatCost,
    usageCost: pricedUsage.cost,
    included,
    overage,
    total: seatCost + overage,
    usageKnown,
    usage,
    byModel: pricedUsage.byModel,
    firstPartyShare: pricedUsage.firstPartyShare,
    usesContractInputs,
    contractComplete: !usesContractInputs || contractBase > 0
  };
}

export function calculateEstimate(data, inputState) {
  const state = clone(inputState);
  state.seats = Math.round(clamp(state.seats, 1, 10000));
  const mix = getMix(data, state.modelMix);
  const spread = clamp(state.rangePct, 0, 90) / 100;
  const factors = state.mode === "actual"
    ? { low: 1, base: 1, high: 1 }
    : { low: 1 - spread, base: 1, high: 1 + spread };

  const results = data.providers.map(provider => {
    const plan = getPlan(provider, state.selectedPlans[provider.id]);
    const adjustments = state.mode === "actual" ? null : workloadAdjustments(data, state);
    const points = {};
    RANGE_KEYS.forEach(key => {
      const usage = state.mode === "actual"
        ? actualUsage(state)
        : scenarioUsage(data, state, factors[key]);
      points[key] = calculatePoint(provider, plan, mix, usage, state);
    });
    const needsContractInput = Boolean(plan.requiresContractInputs) && !points.base.contractComplete;
    return {
      provider,
      plan,
      needsContractInput,
      upperBound: provider.usagePricingMode !== "unquantified" &&
        !needsContractInput &&
        points.base.included === null,
      floorOnly: provider.usagePricingMode === "unquantified",
      adjustments,
      ...points
    };
  });

  return {
    state,
    mix,
    factors,
    adjustments: state.mode === "actual" ? null : workloadAdjustments(data, state),
    results
  };
}

function numberField(id, label, value, options = {}) {
  const { min = 0, max = 1000000, step = 1, suffix = "", note = "", path = "" } = options;
  return `
    <label class="cc-field" for="${id}">
      <span class="cc-label">${label}</span>
      <span class="cc-input-wrap">
        <input id="${id}" data-path="${path}" type="number" min="${min}" max="${max}" step="${step}" value="${value}">
        ${suffix ? `<span class="cc-suffix">${suffix}</span>` : ""}
      </span>
      ${note ? `<span class="cc-note">${note}</span>` : ""}
    </label>`;
}

function selectField(id, label, value, options, attribute, note = "") {
  return `
    <label class="cc-field" for="${id}">
      <span class="cc-label">${label}</span>
      <select id="${id}" ${attribute}>
        ${options.map(option => `<option value="${option.value}"${option.value === value ? " selected" : ""}>${option.label}</option>`).join("")}
      </select>
      ${note ? `<span class="cc-note">${note}</span>` : ""}
    </label>`;
}

function planOptions(provider, selectedId) {
  return provider.plans.map(plan =>
    `<option value="${plan.id}"${plan.id === selectedId ? " selected" : ""}>${plan.label}</option>`
  ).join("");
}

function contractFields(provider, plan, state) {
  if (provider.id !== "codex" || !plan.requiresContractInputs) return "";

  return `
    <div class="cc-contract-fields">
      ${numberField("cc-codex-contract-cost", "Monthly contract cost", state.codexContract.monthlyBaseUsd, {
        min: 0,
        max: 100000000,
        step: 1,
        suffix: "USD",
        path: "codexContract.monthlyBaseUsd",
        note: "Monthly-equivalent cost allocated to the selected team"
      })}
      ${numberField("cc-codex-contract-credits", "Included shared credits", state.codexContract.includedCredits, {
        min: 0,
        max: 1000000000,
        step: 1,
        suffix: "credits",
        path: "codexContract.includedCredits",
        note: "25 credits = $1 of model usage at the published conversion"
      })}
    </div>`;
}

function modeFields(data, state) {
  if (state.mode === "actual") {
    return `
      <div class="cc-section-heading">
        <div>
          <h3>Known monthly model usage</h3>
          <p>Enter gross token volumes from a representative provider usage export.</p>
        </div>
      </div>
      <div class="cc-field-grid cc-field-grid-four">
        ${numberField("cc-uncached", "Uncached input", state.actual.uncachedInputM, { step: 0.1, suffix: "MTok", path: "actual.uncachedInputM" })}
        ${numberField("cc-cache-read", "Cache reads", state.actual.cacheReadM, { step: 0.1, suffix: "MTok", path: "actual.cacheReadM" })}
        ${numberField("cc-cache-write", "Cache writes", state.actual.cacheWriteM, { step: 0.1, suffix: "MTok", path: "actual.cacheWriteM" })}
        ${numberField("cc-output", "Output", state.actual.outputM, { step: 0.1, suffix: "MTok", path: "actual.outputM" })}
      </div>`;
  }

  return `
    <div class="cc-section-heading">
      <div>
        <h3>Estimated agent activity</h3>
        <p>Use runs—not completed tickets—as the unit of activity. Results show ±${state.rangePct}% around the base case.</p>
      </div>
    </div>
    <div class="cc-field-grid cc-field-grid-three">
      ${numberField("cc-runs", "Agent runs per user/day", state.scenario.runsPerUserDay, { min: 0, max: 200, step: 0.5, path: "scenario.runsPerUserDay" })}
      ${numberField("cc-days", "Working days/month", state.scenario.workingDays, { min: 1, max: 31, path: "scenario.workingDays" })}
      ${numberField("cc-input-run", "Profile input per run", state.scenario.inputKPerRun, {
        min: 1,
        max: 1000,
        suffix: "k tokens",
        path: "scenario.inputKPerRun",
        note: profileTokenNote(data, state, "input")
      })}
      ${numberField("cc-output-run", "Profile output per run", state.scenario.outputKPerRun, {
        min: 0.1,
        max: 500,
        step: 0.1,
        suffix: "k tokens",
        path: "scenario.outputKPerRun",
        note: profileTokenNote(data, state, "output")
      })}
      ${numberField("cc-read-pct", "Input served from cache", state.scenario.cacheReadPct, { min: 0, max: 95, suffix: "%", path: "scenario.cacheReadPct" })}
      ${numberField("cc-write-pct", "Input written to cache", state.scenario.cacheWritePct, { min: 0, max: 95, suffix: "%", path: "scenario.cacheWritePct" })}
    </div>
    <p class="cc-workload-adjustment">${workloadAdjustmentMarkup(data, state)}</p>`;
}

function renderRangeChart(estimate) {
  const { results, state } = estimate;
  const width = 860;
  const height = 245;
  const plotTop = 28;
  const plotBottom = 190;
  const plotHeight = plotBottom - plotTop;
  const plottableResults = results.filter(result => !result.needsContractInput);
  const max = Math.max(1, ...plottableResults.map(result => result.high.total)) * 1.12;
  const plotLeft = 90;
  const plotRight = 820;
  const spacing = (plotRight - plotLeft) / results.length;
  const xPositions = results.map((_, index) => plotLeft + spacing * (index + 0.5));
  const y = value => plotBottom - value / max * plotHeight;

  let svg = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="cc-chart-title cc-chart-desc">
    <title id="cc-chart-title">Estimated monthly AI coding tool costs</title>
    <desc id="cc-chart-desc">${state.mode === "actual" ? "Dots show costs calculated from entered token usage." : "Lines show low-to-high scenario costs and dots show base estimates."} An upward arrow from Antigravity’s subscription floor shows that paid AI-credit usage can increase its cost.</desc>`;

  for (let index = 0; index <= 4; index++) {
    const value = max * index / 4;
    const tickY = y(value);
    svg += `<line x1="72" y1="${tickY}" x2="840" y2="${tickY}" stroke="#303030" stroke-width="1"/>
      <text x="62" y="${tickY + 3}" fill="#777" font-size="10" text-anchor="end" font-family="Montserrat, sans-serif">${money(value)}</text>`;
  }

  results.forEach((result, index) => {
    const x = xPositions[index];
    if (result.needsContractInput) {
      svg += `<text x="${x}" y="${plotBottom - 12}" fill="${result.provider.color}" font-size="10" font-weight="700" text-anchor="middle" font-family="Montserrat, sans-serif">contract inputs</text>
        <text x="${x}" y="216" fill="#d0d0d0" font-size="11" text-anchor="middle" font-family="Montserrat, sans-serif">${result.provider.name}</text>
        <text x="${x}" y="232" fill="#777" font-size="9" text-anchor="middle" font-family="Montserrat, sans-serif">${result.plan.label}</text>`;
      return;
    }
    const lowY = y(result.low.total);
    const highY = y(result.high.total);
    const baseY = y(result.base.total);
    const dashed = result.upperBound || result.floorOnly ? ` stroke-dasharray="4 4"` : "";
    const prefix = result.upperBound ? "≤ " : "";

    if (state.mode !== "actual" && !result.floorOnly) {
      svg += `<line x1="${x}" y1="${lowY}" x2="${x}" y2="${highY}" stroke="${result.provider.color}" stroke-width="8" stroke-linecap="round" opacity="0.35"${dashed}/>
        <line x1="${x - 8}" y1="${lowY}" x2="${x + 8}" y2="${lowY}" stroke="${result.provider.color}" stroke-width="2"/>
        <line x1="${x - 8}" y1="${highY}" x2="${x + 8}" y2="${highY}" stroke="${result.provider.color}" stroke-width="2"/>`;
    }

    if (result.floorOnly) {
      const arrowTop = Math.max(plotTop + 8, baseY - 62);
      svg += `<line x1="${x}" y1="${baseY - 9}" x2="${x}" y2="${arrowTop}" stroke="${result.provider.color}" stroke-width="8" stroke-linecap="round" opacity="0.35"/>
        <path d="M ${x - 7} ${arrowTop + 9} L ${x} ${arrowTop} L ${x + 7} ${arrowTop + 9}" fill="none" stroke="${result.provider.color}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" opacity="0.35"/>`;
    }

    svg += `<circle cx="${x}" cy="${baseY}" r="7" fill="${result.upperBound || result.floorOnly ? "#161616" : result.provider.color}" stroke="${result.provider.color}" stroke-width="3"/>
      <text x="${x}" y="${result.floorOnly ? Math.min(plotBottom - 12, baseY + 24) : Math.max(14, baseY - 14)}" fill="${result.provider.color}" font-size="11" font-weight="700" text-anchor="middle" font-family="Montserrat, sans-serif">${prefix}${money(result.base.total)}${result.floorOnly ? " floor" : ""}</text>
      <text x="${x}" y="216" fill="#d0d0d0" font-size="11" text-anchor="middle" font-family="Montserrat, sans-serif">${result.provider.name}</text>
      <text x="${x}" y="232" fill="#777" font-size="9" text-anchor="middle" font-family="Montserrat, sans-serif">${result.plan.label}</text>`;
  });

  return svg + `</svg>`;
}

function usageSummary(estimate) {
  const usage = estimate.results[0].base.usage;
  const input = usage.uncachedInputM + usage.cacheReadM + usage.cacheWriteM;
  const runText = usage.runs === null ? "" : `${Math.round(usage.runs).toLocaleString("en-GB")} runs · `;
  return `${runText}${millions(input)} input tokens · ${millions(usage.outputM)} output tokens`;
}

function resultTotal(result, mode) {
  if (result.needsContractInput) {
    return `<strong>—</strong><span>enter contract terms</span>`;
  }
  const base = money(result.base.total);
  const range = moneyRange(result.low.total, result.high.total);
  if (result.floorOnly) {
    return `<strong>≥ ${base}</strong><span>subscription floor; paid usage can increase cost</span>`;
  }
  if (result.upperBound) {
    return mode === "actual"
      ? `<strong>≤ ${base}</strong><span>upper bound</span>`
      : `<strong>≤ ${base}</strong><span>${range} scenario range</span>`;
  }
  return mode === "actual"
    ? `<strong>${base}</strong><span>entered usage</span>`
    : `<strong>${base}</strong><span>${range} scenario range</span>`;
}

function providerAssumption(result) {
  switch (result.provider.id) {
    case "claude":
      return result.plan.id === "enterprise"
        ? "Seat fee + API usage"
        : "Upper bound: seat fee + usage";
    case "copilot":
      return "Seat fee + usage above pooled credits";
    case "cursor":
      return "Seat fee + third-party usage above allowance";
    case "codex":
      if (result.plan.requiresContractInputs) {
        return "Contract cost + usage above shared credits";
      }
      return result.plan.id === "payg"
        ? "Usage only; no seat fee"
        : "Upper bound: seat fee + usage";
    case "antigravity":
      return result.plan.id === "organization"
        ? "Usage-priced; contract rate required"
        : "Subscription floor; paid overage unknown";
    default:
      return result.plan.note;
  }
}

function providerCalculationDetail(result) {
  switch (result.provider.id) {
    case "copilot":
      return {
        text: "Each Business or Enterprise seat contributes AI credits to an organisation-level pool. Metered agent and chat usage draws from that pool; code completions and next-edit suggestions are not metered.",
        formula: "Seat fees + max(0, metered model usage − pooled AI-credit allowance)"
      };
    case "cursor":
      return {
        text: `The calculator assumes ${Math.round(result.base.firstPartyShare * 100)}% of activity uses Cursor’s first-party Auto and Composer pool. It prices the remaining third-party share at model rates, adds the $0.25-per-million-token processing charge, then deducts the plan allowance.`,
        formula: "Seat fees + max(0, third-party model usage + processing charge − allowance)"
      };
    case "claude":
      return result.plan.id === "enterprise"
        ? {
            text: "Claude Code Enterprise is modelled using the published $20 monthly seat plus usage at Anthropic API rates.",
            formula: "Seat fees + model usage"
          }
        : {
            text: "Team Standard and Premium include usage, but Anthropic does not publish that allowance in transferable tokens or dollars. The result therefore adds all modelled usage and is marked as an upper bound.",
            formula: "Upper bound = seat fees + all modelled usage"
          };
    case "codex":
      if (result.plan.requiresContractInputs) {
        return {
          text: "Enterprise and Edu flexible-pricing customers enter their monthly-equivalent contract cost and shared credit allocation. Model usage consumes that shared pool.",
          formula: "Contract cost + max(0, model usage − shared-credit value)"
        };
      }
      return result.plan.id === "payg"
        ? {
            text: "Codex-only pay-as-you-go has no seat fee or allowance. OpenAI’s token-based credit rate is converted at $0.04 per credit. Eligibility is restricted to Enterprise and qualifying Business workspaces.",
            formula: "Model usage"
          }
        : {
            text: "ChatGPT Business includes Codex usage, but its allowance is unpublished. The result therefore adds all modelled usage and is marked as an upper bound.",
            formula: "Upper bound = seat fees + all modelled usage"
          };
    case "antigravity":
      if (result.plan.id === "organization") {
        return {
          text: "Google Cloud bills Gemini Enterprise Agent Platform consumption under organisation-specific terms. No public subscription seat price is modelled.",
          formula: "Organisation contract rate × usage"
        };
      }
      return {
        text: "The subscription includes Gemini usage up to an unpublished quota ceiling. At the ceiling, users can wait for refresh or, where supported, spend Google AI credits. Because the threshold is unknown, paid overage is omitted rather than priced at zero.",
        formula: "Displayed floor = seats × subscription price; potential paid overage omitted"
      };
    default:
      return { text: result.plan.note, formula: "Provider-specific terms apply" };
  }
}

function calculationTooltip(id, label, detail) {
  return `
    <span class="cc-tooltip">
      <button class="cc-tooltip-trigger" type="button" aria-label="${label}" aria-describedby="${id}">i</button>
      <span class="cc-tooltip-content" id="${id}" role="tooltip">
        <strong>${label}</strong>
        ${detail.text}
        <span class="cc-tooltip-formula">${detail.formula}</span>
      </span>
    </span>`;
}

function overageLabel(result) {
  if (result.needsContractInput) {
    return `Pending<span class="cc-cell-note">enter contract cost and shared credits</span>`;
  }
  if (result.floorOnly) {
    return `Not modelled<span class="cc-cell-note">quota ceiling is unpublished</span>`;
  }
  if (result.upperBound) {
    return `≤ ${money(result.base.overage)}<span class="cc-cell-note">maximum if none of the unpublished allowance applies</span>`;
  }
  const note = result.base.overage === 0
    ? "usage remains inside the allowance"
    : result.base.included > 0
    ? "charged above the allowance"
    : "charged in addition to the subscription";
  return `${money(result.base.overage)}<span class="cc-cell-note">${note}</span>`;
}

function renderResults(estimate) {
  const comparable = estimate.results.filter(result =>
    !result.upperBound && !result.floorOnly && !result.needsContractInput
  );
  const winner = comparable.length
    ? comparable.reduce((lowest, result) => result.base.total < lowest.base.total ? result : lowest)
    : null;

  const rows = estimate.results.map(result => {
    const isWinner = winner && winner.provider.id === result.provider.id;
    const allowance = result.needsContractInput
      ? "Enter shared credits"
      : result.floorOnly
      ? "Included quota ceiling; amount not published"
      : result.base.included === null
      ? "Not published"
      : result.base.included > 0 ? money(result.base.included) : "None";
    const usageLabel = result.floorOnly
      ? "At ceiling: wait for refresh or purchase AI credits"
      : result.provider.hasFirstPartyPool
      ? `${money(result.base.usageCost)} after ${Math.round(result.base.firstPartyShare * 100)}% first-party share`
      : money(result.base.usageCost);
    const subscription = result.plan.requiresContractInputs
      ? result.needsContractInput
        ? `Required<span class="cc-cell-note">monthly contract cost</span>`
        : `${money(result.base.seatCost)}<span class="cc-cell-note">monthly contract input</span>`
      : `${money(result.base.seatCost)}<span class="cc-cell-note">${money(result.base.seatRate)}/seat</span>`;
    return `
      <tr>
        <td>
          <a class="cc-provider-link" href="${result.provider.pricingUrl}" target="_blank" rel="noopener" style="--provider:${result.provider.color}">
            ${result.provider.name} ↗
          </a>
          <span class="cc-cell-note">${result.plan.label}${isWinner ? " · lowest comparable base" : ""}</span>
        </td>
        <td>${subscription}</td>
        <td>${usageLabel}</td>
        <td>${allowance}</td>
        <td>${overageLabel(result)}</td>
        <td>
          ${providerAssumption(result)}
          ${calculationTooltip(
            `cc-method-${result.provider.id}`,
            `${result.provider.name} calculation`,
            providerCalculationDetail(result)
          )}
        </td>
        <td class="cc-total" style="--provider:${result.provider.color}">${resultTotal(result, estimate.state.mode)}</td>
      </tr>`;
  }).join("");

  return `
    <div class="cc-results-heading">
      <div>
        <span class="cc-eyebrow">Estimated monthly cost</span>
        <p>${usageSummary(estimate)} · USD before tax</p>
      </div>
      <div class="cc-legend">${estimate.state.mode === "actual" ? "● entered usage" : "┃ low–high &nbsp; ● base"}${estimate.results.some(result => result.upperBound) ? " &nbsp; ○ upper bound" : ""}${estimate.results.some(result => result.floorOnly) ? " &nbsp; ↑ paid usage can increase cost" : ""}</div>
    </div>
    <div class="cc-chart">${renderRangeChart(estimate)}</div>
    <div class="cc-table-wrap">
      <table class="cc-results-table">
        <thead>
          <tr>
            <th>Provider and plan</th>
            <th>Subscription</th>
            <th>Usage before allowance</th>
            <th>Published allowance</th>
            <th>Additional usage charged</th>
            <th>
              Calculation
              ${calculationTooltip("cc-method-general", "General model-usage calculation", {
                text: "The calculator multiplies uncached input, cache reads, cache writes and output by the selected models’ shares and applicable rates. It then applies the plan’s seat charge and published allowance.",
                formula: "Model usage = Σ(token volume × model share × applicable token rate)"
              })}
            </th>
            <th>Monthly total</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    </div>
    <p class="cc-caveat">Provider-specific assumptions appear beside each result. Estimates exclude taxes, regional multipliers, negotiated discounts and enterprise contract terms.</p>`;
}

function renderAssumptions(data, estimate) {
  const rateRows = data.providers.map(provider => {
    if (provider.usagePricingMode === "unquantified") {
      return `
        <tr>
          <td><a href="${provider.modelPricingUrl}" target="_blank" rel="noopener">${provider.name} plans ↗</a></td>
          <td colspan="3">
            <strong>Included quota ceiling</strong>
            <span>The ceiling has no published transferable token amount. At the limit, Pro and Ultra users can wait for refresh or purchase AI credits consumed at Vertex API pricing.</span>
          </td>
        </tr>`;
    }
    return `
      <tr>
        <td><a href="${provider.modelPricingUrl}" target="_blank" rel="noopener">${provider.name} rates ↗</a></td>
        ${provider.rates.map(rate => `
          <td>
            <strong>${rate.label}</strong>
            <span>$${rate.input} input · $${rate.cacheRead} read · $${rate.cacheWrite} write · $${rate.output} output</span>
          </td>`).join("")}
      </tr>`;
  }).join("");

  return `
    <details class="cc-assumptions">
      <summary>Rate sources and shared calculation assumptions</summary>
      <div class="cc-assumptions-body">
        <p>
          Prices were verified on <strong>${data._lastVerified}</strong>. Rates are per million tokens in USD. The selected <strong>${estimate.mix.label.toLowerCase()}</strong> mix routes ${Math.round(estimate.mix.shares[0] * 100)}% to efficient, ${Math.round(estimate.mix.shares[1] * 100)}% to standard and ${Math.round(estimate.mix.shares[2] * 100)}% to frontier models.
        </p>
        <div class="cc-table-wrap">
          <table class="cc-rate-table">
            <thead><tr><th>Provider</th><th>Efficient</th><th>Standard</th><th>Frontier</th></tr></thead>
            <tbody>${rateRows}</tbody>
          </table>
        </div>
        <ul>
          ${estimate.adjustments ? `<li><strong>Repository and change adjustment:</strong> ${estimate.adjustments.repositoryScale.label} applies ${estimate.adjustments.repositoryScale.inputMultiplier}× input; ${estimate.adjustments.changeScope.label} applies ${estimate.adjustments.changeScope.inputMultiplier}× input and ${estimate.adjustments.changeScope.outputMultiplier}× output. Combined: ${estimate.adjustments.inputMultiplier.toFixed(2).replace(/\.?0+$/, "")}× input and ${estimate.adjustments.outputMultiplier.toFixed(2).replace(/\.?0+$/, "")}× output. Repository factors assume efficient native indexing or a graph-aware search plugin is configured.</li>` : ""}
          <li>Sonnet 5 uses its introductory $2/$10 input/output rate through 31 August 2026.</li>
          <li>Scenario ranges vary activity volume by ±${estimate.state.rangePct}%; seat costs and allowances remain fixed.</li>
          <li>Cache reads and writes are priced separately. In activity mode, their percentages divide the stated total input volume.</li>
          <li>Annual prices are shown as monthly equivalents. Enterprise contracts, taxes, regional multipliers and negotiated discounts are excluded.</li>
        </ul>
      </div>
    </details>`;
}

function setPath(target, path, value) {
  const keys = path.split(".");
  const last = keys.pop();
  const parent = keys.reduce((object, key) => object[key], target);
  parent[last] = value;
}

function renderCalculator(root, data) {
  let state = clone(data.defaults);

  function shell() {
    const mixOptions = data.modelMixes.map(mix => ({ value: mix.id, label: mix.label }));
    const repositoryScaleOptions = data.repositoryScales.map(scale => ({ value: scale.id, label: scale.label }));
    const changeScopeOptions = data.changeScopes.map(scope => ({ value: scope.id, label: scope.label }));
    const operatingModelOptions = [
      ...data.operatingModels.map(model => ({ value: model.id, label: model.label })),
      { value: "custom", label: "Custom workload" }
    ];
    const operatingModel = getOperatingModel(data, state.operatingModel);
    const operatingModelNote = operatingModel
      ? `${operatingModel.description} Selecting this profile resets the editable activity fields below.`
      : "Activity or model-mix inputs have been adjusted from a preset.";
    root.innerHTML = `
      <div class="cc-shell">
        <div class="cc-topline">
          <div>
            <span class="cc-eyebrow">AI coding cost model</span>
            <h2>Compare plans, allowances and model usage</h2>
            <p>Use an activity scenario for budgeting, or enter known monthly token volumes for a tighter estimate.</p>
          </div>
          <button class="cc-reset" id="cc-reset" type="button">Reset</button>
        </div>

        <div class="cc-mode" role="group" aria-label="Calculation mode">
          <button type="button" data-mode="scenario" aria-pressed="${state.mode === "scenario"}" class="${state.mode === "scenario" ? "active" : ""}">Estimate activity</button>
          <button type="button" data-mode="actual" aria-pressed="${state.mode === "actual"}" class="${state.mode === "actual" ? "active" : ""}">Use known usage</button>
        </div>

        <section class="cc-section" aria-labelledby="cc-team-heading">
          <div class="cc-section-heading">
            <div>
              <h3 id="cc-team-heading">Team and usage profile</h3>
              <p>All prices are monthly equivalents in USD before tax.</p>
            </div>
          </div>
          <div class="cc-field-grid cc-field-grid-four">
            ${numberField("cc-seats", "Developer seats", state.seats, { min: 1, max: 10000, path: "seats" })}
            ${selectField("cc-billing", "Billing term", state.billingTerm, [
              { value: "monthly", label: "Monthly" },
              { value: "annual", label: "Annual commitment" }
            ], 'data-path="billingTerm"')}
            ${state.mode === "scenario"
              ? selectField(
                  "cc-operating-model",
                  "AI coding operating model",
                  state.operatingModel,
                  operatingModelOptions,
                  "data-operating-model",
                  operatingModelNote
                )
              : ""}
            ${state.mode === "scenario"
              ? selectField(
                  "cc-repository-scale",
                  "Codebase size",
                  state.repositoryScale,
                  repositoryScaleOptions,
                  'data-path="repositoryScale"',
                  getRepositoryScale(data, state.repositoryScale).description
                )
              : ""}
            ${state.mode === "scenario"
              ? selectField(
                  "cc-change-scope",
                  "Average change size",
                  state.changeScope,
                  changeScopeOptions,
                  'data-path="changeScope"',
                  getChangeScope(data, state.changeScope).description
                )
              : ""}
            ${selectField("cc-mix", "Model mix", state.modelMix, mixOptions, 'data-path="modelMix"', getMix(data, state.modelMix).description)}
          </div>
        </section>

        <section class="cc-section" aria-labelledby="cc-plan-heading">
          <div class="cc-section-heading">
            <div>
              <h3 id="cc-plan-heading">Plans to compare</h3>
              <p>Choose the closest commercial plan for each provider.</p>
            </div>
          </div>
        <div class="cc-plan-grid">
            ${data.providers.map(provider => {
              const plan = getPlan(provider, state.selectedPlans[provider.id]);
              return `
                <div class="cc-field">
                  <label for="cc-plan-${provider.id}">
                    <span class="cc-label" style="color:${provider.color}">${provider.name}</span>
                  </label>
                  <select id="cc-plan-${provider.id}" data-plan="${provider.id}">
                    ${planOptions(provider, state.selectedPlans[provider.id])}
                  </select>
                  <span class="cc-note" data-plan-note="${provider.id}">${plan.note}</span>
                  ${contractFields(provider, plan, state)}
                </div>`;
            }).join("")}
          </div>
        </section>

        <section class="cc-section" id="cc-mode-fields">${modeFields(data, state)}</section>
        <section class="cc-results" id="cc-results" aria-live="polite"></section>
        <div id="cc-assumptions"></div>
      </div>`;

    bind();
    update();
  }

  function bind() {
    root.querySelectorAll("[data-mode]").forEach(button => {
      button.addEventListener("click", () => {
        state.mode = button.dataset.mode;
        shell();
      });
    });

    root.querySelectorAll("[data-path]").forEach(control => {
      const eventName = control.tagName === "SELECT" ? "change" : "input";
      control.addEventListener(eventName, () => {
        const value = control.type === "number" ? Number(control.value) : control.value;
        setPath(state, control.dataset.path, value);
        if (control.dataset.path === "modelMix" || control.dataset.path.startsWith("scenario.")) {
          state.operatingModel = "custom";
          const operatingModelSelect = root.querySelector("#cc-operating-model");
          if (operatingModelSelect) operatingModelSelect.value = "custom";
        }
        if (control.dataset.path === "scenario.inputKPerRun" || control.dataset.path === "scenario.outputKPerRun") {
          const note = control.closest(".cc-field")?.querySelector(".cc-note");
          if (note) {
            note.textContent = profileTokenNote(
              data,
              state,
              control.dataset.path === "scenario.inputKPerRun" ? "input" : "output"
            );
          }
        }
        update();
      });
    });

    root.querySelector("[data-operating-model]")?.addEventListener("change", event => {
      if (event.target.value === "custom") {
        state.operatingModel = "custom";
        update();
        return;
      }
      state = applyOperatingModel(data, state, event.target.value);
      shell();
    });

    root.querySelectorAll("[data-plan]").forEach(select => {
      select.addEventListener("change", () => {
        state.selectedPlans[select.dataset.plan] = select.value;
        shell();
      });
    });

    root.querySelector("#cc-reset").addEventListener("click", () => {
      state = clone(data.defaults);
      shell();
    });
  }

  function update() {
    const estimate = calculateEstimate(data, state);
    state = estimate.state;
    const mixNote = root.querySelector("#cc-mix")?.closest(".cc-field")?.querySelector(".cc-note");
    if (mixNote) mixNote.textContent = estimate.mix.description;
    const repositoryNote = root.querySelector("#cc-repository-scale")?.closest(".cc-field")?.querySelector(".cc-note");
    if (repositoryNote) repositoryNote.textContent = getRepositoryScale(data, state.repositoryScale).description;
    const changeScopeNote = root.querySelector("#cc-change-scope")?.closest(".cc-field")?.querySelector(".cc-note");
    if (changeScopeNote) changeScopeNote.textContent = getChangeScope(data, state.changeScope).description;
    const inputNote = root.querySelector("#cc-input-run")?.closest(".cc-field")?.querySelector(".cc-note");
    if (inputNote) inputNote.textContent = profileTokenNote(data, state, "input");
    const outputNote = root.querySelector("#cc-output-run")?.closest(".cc-field")?.querySelector(".cc-note");
    if (outputNote) outputNote.textContent = profileTokenNote(data, state, "output");
    const workloadNote = root.querySelector(".cc-workload-adjustment");
    if (workloadNote) workloadNote.innerHTML = workloadAdjustmentMarkup(data, state);
    const operatingModelNote = root.querySelector("#cc-operating-model")?.closest(".cc-field")?.querySelector(".cc-note");
    if (operatingModelNote) {
      const profile = getOperatingModel(data, state.operatingModel);
      operatingModelNote.textContent = profile
        ? `${profile.description} Selecting this profile resets the editable activity fields below.`
        : "Activity or model-mix inputs have been adjusted from a preset.";
    }
    estimate.results.forEach(result => {
      const note = root.querySelector(`[data-plan-note="${result.provider.id}"]`);
      if (note) note.textContent = result.plan.note;
    });
    root.querySelector("#cc-results").innerHTML = renderResults(estimate);
    root.querySelector("#cc-assumptions").innerHTML = renderAssumptions(data, estimate);
  }

  shell();
}

export function initCalculator(containerId, pricingUrl = "pricing.json") {
  const root = document.getElementById(containerId);
  if (!root) return;

  root.innerHTML = `<div class="cc-loading" role="status">Loading current pricing…</div>`;
  fetch(pricingUrl)
    .then(response => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then(data => renderCalculator(root, data))
    .catch(error => {
      console.error("ai-cost-calculator: failed to load pricing data", error);
      root.innerHTML = `
        <div class="cc-error" role="alert">
          <strong>The calculator could not load its pricing data.</strong>
          <span>Please refresh the page or use the linked provider pricing pages below.</span>
        </div>`;
    });
}

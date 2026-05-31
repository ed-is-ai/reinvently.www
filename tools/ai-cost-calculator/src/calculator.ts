// ─────────────────────────────────────────────────────────────────────────────
// AI Coding Tool Cost Calculator
// Pricing data loaded from pricing.json at runtime.
// Call: initCalculator("element-id")          — loads pricing.json from same dir
//       initCalculator("id", "/path/pricing.json") — explicit URL
// ─────────────────────────────────────────────────────────────────────────────

// ── Types ────────────────────────────────────────────────────────────────────

interface ModelRate {
  input: number;
  output: number;
  cachedInput?: number;
}

interface TaskTier {
  label: string;
  description: string;
  inputK: number;
  outputK: number;
}

interface ToolDef {
  id: string;
  name: string;
  color: string;
  pricingUrl: string;
  modelPricingUrl: string;
  seatCostPerUser: number;
  creditsPerUser: number;
  baseCost: (engineers: number) => number;
  includedCredits: (engineers: number) => number;
  rates: ModelRate[];
  rateLabels: string[];
}

interface UserTypeProfile {
  id: string;
  label: string;
  desc: string;
  tasksPerDay: number;
  opusPct: number;
}

interface CalcInputs {
  engineers: number;
  tasksPerDay: number;
  workingDays: number;
  opusPct: number;
  codebaseLines: number;
}

interface TierCost {
  tasks: number;
  inputM: number;
  outputM: number;
  tokenCost: number;
}

interface ToolResult {
  tiers: TierCost[];
  tokenTotal: number;
  baseCost: number;
  credits: number;
  total: number;
}

interface UserTypeCost {
  label: string;
  count: number;
  tokenCosts: number[];
}

interface BreakdownResult {
  userTypeCosts: UserTypeCost[];
  toolTotals: ToolResult[];
}

// ── JSON schema (mirrors pricing.json) ───────────────────────────────────────

interface PricingJSON {
  tools: Array<{
    id: string; name: string; color: string;
    pricingUrl: string; modelPricingUrl: string;
    seatCostPerUser: number; creditsPerUser: number;
    rates: Array<{ label: string; input: number; output: number; cachedInput?: number }>;
  }>;
  userTypes: Array<{ id: string; label: string; desc: string; tasksPerDay: number; opusPct: number }>;
  taskTiers: Array<{ label: string; description: string; inputK: number; outputK: number }>;
  model: {
    workingDaysPerMonth: number;
    cacheHitRate: number;
    taskSplitNonOpus: number[];
    defaultCounts: number[];
    defaultCodebaseLines: number;
    codebaseMinLines: number;
    codebaseMaxLines: number;
    codebaseExponent: number;
  };
}

// ── Runtime config (populated from JSON) ─────────────────────────────────────

interface Config {
  tools: ToolDef[];
  userTypes: UserTypeProfile[];
  tiers: TaskTier[];
  baseSplit: number[];
  baseTotal: number;
  workingDays: number;
  cacheHitRate: number;
  defaultCounts: number[];
  cbDefaultLines: number;
  cbLogMin: number;
  cbLogMax: number;
  cbDefaultPos: number;
  cbExponent: number;
}

function buildConfig(data: PricingJSON): Config {
  const tools: ToolDef[] = data.tools.map(t => ({
    id: t.id, name: t.name, color: t.color,
    pricingUrl: t.pricingUrl, modelPricingUrl: t.modelPricingUrl,
    seatCostPerUser: t.seatCostPerUser,
    creditsPerUser: t.creditsPerUser,
    baseCost: (eng: number) => eng * t.seatCostPerUser,
    includedCredits: (eng: number) => eng * t.creditsPerUser,
    rates: t.rates.map(r => ({ input: r.input, output: r.output, ...(r.cachedInput !== undefined ? { cachedInput: r.cachedInput } : {}) })),
    rateLabels: t.rates.map(r => r.label),
  }));

  const cbLogMin = Math.log10(data.model.codebaseMinLines);
  const cbLogMax = Math.log10(data.model.codebaseMaxLines);
  const cbDefaultPos = Math.round(
    ((Math.log10(data.model.defaultCodebaseLines) - cbLogMin) / (cbLogMax - cbLogMin)) * 100
  );
  const baseSplit = data.model.taskSplitNonOpus;

  return {
    tools,
    userTypes: data.userTypes,
    tiers: data.taskTiers,
    baseSplit,
    baseTotal: baseSplit.reduce((a, b) => a + b, 0),
    workingDays: data.model.workingDaysPerMonth,
    cacheHitRate: data.model.cacheHitRate,
    defaultCounts: data.model.defaultCounts,
    cbDefaultLines: data.model.defaultCodebaseLines,
    cbLogMin, cbLogMax, cbDefaultPos,
    cbExponent: data.model.codebaseExponent,
  };
}

// ── Calculation ───────────────────────────────────────────────────────────────

function codebaseMultiplier(cfg: Config, lines: number): number {
  return Math.pow(lines / cfg.cbDefaultLines, cfg.cbExponent);
}

function sliderToLines(cfg: Config, pos: number): number {
  return Math.round(Math.pow(10, cfg.cbLogMin + (pos / 100) * (cfg.cbLogMax - cfg.cbLogMin)));
}

function calcTierSplit(cfg: Config, opusPct: number): number[] {
  const remaining = 1 - opusPct;
  return [
    ...cfg.baseSplit.map(s => (s / cfg.baseTotal) * remaining),
    opusPct,
  ];
}

function calcTool(cfg: Config, tool: ToolDef, inputs: CalcInputs): ToolResult {
  const { engineers, tasksPerDay, workingDays, codebaseLines } = inputs;
  const totalTasks = engineers * tasksPerDay * workingDays;
  const split = calcTierSplit(cfg, inputs.opusPct);
  const cbMult = codebaseMultiplier(cfg, codebaseLines);

  const tiers: TierCost[] = cfg.tiers.map((tier, i) => {
    const tasks = Math.round(totalTasks * split[i]);
    const inputM = (tasks * tier.inputK * cbMult) / 1000;
    const outputM = (tasks * tier.outputK) / 1000;
    const rate = tool.rates[i];
    let tokenCost: number;
    if (rate.cachedInput !== undefined && tool.id === "cc" && i > 0) {
      tokenCost = inputM * cfg.cacheHitRate * rate.cachedInput
                + inputM * (1 - cfg.cacheHitRate) * rate.input
                + outputM * rate.output;
    } else {
      tokenCost = inputM * rate.input + outputM * rate.output;
    }
    return { tasks, inputM, outputM, tokenCost };
  });

  const tokenTotal = tiers.reduce((sum, t) => sum + t.tokenCost, 0);
  const baseCost   = tool.baseCost(engineers);
  const credits    = tool.includedCredits(engineers);
  return { tiers, tokenTotal, baseCost, credits, total: baseCost - credits + tokenTotal };
}

function deriveFromUserCounts(cfg: Config, counts: number[]): { engineers: number; tasksPerDay: number; opusPct: number } {
  const total = counts.reduce((s, c) => s + c, 0);
  if (total === 0) return { engineers: 0, tasksPerDay: 0, opusPct: 0 };
  const wTasks = cfg.userTypes.reduce((s, t, i) => s + t.tasksPerDay * counts[i], 0) / total;
  const wOpus  = cfg.userTypes.reduce((s, t, i) => s + t.opusPct   * counts[i], 0) / total;
  return { engineers: total, tasksPerDay: Math.round(wTasks), opusPct: +wOpus.toFixed(3) };
}

function calcByUserType(cfg: Config, counts: number[], codebaseLines: number): BreakdownResult {
  const userTypeCosts: UserTypeCost[] = cfg.userTypes.map((ut, i) => ({
    label: ut.label,
    count: counts[i],
    tokenCosts: cfg.tools.map(tool =>
      counts[i] === 0 ? 0 :
      calcTool(cfg, tool, { engineers: counts[i], tasksPerDay: ut.tasksPerDay,
                            workingDays: cfg.workingDays, opusPct: ut.opusPct, codebaseLines }).tokenTotal
    ),
  }));

  const totalEngineers = counts.reduce((s, c) => s + c, 0);
  const toolTotals: ToolResult[] = cfg.tools.map((tool, ti) => {
    const tokenTotal = userTypeCosts.reduce((sum, utc) => sum + utc.tokenCosts[ti], 0);
    const baseCost   = tool.baseCost(totalEngineers);
    const credits    = tool.includedCredits(totalEngineers);
    return { tiers: [], tokenTotal, baseCost, credits, total: baseCost - credits + tokenTotal };
  });

  return { userTypeCosts, toolTotals };
}

// ── Formatting ────────────────────────────────────────────────────────────────

function fmt(n: number): string {
  return "$" + Math.round(n).toLocaleString("en-GB");
}

function pct(n: number): string {
  return Math.round(n * 100) + "%";
}

function fmtLines(n: number): string {
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1).replace(/\.0$/, "") + "M lines";
  if (n >= 1_000)     return Math.round(n / 1_000) + "k lines";
  return n + " lines";
}

// ── Styles ────────────────────────────────────────────────────────────────────

function thStyle(align: string): string {
  return `text-align:${align};padding:10px 14px;color:#969696;font-family:'Montserrat',sans-serif;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;font-weight:400;background:#111;`;
}

function tdStyle(align: string, bg: string): string {
  return `text-align:${align};padding:10px 14px;background:${bg};vertical-align:middle;`;
}

// ── Render ────────────────────────────────────────────────────────────────────

function renderBarChart(cfg: Config, results: ToolResult[], container: HTMLElement): void {
  const max = Math.max(...results.map(r => r.total)) * 1.1;
  const W = 320, H = 140, barW = 64, gap = 24;
  const startX = (W - (cfg.tools.length * barW + (cfg.tools.length - 1) * gap)) / 2;

  let svg = `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:${W}px;display:block;margin:0 auto;">`;
  for (let i = 0; i <= 4; i++) {
    const y = 10 + (i / 4) * (H - 50);
    const val = Math.round(max * (1 - i / 4));
    svg += `<line x1="0" y1="${y}" x2="${W}" y2="${y}" stroke="#2a2a2a" stroke-width="1"/>`;
    svg += `<text x="2" y="${y - 3}" fill="#666" font-size="8" font-family="Montserrat,sans-serif">$${(val / 1000).toFixed(1)}k</text>`;
  }
  results.forEach((r, i) => {
    const tool = cfg.tools[i];
    const barH = max > 0 ? (r.total / max) * (H - 50) : 0;
    const x = startX + i * (barW + gap);
    const y = H - 38 - barH;
    svg += `<rect x="${x}" y="${y}" width="${barW}" height="${barH}" fill="${tool.color}" rx="2" opacity="0.85"/>`;
    svg += `<text x="${x + barW / 2}" y="${y - 5}" fill="${tool.color}" font-size="9" font-weight="bold" font-family="Montserrat,sans-serif" text-anchor="middle">${fmt(r.total)}</text>`;
    svg += `<text x="${x + barW / 2}" y="${H - 20}" fill="#969696" font-size="8" font-family="Montserrat,sans-serif" text-anchor="middle">${tool.name}</text>`;
  });
  svg += `</svg>`;
  container.innerHTML = svg;
}

// ── Slider component ──────────────────────────────────────────────────────────

function makeSlider(opts: {
  id: string; label: string; min: number; max: number; step: number;
  value: number; format: (v: number) => string; note?: string;
}): string {
  return `
    <div style="margin-bottom:20px;">
      <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px;">
        <label for="${opts.id}" style="color:#969696;font-family:'Montserrat',sans-serif;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;">${opts.label}</label>
        <span id="${opts.id}-val" style="color:#e2e2e2;font-size:15px;font-weight:600;">${opts.format(opts.value)}</span>
      </div>
      <input type="range" id="${opts.id}" min="${opts.min}" max="${opts.max}" step="${opts.step}" value="${opts.value}"
        style="width:100%;accent-color:#4A90D9;cursor:pointer;"/>
      ${opts.note ? `<p style="margin:4px 0 0;color:#555;font-size:11px;">${opts.note}</p>` : ""}
    </div>`;
}

// ── Main render (called after config is loaded) ───────────────────────────────

function renderCalculator(containerId: string, cfg: Config): void {
  const root = document.getElementById(containerId);
  if (!root) return;

  const DEFAULT_COUNTS = [...cfg.defaultCounts];
  let userCounts = [...DEFAULT_COUNTS];

  const initDerived = deriveFromUserCounts(cfg, DEFAULT_COUNTS);
  let inputs: CalcInputs = {
    engineers:     initDerived.engineers,
    tasksPerDay:   initDerived.tasksPerDay,
    workingDays:   cfg.workingDays,
    opusPct:       initDerived.opusPct,
    codebaseLines: cfg.cbDefaultLines,
  };

  root.style.cssText = "background:#161616;border:1px solid #2a2a2a;padding:28px 28px 20px;font-family:'Georgia','Times New Roman',serif;color:#e2e2e2;";

  root.innerHTML = `
    <h2 style="font-family:'Playfair Display',Georgia,serif;font-weight:400;font-size:22px;color:#e2e2e2;margin:0 0 6px;">AI Coding Tool Cost Estimator</h2>
    <p style="color:#969696;font-size:14px;margin:0 0 28px;">Real-time cost comparison across ${cfg.tools.map(t => t.name).join(", ")}. Adjust the inputs to match your team's usage pattern.</p>

    <div style="margin-bottom:16px;">
      <p style="font-family:'Montserrat',sans-serif;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#969696;margin:0 0 10px;">Team composition</p>
      ${cfg.userTypes.map((ut, i) => `
        <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #222;">
          <div>
            <span style="color:#e2e2e2;font-size:14px;">${ut.label}</span>
            <br><span style="color:#555;font-size:11px;">${ut.desc}</span>
          </div>
          <div style="display:flex;align-items:center;gap:10px;">
            <button id="cc-${ut.id}-dec" style="background:#222;border:1px solid #333;color:#969696;width:28px;height:28px;cursor:pointer;font-size:16px;line-height:1;border-radius:3px;">−</button>
            <span id="cc-${ut.id}-val" style="color:#e2e2e2;font-size:16px;font-weight:600;min-width:20px;text-align:center;">${DEFAULT_COUNTS[i]}</span>
            <button id="cc-${ut.id}-inc" style="background:#222;border:1px solid #333;color:#969696;width:28px;height:28px;cursor:pointer;font-size:16px;line-height:1;border-radius:3px;">+</button>
          </div>
        </div>`).join("")}
      <p id="cc-team-summary" style="color:#555;font-size:11px;margin:10px 0 0;">
        ${initDerived.engineers} engineer${initDerived.engineers !== 1 ? "s" : ""} &nbsp;·&nbsp; ${initDerived.tasksPerDay} tasks/day avg &nbsp;·&nbsp; ${pct(initDerived.opusPct)} Opus
      </p>
    </div>
    <div style="margin-bottom:24px;">
      ${makeSlider({ id: "cc-codebase", label: "Codebase size", min: 0, max: 100, step: 1, value: cfg.cbDefaultPos, format: () => fmtLines(cfg.cbDefaultLines), note: "Larger codebases require agents to read more files per task" })}
    </div>

    <div style="border-top:1px solid #2a2a2a;padding-top:24px;margin-bottom:20px;">
      <p style="font-family:'Montserrat',sans-serif;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#969696;margin:0 0 16px;">Estimated monthly cost</p>
      <div id="cc-chart" data-chart style="margin-bottom:20px;"></div>
      <div id="cc-results"></div>
    </div>

    <details style="border-top:1px solid #2a2a2a;padding-top:16px;margin-top:4px;">
      <summary style="cursor:pointer;color:#555;font-family:'Montserrat',sans-serif;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;list-style:none;">Model assumptions</summary>
      <div id="cc-assumptions" style="margin-top:14px;"></div>
    </details>

    <p style="margin:20px 0 0;font-size:11px;color:#444;">
      Estimates only. User type counts drive engineers and average tasks/day. Task mix: ${cfg.baseSplit.join("/")}% non-Opus. Working days: ${cfg.workingDays}/month.
    </p>
  `;

  const resultsEl     = root.querySelector<HTMLElement>("#cc-results")!;
  const chartEl       = root.querySelector<HTMLElement>("#cc-chart")!;
  const assumptionsEl = root.querySelector<HTMLElement>("#cc-assumptions")!;
  const summaryEl     = root.querySelector<HTMLElement>("#cc-team-summary")!;

  function renderAssumptions(): void {
    const linkStyle = (color: string) => `color:${color};font-size:10px;text-decoration:none;border-bottom:1px solid ${color}55;`;
    let html = `<table style="width:100%;border-collapse:collapse;font-size:12px;">
      <thead><tr style="border-bottom:1px solid #2a2a2a;">
        <th style="${thStyle("left")}">Type of task</th>`;
    cfg.tools.forEach(t => {
      html += `<th style="${thStyle("right")}"><a href="${t.modelPricingUrl}" target="_blank" rel="noopener" style="${linkStyle(t.color)}">${t.name} rates ↗</a></th>`;
    });
    html += `</tr></thead><tbody>`;
    cfg.tiers.forEach((tier, i) => {
      const bg = i % 2 === 0 ? "#1a1a1a" : "#1e1e1e";
      html += `<tr><td style="${tdStyle("left", bg)};color:#969696;">${tier.label}<br><span style="color:#555;font-size:10px;">${tier.description}</span></td>`;
      cfg.tools.forEach(t => {
        const r = t.rates[i];
        const cacheNote = r.cachedInput && t.id === "cc" ? ` (cached $${r.cachedInput})` : "";
        html += `<td style="${tdStyle("right", bg)};color:#666;font-size:11px;">${t.rateLabels[i]}<br>$${r.input}/$${r.output}/M${cacheNote}</td>`;
      });
      html += `</tr>`;
    });
    html += `</tbody></table>`;
    assumptionsEl.innerHTML = html;
  }

  function buildResultsTable({ userTypeCosts, toolTotals }: BreakdownResult): string {
    const minTotal = Math.min(...toolTotals.map(r => r.total));
    let html = `<div style="overflow-x:auto;margin-bottom:16px;">
      <table style="width:100%;border-collapse:collapse;font-size:13px;">
        <thead><tr style="border-bottom:2px solid #2a2a2a;">
          <th style="${thStyle("left")}">User type</th>`;
    cfg.tools.forEach((tool, i) => {
      const isWinner = toolTotals[i].total === minTotal;
      html += `<th style="${thStyle("right")}">
        <a href="${tool.pricingUrl}" target="_blank" rel="noopener" style="color:${tool.color};font-weight:600;text-decoration:none;border-bottom:1px solid ${tool.color}33;">${tool.name}</a>
        ${isWinner ? ' <span style="color:#f0ad4e;font-size:10px;">★</span>' : ''}
      </th>`;
    });
    html += `</tr></thead><tbody>`;

    userTypeCosts.forEach((utc, i) => {
      if (utc.count === 0) return;
      const bg = i % 2 === 0 ? "#1e1e1e" : "#242424";
      const ut = cfg.userTypes[i];
      const totalTasks = utc.count * ut.tasksPerDay * cfg.workingDays;
      html += `<tr style="border-bottom:1px solid #2a2a2a;">
        <td style="${tdStyle("left", bg)}">
          <span style="color:#e2e2e2;">${utc.count}× ${utc.label}</span>
          <br><span style="color:#444;font-size:11px;">${ut.tasksPerDay} tasks/day · ${totalTasks.toLocaleString()} tasks/mo · ${pct(ut.opusPct)} Opus</span>
        </td>`;
      utc.tokenCosts.forEach(cost => { html += `<td style="${tdStyle("right", bg)}">${fmt(cost)}</td>`; });
      html += `</tr>`;
    });

    const subtotalBg = "#1a1a1a";
    html += `<tr style="border-top:1px solid #444;"><td style="${tdStyle("left", subtotalBg)};color:#555;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Token total</td>`;
    toolTotals.forEach(r => { html += `<td style="${tdStyle("right", subtotalBg)};color:#555;">${fmt(r.tokenTotal)}</td>`; });
    html += `</tr>`;

    html += `<tr><td style="${tdStyle("left", "#1e1e1e")};color:#555;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Seat cost</td>`;
    toolTotals.forEach((r, i) => {
      const perSeat = cfg.tools[i].seatCostPerUser;
      const note = perSeat > 0 ? `${fmt(r.baseCost)} ($${perSeat}/seat)` : "No seat cost";
      html += `<td style="${tdStyle("right", "#1e1e1e")};color:#555;font-size:11px;">${note}</td>`;
    });
    html += `</tr>`;

    html += `<tr><td style="${tdStyle("left", "#242424")};color:#555;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Included credits</td>`;
    toolTotals.forEach(r => {
      html += `<td style="${tdStyle("right", "#242424")};color:#555;font-size:11px;">${r.credits > 0 ? `−${fmt(r.credits)}` : "—"}</td>`;
    });
    html += `</tr>`;

    html += `<tr><td style="${tdStyle("left", "#111")};font-weight:700;font-size:13px;text-transform:uppercase;letter-spacing:1px;">Total / month</td>`;
    toolTotals.forEach((r, i) => {
      const isWinner = r.total === minTotal;
      const c = isWinner ? "#f0ad4e" : cfg.tools[i].color;
      html += `<td style="${tdStyle("right", "#111")};font-weight:700;font-size:16px;color:${c};">${fmt(r.total)}</td>`;
    });
    html += `</tr></tbody></table></div>`;

    html += `<p style="font-size:11px;color:#444;margin:0;">★ lowest cost &nbsp;·&nbsp; Copilot Opus rate is currently ~⅓ of direct API price — Microsoft preferential rate at time of writing &nbsp;·&nbsp; Claude Code costs reflect prompt caching</p>`;
    return html;
  }

  function update(): void {
    const breakdown = calcByUserType(cfg, userCounts, inputs.codebaseLines);
    renderBarChart(cfg, breakdown.toolTotals, chartEl);
    resultsEl.innerHTML = buildResultsTable(breakdown);
    renderAssumptions();
  }

  function syncFromCounts(): void {
    const derived = deriveFromUserCounts(cfg, userCounts);
    inputs.engineers   = derived.engineers;
    inputs.tasksPerDay = derived.tasksPerDay;
    inputs.opusPct     = derived.opusPct;
    summaryEl.innerHTML =
      `${derived.engineers} engineer${derived.engineers !== 1 ? "s" : ""} &nbsp;·&nbsp; ${derived.tasksPerDay} tasks/day avg &nbsp;·&nbsp; ${pct(derived.opusPct)} Opus`;
    cfg.userTypes.forEach((ut, i) => {
      root!.querySelector<HTMLElement>(`#cc-${ut.id}-val`)!.textContent = String(userCounts[i]);
    });
    update();
  }

  cfg.userTypes.forEach((ut, i) => {
    root!.querySelector(`#cc-${ut.id}-dec`)!.addEventListener("click", () => {
      if (userCounts[i] > 0) { userCounts[i]--; syncFromCounts(); }
    });
    root!.querySelector(`#cc-${ut.id}-inc`)!.addEventListener("click", () => {
      if (userCounts[i] < 20) { userCounts[i]++; syncFromCounts(); }
    });
  });

  // Codebase size log-scale slider
  const cbSlider = root.querySelector<HTMLInputElement>("#cc-codebase")!;
  const cbValEl  = root.querySelector<HTMLElement>("#cc-codebase-val")!;
  cbSlider.addEventListener("input", () => {
    const lines = sliderToLines(cfg, parseFloat(cbSlider.value));
    inputs.codebaseLines = lines;
    cbValEl.textContent  = fmtLines(lines);
    update();
  });

  renderAssumptions();
  update();
}

// ── Public entry point ────────────────────────────────────────────────────────

export function initCalculator(containerId: string, pricingUrl = "pricing.json"): void {
  fetch(pricingUrl)
    .then(r => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json() as Promise<PricingJSON>;
    })
    .then(data => renderCalculator(containerId, buildConfig(data)))
    .catch(err => {
      console.error("ai-cost-calculator: failed to load pricing data from", pricingUrl, err);
    });
}

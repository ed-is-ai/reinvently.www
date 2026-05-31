// ─────────────────────────────────────────────────────────────────────────────
// AI Coding Tool Cost Calculator
// Self-contained embeddable component — call initCalculator("element-id")
// ─────────────────────────────────────────────────────────────────────────────

// ── Types ────────────────────────────────────────────────────────────────────

interface ModelRate {
  input: number;        // $/M tokens
  output: number;       // $/M tokens
  cachedInput?: number; // $/M tokens when cache hits (Claude Code only)
}

interface TaskTier {
  label: string;
  inputK: number;   // k tokens input per task
  outputK: number;  // k tokens output per task
}

interface ToolDef {
  id: string;
  name: string;
  color: string;
  pricingUrl: string;
  modelPricingUrl: string;
  baseCost: (engineers: number) => number;
  includedCredits: (engineers: number) => number;
  rates: ModelRate[];  // one entry per TaskTier index
  rateLabels: string[];
}

interface CalcInputs {
  engineers: number;
  tasksPerDay: number;
  workingDays: number;
  opusPct: number;      // 0..1
  cacheHitRate: number; // 0..1 — Claude Code only
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

// ── Constants ─────────────────────────────────────────────────────────────────

const TIERS: TaskTier[] = [
  { label: "Simple",           inputK: 15, outputK: 1  },
  { label: "Medium",           inputK: 35, outputK: 3  },
  { label: "Complex",          inputK: 60, outputK: 8  },
  { label: "Planning (Opus)",  inputK: 80, outputK: 10 },
];

// Base split for non-Opus tasks: simple 40 / medium 35 / complex 15 (out of 90)
const BASE_SPLIT = [40, 35, 15];
const BASE_TOTAL = BASE_SPLIT.reduce((a, b) => a + b, 0); // 90

const TOOLS: ToolDef[] = [
  {
    id: "cc",
    name: "Claude Code",
    color: "#4A90D9",
    pricingUrl: "https://claude.ai/pricing",
    modelPricingUrl: "https://www.anthropic.com/pricing",
    baseCost: () => 0,
    includedCredits: () => 0,
    rates: [
      { input: 1.00, output: 5.00 },                          // Simple — Haiku
      { input: 3.00, output: 15.00, cachedInput: 0.30 },      // Medium — Sonnet
      { input: 3.00, output: 15.00, cachedInput: 0.30 },      // Complex — Sonnet
      { input: 15.00, output: 75.00, cachedInput: 0.50 },     // Planning — Opus
    ],
    rateLabels: ["Haiku", "Sonnet", "Sonnet", "Opus (direct)"],
  },
  {
    id: "cop",
    name: "Copilot",
    color: "#E07B39",
    pricingUrl: "https://github.com/features/copilot#pricing",
    modelPricingUrl: "https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing",
    baseCost: (eng) => eng * 19,
    includedCredits: (eng) => eng * 19,
    rates: [
      { input: 0.25, output: 2.00 },   // Simple — GPT-5 mini
      { input: 2.00, output: 8.00 },   // Medium — GPT-4.1
      { input: 3.00, output: 15.00 },  // Complex — Sonnet
      { input: 5.00, output: 25.00 },  // Planning — Opus via Copilot (discounted)
    ],
    rateLabels: ["GPT-5 mini", "GPT-4.1", "Sonnet", "Opus (preferential rate)"],
  },
  {
    id: "cur",
    name: "Cursor",
    color: "#5CB85C",
    pricingUrl: "https://cursor.com/pricing",
    modelPricingUrl: "https://cursor.com/pricing",
    baseCost: (eng) => eng * 40,
    includedCredits: (eng) => eng * 20,  // $20 of the $40 is credits
    rates: [
      { input: 1.25, output: 6.00 },   // Simple — Auto
      { input: 1.25, output: 6.00 },   // Medium — Auto
      { input: 3.00, output: 15.00 },  // Complex — Max Sonnet
      { input: 15.00, output: 75.00 }, // Planning — Max Opus (full rate)
    ],
    rateLabels: ["Auto", "Auto", "Max Sonnet", "Max Opus (full rate)"],
  },
];

// ── Calculation ───────────────────────────────────────────────────────────────

function calcTierSplit(inputs: CalcInputs): number[] {
  const { opusPct } = inputs;
  const remaining = 1 - opusPct;
  return [
    (BASE_SPLIT[0] / BASE_TOTAL) * remaining,
    (BASE_SPLIT[1] / BASE_TOTAL) * remaining,
    (BASE_SPLIT[2] / BASE_TOTAL) * remaining,
    opusPct,
  ];
}

function calcTool(tool: ToolDef, inputs: CalcInputs): ToolResult {
  const { engineers, tasksPerDay, workingDays, cacheHitRate } = inputs;
  const totalTasks = engineers * tasksPerDay * workingDays;
  const split = calcTierSplit(inputs);

  const tiers: TierCost[] = TIERS.map((tier, i) => {
    const tasks = Math.round(totalTasks * split[i]);
    const inputM = (tasks * tier.inputK) / 1000;
    const outputM = (tasks * tier.outputK) / 1000;

    const rate = tool.rates[i];
    let tokenCost: number;

    // Apply caching for Claude Code tiers that have a cachedInput rate
    if (rate.cachedInput !== undefined && tool.id === "cc" && i > 0) {
      const cachedIn = inputM * cacheHitRate * rate.cachedInput;
      const freshIn = inputM * (1 - cacheHitRate) * rate.input;
      tokenCost = cachedIn + freshIn + outputM * rate.output;
    } else {
      tokenCost = inputM * rate.input + outputM * rate.output;
    }

    return { tasks, inputM, outputM, tokenCost };
  });

  const tokenTotal = tiers.reduce((sum, t) => sum + t.tokenCost, 0);
  const baseCost = tool.baseCost(engineers);
  const credits = tool.includedCredits(engineers);
  const overage = Math.max(0, tokenTotal - credits);
  const total = baseCost - credits + tokenTotal; // simplifies to: platform_fee + token_total

  return { tiers, tokenTotal, baseCost, credits, total };
}

// ── Formatting ────────────────────────────────────────────────────────────────

function fmt(n: number): string {
  return "$" + Math.round(n).toLocaleString("en-GB");
}

function pct(n: number): string {
  return Math.round(n * 100) + "%";
}

// ── Render ────────────────────────────────────────────────────────────────────

function renderBarChart(results: ToolResult[], container: HTMLElement): void {
  const max = Math.max(...results.map(r => r.total)) * 1.1;
  const W = 320, H = 140, barW = 64, gap = 24;
  const startX = (W - (TOOLS.length * barW + (TOOLS.length - 1) * gap)) / 2;

  let svg = `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:${W}px;display:block;margin:0 auto;">`;

  // Gridlines
  for (let i = 0; i <= 4; i++) {
    const y = 10 + (i / 4) * (H - 50);
    const val = Math.round(max * (1 - i / 4));
    svg += `<line x1="0" y1="${y}" x2="${W}" y2="${y}" stroke="#2a2a2a" stroke-width="1"/>`;
    svg += `<text x="2" y="${y - 3}" fill="#666" font-size="8" font-family="Montserrat,sans-serif">$${(val/1000).toFixed(1)}k</text>`;
  }

  results.forEach((r, i) => {
    const tool = TOOLS[i];
    const barH = max > 0 ? ((r.total / max) * (H - 50)) : 0;
    const x = startX + i * (barW + gap);
    const y = H - 38 - barH;

    // Bar
    svg += `<rect x="${x}" y="${y}" width="${barW}" height="${barH}" fill="${tool.color}" rx="2" opacity="0.85"/>`;

    // Value label
    svg += `<text x="${x + barW / 2}" y="${y - 5}" fill="${tool.color}" font-size="9" font-weight="bold" font-family="Montserrat,sans-serif" text-anchor="middle">${fmt(r.total)}</text>`;

    // Tool name
    svg += `<text x="${x + barW / 2}" y="${H - 20}" fill="#969696" font-size="8" font-family="Montserrat,sans-serif" text-anchor="middle">${tool.name}</text>`;
  });

  svg += `</svg>`;
  container.innerHTML = svg;
}

function renderResults(results: ToolResult[], container: HTMLElement): void {
  const minTotal = Math.min(...results.map(r => r.total));

  // ── Table ──
  let html = `<div style="overflow-x:auto;margin-bottom:24px;">
    <table style="width:100%;border-collapse:collapse;font-size:13px;">
      <thead>
        <tr style="border-bottom:2px solid #2a2a2a;">
          <th style="${thStyle("left")}">Tier</th>`;

  TOOLS.forEach((tool, i) => {
    const isWinner = results[i].total === minTotal;
    html += `<th style="${thStyle("right")}"><span style="color:${tool.color};font-weight:600;">${tool.name}</span>${isWinner ? ' <span style="color:#f0ad4e;font-size:10px;">★</span>' : ''}</th>`;
  });
  html += `</tr></thead><tbody>`;

  // Tier rows
  TIERS.forEach((tier, ti) => {
    const rowBg = ti % 2 === 0 ? "#1e1e1e" : "#242424";
    html += `<tr style="border-bottom:1px solid #2a2a2a;">
      <td style="${tdStyle("left", rowBg)}">
        <span style="color:#e2e2e2;">${tier.label}</span>
        <br><span style="color:#555;font-size:11px;">${TOOLS.map(t => t.rateLabels[ti]).join(" / ")}</span>
      </td>`;
    results.forEach((r) => {
      html += `<td style="${tdStyle("right", rowBg)}">${fmt(r.tiers[ti].tokenCost)}</td>`;
    });
    html += `</tr>`;
  });

  // Token total
  html += `<tr style="border-bottom:1px solid #333;border-top:1px solid #444;">
    <td style="${tdStyle("left", "#1a1a1a")}"><span style="color:#969696;font-size:11px;letter-spacing:1px;text-transform:uppercase;">Token total</span></td>`;
  results.forEach(r => {
    html += `<td style="${tdStyle("right", "#1a1a1a")};color:#969696;">${fmt(r.tokenTotal)}</td>`;
  });
  html += `</tr>`;

  // Credits / adjustments
  html += `<tr style="border-bottom:1px solid #2a2a2a;">
    <td style="${tdStyle("left", "#1e1e1e")}"><span style="color:#969696;font-size:11px;letter-spacing:1px;text-transform:uppercase;">Plan / credits</span></td>`;
  results.forEach((r, i) => {
    const tool = TOOLS[i];
    const platformFee = r.baseCost - r.credits;
    let note = "";
    if (platformFee > 0) note = `+${fmt(platformFee)} platform`;
    else if (r.credits > 0) note = `-${fmt(r.credits)} credits`;
    else note = "API billing";
    html += `<td style="${tdStyle("right", "#1e1e1e")};color:#666;font-size:11px;">${note}</td>`;
  });
  html += `</tr>`;

  // Total
  html += `<tr>
    <td style="${tdStyle("left", "#111")};font-weight:700;color:#e2e2e2;font-size:14px;letter-spacing:1px;text-transform:uppercase;">Total / month</td>`;
  results.forEach((r, i) => {
    const isWinner = r.total === minTotal;
    const color = isWinner ? "#f0ad4e" : TOOLS[i].color;
    html += `<td style="${tdStyle("right", "#111")};font-weight:700;font-size:15px;color:${color};">${fmt(r.total)}</td>`;
  });
  html += `</tr></tbody></table></div>`;

  // ── Breakdown note ──
  html += `<p style="font-size:11px;color:#555;margin:0 0 16px;">
    ★ lowest cost &nbsp;·&nbsp; Copilot Opus rate ($5/M) is currently ~⅓ of direct API price — Microsoft preferential rate at time of writing &nbsp;·&nbsp; Claude Code costs include prompt caching benefit
  </p>`;

  container.innerHTML = html;

  // Bar chart
  const chartDiv = container.querySelector<HTMLElement>("[data-chart]")!;
  if (chartDiv) renderBarChart(results, chartDiv);
}

function thStyle(align: string): string {
  return `text-align:${align};padding:10px 14px;color:#969696;font-family:'Montserrat',sans-serif;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;font-weight:400;background:#111;`;
}

function tdStyle(align: string, bg: string): string {
  return `text-align:${align};padding:10px 14px;background:${bg};vertical-align:middle;`;
}

// ── Slider component ──────────────────────────────────────────────────────────

function makeSlider(opts: {
  id: string;
  label: string;
  min: number;
  max: number;
  step: number;
  value: number;
  format: (v: number) => string;
  note?: string;
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

// ── Main init ─────────────────────────────────────────────────────────────────

export function initCalculator(containerId: string): void {
  const root = document.getElementById(containerId);
  if (!root) return;

  const defaultInputs: CalcInputs = {
    engineers: 10,
    tasksPerDay: 20,
    workingDays: 22,
    opusPct: 0.10,
    cacheHitRate: 0.40,
  };

  root.style.cssText = "background:#161616;border:1px solid #2a2a2a;padding:28px 28px 20px;font-family:'Georgia','Times New Roman',serif;color:#e2e2e2;";

  root.innerHTML = `
    <h2 style="font-family:'Playfair Display',Georgia,serif;font-weight:400;font-size:22px;color:#e2e2e2;margin:0 0 6px;">AI Coding Tool Cost Estimator</h2>
    <p style="color:#969696;font-size:14px;margin:0 0 28px;">Real-time cost comparison across GitHub Copilot, Claude Code, and Cursor. Adjust the inputs to match your team's usage pattern.</p>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:8px;">
      ${makeSlider({ id: "cc-engineers", label: "Engineers", min: 1, max: 50, step: 1, value: defaultInputs.engineers, format: v => String(v) })}
      ${makeSlider({ id: "cc-tasks", label: "Tasks / engineer / day", min: 5, max: 50, step: 1, value: defaultInputs.tasksPerDay, format: v => String(v) })}
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px;">
      ${makeSlider({ id: "cc-opus", label: "Opus planning tasks", min: 0, max: 0.30, step: 0.01, value: defaultInputs.opusPct, format: pct, note: "Share of tasks using Opus for design / architecture" })}
      ${makeSlider({ id: "cc-cache", label: "Claude Code cache hit rate", min: 0, max: 0.80, step: 0.05, value: defaultInputs.cacheHitRate, format: pct, note: "Repeated file reads within a session billed at ~10% of standard rate" })}
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
      Estimates only. Task mix: 40% simple / 35% medium / 15% complex + Opus planning %. Context per task: 15k–80k input tokens, 1k–10k output tokens. Working days: ${defaultInputs.workingDays}/month.
    </p>
  `;

  const resultsEl = root.querySelector<HTMLElement>("#cc-results")!;
  const chartEl = root.querySelector<HTMLElement>("#cc-chart")!;
  const assumptionsEl = root.querySelector<HTMLElement>("#cc-assumptions")!;

  let inputs = { ...defaultInputs };

  function renderAssumptions(): void {
    const linkStyle = (color: string) => `color:${color};font-size:10px;text-decoration:none;border-bottom:1px solid ${color}55;`;
    let html = `<table style="width:100%;border-collapse:collapse;font-size:12px;">
      <thead><tr style="border-bottom:1px solid #2a2a2a;">
        <th style="${thStyle("left")}">Tier</th>`;
    TOOLS.forEach(t => {
      html += `<th style="${thStyle("right")}">
        <a href="${t.modelPricingUrl}" target="_blank" rel="noopener" style="${linkStyle(t.color)}">${t.name} rates ↗</a>
      </th>`;
    });
    html += `</tr></thead><tbody>`;
    TIERS.forEach((tier, i) => {
      const bg = i % 2 === 0 ? "#1a1a1a" : "#1e1e1e";
      html += `<tr><td style="${tdStyle("left", bg)};color:#969696;">${tier.label}</td>`;
      TOOLS.forEach(t => {
        const r = t.rates[i];
        const label = t.rateLabels[i];
        const cacheNote = r.cachedInput && t.id === "cc" ? ` (cached $${r.cachedInput})` : "";
        html += `<td style="${tdStyle("right", bg)};color:#666;font-size:11px;">${label}<br>$${r.input}/$${r.output}/M${cacheNote}</td>`;
      });
      html += `</tr>`;
    });
    html += `</tbody></table>`;
    assumptionsEl.innerHTML = html;
  }

  function update(): void {
    const results = TOOLS.map(tool => calcTool(tool, inputs));
    const minTotal = Math.min(...results.map(r => r.total));

    renderBarChart(results, chartEl);

    const resultsHtml = buildResultsTable(results, minTotal);
    resultsEl.innerHTML = resultsHtml;

    renderAssumptions();
  }

  function buildResultsTable(results: ToolResult[], minTotal: number): string {
    let html = `<div style="overflow-x:auto;margin-bottom:16px;">
      <table style="width:100%;border-collapse:collapse;font-size:13px;">
        <thead><tr style="border-bottom:2px solid #2a2a2a;">
          <th style="${thStyle("left")}">Tier</th>`;

    TOOLS.forEach((tool, i) => {
      const isWinner = results[i].total === minTotal;
      html += `<th style="${thStyle("right")}">
        <a href="${tool.pricingUrl}" target="_blank" rel="noopener" style="color:${tool.color};font-weight:600;text-decoration:none;border-bottom:1px solid ${tool.color}33;">${tool.name}</a>
        ${isWinner ? ' <span style="color:#f0ad4e;font-size:10px;">★</span>' : ''}
      </th>`;
    });
    html += `</tr></thead><tbody>`;

    TIERS.forEach((tier, ti) => {
      const bg = ti % 2 === 0 ? "#1e1e1e" : "#242424";
      html += `<tr style="border-bottom:1px solid #2a2a2a;">
        <td style="${tdStyle("left", bg)}">
          <span style="color:#e2e2e2;">${tier.label}</span>
          <br><span style="color:#444;font-size:11px;">${TOOLS.map(t => t.rateLabels[ti]).join(" · ")}</span>
        </td>`;
      results.forEach(r => {
        html += `<td style="${tdStyle("right", bg)}">${fmt(r.tiers[ti].tokenCost)}</td>`;
      });
      html += `</tr>`;
    });

    const subtotalBg = "#1a1a1a";
    html += `<tr style="border-top:1px solid #444;">
      <td style="${tdStyle("left", subtotalBg)};color:#555;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Token total</td>`;
    results.forEach(r => { html += `<td style="${tdStyle("right", subtotalBg)};color:#555;">${fmt(r.tokenTotal)}</td>`; });
    html += `</tr>`;

    html += `<tr><td style="${tdStyle("left", "#1e1e1e")};color:#555;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Plan / credits</td>`;
    results.forEach((r, i) => {
      const platformFee = r.baseCost - r.credits;
      let note = platformFee > 0 ? `+${fmt(platformFee)} platform` : r.credits > 0 ? `−${fmt(r.credits)} credits` : "API billing only";
      html += `<td style="${tdStyle("right", "#1e1e1e")};color:#555;font-size:11px;">${note}</td>`;
    });
    html += `</tr>`;

    html += `<tr><td style="${tdStyle("left", "#111")};font-weight:700;font-size:13px;text-transform:uppercase;letter-spacing:1px;">Total / month</td>`;
    results.forEach((r, i) => {
      const isWinner = r.total === minTotal;
      const c = isWinner ? "#f0ad4e" : TOOLS[i].color;
      html += `<td style="${tdStyle("right", "#111")};font-weight:700;font-size:16px;color:${c};">${fmt(r.total)}</td>`;
    });
    html += `</tr></tbody></table></div>`;

    html += `<p style="font-size:11px;color:#444;margin:0;">★ lowest cost at current settings &nbsp;·&nbsp; Copilot Opus rate is ~⅓ of direct API price &nbsp;·&nbsp; Claude Code costs reflect prompt caching</p>`;
    return html;
  }

  // Wire up sliders
  const sliders: Array<{ id: string; key: keyof CalcInputs; transform?: (v: number) => number }> = [
    { id: "cc-engineers", key: "engineers" },
    { id: "cc-tasks",     key: "tasksPerDay" },
    { id: "cc-opus",      key: "opusPct" },
    { id: "cc-cache",     key: "cacheHitRate" },
  ];

  sliders.forEach(({ id, key }) => {
    const slider = root.querySelector<HTMLInputElement>(`#${id}`)!;
    const valEl  = root.querySelector<HTMLElement>(`#${id}-val`)!;
    const fmt_fn = key === "engineers" || key === "tasksPerDay" ? String : pct;

    slider.addEventListener("input", () => {
      const v = parseFloat(slider.value);
      (inputs as Record<string, number>)[key] = v;
      valEl.textContent = fmt_fn(v);
      update();
    });
  });

  // Initial render
  renderAssumptions();
  update();
}

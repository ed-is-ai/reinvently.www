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
  description: string;
  inputK: number;   // k tokens input per task at 1M-line codebase baseline
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
  opusPct: number;        // 0..1
  codebaseLines: number;  // 10_000 to 100_000_000
}

const CACHE_HIT_RATE = 0.40; // Claude Code prompt cache hit rate — fixed assumption

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

// ── User type profiles ───────────────────────────────────────────────────────

interface UserTypeProfile {
  id: string;
  label: string;
  desc: string;
  tasksPerDay: number;
  opusPct: number;
}

// Calibrated against Cursor Teams rates so each profile hits the described monthly spend tier.
// Daily Tab: ~$17.50/mo · Limited Agent: ~$23.60/mo (often within $20) ·
// Daily Agent: ~$83.70/mo · Power user: ~$201.80/mo
const USER_TYPES: UserTypeProfile[] = [
  { id: "tab",     label: "Daily Tab users",     desc: "Always stay within $20",               tasksPerDay: 5,  opusPct: 0.00 },
  { id: "limited", label: "Limited Agent users", desc: "Often stay within the included $20",   tasksPerDay: 5,  opusPct: 0.03 },
  { id: "daily",   label: "Daily Agent users",   desc: "Typically $60–$100/mo total usage",    tasksPerDay: 10, opusPct: 0.08 },
  { id: "power",   label: "Power users",         desc: "Multiple agents / automation · $200+", tasksPerDay: 16, opusPct: 0.15 },
];

function deriveFromUserCounts(counts: number[]): { engineers: number; tasksPerDay: number; opusPct: number } {
  const total = counts.reduce((s, c) => s + c, 0);
  if (total === 0) return { engineers: 0, tasksPerDay: 0, opusPct: 0 };
  const wTasks = USER_TYPES.reduce((s, t, i) => s + t.tasksPerDay * counts[i], 0) / total;
  const wOpus  = USER_TYPES.reduce((s, t, i) => s + t.opusPct  * counts[i], 0) / total;
  return { engineers: total, tasksPerDay: Math.round(wTasks), opusPct: +wOpus.toFixed(3) };
}

// ── Constants ─────────────────────────────────────────────────────────────────

// Log-scale slider constants for codebase size (10k–100M lines)
const CB_LOG_MIN = Math.log10(10_000);        // 4
const CB_LOG_MAX = Math.log10(100_000_000);   // 8
const CB_DEFAULT_LINES = 1_000_000;
// Raw slider position (0–100) for default 1M lines
const CB_DEFAULT_POS = Math.round(
  ((Math.log10(CB_DEFAULT_LINES) - CB_LOG_MIN) / (CB_LOG_MAX - CB_LOG_MIN)) * 100
); // ≈ 50

const TIERS: TaskTier[] = [
  { label: "Small bug fix",         description: "Quick edits, single-file fixes",          inputK: 15,  outputK: 1  },
  { label: "Minor change",          description: "Multi-file edits, small refactors",        inputK: 35,  outputK: 3  },
  { label: "New feature",           description: "Full feature implementation",              inputK: 60,  outputK: 8  },
  { label: "Architectural refactor",description: "Cross-cutting changes, system-level work", inputK: 100, outputK: 12 },
  { label: "Architecture (Opus)",   description: "Design sessions, planning",                inputK: 120, outputK: 15 },
];

// Non-Opus task split: bug fix 35 / minor 30 / feature 20 / arch refactor 15
const BASE_SPLIT = [35, 30, 20, 15];
const BASE_TOTAL = BASE_SPLIT.reduce((a, b) => a + b, 0); // 100

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
      { input: 1.00,  output: 5.00  },                       // Small bug fix — Haiku
      { input: 3.00,  output: 15.00, cachedInput: 0.30 },    // Minor change — Sonnet
      { input: 3.00,  output: 15.00, cachedInput: 0.30 },    // New feature — Sonnet
      { input: 3.00,  output: 15.00, cachedInput: 0.30 },    // Arch refactor — Sonnet
      { input: 15.00, output: 75.00, cachedInput: 0.50 },    // Architecture — Opus
    ],
    rateLabels: ["Haiku", "Sonnet", "Sonnet", "Sonnet", "Opus (direct)"],
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
      { input: 0.25, output: 2.00  },  // Small bug fix — GPT-5 mini
      { input: 2.00, output: 8.00  },  // Minor change — GPT-4.1
      { input: 3.00, output: 15.00 },  // New feature — Sonnet
      { input: 3.00, output: 15.00 },  // Arch refactor — Sonnet
      { input: 5.00, output: 25.00 },  // Architecture — Opus via Copilot (preferential)
    ],
    rateLabels: ["GPT-5 mini", "GPT-4.1", "Sonnet", "Sonnet", "Opus (preferential rate)"],
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
      { input: 1.25,  output: 6.00  },  // Small bug fix — Auto
      { input: 1.25,  output: 6.00  },  // Minor change — Auto
      { input: 3.00,  output: 15.00 },  // New feature — Max Sonnet
      { input: 3.00,  output: 15.00 },  // Arch refactor — Max Sonnet
      { input: 15.00, output: 75.00 },  // Architecture — Max Opus (full rate)
    ],
    rateLabels: ["Auto", "Auto", "Max Sonnet", "Max Sonnet", "Max Opus (full rate)"],
  },
];

// ── Calculation ───────────────────────────────────────────────────────────────

interface UserTypeCost {
  label: string;
  count: number;
  tokenCosts: number[]; // one entry per tool
}

interface BreakdownResult {
  userTypeCosts: UserTypeCost[];
  toolTotals: ToolResult[];
}

function calcByUserType(counts: number[], codebaseLines: number): BreakdownResult {
  const userTypeCosts: UserTypeCost[] = USER_TYPES.map((ut, i) => ({
    label: ut.label,
    count: counts[i],
    tokenCosts: TOOLS.map(tool =>
      counts[i] === 0 ? 0 :
      calcTool(tool, { engineers: counts[i], tasksPerDay: ut.tasksPerDay,
                       workingDays: 22, opusPct: ut.opusPct, codebaseLines }).tokenTotal
    ),
  }));

  const totalEngineers = counts.reduce((s, c) => s + c, 0);
  const toolTotals: ToolResult[] = TOOLS.map((tool, ti) => {
    const tokenTotal = userTypeCosts.reduce((sum, utc) => sum + utc.tokenCosts[ti], 0);
    const baseCost   = tool.baseCost(totalEngineers);
    const credits    = tool.includedCredits(totalEngineers);
    return { tiers: [], tokenTotal, baseCost, credits, total: baseCost - credits + tokenTotal };
  });

  return { userTypeCosts, toolTotals };
}

// Input tokens scale with codebase size (log, anchored at 1M lines = 1.0×)
function codebaseMultiplier(lines: number): number {
  return Math.pow(lines / 1_000_000, 0.2);
}

// Convert raw log-slider position (0–100) to line count
function sliderToLines(pos: number): number {
  return Math.round(Math.pow(10, CB_LOG_MIN + (pos / 100) * (CB_LOG_MAX - CB_LOG_MIN)));
}

function calcTierSplit(inputs: CalcInputs): number[] {
  const { opusPct } = inputs;
  const remaining = 1 - opusPct;
  return [
    (BASE_SPLIT[0] / BASE_TOTAL) * remaining,
    (BASE_SPLIT[1] / BASE_TOTAL) * remaining,
    (BASE_SPLIT[2] / BASE_TOTAL) * remaining,
    (BASE_SPLIT[3] / BASE_TOTAL) * remaining,
    opusPct,
  ];
}

function calcTool(tool: ToolDef, inputs: CalcInputs): ToolResult {
  const { engineers, tasksPerDay, workingDays, codebaseLines } = inputs;
  const totalTasks = engineers * tasksPerDay * workingDays;
  const split = calcTierSplit(inputs);
  const cbMult = codebaseMultiplier(codebaseLines);

  const tiers: TierCost[] = TIERS.map((tier, i) => {
    const tasks = Math.round(totalTasks * split[i]);
    // Only input tokens scale with codebase size; output is fixed by task type
    const inputM = (tasks * tier.inputK * cbMult) / 1000;
    const outputM = (tasks * tier.outputK) / 1000;

    const rate = tool.rates[i];
    let tokenCost: number;

    if (rate.cachedInput !== undefined && tool.id === "cc" && i > 0) {
      const cachedIn = inputM * CACHE_HIT_RATE * rate.cachedInput;
      const freshIn  = inputM * (1 - CACHE_HIT_RATE) * rate.input;
      tokenCost = cachedIn + freshIn + outputM * rate.output;
    } else {
      tokenCost = inputM * rate.input + outputM * rate.output;
    }

    return { tasks, inputM, outputM, tokenCost };
  });

  const tokenTotal = tiers.reduce((sum, t) => sum + t.tokenCost, 0);
  const baseCost   = tool.baseCost(engineers);
  const credits    = tool.includedCredits(engineers);
  const total      = baseCost - credits + tokenTotal;

  return { tiers, tokenTotal, baseCost, credits, total };
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

function renderBarChart(results: ToolResult[], container: HTMLElement): void {
  const max = Math.max(...results.map(r => r.total)) * 1.1;
  const W = 320, H = 140, barW = 64, gap = 24;
  const startX = (W - (TOOLS.length * barW + (TOOLS.length - 1) * gap)) / 2;

  let svg = `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:${W}px;display:block;margin:0 auto;">`;

  for (let i = 0; i <= 4; i++) {
    const y = 10 + (i / 4) * (H - 50);
    const val = Math.round(max * (1 - i / 4));
    svg += `<line x1="0" y1="${y}" x2="${W}" y2="${y}" stroke="#2a2a2a" stroke-width="1"/>`;
    svg += `<text x="2" y="${y - 3}" fill="#666" font-size="8" font-family="Montserrat,sans-serif">$${(val / 1000).toFixed(1)}k</text>`;
  }

  results.forEach((r, i) => {
    const tool = TOOLS[i];
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

  // Default user type counts: tab=2, limited=4, daily=3, power=1 → 10 engineers
  const DEFAULT_COUNTS = [2, 4, 3, 1];
  let userCounts = [...DEFAULT_COUNTS];

  const initDerived = deriveFromUserCounts(DEFAULT_COUNTS);
  const defaultInputs: CalcInputs = {
    engineers:     initDerived.engineers,
    tasksPerDay:   initDerived.tasksPerDay,
    workingDays:   22,
    opusPct:       initDerived.opusPct,
    codebaseLines: CB_DEFAULT_LINES,
  };

  root.style.cssText = "background:#161616;border:1px solid #2a2a2a;padding:28px 28px 20px;font-family:'Georgia','Times New Roman',serif;color:#e2e2e2;";

  root.innerHTML = `
    <h2 style="font-family:'Playfair Display',Georgia,serif;font-weight:400;font-size:22px;color:#e2e2e2;margin:0 0 6px;">AI Coding Tool Cost Estimator</h2>
    <p style="color:#969696;font-size:14px;margin:0 0 28px;">Real-time cost comparison across GitHub Copilot, Claude Code, and Cursor. Adjust the inputs to match your team's usage pattern.</p>

    <div style="margin-bottom:16px;">
      <p style="font-family:'Montserrat',sans-serif;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#969696;margin:0 0 10px;">Team composition</p>
      ${USER_TYPES.map((ut, i) => `
        <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #222;">
          <span style="color:#e2e2e2;font-size:14px;">${ut.label}</span>
          <div style="display:flex;align-items:center;gap:10px;">
            <button id="cc-${ut.id}-dec" style="background:#222;border:1px solid #333;color:#969696;width:28px;height:28px;cursor:pointer;font-size:16px;line-height:1;border-radius:3px;">−</button>
            <span id="cc-${ut.id}-val" style="color:#e2e2e2;font-size:16px;font-weight:600;min-width:20px;text-align:center;">${DEFAULT_COUNTS[i]}</span>
            <button id="cc-${ut.id}-inc" style="background:#222;border:1px solid #333;color:#969696;width:28px;height:28px;cursor:pointer;font-size:16px;line-height:1;border-radius:3px;">+</button>
          </div>
        </div>`).join("")}
      <p id="cc-team-summary" style="color:#555;font-size:11px;margin:10px 0 0;">
        ${initDerived.engineers} engineers &nbsp;·&nbsp; ${initDerived.tasksPerDay} tasks/day avg &nbsp;·&nbsp; ${pct(initDerived.opusPct)} Opus
      </p>
    </div>
    <div style="margin-bottom:24px;">
      ${makeSlider({ id: "cc-codebase", label: "Codebase size", min: 0, max: 100, step: 1, value: CB_DEFAULT_POS, format: () => fmtLines(CB_DEFAULT_LINES), note: "Larger codebases require agents to read more files per task" })}
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
      Estimates only. User type counts drive engineers and average tasks/day. Codebase size and Opus % can be adjusted independently. Task mix: 35% small bug fixes / 30% minor changes / 20% new features / 15% architectural refactors. Working days: ${defaultInputs.workingDays}/month.
    </p>
  `;

  const resultsEl     = root.querySelector<HTMLElement>("#cc-results")!;
  const chartEl       = root.querySelector<HTMLElement>("#cc-chart")!;
  const assumptionsEl = root.querySelector<HTMLElement>("#cc-assumptions")!;

  let inputs = { ...defaultInputs };

  function renderAssumptions(): void {
    const linkStyle = (color: string) => `color:${color};font-size:10px;text-decoration:none;border-bottom:1px solid ${color}55;`;
    let html = `<table style="width:100%;border-collapse:collapse;font-size:12px;">
      <thead><tr style="border-bottom:1px solid #2a2a2a;">
        <th style="${thStyle("left")}">Type of task</th>`;
    TOOLS.forEach(t => {
      html += `<th style="${thStyle("right")}">
        <a href="${t.modelPricingUrl}" target="_blank" rel="noopener" style="${linkStyle(t.color)}">${t.name} rates ↗</a>
      </th>`;
    });
    html += `</tr></thead><tbody>`;
    TIERS.forEach((tier, i) => {
      const bg = i % 2 === 0 ? "#1a1a1a" : "#1e1e1e";
      html += `<tr><td style="${tdStyle("left", bg)};color:#969696;">${tier.label}<br><span style="color:#555;font-size:10px;">${tier.description}</span></td>`;
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

  function buildResultsTable({ userTypeCosts, toolTotals }: BreakdownResult): string {
    const minTotal = Math.min(...toolTotals.map(r => r.total));

    let html = `<div style="overflow-x:auto;margin-bottom:16px;">
      <table style="width:100%;border-collapse:collapse;font-size:13px;">
        <thead><tr style="border-bottom:2px solid #2a2a2a;">
          <th style="${thStyle("left")}">User type</th>`;

    TOOLS.forEach((tool, i) => {
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
      const ut = USER_TYPES[i];
      html += `<tr style="border-bottom:1px solid #2a2a2a;">
        <td style="${tdStyle("left", bg)}">
          <span style="color:#e2e2e2;">${utc.count}× ${utc.label}</span>
          <br><span style="color:#444;font-size:11px;">${ut.tasksPerDay} tasks/day · ${pct(ut.opusPct)} Opus</span>
        </td>`;
      utc.tokenCosts.forEach(cost => {
        html += `<td style="${tdStyle("right", bg)}">${fmt(cost)}</td>`;
      });
      html += `</tr>`;
    });

    const subtotalBg = "#1a1a1a";
    html += `<tr style="border-top:1px solid #444;">
      <td style="${tdStyle("left", subtotalBg)};color:#555;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Token total</td>`;
    toolTotals.forEach(r => { html += `<td style="${tdStyle("right", subtotalBg)};color:#555;">${fmt(r.tokenTotal)}</td>`; });
    html += `</tr>`;

    html += `<tr><td style="${tdStyle("left", "#1e1e1e")};color:#555;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Plan / credits</td>`;
    toolTotals.forEach(r => {
      const platformFee = r.baseCost - r.credits;
      const note = platformFee > 0 ? `+${fmt(platformFee)} platform` : r.credits > 0 ? `−${fmt(r.credits)} credits` : "API billing only";
      html += `<td style="${tdStyle("right", "#1e1e1e")};color:#555;font-size:11px;">${note}</td>`;
    });
    html += `</tr>`;

    html += `<tr><td style="${tdStyle("left", "#111")};font-weight:700;font-size:13px;text-transform:uppercase;letter-spacing:1px;">Total / month</td>`;
    toolTotals.forEach((r, i) => {
      const isWinner = r.total === minTotal;
      const c = isWinner ? "#f0ad4e" : TOOLS[i].color;
      html += `<td style="${tdStyle("right", "#111")};font-weight:700;font-size:16px;color:${c};">${fmt(r.total)}</td>`;
    });
    html += `</tr></tbody></table></div>`;

    html += `<p style="font-size:11px;color:#444;margin:0;">★ lowest cost at current settings &nbsp;·&nbsp; Copilot Opus rate is currently ~⅓ of direct API price — Microsoft preferential rate at time of writing &nbsp;·&nbsp; Claude Code costs reflect prompt caching</p>`;
    return html;
  }

  function update(): void {
    const breakdown = calcByUserType(userCounts, inputs.codebaseLines);
    renderBarChart(breakdown.toolTotals, chartEl);
    resultsEl.innerHTML = buildResultsTable(breakdown);
    renderAssumptions();
  }

  // ── Wire up user type +/− buttons ────────────────────────────────────────
  const summaryEl = root.querySelector<HTMLElement>("#cc-team-summary")!;

  function syncFromCounts(): void {
    const derived = deriveFromUserCounts(userCounts);
    inputs.engineers   = derived.engineers;
    inputs.tasksPerDay = derived.tasksPerDay;
    inputs.opusPct     = derived.opusPct;
    summaryEl.innerHTML =
      `${derived.engineers} engineer${derived.engineers !== 1 ? "s" : ""} &nbsp;·&nbsp; ${derived.tasksPerDay} tasks/day avg &nbsp;·&nbsp; ${pct(derived.opusPct)} Opus`;
    USER_TYPES.forEach((ut, i) => {
      root.querySelector<HTMLElement>(`#cc-${ut.id}-val`)!.textContent = String(userCounts[i]);
    });
    update();
  }

  USER_TYPES.forEach((ut, i) => {
    root!.querySelector(`#cc-${ut.id}-dec`)!.addEventListener("click", () => {
      if (userCounts[i] > 0) { userCounts[i]--; syncFromCounts(); }
    });
    root!.querySelector(`#cc-${ut.id}-inc`)!.addEventListener("click", () => {
      if (userCounts[i] < 20) { userCounts[i]++; syncFromCounts(); }
    });
  });

  // ── Wire up standard sliders (codebase only — Opus is derived from user types) ──
  const sliders: Array<{ id: string; key: keyof CalcInputs }> = [];

  sliders.forEach(({ id, key }) => {
    const slider = root.querySelector<HTMLInputElement>(`#${id}`)!;
    const valEl  = root.querySelector<HTMLElement>(`#${id}-val`)!;
    const fmtFn  = key === "engineers" || key === "tasksPerDay" ? String : pct;

    slider.addEventListener("input", () => {
      const v = parseFloat(slider.value);
      (inputs as Record<string, number>)[key] = v;
      valEl.textContent = fmtFn(v);
      update();
    });
  });

  // ── Wire up log-scale codebase slider ────────────────────────────────────
  const cbSlider = root.querySelector<HTMLInputElement>("#cc-codebase")!;
  const cbValEl  = root.querySelector<HTMLElement>("#cc-codebase-val")!;

  cbSlider.addEventListener("input", () => {
    const lines = sliderToLines(parseFloat(cbSlider.value));
    inputs.codebaseLines = lines;
    cbValEl.textContent  = fmtLines(lines);
    update();
  });

  // Initial render
  renderAssumptions();
  update();
}

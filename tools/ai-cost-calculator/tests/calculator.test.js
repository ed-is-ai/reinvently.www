import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";
import { applyOperatingModel, calculateEstimate } from "../src/calculator.js";

const pricing = JSON.parse(
  fs.readFileSync(new URL("../pricing.json", import.meta.url), "utf8")
);

test("pricing data has a complete default plan and model mapping", () => {
  pricing.modelMixes.forEach(mix => {
    assert.ok(Math.abs(mix.shares.reduce((sum, share) => sum + share, 0) - 1) < 0.000001);
  });

  pricing.operatingModels.forEach(profile => {
    assert.ok(pricing.modelMixes.some(mix => mix.id === profile.modelMix));
  });

  pricing.providers.forEach(provider => {
    assert.ok(provider.plans.some(plan => plan.id === pricing.defaults.selectedPlans[provider.id]));
    if (provider.usagePricingMode !== "unquantified") {
      assert.equal(provider.rates.length, 3);
    }
  });
});

test("the default scenario returns ordered ranges above each seat floor", () => {
  const estimate = calculateEstimate(pricing, pricing.defaults);

  assert.equal(estimate.results.length, 5);
  estimate.results.forEach(result => {
    assert.ok(result.low.total <= result.base.total);
    assert.ok(result.base.total <= result.high.total);
    assert.ok(result.base.total >= result.base.seatCost);
  });
});

test("operating-model profiles increase workload from assisted to agent-native", () => {
  const workloads = pricing.operatingModels.map(profile => {
    const state = applyOperatingModel(pricing, pricing.defaults, profile.id);
    const usage = calculateEstimate(pricing, state).results[0].base.usage;
    return {
      id: profile.id,
      input: usage.uncachedInputM + usage.cacheReadM + usage.cacheWriteM,
      output: usage.outputM
    };
  });

  assert.deepEqual(workloads.map(workload => workload.id), ["assisted", "spec-driven", "agent-native"]);
  assert.ok(workloads[0].input < workloads[1].input);
  assert.ok(workloads[1].input < workloads[2].input);
  assert.ok(workloads[0].output < workloads[1].output);
  assert.ok(workloads[1].output < workloads[2].output);
});

test("repository scale increases input usage without changing output usage", () => {
  const medium = structuredClone(pricing.defaults);
  medium.repositoryScale = "medium";
  const large = structuredClone(pricing.defaults);
  large.repositoryScale = "large";

  const mediumUsage = calculateEstimate(pricing, medium).results[0].base.usage;
  const largeUsage = calculateEstimate(pricing, large).results[0].base.usage;
  const mediumInput = mediumUsage.uncachedInputM + mediumUsage.cacheReadM + mediumUsage.cacheWriteM;
  const largeInput = largeUsage.uncachedInputM + largeUsage.cacheReadM + largeUsage.cacheWriteM;

  assert.ok(Math.abs(largeInput / mediumInput - 1.1) < 0.000001);
  assert.equal(largeUsage.outputM, mediumUsage.outputM);
});

test("optimised code search applies the same repository adjustment across providers", () => {
  const state = structuredClone(pricing.defaults);
  state.repositoryScale = "large";
  const estimate = calculateEstimate(pricing, state);
  const claude = estimate.results.find(result => result.provider.id === "claude");
  const cursor = estimate.results.find(result => result.provider.id === "cursor");
  const totalInput = result =>
    result.base.usage.uncachedInputM +
    result.base.usage.cacheReadM +
    result.base.usage.cacheWriteM;

  assert.ok(Math.abs(totalInput(claude) / 88 - 1.1) < 0.000001);
  assert.ok(Math.abs(totalInput(cursor) / 88 - 1.1) < 0.000001);
  assert.equal(totalInput(cursor), totalInput(claude));
});

test("change scope adjusts both input and output usage", () => {
  const typical = structuredClone(pricing.defaults);
  typical.changeScope = "typical";
  const broad = structuredClone(pricing.defaults);
  broad.changeScope = "broad";

  const typicalUsage = calculateEstimate(pricing, typical).results[0].base.usage;
  const broadUsage = calculateEstimate(pricing, broad).results[0].base.usage;
  const typicalInput = typicalUsage.uncachedInputM + typicalUsage.cacheReadM + typicalUsage.cacheWriteM;
  const broadInput = broadUsage.uncachedInputM + broadUsage.cacheReadM + broadUsage.cacheWriteM;

  assert.ok(Math.abs(broadInput / typicalInput - 1.35) < 0.000001);
  assert.ok(Math.abs(broadUsage.outputM / typicalUsage.outputM - 1.5) < 0.000001);
});

test("known usage returns a point estimate rather than a scenario range", () => {
  const state = structuredClone(pricing.defaults);
  state.mode = "actual";
  const estimate = calculateEstimate(pricing, state);

  estimate.results.forEach(result => {
    assert.equal(result.low.total, result.base.total);
    assert.equal(result.base.total, result.high.total);
  });
});

test("Cursor first-party usage is not assigned third-party model charges", () => {
  const state = structuredClone(pricing.defaults);
  state.cursorFirstPartyPct = 100;
  const cursor = calculateEstimate(pricing, state).results.find(
    result => result.provider.id === "cursor"
  );

  assert.equal(cursor.base.usageCost, 0);
  assert.equal(cursor.base.total, cursor.base.seatCost);
});

test("Cursor usage below its included allowance does not increase the subscription total", () => {
  const cursor = calculateEstimate(pricing, pricing.defaults).results.find(
    result => result.provider.id === "cursor"
  );

  assert.ok(cursor.base.usageCost > 0);
  assert.ok(cursor.base.usageCost < cursor.base.included);
  assert.equal(cursor.base.overage, 0);
  assert.equal(cursor.base.total, cursor.base.seatCost);
});

test("Claude Team plans are marked as upper bounds", () => {
  const state = structuredClone(pricing.defaults);
  state.selectedPlans.claude = "team-standard";
  const claude = calculateEstimate(pricing, state).results.find(
    result => result.provider.id === "claude"
  );

  assert.equal(claude.upperBound, true);
  assert.equal(claude.base.included, null);
});

test("cache writes are charged separately from cache reads", () => {
  const withoutWrites = structuredClone(pricing.defaults);
  withoutWrites.scenario.cacheWritePct = 0;
  const withWrites = structuredClone(pricing.defaults);
  withWrites.scenario.cacheWritePct = 20;

  const low = calculateEstimate(pricing, withoutWrites).results[0].base.usageCost;
  const high = calculateEstimate(pricing, withWrites).results[0].base.usageCost;
  assert.ok(high > low);
});

test("Codex pay-as-you-go applies the token-based credit rate without a seat fee", () => {
  const state = structuredClone(pricing.defaults);
  state.selectedPlans.codex = "payg";
  const codex = calculateEstimate(pricing, state).results.find(
    result => result.provider.id === "codex"
  );

  assert.equal(codex.base.seatCost, 0);
  assert.ok(codex.base.usageCost > 0);
  assert.equal(codex.base.total, codex.base.usageCost);
});

test("Codex Business is the default and is marked as an upper bound", () => {
  const codex = calculateEstimate(pricing, pricing.defaults).results.find(
    result => result.provider.id === "codex"
  );

  assert.equal(codex.plan.id, "business");
  assert.equal(codex.upperBound, true);
  assert.equal(codex.base.included, null);
});

test("Codex Enterprise uses entered contract cost and shared credits", () => {
  const state = structuredClone(pricing.defaults);
  state.selectedPlans.codex = "enterprise-flex";
  state.codexContract.monthlyBaseUsd = 1000;
  state.codexContract.includedCredits = 10000;
  const codex = calculateEstimate(pricing, state).results.find(
    result => result.provider.id === "codex"
  );

  assert.equal(codex.needsContractInput, false);
  assert.equal(codex.base.seatCost, 1000);
  assert.equal(codex.base.included, 400);
  assert.equal(codex.base.total, 1000 + Math.max(0, codex.base.usageCost - 400));
});

test("Codex Enterprise does not present a zero-cost result without contract inputs", () => {
  const state = structuredClone(pricing.defaults);
  state.selectedPlans.codex = "enterprise-flex";
  const codex = calculateEstimate(pricing, state).results.find(
    result => result.provider.id === "codex"
  );

  assert.equal(codex.needsContractInput, true);
});

test("Antigravity is reported as a seat floor when usage cannot be quantified", () => {
  const antigravity = calculateEstimate(pricing, pricing.defaults).results.find(
    result => result.provider.id === "antigravity"
  );

  assert.equal(antigravity.floorOnly, true);
  assert.equal(antigravity.base.usageKnown, false);
  assert.equal(antigravity.base.total, antigravity.base.seatCost);
});

test("the crawlable default-cost snapshot matches calculator totals", () => {
  const html = fs.readFileSync(new URL("../index.html", import.meta.url), "utf8");
  const estimate = calculateEstimate(pricing, pricing.defaults);

  estimate.results.forEach(result => {
    const pattern = new RegExp(
      `data-default-provider="${result.provider.id}" data-default-total="([0-9]+)"`
    );
    const match = html.match(pattern);
    assert.ok(match, `missing static snapshot for ${result.provider.id}`);
    assert.equal(Number(match[1]), Math.round(result.base.total));
  });
});

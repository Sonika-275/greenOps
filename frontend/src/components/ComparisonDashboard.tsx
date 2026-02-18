import { useState } from "react";
import { compareCode } from "../services/api";
import type { ComparisonResponse } from "../types/comparison";

import MetricCard from "./MetricsCard";
import ImpactVisualization from "./ImpactVisualisation";

const ComparisonDashboard = () => {
  const [originalCode, setOriginalCode] = useState("");
  const [optimizedCode, setOptimizedCode] = useState("");
  const [result, setResult] = useState<ComparisonResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);


  // ✅ NEW: scale state
  const [runsPerDay, setRunsPerDay] = useState(1000);

  const handleCompare = async () => {
    if (!originalCode || !optimizedCode) {
      setError("Please provide both original and optimized code.");
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const data = await compareCode(originalCode, optimizedCode);
      setResult(data);
    } catch {
      setError("Failed to compare code. Check backend connection.");
    } finally {
      setLoading(false);
    }
  };

  // ✅ NEW: dynamic scaling calculations
  const dailyBefore =
    result ? result.original.co2_kg * runsPerDay : 0;

  const dailyAfter =
    result ? result.optimized.co2_kg * runsPerDay : 0;

  const annualSavings =
    result ? (dailyBefore - dailyAfter) * 365 : 0;

  const treesSaved =
    annualSavings > 0 ? annualSavings / 21 : 0;

  return (
    <div className="w-full max-w-6xl mx-auto p-8">
      <h1 className="text-4xl font-bold mb-8 text-green-400">
        GreenOps Carbon Intelligence Dashboard
      </h1>

      {/* Code Input Section */}
      <div className="grid grid-cols-2 gap-6 mb-6">
        <textarea
          className="bg-gray-900 p-4 rounded-lg border border-gray-700 focus:outline-none focus:border-green-400"
          rows={12}
          placeholder="Paste Original Code..."
          value={originalCode}
          onChange={(e) => setOriginalCode(e.target.value)}
        />

        <textarea
          className="bg-gray-900 p-4 rounded-lg border border-gray-700 focus:outline-none focus:border-green-400"
          rows={12}
          placeholder="Paste Optimized Code..."
          value={optimizedCode}
          onChange={(e) => setOptimizedCode(e.target.value)}
        />
      </div>

      <button
        onClick={handleCompare}
        className="bg-green-500 hover:bg-green-600 text-black font-semibold px-6 py-3 rounded-lg transition"
      >
        {loading ? "Analyzing..." : "Compare Carbon Impact"}
      </button>

      {error && (
        <p className="text-red-400 mt-4">{error}</p>
      )}

      {/* Results Section */}
      {result && (
        <div className="mt-12 space-y-8">
          <h2 className="text-2xl font-semibold text-green-400">
            Carbon Impact Analysis
          </h2>

          {/* Per-run Metrics (unchanged) */}
          <div className="grid grid-cols-2 gap-6">
            <MetricCard
              title="Original CO₂ per Run"
              value={`${result.original.co2_kg} kg`}
            />
            <MetricCard
              title="Optimized CO₂ per Run"
              value={`${result.optimized.co2_kg} kg`}
            />
            <MetricCard
              title="Reduction %"
              value={`${result.comparison.reduction_percent}%`}
              highlight
            />
            <MetricCard
              title="CO₂ Saved per Run"
              value={`${result.comparison.co2_saved_kg} kg`}
              highlight
            />
          </div>

          {/* ✅ NEW: Scaling Section */}
          <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
            <p className="text-lg text-gray-300 mb-4">
              {result.comparison.impact_message}
            </p>

            {/* Scale Slider */}
            <div className="mb-6">
              <label className="block text-gray-400 mb-2">
                Production Scale: {runsPerDay.toLocaleString()} runs per day
              </label>

              <input
                type="range"
                min="100"
                max="100000"
                step="100"
                value={runsPerDay}
                onChange={(e) => setRunsPerDay(Number(e.target.value))}
                className="w-full"
              />
            </div>

            {/* Dynamic Impact */}
            <div className="space-y-2 text-green-400 font-semibold">
              <p>
                Daily CO₂ Before: {dailyBefore.toFixed(2)} kg
              </p>
              <p>
                Daily CO₂ After: {dailyAfter.toFixed(2)} kg
              </p>
              <p className="text-xl">
                Annual CO₂ Savings: {annualSavings.toFixed(0)} kg
              </p>
              <p>
                Trees Saved Per Year: {Math.round(treesSaved)}
              </p>
              
             <ImpactVisualization
                perRunBefore={result.original.co2_kg}
                perRunAfter={result.optimized.co2_kg}
 
            />

            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ComparisonDashboard;

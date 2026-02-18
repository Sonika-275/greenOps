import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend,
} from "recharts";

interface Props {
  perRunBefore: number;
  perRunAfter: number;
}

// Cost per kg CO₂ saved
const CARBON_COST_PER_KG = 0.1;

const SCALE_POINTS = [1000, 10000, 25000, 50000, 75000, 100000];

const ImpactVisualization = ({ perRunBefore, perRunAfter }: Props) => {
  const data = SCALE_POINTS.map((runs) => {
    const annualBefore = perRunBefore * runs * 365;
    const annualAfter = perRunAfter * runs * 365;

    const carbonSaved = annualBefore - annualAfter;
    const revenueSaved = carbonSaved * CARBON_COST_PER_KG;

    return {
      runs,
      carbon: carbonSaved,
      revenue: revenueSaved,
    };
  });

  const tickFormatter = (value: number) => {
    if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`;
    if (value >= 1000) return `${(value / 1000).toFixed(0)}k`;
    return value.toString();
  };

  return (
    <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 mt-10">
      <h3 className="text-xl font-semibold text-green-400 mb-6">
        Annual Carbon & Revenue Impact
      </h3>

      <ResponsiveContainer width="100%" height={400}>
        <ComposedChart data={data}>
          <defs>
            <linearGradient id="carbonGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#22c55e" stopOpacity={0.8} />
              <stop offset="100%" stopColor="#22c55e" stopOpacity={0.3} />
            </linearGradient>
          </defs>

          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis
            dataKey="runs"
            stroke="#aaa"
            tickFormatter={(value) => `${value / 1000}k`}
          />

          <YAxis
            yAxisId="left"
            stroke="#22c55e"
            tickFormatter={tickFormatter}
            label={{
              value: "Carbon Saved (kg)",
              angle: -90,
              position: "insideLeft",
              dy: 0,
              fill: "#22c55e",
              style: { fontWeight: 600 },
            }}
          />

          <YAxis
            yAxisId="right"
            orientation="right"
            stroke="#facc15"
            tickFormatter={tickFormatter}
            label={{
              value: "Revenue Saved (₹)",
              angle: 90,
              position: "insideRight",
              dy: 0,
              fill: "#facc15",
              style: { fontWeight: 600 },
            }}
          />

          <Tooltip
            formatter={(value, name) => {
              if (value === undefined || value === null) return "";
              if (name === "carbon") return [`${(value as number).toLocaleString()} kg`, "Carbon Saved"];
              if (name === "revenue") return [`₹${(value as number).toLocaleString()}`, "Revenue Saved"];
              return value;
            }}
          />

          {/* Updated Legend */}
          <Legend
            verticalAlign="bottom"
            align="center"
            wrapperStyle={{
              color: "#fff",
              fontSize: 12,
              marginTop: 20,
            }}
          />

          <Bar
            yAxisId="left"
            dataKey="carbon"
            fill="url(#carbonGradient)"
            barSize={30}
            fillOpacity={0.8}
            name="Carbon Saved"
          />

          <Line
            yAxisId="right"
            type="monotone"
            dataKey="revenue"
            stroke="#facc15"
            strokeWidth={4}
            dot={{ r: 4, stroke: "#facc15", strokeWidth: 2, fill: "#fff" }}
            name="Revenue Saved"
          />
        </ComposedChart>
      </ResponsiveContainer>

      <div className="mt-4 text-sm text-gray-400">
        Green Bars = Carbon Saved (kg) | Yellow Line = Revenue Saved (₹)
      </div>
    </div>
  );
};

export default ImpactVisualization;

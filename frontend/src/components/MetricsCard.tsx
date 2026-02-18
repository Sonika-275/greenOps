interface MetricCardProps {
  title: string;
  value: string | number;
  highlight?: boolean;
}

const MetricCard = ({ title, value, highlight }: MetricCardProps) => {
  return (
    <div
      className={`p-6 rounded-xl border ${
        highlight
          ? "bg-green-900/40 border-green-500"
          : "bg-gray-900 border-gray-800"
      }`}
    >
      <p className="text-sm text-gray-400 mb-2">{title}</p>
      <p
        className={`text-3xl font-bold ${
          highlight ? "text-green-400" : "text-white"
        }`}
      >
        {value}
      </p>
    </div>
  );
};

export default MetricCard;

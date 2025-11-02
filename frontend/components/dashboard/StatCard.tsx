interface StatCardProps {
  title: string;
  value: string | number;
  icon: string;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  subtitle?: string;
}

export default function StatCard({
  title,
  value,
  icon,
  trend,
  subtitle,
}: StatCardProps) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mb-2">{value}</p>
          {subtitle && (
            <p className="text-sm text-gray-500">{subtitle}</p>
          )}
        </div>
        <div className="ml-4 flex-shrink-0">
          <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center text-2xl">
            {icon}
          </div>
        </div>
      </div>

      {trend && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          <div className="flex items-center">
            <span
              className={`inline-flex items-center text-sm font-medium ${
                trend.isPositive ? "text-green-600" : "text-red-600"
              }`}
            >
              {trend.isPositive ? "↑" : "↓"} {Math.abs(trend.value)}%
            </span>
            <span className="ml-2 text-sm text-gray-500">vs last month</span>
          </div>
        </div>
      )}
    </div>
  );
}

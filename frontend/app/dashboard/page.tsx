"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import DashboardLayout from "@/components/dashboard/DashboardLayout";
import { Search, Play, ExternalLink, Clock, CheckCircle, XCircle, Loader } from "lucide-react";

interface Scan {
  id: string;
  target_id?: string;
  url?: string;
  status: string;
  progress: number;
  checks: string[];
  started_at?: string;
  completed_at?: string;
  created_at: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const [searchUrl, setSearchUrl] = useState("");
  const [isScanning, setIsScanning] = useState(false);
  const [scans, setScans] = useState<Scan[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Fetch scan history on mount
  useEffect(() => {
    fetchScans(true);
  }, []);

  // Auto-refresh when there are running/queued scans
  useEffect(() => {
    const hasActiveScans = scans.some(
      (scan) => scan.status === "running" || scan.status === "queued"
    );

    if (hasActiveScans) {
      const interval = setInterval(() => {
        fetchScans(false); // Silent refresh
      }, 3000); // Refresh every 3 seconds

      return () => clearInterval(interval);
    }
  }, [scans]);

  const fetchScans = async (showLoading = false) => {
    try {
      if (showLoading) {
        setLoading(true);
      } else {
        setIsRefreshing(true);
      }

      const token = localStorage.getItem("access_token");
      if (!token) {
        router.push("/login");
        return;
      }

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/scans?limit=20`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.status === 401) {
        // Token is invalid or expired, clear and redirect to login
        localStorage.clear();
        router.push("/login");
        return;
      }

      if (!response.ok) {
        throw new Error("Failed to fetch scans");
      }

      const data = await response.json();
      setScans(data.scans || []);
    } catch (err) {
      console.error("Error fetching scans:", err);
      setError("Failed to load scan history");
    } finally {
      if (showLoading) {
        setLoading(false);
      } else {
        setIsRefreshing(false);
      }
    }
  };

  const handleQuickScan = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!searchUrl.trim()) return;

    setIsScanning(true);
    setError("");

    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        router.push("/login");
        return;
      }

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/scans`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            url: searchUrl,
            checks: ["headers", "ssl"],
            config: {
              port_scan_enabled: false,
              headers_check_enabled: true,
              ssl_check_enabled: true,
              dns_check_enabled: false,
              bruteforce_enabled: false,
              ping_check_enabled: false,
              timeout: 300,
            },
          }),
        }
      );

      const responseText = await response.text();

      if (response.status === 401) {
        // Token is invalid or expired, clear and redirect to login
        localStorage.clear();
        router.push("/login");
        return;
      }

      if (!response.ok) {
        let errorMessage = "Failed to start scan";
        try {
          const errorData = JSON.parse(responseText);
          errorMessage = errorData.error || errorMessage;
        } catch {
          errorMessage = responseText || errorMessage;
        }
        throw new Error(errorMessage);
      }

      const newScan = JSON.parse(responseText);

      // Add to scans list at the top
      setScans([newScan, ...scans]);
      setSearchUrl("");
    } catch (err: any) {
      console.error("Error starting scan:", err);
      setError(err.message || "Failed to start scan");
    } finally {
      setIsScanning(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case "failed":
        return <XCircle className="w-5 h-5 text-red-600" />;
      case "running":
        return <Loader className="w-5 h-5 text-blue-600 animate-spin" />;
      case "queued":
        return <Clock className="w-5 h-5 text-yellow-600" />;
      default:
        return <Clock className="w-5 h-5 text-gray-600" />;
    }
  };

  const getStatusBadge = (status: string) => {
    const styles = {
      completed: "bg-green-100 text-green-800 border-green-200",
      running: "bg-blue-100 text-blue-800 border-blue-200",
      failed: "bg-red-100 text-red-800 border-red-200",
      queued: "bg-yellow-100 text-yellow-800 border-yellow-200",
      cancelled: "bg-gray-100 text-gray-800 border-gray-200",
    };
    return (
      styles[status as keyof typeof styles] || styles.queued
    );
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const getDisplayUrl = (scan: Scan) => {
    return scan.url || `Target ID: ${scan.target_id}`;
  };

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Page header */}
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold text-gray-900">Quick Scan</h1>
            {isRefreshing && (
              <span className="text-xs text-blue-600 flex items-center gap-1">
                <Loader className="w-3 h-3 animate-spin" />
                Updating...
              </span>
            )}
          </div>
          <p className="mt-2 text-gray-600">
            Enter any URL to start scanning for vulnerabilities
          </p>
        </div>

        {/* Quick Search Form */}
        <div className="bg-white rounded-xl border-2 border-gray-200 p-8 shadow-sm">
          <form onSubmit={handleQuickScan}>
            <div className="flex gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <input
                    type="text"
                    value={searchUrl}
                    onChange={(e) => setSearchUrl(e.target.value)}
                    placeholder="Enter URL or domain (e.g., example.com or https://example.com)"
                    className="w-full pl-12 pr-4 py-4 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
                    disabled={isScanning}
                  />
                </div>
              </div>
              <button
                type="submit"
                disabled={isScanning || !searchUrl.trim()}
                className="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 whitespace-nowrap"
              >
                {isScanning ? (
                  <>
                    <Loader className="w-5 h-5 animate-spin" />
                    Scanning...
                  </>
                ) : (
                  <>
                    <Play className="w-5 h-5" />
                    Start Scan
                  </>
                )}
              </button>
            </div>
          </form>

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-600">{error}</p>
            </div>
          )}

          <div className="mt-6 flex items-center gap-2 text-sm text-gray-600">
            <div className="flex items-center gap-1">
              <CheckCircle className="w-4 h-4 text-blue-600" />
              <span>Security Headers</span>
            </div>
            <span>•</span>
            <div className="flex items-center gap-1">
              <CheckCircle className="w-4 h-4 text-blue-600" />
              <span>SSL/TLS Certificate</span>
            </div>
          </div>
          <p className="mt-3 text-xs text-gray-500">
            ⚡ Ultra-fast scan - completes in ~10 seconds!
          </p>
        </div>

        {/* Scan History */}
        <div className="bg-white rounded-lg border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">
              Scan History
            </h2>
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-12">
              <Loader className="w-8 h-8 text-blue-600 animate-spin" />
            </div>
          ) : scans.length === 0 ? (
            <div className="text-center py-12">
              <Search className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">No scans yet. Start your first scan above!</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Target / URL
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Progress
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Checks
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {scans.map((scan) => (
                    <tr key={scan.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <ExternalLink className="w-4 h-4 text-gray-400" />
                          <span className="font-medium text-gray-900 truncate max-w-xs">
                            {getDisplayUrl(scan)}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          {getStatusIcon(scan.status)}
                          <span
                            className={`px-3 py-1 text-xs font-medium rounded-full border ${getStatusBadge(
                              scan.status
                            )}`}
                          >
                            {scan.status}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-600 h-2 rounded-full transition-all"
                              style={{ width: `${scan.progress}%` }}
                            />
                          </div>
                          <span className="text-sm text-gray-600">
                            {scan.progress}%
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {scan.checks.length} checks
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {formatDate(scan.created_at)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          onClick={() => router.push(`/dashboard/scans/${scan.id}`)}
                          className="text-blue-600 hover:text-blue-800 font-medium"
                        >
                          View
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}

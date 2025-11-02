"use client";

import { useState } from "react";
import DashboardLayout from "@/components/dashboard/DashboardLayout";

export default function TargetsPage() {
  const [showAddModal, setShowAddModal] = useState(false);

  // Mock data - will be replaced with real API calls
  const targets = [
    {
      id: "1",
      name: "Main Website",
      hostname: "example.com",
      description: "Primary customer-facing website",
      tags: ["production", "high-priority"],
      lastScan: "2025-11-02 14:30",
      status: "active",
    },
    {
      id: "2",
      name: "API Server",
      hostname: "api.example.com",
      description: "Backend API services",
      tags: ["production", "api"],
      lastScan: "2025-11-02 15:45",
      status: "active",
    },
    {
      id: "3",
      name: "Mobile App Backend",
      hostname: "app.example.com",
      description: "Mobile application backend",
      tags: ["staging"],
      lastScan: "2025-11-01 09:15",
      status: "active",
    },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Targets</h1>
            <p className="mt-2 text-gray-600">
              Manage your security scan targets
            </p>
          </div>
          <button
            onClick={() => setShowAddModal(true)}
            className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors font-medium"
          >
            + Add Target
          </button>
        </div>

        {/* Filters */}
        <div className="flex items-center gap-4">
          <input
            type="text"
            placeholder="Search targets..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
          />
          <select className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent">
            <option>All Statuses</option>
            <option>Active</option>
            <option>Inactive</option>
          </select>
        </div>

        {/* Targets list */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {targets.map((target) => (
            <div
              key={target.id}
              className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {target.name}
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">
                    {target.hostname}
                  </p>
                </div>
                <span className="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800">
                  {target.status}
                </span>
              </div>

              <p className="text-sm text-gray-600 mb-4">
                {target.description}
              </p>

              {/* Tags */}
              <div className="flex flex-wrap gap-2 mb-4">
                {target.tags.map((tag) => (
                  <span
                    key={tag}
                    className="px-2 py-1 text-xs font-medium rounded bg-gray-100 text-gray-700"
                  >
                    {tag}
                  </span>
                ))}
              </div>

              {/* Last scan info */}
              <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                <span className="text-xs text-gray-500">
                  Last scan: {target.lastScan}
                </span>
                <div className="flex items-center gap-2">
                  <button className="px-3 py-1 text-sm font-medium text-primary hover:bg-primary/10 rounded transition-colors">
                    Scan
                  </button>
                  <button className="px-3 py-1 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded transition-colors">
                    Edit
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Add target modal */}
        {showAddModal && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
              <h2 className="text-xl font-bold text-gray-900 mb-4">
                Add New Target
              </h2>
              <form className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Name
                  </label>
                  <input
                    type="text"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                    placeholder="My Website"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Hostname
                  </label>
                  <input
                    type="text"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                    placeholder="example.com"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                    rows={3}
                    placeholder="Brief description of this target"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Tags (comma-separated)
                  </label>
                  <input
                    type="text"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                    placeholder="production, high-priority"
                  />
                </div>
                <div className="flex items-center gap-3 pt-4">
                  <button
                    type="submit"
                    className="flex-1 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors font-medium"
                  >
                    Add Target
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowAddModal(false)}
                    className="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

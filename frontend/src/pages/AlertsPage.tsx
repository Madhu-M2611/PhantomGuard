import { useDeferredValue, useEffect, useState } from "react";
import { motion } from "framer-motion";
import { AlertTriangle, Search } from "lucide-react";

import { useAuth } from "../auth/useAuth";
import { fetchAlerts } from "../lib/api";
import type { Alert } from "../lib/types";

const severityOptions = ["all", "critical", "high", "medium", "low"];

const AlertsPage = () => {
  const { token } = useAuth();
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [severity, setSeverity] = useState("all");
  const [search, setSearch] = useState("");
  const [error, setError] = useState<string | null>(null);

  const deferredSearch = useDeferredValue(search);

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      try {
        const response = await fetchAlerts(
          token,
          severity === "all" ? undefined : severity,
        );
        if (!cancelled) {
          setAlerts(response);
          setError(null);
        }
      } catch (loadError) {
        if (!cancelled) {
          setError(
            loadError instanceof Error ? loadError.message : "Failed to load alerts",
          );
        }
      }
    };

    void load();
    return () => {
      cancelled = true;
    };
  }, [severity, token]);

  const filteredAlerts = alerts.filter((alert) => {
    const haystack = [
      alert.title,
      alert.description,
      alert.file_path,
      alert.process_name,
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase();
    return haystack.includes(deferredSearch.toLowerCase());
  });

  return (
    <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="eyebrow">Alerts & Incidents</p>
          <h1 className="mt-2 font-headline text-4xl font-black tracking-tight text-on-surface">
            Threat queue
          </h1>
          <p className="mt-3 max-w-2xl text-sm leading-7 text-on-surface-variant">
            Review every alert emitted by the detection pipeline, filter by severity,
            and inspect the impacted file path or process.
          </p>
        </div>

        <div className="grid gap-3 sm:grid-cols-2">
          <div className="relative">
            <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-on-surface-variant" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="field pl-11"
              placeholder="Search title, process, or file path"
            />
          </div>
          <select
            value={severity}
            onChange={(e) => setSeverity(e.target.value)}
            className="field"
          >
            {severityOptions.map((option) => (
              <option key={option} value={option}>
                {option.toUpperCase()}
              </option>
            ))}
          </select>
        </div>
      </div>

      {error ? <div className="panel border-error/30 text-error">{error}</div> : null}

      <div className="grid gap-4 md:grid-cols-3">
        <div className="metric-panel">
          <p className="eyebrow">Visible Alerts</p>
          <p className="mt-4 font-headline text-4xl font-bold text-on-surface">
            {filteredAlerts.length}
          </p>
          <p className="mt-2 text-sm text-on-surface-variant">Current table result set.</p>
        </div>
        <div className="metric-panel">
          <p className="eyebrow">Severity Filter</p>
          <p className="mt-4 font-headline text-4xl font-bold uppercase text-on-surface">
            {severity}
          </p>
          <p className="mt-2 text-sm text-on-surface-variant">Focused incident view.</p>
        </div>
        <div className="metric-panel">
          <p className="eyebrow">Response Mode</p>
          <div className="mt-4 inline-flex items-center gap-3">
            <AlertTriangle className="h-5 w-5 text-primary" />
            <span className="font-headline text-2xl font-bold text-on-surface">Live triage</span>
          </div>
          <p className="mt-2 text-sm text-on-surface-variant">Operator-ready forensic review.</p>
        </div>
      </div>

      <div className="table-shell">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-outline-variant/20 text-left">
            <thead className="bg-surface-container-high/80 font-label text-xs uppercase tracking-[0.24em] text-on-surface-variant">
              <tr>
                <th className="px-5 py-4">Severity</th>
                <th className="px-5 py-4">Title</th>
                <th className="px-5 py-4">Process</th>
                <th className="px-5 py-4">Path</th>
                <th className="px-5 py-4">Time</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-outline-variant/10 text-sm">
              {filteredAlerts.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-5 py-10 text-center text-on-surface-variant">
                    No alerts match the current filters.
                  </td>
                </tr>
              ) : (
                filteredAlerts.map((alert) => (
                  <tr key={alert.id} className="bg-surface-container/40 transition hover:bg-surface-container-high/55">
                    <td className="px-5 py-4">
                      <span className="rounded-full border border-primary/25 bg-primary/10 px-3 py-1 font-label text-[11px] font-bold uppercase tracking-[0.22em] text-primary">
                        {alert.severity}
                      </span>
                    </td>
                    <td className="px-5 py-4">
                      <p className="font-semibold text-on-surface">{alert.title}</p>
                      <p className="mt-1 max-w-md text-on-surface-variant">
                        {alert.description || "No description"}
                      </p>
                    </td>
                    <td className="px-5 py-4 text-on-surface-variant">
                      {alert.process_name || "n/a"}
                    </td>
                    <td className="px-5 py-4 text-on-surface-variant">
                      {alert.file_path || "n/a"}
                    </td>
                    <td className="px-5 py-4 font-label text-on-surface-variant">
                      {new Date(alert.timestamp).toLocaleString()}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </motion.div>
  );
};

export default AlertsPage;

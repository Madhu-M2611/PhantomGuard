import { useEffect, useState } from "react";
import { motion } from "framer-motion";

import { useAuth } from "../auth/useAuth";
import { fetchLogs, fetchStats } from "../lib/api";
import type { LogEntry, StatsResponse } from "../lib/types";

const AnalyticsPage = () => {
  const { token } = useAuth();
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      try {
        const [statsResponse, logsResponse] = await Promise.all([
          fetchStats(token),
          fetchLogs(token),
        ]);
        if (!cancelled) {
          setStats(statsResponse);
          setLogs(logsResponse.slice(0, 12));
          setError(null);
        }
      } catch (loadError) {
        if (!cancelled) {
          setError(
            loadError instanceof Error
              ? loadError.message
              : "Failed to load analytics data",
          );
        }
      }
    };

    void load();
    return () => {
      cancelled = true;
    };
  }, [token]);

  const cpuSeries = logs.map((log) => Math.min(Math.round(log.cpu_usage ?? 0), 100));
  const entropySeries = logs.map((log) =>
    Math.min(Math.round((log.entropy ?? 0) * 12.5), 100),
  );

  return (
    <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
      <div>
        <p className="eyebrow">Analytics</p>
        <h1 className="mt-2 font-headline text-4xl font-black tracking-tight text-on-surface">
          Detection metrics
        </h1>
          <p className="mt-3 max-w-2xl text-sm leading-7 text-on-surface-variant">
            Compare recent CPU usage, event entropy, and alert throughput to understand
            how the monitored host is behaving over time.
          </p>
        </div>

      {error ? <div className="panel border-error/30 text-error">{error}</div> : null}

      <section className="grid gap-6 lg:grid-cols-3">
        <div className="metric-panel">
          <p className="eyebrow">24h Volume</p>
          <p className="mt-4 text-4xl font-black text-on-surface">
            {stats?.recent_activity.logs_24h ?? 0}
          </p>
          <p className="mt-2 text-sm text-on-surface-variant">Log events captured over the last 24 hours.</p>
        </div>
        <div className="metric-panel">
          <p className="eyebrow">24h Alerts</p>
          <p className="mt-4 text-4xl font-black text-on-surface">
            {stats?.recent_activity.alerts_24h ?? 0}
          </p>
          <p className="mt-2 text-sm text-on-surface-variant">Security alerts emitted in the last 24 hours.</p>
        </div>
        <div className="metric-panel">
          <p className="eyebrow">Severity Spread</p>
          <p className="mt-4 text-4xl font-black capitalize text-on-surface">
            {stats?.system_status ?? "loading"}
          </p>
          <p className="mt-2 text-sm text-on-surface-variant">
            Current backend system assessment derived from alert rate.
          </p>
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-2">
        <div className="panel">
          <p className="eyebrow">CPU Usage</p>
          <h2 className="mt-2 font-headline text-2xl font-bold text-on-surface">
            Recent process load
          </h2>
          <div className="mt-8 flex h-64 items-end gap-2">
            {(cpuSeries.length ? cpuSeries : [0]).map((point, index) => (
              <div key={`cpu-${index}`} className="flex flex-1 flex-col items-center gap-3">
                <div
                  className="w-full rounded-t-2xl bg-primary/80 shadow-primary-glow"
                  style={{ height: `${Math.max(point, 8)}%` }}
                />
                <span className="font-label text-[10px] uppercase tracking-[0.2em] text-on-surface-variant">
                  {index + 1}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <p className="eyebrow">Entropy Trend</p>
          <h2 className="mt-2 font-headline text-2xl font-bold text-on-surface">
            File activity volatility
          </h2>
          <div className="mt-8 flex h-64 items-end gap-2">
            {(entropySeries.length ? entropySeries : [0]).map((point, index) => (
              <div key={`entropy-${index}`} className="flex flex-1 flex-col items-center gap-3">
                <div
                  className="w-full rounded-t-2xl bg-secondary-container/80 shadow-kinetic-pulse"
                  style={{ height: `${Math.max(point, 8)}%` }}
                />
                <span className="font-label text-[10px] uppercase tracking-[0.2em] text-on-surface-variant">
                  {index + 1}
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>
    </motion.div>
  );
};

export default AnalyticsPage;

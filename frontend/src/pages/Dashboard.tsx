import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  Activity,
  AlertTriangle,
  Clock3,
  FileSearch,
  Shield,
} from "lucide-react";

import { useAuth } from "../auth/useAuth";
import { fetchAlerts, fetchLogs, fetchStats } from "../lib/api";
import type { Alert, LogEntry, StatsResponse } from "../lib/types";

const Dashboard = () => {
  const { token } = useAuth();
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      try {
        const [statsResponse, alertsResponse, logsResponse] = await Promise.all([
          fetchStats(token),
          fetchAlerts(token),
          fetchLogs(token),
        ]);

        if (cancelled) {
          return;
        }

        setStats(statsResponse);
        setAlerts(alertsResponse.slice(0, 5));
        setLogs(logsResponse.slice(0, 6));
        setError(null);
      } catch (loadError) {
        if (!cancelled) {
          setError(
            loadError instanceof Error
              ? loadError.message
              : "Failed to load dashboard data",
          );
        }
      }
    };

    void load();
    const intervalId = window.setInterval(() => {
      void load();
    }, 15000);

    return () => {
      cancelled = true;
      window.clearInterval(intervalId);
    };
  }, [token]);

  const severityCounts = stats?.alerts_by_severity ?? {};
  const activeCritical = severityCounts.critical ?? 0;
  const totalLogs = stats?.total_logs ?? 0;

  const cards = [
    {
      title: "Files Scanned",
      value: totalLogs.toLocaleString(),
      subtitle: `${stats?.recent_activity.logs_24h ?? 0} events in the last 24h`,
      icon: FileSearch,
      tone: "text-primary",
    },
    {
      title: "Active Alerts",
      value: (stats?.total_alerts ?? 0).toLocaleString(),
      subtitle: `${stats?.recent_activity.alerts_24h ?? 0} triggered in the last 24h`,
      icon: AlertTriangle,
      tone: activeCritical > 0 ? "text-error" : "text-secondary-container",
    },
    {
      title: "System Status",
      value: stats?.system_status ?? "loading",
      subtitle: activeCritical > 0 ? "Critical action required" : "No blocking threat pattern",
      icon: Shield,
      tone: activeCritical > 0 ? "text-error" : "text-secondary-container",
    },
    {
      title: "Critical Alerts",
      value: activeCritical.toString(),
      subtitle: "High-priority incidents to review",
      icon: Clock3,
      tone: activeCritical > 0 ? "text-error" : "text-outline",
    },
  ];

  return (
    <div className="space-y-8">
      <motion.section
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        className="panel overflow-hidden"
      >
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(108,242,255,0.18),transparent_28%),radial-gradient(circle_at_bottom_right,_rgba(141,255,182,0.12),transparent_24%)]" />
        <div className="relative flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="eyebrow">Central Command</p>
            <h1 className="mt-3 max-w-3xl font-headline text-4xl font-black tracking-tight text-on-surface sm:text-6xl">
              Real-time ransomware telemetry.
            </h1>
            <p className="mt-5 max-w-2xl text-sm leading-7 text-on-surface-variant">
              Review current detection volume, severity distribution, and recent
              host activity from the PhantomGuard pipeline.
            </p>
          </div>

          <div className="rounded-[1.6rem] border border-secondary-container/30 bg-secondary-container/10 px-5 py-4 shadow-kinetic-pulse">
            <p className="font-label text-[11px] uppercase tracking-[0.28em] text-secondary-container">
              Live Monitor
            </p>
            <p className="mt-3 text-lg font-semibold text-on-surface">
              {activeCritical > 0 ? "Escalated state detected" : "All monitored paths stable"}
            </p>
            <p className="mt-2 text-xs uppercase tracking-[0.22em] text-on-surface-variant">
              Adaptive watchdog online
            </p>
          </div>
        </div>
      </motion.section>

      {error ? (
        <div className="rounded-3xl border border-error/30 bg-error-container/20 px-5 py-4 text-sm text-error">
          {error}
        </div>
      ) : null}

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {cards.map((card, index) => (
          <motion.article
            key={card.title}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            className="metric-panel"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="eyebrow">{card.title}</p>
                <p className="mt-4 text-4xl font-black tracking-tight text-on-surface">
                  {card.value}
                </p>
              </div>
              <card.icon className={`h-6 w-6 ${card.tone}`} />
            </div>
            <p className="mt-5 text-sm text-on-surface-variant">{card.subtitle}</p>
          </motion.article>
        ))}
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.5fr_1fr]">
        <div className="panel">
          <div className="flex items-center justify-between">
            <div>
              <p className="eyebrow">Recent Events</p>
              <h2 className="mt-2 font-headline text-2xl font-bold text-on-surface">
                Activity stream
              </h2>
            </div>
            <Activity className="h-5 w-5 text-primary" />
          </div>

          <div className="mt-6 space-y-3">
            {logs.length === 0 ? (
              <p className="text-sm text-on-surface-variant">No log entries available yet.</p>
            ) : (
              logs.map((log) => (
                <div
                  key={log.id}
                  className="rounded-[1.4rem] border border-outline-variant/30 bg-surface-container-high/55 px-4 py-4"
                >
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <p className="text-sm font-semibold text-on-surface">
                      {log.process_name || log.file_path || "System activity"}
                    </p>
                    <p className="font-label text-[11px] uppercase tracking-[0.22em] text-on-surface-variant">
                      {new Date(log.timestamp).toLocaleString()}
                    </p>
                  </div>
                  <div className="mt-3 grid gap-2 text-sm text-on-surface-variant sm:grid-cols-3">
                    <span>Method: {log.detection_method ?? "unknown"}</span>
                    <span>CPU: {log.cpu_usage?.toFixed(1) ?? "0.0"}%</span>
                    <span>Entropy: {log.entropy?.toFixed(2) ?? "0.00"}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="space-y-6">
          <div className="panel">
            <p className="eyebrow">Severity Matrix</p>
            <h2 className="mt-2 font-headline text-2xl font-bold text-on-surface">
              Alert distribution
            </h2>

            <div className="mt-6 space-y-4">
              {["critical", "high", "medium", "low"].map((severity) => {
                const count = severityCounts[severity] ?? 0;
                const max = Math.max(stats?.total_alerts ?? 1, 1);
                return (
                  <div key={severity}>
                    <div className="mb-2 flex items-center justify-between text-sm">
                      <span className="capitalize text-on-surface">{severity}</span>
                      <span className="font-label text-on-surface-variant">{count}</span>
                    </div>
                    <div className="h-2 rounded-full bg-surface-container-highest/60">
                      <div
                        className="h-2 rounded-full bg-[linear-gradient(90deg,#6cf2ff,#35ff9c)] shadow-primary-glow"
                        style={{ width: `${(count / max) * 100}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="panel">
            <p className="eyebrow">Open Incidents</p>
            <h2 className="mt-2 font-headline text-2xl font-bold text-on-surface">
              Latest alerts
            </h2>

            <div className="mt-6 space-y-3">
              {alerts.length === 0 ? (
                <p className="text-sm text-on-surface-variant">No alerts recorded.</p>
              ) : (
                alerts.map((alert) => (
                  <div
                    key={alert.id}
                    className="rounded-[1.4rem] border border-outline-variant/30 bg-surface-container-high/55 px-4 py-4"
                  >
                    <div className="flex items-center justify-between gap-3">
                      <span className="rounded-full border border-primary/25 bg-primary/10 px-3 py-1 font-label text-[11px] font-bold uppercase tracking-[0.22em] text-primary">
                        {alert.severity}
                      </span>
                      <span className="font-label text-[11px] text-on-surface-variant">
                        {new Date(alert.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                    <p className="mt-3 text-sm font-semibold text-on-surface">
                      {alert.title}
                    </p>
                    <p className="mt-2 text-sm text-on-surface-variant">
                      {alert.description || "No alert description provided."}
                    </p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;

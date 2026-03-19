import { motion } from "framer-motion";
import { ArrowRight, BrainCircuit, Database, ScanSearch, ShieldAlert } from "lucide-react";

const stages = [
  {
    title: "Agent",
    description: "System monitor inspects file events, CPU load, and honeyfile triggers.",
    icon: ScanSearch,
  },
  {
    title: "Features",
    description: "Behavioral metrics are normalized into anomaly-ready signals.",
    icon: Database,
  },
  {
    title: "Detection",
    description: "Rules and sequence analysis score suspicious activity in real time.",
    icon: BrainCircuit,
  },
  {
    title: "Alert",
    description: "Backend persists the incident and exposes it to the dashboard.",
    icon: ShieldAlert,
  },
];

const FlowVisualizerPage = () => {
  return (
    <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
      <div>
        <p className="eyebrow">Flow Visualizer</p>
        <h1 className="mt-2 font-headline text-4xl font-black tracking-tight text-on-surface">
          End-to-end detection pipeline
        </h1>
        <p className="mt-3 max-w-2xl text-sm leading-7 text-on-surface-variant">
          This view maps how PhantomGuard moves from local host telemetry to scored
          incidents that appear inside the operator console.
        </p>
      </div>

      <div className="panel overflow-hidden">
        <div className="absolute inset-0 bg-[linear-gradient(120deg,rgba(108,242,255,0.08),transparent_35%,rgba(141,255,182,0.08))]" />
        <div className="relative grid gap-6 xl:grid-cols-[1.4fr_1fr]">
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {stages.map((stage, index) => (
              <div key={stage.title} className="metric-panel">
                <div className="flex h-12 w-12 items-center justify-center rounded-[1.1rem] border border-primary/20 bg-primary/10 shadow-primary-glow">
                  <stage.icon className="h-6 w-6 text-primary" />
                </div>
                <p className="mt-5 font-label text-[11px] uppercase tracking-[0.25em] text-primary">
                  Step {index + 1}
                </p>
                <h2 className="mt-2 font-headline text-2xl font-bold text-on-surface">
                  {stage.title}
                </h2>
                <p className="mt-3 text-sm leading-7 text-on-surface-variant">
                  {stage.description}
                </p>
              </div>
            ))}
          </div>

          <div className="rounded-[1.6rem] border border-secondary-container/20 bg-secondary-container/10 p-6 shadow-kinetic-pulse">
            <p className="font-label text-[11px] uppercase tracking-[0.28em] text-secondary-container">Pipeline Order</p>
            <div className="mt-6 space-y-4">
              {stages.map((stage, index) => (
                <div key={stage.title} className="flex items-center gap-3 text-sm text-on-surface">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full border border-secondary-container/30 bg-surface-container font-label">
                    {index + 1}
                  </div>
                  <span className="font-semibold">{stage.title}</span>
                  {index < stages.length - 1 ? (
                    <ArrowRight className="h-4 w-4 text-secondary-container" />
                  ) : null}
                </div>
              ))}
            </div>
            <p className="mt-8 text-sm leading-7 text-on-surface-variant">
              The frontend now consumes backend `stats`, `alerts`, and `logs`
              endpoints, so this diagram matches the actual application flow rather
              than a placeholder.
            </p>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default FlowVisualizerPage;

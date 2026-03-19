import { NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";
import {
  AlertTriangle,
  BarChart3,
  GitBranch,
  LayoutDashboard,
  LogOut,
  Shield,
} from "lucide-react";

import { useAuth } from "../auth/useAuth";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Alerts", href: "/alerts", icon: AlertTriangle },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
  { name: "Flow", href: "/flow", icon: GitBranch },
];

const Layout = () => {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const { logout, user } = useAuth();

  return (
    <div className="min-h-screen bg-background text-on-background">
      <div className="fixed inset-x-0 top-0 z-50 border-b border-outline-variant/30 bg-surface/75 backdrop-blur-2xl">
        <header className="mx-auto flex h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-[1.35rem] border border-primary/40 bg-primary/10 shadow-primary-glow">
              <Shield className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="font-headline text-xl font-bold tracking-tight text-primary">
                PhantomGuard 2.0
              </p>
              <p className="font-label text-[11px] uppercase tracking-[0.32em] text-on-surface-variant">
                Cyber Modern Operations Grid
              </p>
            </div>
          </div>

          <div className="hidden items-center gap-3 md:flex">
            <div className="nav-pill">
              Route {navigation.find((item) => pathname.startsWith(item.href))?.name ?? "Overview"}
            </div>
            <div className="status-chip border-secondary-container/40 bg-secondary-container/10 text-secondary-container shadow-kinetic-pulse">
              Systems nominal
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden text-right sm:block">
              <p className="text-sm font-semibold text-on-surface">
                {user?.fullName || user?.email || "Operator"}
              </p>
              <p className="font-label text-[11px] uppercase tracking-[0.24em] text-on-surface-variant">
                Authenticated session
              </p>
            </div>
            <button
              type="button"
              onClick={() => {
                logout();
                navigate("/login", { replace: true });
              }}
              className="inline-flex items-center gap-2 rounded-full border border-outline-variant/50 bg-surface/70 px-4 py-2 font-label text-[11px] uppercase tracking-[0.24em] text-on-surface-variant transition hover:border-primary/50 hover:text-primary"
            >
              <LogOut className="h-4 w-4" />
              Logout
            </button>
          </div>
        </header>
      </div>

      <div className="mx-auto flex max-w-7xl gap-8 px-4 pb-10 pt-28 sm:px-6 lg:px-8">
        <aside className="hidden w-72 shrink-0 lg:block">
          <div className="sticky top-28 overflow-hidden rounded-[2rem] border border-outline-variant/40 bg-surface-container/75 p-5 shadow-hud backdrop-blur-xl">
            <div className="mb-8 rounded-[1.6rem] border border-primary/20 bg-[linear-gradient(135deg,rgba(108,242,255,0.18),transparent_42%),linear-gradient(180deg,rgba(255,255,255,0.04),transparent_35%)] p-5">
              <p className="font-label text-[11px] uppercase tracking-[0.3em] text-primary">
                Active Route
              </p>
              <p className="mt-3 font-headline text-3xl font-bold text-on-surface">
                {navigation.find((item) => pathname.startsWith(item.href))?.name ??
                  "Overview"}
              </p>
              <p className="mt-2 text-sm leading-6 text-on-surface-variant">
                Threat telemetry, operator controls, and forensic context.
              </p>
            </div>

            <nav className="space-y-2.5">
              {navigation.map((item) => (
                <NavLink
                  key={item.href}
                  to={item.href}
                  className={({ isActive }) =>
                    [
                      "group flex items-center gap-3 rounded-[1.25rem] border px-4 py-3.5 text-sm font-semibold uppercase tracking-[0.22em] transition",
                      isActive
                        ? "border-primary/40 bg-primary/90 text-on-primary shadow-primary-glow"
                        : "border-transparent text-on-surface-variant hover:border-outline-variant/50 hover:bg-surface-container-high/80 hover:text-on-surface",
                    ].join(" ")
                  }
                >
                  <item.icon className="h-5 w-5 transition group-hover:scale-110" />
                  {item.name}
                </NavLink>
              ))}
            </nav>

            <div className="mt-8 rounded-[1.5rem] border border-secondary-container/25 bg-secondary-container/10 p-4">
              <p className="font-label text-[11px] uppercase tracking-[0.28em] text-secondary-container">
                Security Pulse
              </p>
              <div className="mt-4 grid grid-cols-3 gap-3 text-center">
                <div>
                  <p className="font-headline text-2xl font-bold text-on-surface">24</p>
                  <p className="font-label text-[10px] uppercase tracking-[0.22em] text-on-surface-variant">
                    Nodes
                  </p>
                </div>
                <div>
                  <p className="font-headline text-2xl font-bold text-on-surface">99%</p>
                  <p className="font-label text-[10px] uppercase tracking-[0.22em] text-on-surface-variant">
                    Shield
                  </p>
                </div>
                <div>
                  <p className="font-headline text-2xl font-bold text-on-surface">7ms</p>
                  <p className="font-label text-[10px] uppercase tracking-[0.22em] text-on-surface-variant">
                    Sync
                  </p>
                </div>
              </div>
            </div>
          </div>
        </aside>

        <main className="min-w-0 flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;

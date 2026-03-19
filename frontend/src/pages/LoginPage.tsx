import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Eye, EyeOff, Shield } from "lucide-react";
import toast from "react-hot-toast";

import { useAuth } from "../auth/useAuth";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const redirectPath =
    (location.state as { from?: string } | null)?.from ?? "/dashboard";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await login({ email, password });
      toast.success("Login successful");
      navigate(redirectPath, { replace: true });
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Login failed");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-background px-4 py-10">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(108,242,255,0.2),transparent_28%),radial-gradient(circle_at_bottom_right,_rgba(154,124,255,0.14),transparent_25%)]" />
      <div className="absolute inset-y-0 left-0 hidden w-[42%] border-r border-outline-variant/30 bg-[linear-gradient(180deg,rgba(108,242,255,0.05),transparent_40%),linear-gradient(90deg,rgba(0,0,0,0.18),transparent)] lg:block" />
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative z-10 grid w-full max-w-6xl overflow-hidden rounded-[2rem] border border-outline-variant/40 shadow-hud lg:grid-cols-[1.1fr_0.9fr]"
      >
        <div className="hidden border-r border-outline-variant/30 bg-[linear-gradient(180deg,rgba(8,16,33,0.92),rgba(7,10,22,0.98))] p-10 lg:flex lg:flex-col lg:justify-between">
          <div>
            <div className="inline-flex items-center gap-3 rounded-full border border-primary/25 bg-primary/10 px-4 py-2 font-label text-[11px] uppercase tracking-[0.28em] text-primary">
              <Shield className="h-4 w-4" />
              Cyber-Modern Control Layer
            </div>
            <h2 className="mt-10 max-w-md font-headline text-6xl font-bold leading-none tracking-tight text-on-surface">
              Enter the
              <span className="mt-3 block text-primary">defense grid.</span>
            </h2>
            <p className="mt-6 max-w-md text-base leading-8 text-on-surface-variant">
              A dark futuristic interface for live anomaly telemetry, routed alerts,
              and operator-grade incident review.
            </p>
          </div>

          <div className="grid gap-4">
            {[
              ["Signal", "Stable quantum-encrypted link"],
              ["Response", "Sub-second alert propagation"],
              ["Mode", "Adaptive ransomware surveillance"],
            ].map(([label, value]) => (
              <div
                key={label}
                className="rounded-[1.4rem] border border-outline-variant/35 bg-surface-container/65 p-4"
              >
                <p className="font-label text-[11px] uppercase tracking-[0.26em] text-primary">
                  {label}
                </p>
                <p className="mt-2 text-sm text-on-surface">{value}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="auth-frame p-8 lg:p-10">
          <div className="mb-8 text-center lg:text-left">
            <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-[1.4rem] border border-primary/30 bg-primary/10 shadow-primary-glow lg:mx-0">
              <Shield className="h-8 w-8 text-primary" />
            </div>
            <p className="font-label text-[11px] uppercase tracking-[0.34em] text-primary">
              Secure Access
            </p>
            <h1 className="mt-3 font-headline text-4xl font-black tracking-tight text-on-surface">
              PhantomGuard
            </h1>
            <p className="mt-3 text-sm leading-7 text-on-surface-variant">
              Authenticate into the live cyber-modern operations console.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <label className="block">
              <span className="mb-2 block font-label text-[11px] uppercase tracking-[0.24em] text-primary">
                Email
              </span>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="field"
                placeholder="operator@phantomguard.local"
                required
              />
            </label>

            <label className="block">
              <span className="mb-2 block font-label text-[11px] uppercase tracking-[0.24em] text-primary">
                Password
              </span>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="field pr-12"
                  placeholder="Enter your password"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((current) => !current)}
                  className="absolute inset-y-0 right-0 inline-flex items-center px-4 text-on-surface-variant transition hover:text-primary"
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </label>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full rounded-[1.2rem] bg-primary px-4 py-3 font-label text-sm font-bold uppercase tracking-[0.28em] text-on-primary shadow-primary-glow transition hover:scale-[1.01] hover:opacity-95 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isLoading ? "Authorizing..." : "Sign In"}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-on-surface-variant lg:text-left">
            No account yet?{" "}
            <Link to="/register" className="font-semibold text-primary transition hover:text-primary-container">
              Create one
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
};

export default LoginPage;

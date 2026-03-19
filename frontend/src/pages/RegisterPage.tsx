import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Eye, EyeOff, ShieldCheck } from "lucide-react";
import toast from "react-hot-toast";

import { useAuth } from "../auth/useAuth";

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
    fullName: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { register } = useAuth();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((current) => ({
      ...current,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }

    if (formData.password.length < 8) {
      toast.error("Password must be at least 8 characters long");
      return;
    }

    setIsLoading(true);

    try {
      await register({
        email: formData.email,
        password: formData.password,
        fullName: formData.fullName,
      });
      toast.success("Account created. Please sign in.");
      navigate("/login", { replace: true });
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Registration failed");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-background px-4 py-10">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(108,242,255,0.18),transparent_30%),radial-gradient(circle_at_bottom_right,_rgba(141,255,182,0.12),transparent_25%)]" />
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        className="auth-frame relative z-10 w-full max-w-2xl p-8 lg:p-10"
      >
        <div className="mb-8 text-center">
          <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-[1.4rem] border border-secondary-container/30 bg-secondary-container/10 shadow-kinetic-pulse">
            <ShieldCheck className="h-8 w-8 text-secondary-container" />
          </div>
          <p className="font-label text-[11px] uppercase tracking-[0.35em] text-secondary-container">
            Operator Enrollment
          </p>
          <h1 className="mt-3 font-headline text-4xl font-black tracking-tight text-on-surface">
            Create Access
          </h1>
          <p className="mt-3 text-sm leading-7 text-on-surface-variant">
            Provision a new operator identity into the dark futuristic command layer.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="grid gap-5 md:grid-cols-2">
          <label className="block md:col-span-2">
            <span className="mb-2 block font-label text-[11px] uppercase tracking-[0.24em] text-primary">
              Full Name
            </span>
            <input
              name="fullName"
              type="text"
              value={formData.fullName}
              onChange={handleChange}
              className="field"
              placeholder="Security Operator"
              required
            />
          </label>

          <label className="block md:col-span-2">
            <span className="mb-2 block font-label text-[11px] uppercase tracking-[0.24em] text-primary">
              Email
            </span>
            <input
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
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
                name="password"
                type={showPassword ? "text" : "password"}
                value={formData.password}
                onChange={handleChange}
                className="field pr-12"
                placeholder="Minimum 8 characters"
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

          <label className="block">
            <span className="mb-2 block font-label text-[11px] uppercase tracking-[0.24em] text-primary">
              Confirm Password
            </span>
            <div className="relative">
              <input
                name="confirmPassword"
                type={showConfirmPassword ? "text" : "password"}
                value={formData.confirmPassword}
                onChange={handleChange}
                className="field pr-12"
                placeholder="Repeat password"
                required
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword((current) => !current)}
                className="absolute inset-y-0 right-0 inline-flex items-center px-4 text-on-surface-variant transition hover:text-primary"
              >
                {showConfirmPassword ? (
                  <EyeOff className="h-4 w-4" />
                ) : (
                  <Eye className="h-4 w-4" />
                )}
              </button>
            </div>
          </label>

          <button
            type="submit"
            disabled={isLoading}
            className="md:col-span-2 w-full rounded-[1.2rem] bg-primary px-4 py-3 font-label text-sm font-bold uppercase tracking-[0.28em] text-on-primary shadow-primary-glow transition hover:scale-[1.01] hover:opacity-95 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isLoading ? "Provisioning..." : "Create Account"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-on-surface-variant">
          Already authorized?{" "}
          <Link to="/login" className="font-semibold text-primary transition hover:text-primary-container">
            Sign in
          </Link>
        </p>
      </motion.div>
    </div>
  );
};

export default RegisterPage;

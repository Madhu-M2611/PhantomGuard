import {
  createContext,
  startTransition,
  useEffect,
  useState,
  type ReactNode,
} from "react";

import {
  loginRequest,
  registerRequest,
  type LoginCredentials,
  type RegisterPayload,
} from "../lib/api";
import type { AuthUser } from "../lib/types";

interface AuthContextValue {
  isAuthenticated: boolean;
  token: string | null;
  user: AuthUser | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (payload: RegisterPayload) => Promise<void>;
  logout: () => void;
}

const TOKEN_STORAGE_KEY = "phantomguard.auth.token";
const USER_STORAGE_KEY = "phantomguard.auth.user";

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<AuthUser | null>(null);

  useEffect(() => {
    const storedToken = window.localStorage.getItem(TOKEN_STORAGE_KEY);
    const storedUser = window.localStorage.getItem(USER_STORAGE_KEY);

    startTransition(() => {
      setToken(storedToken);
      setUser(storedUser ? (JSON.parse(storedUser) as AuthUser) : null);
    });
  }, []);

  const persistSession = (nextToken: string, nextUser: AuthUser) => {
    window.localStorage.setItem(TOKEN_STORAGE_KEY, nextToken);
    window.localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(nextUser));

    startTransition(() => {
      setToken(nextToken);
      setUser(nextUser);
    });
  };

  const login = async (credentials: LoginCredentials) => {
    const response = await loginRequest(credentials);
    persistSession(response.access_token, {
      email: credentials.email,
      fullName: credentials.email.split("@")[0],
    });
  };

  const register = async (payload: RegisterPayload) => {
    const response = await registerRequest(payload);
    setUser({
      email: response.email,
      fullName: response.full_name ?? response.email,
    });
  };

  const logout = () => {
    window.localStorage.removeItem(TOKEN_STORAGE_KEY);
    window.localStorage.removeItem(USER_STORAGE_KEY);
    startTransition(() => {
      setToken(null);
      setUser(null);
    });
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: Boolean(token),
        token,
        user,
        login,
        logout,
        register,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export { AuthContext };

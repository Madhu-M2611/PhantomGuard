@echo off
REM Run script for PhantomGuard Frontend (Windows)

cd frontend
if not exist node_modules (
  echo Frontend dependencies are not installed. Run: npm.cmd install
  exit /b 1
)
npm.cmd run dev -- --host 0.0.0.0

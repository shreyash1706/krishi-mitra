@echo off
color 0A
echo =======================================================
echo 🚜 KRISHI MITRA - ENTERPRISE LAUNCH SEQUENCE INITIATED
echo =======================================================
echo.

echo [1/3] Booting Standalone Native Llama Model Server (GPU)...
start "LLM Microservice (Port 8080)" cmd /c "powershell -ExecutionPolicy Bypass -File .\run_llama.ps1"
echo Waiting for VRAM Initialization...
timeout /t 5 /nobreak >nul
echo.

echo [2/3] Booting Python FastAPI Logic Backend...
start "FastAPI Backend (Port 8000)" cmd /c ".\venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000"
echo Waiting for Router API Boot...
timeout /t 3 /nobreak >nul
echo.

echo [3/3] Booting Streamlit UI Application...
start "Krishi Mitra Dashboard (Port 8501)" cmd /c ".\venv\Scripts\streamlit.exe run app.py"
echo.

echo =======================================================
echo ✅ ALL SYSTEMS ONLINE!
echo 🌍 The Krishi-Mitra browser window should open shortly.
echo.
echo [Note: Do NOT close the black terminal windows that popped up.
echo They are actively processing RAG logic and GPU limits in the background.]
echo =======================================================
pause

Write-Host "Starting llama.cpp server with Official Qwen3-4B-Instruct model..." -ForegroundColor Green
Write-Host "Listening on http://127.0.0.1:8080" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow

# Add CUDA runtime DLLs to path just in case
$env:PATH = ".\llama-cpp;" + $env:PATH

.\llama-cpp\llama-server.exe -m models\Qwen3-4B-Instruct-2507-Q4_K_M.gguf --port 8080 -ngl 28 -fa on -t 8 -c 8192 -b 512 -ctk q8_0 -ctv q8_0 --no-warmup

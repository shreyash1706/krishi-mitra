#!/bin/bash

# Make sure we're in the project root
cd "$(dirname "$0")"

echo "Starting llama.cpp server with Official Qwen3-4B-Instruct model on Linux..."

# Check if model exists
if [ ! -f "models/Qwen3-4B-Instruct-2507-Q4_K_M.gguf" ]; then
    echo "Model file not found! Please ensure it exists in models/Qwen3-4B-Instruct-2507-Q4_K_M.gguf"
    exit 1
fi

# Run the native linux llama-server binary
# Replace './llama-cpp/llama-server' with the path to your linux compiled llama-server if different
./llama-server -m models/Qwen3-4B-Instruct-2507-Q4_K_M.gguf --port 8080 -ngl 28 -fa on -t 8 -c 8192 -b 512 -ctk q8_0 -ctv q8_0 --no-warmup

echo "Server stopped."

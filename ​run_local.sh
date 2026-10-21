#!/bin/bash

echo "=========================================================="
echo "    STARTING OFFLINE LOCAL AI VOICE AGENT ON ANDROID      "
echo "=========================================================="

# 1. Acquire Android Wake-Lock to keep CPU and microphone awake 24/7
if command -v termux-wake-lock &> /dev/null; then
    termux-wake-lock
    echo "[Hardware] Android wake-lock acquired successfully."
else
    echo "[Hardware Warning] termux-wake-lock not found. Ensure you are running inside Termux."
fi

# 2. Verify storage permissions
if command -v termux-setup-storage &> /dev/null; then
    echo "[Hardware] Verifying storage and telephony permissions..."
fi

# 3. Launch the offline Python application
echo "[Hardware] Starting main.py..."
python main.py

# Raspberry Pi 4B Setup Guide

This guide will help you set up and run the crack detection project on Raspberry Pi 4B.

## Quick Start (First Time Setup)

```bash
# 1. Clone the repository
cd ~
git clone https://github.com/sahilsourav03/majorproject2.1.git
cd majorproject2.1

# 2. Run the automated setup script
bash scripts/setup_pi.sh

# 3. Run the project
source .venv/bin/activate
./scripts/run.sh
```

## Manual Setup (If automated setup fails)

### Step 1: Install System Dependencies

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3-venv python3-dev python3-pip git
sudo apt install -y libatlas-base-dev libjpeg-dev
```

### Step 2: Setup Project

```bash
cd ~/majorproject2.1  # or your project directory

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Fix indentation (IMPORTANT!)
python3 scripts/fix_indentation.py
```

### Step 3: Configure Camera

Check available cameras:
```bash
ls -l /dev/video*
```

Edit config if needed:
```bash
nano configs/default.yaml
```

Default camera index is `0` (which becomes `/dev/video0`).

### Step 4: Run

```bash
source .venv/bin/activate
./scripts/run.sh
```

## Troubleshooting Indentation Errors

If you still get `TabError`, run:

```bash
# Method 1: Use the fix script
python3 scripts/fix_indentation.py

# Method 2: Manual fix (one-liner)
python3 -c "from pathlib import Path; [p.write_bytes(p.read_bytes().replace(b'\t', b'    ')) for p in Path('src').rglob('*.py') if b'\t' in p.read_bytes()]"

# Method 3: Use sed (if available)
find src -name "*.py" -exec sed -i 's/\t/    /g' {} \;
```

## Camera Issues

### Permission Denied
```bash
sudo usermod -a -G video $USER
# Log out and back in, or reboot
```

### Camera Not Found
- Check: `ls -l /dev/video*`
- Try different index values (0, 1, 2) in `configs/default.yaml`
- For USB cameras, ensure they're properly connected

### Low Performance
- Lower resolution in `configs/default.yaml` (e.g., 640x480)
- Reduce FPS to 15-20

## Daily Usage

After initial setup, just run:

```bash
cd ~/majorproject2.1
source .venv/bin/activate
./scripts/run.sh
```

The `run.sh` script automatically fixes indentation before running!

## Stopping the Application

- Press `q` in the preview window, OR
- Press `Ctrl+C` in the terminal


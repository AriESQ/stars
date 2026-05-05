# WAAAVE_POOL for Raspberry Pi 5

Run waaave_pool video synthesizer on Raspberry Pi 5 at **1920x1080 @ 60fps**.

Original waaave_pool by **Andrei Jay (ex-zee-ex)**: https://github.com/ex-zee-ex/waaaave_pool

## What Changed from Original

The original waaave_pool was built for Pi 3/4 using OpenGL ES 2.0. Pi 5 with Ubuntu uses the Mesa V3D driver with desktop OpenGL 3.1.

**Summary of changes:**

| File | Change |
|------|--------|
| `main.cpp` | Use `ofGLFWWindowSettings` with GL 3.1 instead of `ofGLESWindowSettings` with GLES 2 |
| `ofApp.cpp` | Add `ofDisableArbTex()` at start of setup(), change `TRUE/FALSE` to `true/false`, update resolution to 1920x1080, change framerate to 60fps |
| Shaders | **No changes needed** - original GLES2 shaders work on Pi 5 Mesa driver |
| Startup script | Use semicolons (`;`) not OR (`||`) for xrandr to set BOTH HDMI outputs |

The modified source files are included in `src/` - just copy them over the originals.

---

## Pre-built Image

**Download:** [waavepool_pi5_1080p.img.xz](https://drive.google.com/file/d/12DMCpA8CoG-VFM0qjZTukl10zxnK-8f-/view?usp=sharing)

- Requires 32GB SD card (~9GB uncompressed)
- SSH username: `miapi`
- SSH password: `mia`

Flash with Raspberry Pi Imager (supports .xz directly) or dd:

```bash
xzcat waavepool_pi5_1080p.img.xz | sudo dd of=/dev/rdiskX bs=4m status=progress
```

---

## Build From Source

### Step 1: Install Ubuntu 24.04

Flash Ubuntu 24.04 Desktop or Server to SD card.

### Step 2: Install Dependencies

```bash
sudo apt update && sudo apt install -y \
  build-essential git pkg-config \
  libglfw3-dev libgl1-mesa-dev mesa-utils \
  libasound2-dev libpulse-dev libudev-dev \
  libfreetype6-dev libfontconfig1-dev libcurl4-openssl-dev \
  libgtk-3-dev libmpg123-dev libsndfile1-dev \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-bad gstreamer1.0-libav \
  libboost-filesystem-dev libopencv-dev \
  libopenal-dev libjack-jackd2-dev \
  v4l-utils xinit x11-xserver-utils
```

### Step 3: Build OpenFrameworks

```bash
cd ~
git clone --depth 1 --branch 0.12.1 https://github.com/openframeworks/openFrameworks.git
cd openFrameworks/scripts/linux
./download_libs.sh

# Patch for Pi 5 (Cortex-A76 instead of A72)
sed -i 's/cortex-a72/cortex-a76/g' \
  ~/openFrameworks/libs/openFrameworksCompiled/project/linuxaarch64/config.linuxaarch64.default.mk

cd ~/openFrameworks/scripts/linux/debian
sudo ./install_dependencies.sh

cd ~/openFrameworks/libs/openFrameworksCompiled/project
make Release -j4
```

### Step 4: Install ofxMidi Addon

```bash
cd ~/openFrameworks/addons
git clone https://github.com/danomatika/ofxMidi.git
```

### Step 5: Clone waaave_pool

```bash
cd ~/openFrameworks/apps/myApps
git clone https://github.com/ex-zee-ex/waaaave_pool.git
cd waaaave_pool/WAAAVE_POOL_4_5
```

### Step 6: Replace Source Files

Copy the modified source files from this repo's `src/` folder:

```bash
cp /path/to/this/repo/src/main.cpp src/
cp /path/to/this/repo/src/ofApp.cpp src/
cp /path/to/this/repo/src/ofApp.h src/
```

### Step 7: Configure Build

```bash
echo "ofxMidi" > addons.make

cat > config.make << 'EOF'
OF_ROOT = ~/openFrameworks
PROJECT_LDFLAGS = -ljack
EOF
```

### Step 8: Compile

```bash
make Release -j4
```

### Step 9: Test

```bash
cd bin
./WAAAVE_POOL_4_5
```

---

## Autostart Setup

### Deploy Binary

```bash
mkdir -p ~/WAAAVE_POOL
cp bin/WAAAVE_POOL_4_5 ~/WAAAVE_POOL/
cp -r bin/data ~/WAAAVE_POOL/
```

### Install Startup Script

Copy `scripts/start_waavepool.sh` to home directory:

```bash
cp /path/to/this/repo/scripts/start_waavepool.sh ~/
chmod +x ~/start_waavepool.sh
```

**CRITICAL:** The script uses semicolons (`;`) not OR (`||`) to set BOTH HDMI outputs. This fixes the stretching bug.

### Install Systemd Service

```bash
sudo cp /path/to/this/repo/scripts/waavepool.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable waavepool.service
```

### Force HDMI Output

Append to `/boot/firmware/cmdline.txt` (same line, add to end):

```
video=HDMI-A-1:1920x1080@60e video=HDMI-A-2:1920x1080@60e
```

### Configure X11

```bash
echo "allowed_users = anybody" | sudo tee /etc/X11/Xwrapper.config
sudo usermod -aG video,audio,render $USER
```

### Disable Desktop & Reboot

```bash
sudo systemctl disable gdm3
sudo reboot
```

---

## The Stretching Bug

If output looks stretched, check both HDMI outputs are 1920x1080:

```bash
DISPLAY=:0 xrandr
```

**Wrong (only sets one):**
```bash
xrandr --output HDMI-1 --mode 1920x1080 || xrandr --output HDMI-2 --mode 1920x1080
```

**Correct (sets both):**
```bash
xrandr --output HDMI-1 --mode 1920x1080; xrandr --output HDMI-2 --mode 1920x1080
```

---

## Controls

- **nanoKONTROL2:** See `wp_nanokontrol_guide.jpg` in original waaave_pool repo
- **Keyboard `3`:** Toggle aspect ratio mode
- **MIDI CC 62:** Same as keyboard `3`

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Black screen | Check `journalctl -u waavepool` for errors |
| Stretched image | Verify both HDMI outputs at 1920x1080 with `xrandr` |
| No video input | Check `v4l2-ctl --list-devices` |
| MIDI not working | Run `aconnect -l`, connect controller before boot |

---

## Credits

- **waaave_pool** by Andrei Jay: https://github.com/ex-zee-ex/waaaave_pool
  - The source files in `src/` are modified versions of Andrei Jay's original code
- **OpenFrameworks**: https://openframeworks.cc
- **ofxMidi** by Dan Wilcox: https://github.com/danomatika/ofxMidi

# Linux kernel FL2000DX dongle DRM driver

Added VGA support to this [driver](https://github.com/klogg/fl2000_drm). HDMI support has been removed.

### Installing driver automatically with DKMS

[Install DKMS](https://github.com/dell/dkms?tab=readme-ov-file) (your distribution will likely have a package for it), then check out the code and type:
```
dkms install .
```
with sudo or in a root shell. DKMS will automatically install the driver into your kernel and reinstall it on kernel updates.

To update the version used by DKMS (when this driver is updated), check out the updated code and run the above command again.

If DKMS reports that the DKMS tree already contains fl2000\_drm, run:
```
dkms install . --force
```
with sudo or in a root shell.

### Building driver manually

Check out the code and type
```
make
```
Use
```
insmod fl2000.ko
```
with sudo or in root shell to start the driver. If you are running on a system with secure boot enabled, you may need to sign kernel modules. Try using provided script for this:
```
./scripts/sign.sh
```
ensure that DRM components are loaded in your system, if not - please use
```
modprobe drm
modprobe drm_kms_helper
```
**NOTE:** proper kernel headers and build tools (e.g. "build-essential" package) must be installed on the system. Driver is developed and tested on linux 5.17.


## Not Implemented (or removed)
 * HDMI detection
 * VGA compression

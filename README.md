# Rigol over USB on RaspberryPi using Python  
Rigol Python RaspberryPi - automated, remote control scripts, USB, test equipment.
This is example code for controlling benchtop instruments over USB running Python3 on a RaspberryPi (or similar SBC). 

## REFERENCE
Hackaday.com PyVisa project
https://hackaday.com/2016/11/16/how-to-control-your-instruments-from-a-computer-its-easier-than-you-think/

## SUPPORTED INSTRUMENTS
- **DP832** - Triple-channel programmable DC power supply
- **DL3021** - 200W DC electronic load
- **DM3058/DM3068** - 5½-digit benchtop digital multimeters
- **DG1022** - Dual-channel 25MHz arbitrary waveform generator
- **DS1054Z** - 4-channel 50MHz digital oscilloscope
- **DS1102E** - 2-channel 100MHz digital oscilloscope

## DEPENDENCIES
### Python Libraries
- **pyvisa** - Python VISA interface library
- **pyvisa-py** - Pure Python VISA backend
- **pyusb** - USB communication library

### System Libraries
- **libusb** - USB backend for PyUSB (required on macOS/Linux)

## INSTALLATION

### Quick Setup (Recommended)
This project includes a Python virtual environment setup for dependency isolation:

```bash
# Clone or download this repository
cd pyRigol

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install pyvisa pyvisa-py pyusb

# Install system USB backend (macOS)
brew install libusb

# Install system USB backend (Linux/Raspberry Pi)
sudo apt-get install libusb-1.0-0-dev

# Verify installation
python3 test_setup.py
```

### Manual Installation (Alternative)
If you prefer system-wide installation:

```bash
# Install Python packages
sudo pip3 install pyvisa pyvisa-py pyusb

# Install libusb (macOS)
brew install libusb

# Install libusb (Linux/Raspberry Pi)
sudo apt-get install libusb-1.0-0-dev
```

## USAGE

### Test Your Setup
Before running the main script, verify your installation:
```bash
python3 test_setup.py
```

This will confirm all dependencies are installed and list any connected USB instruments.

### Run the Main Script
1. Connect your Rigol instruments via USB
2. Update device serial numbers in `pyRigol.py` to match your instruments
3. Enable/disable specific instruments using the boolean flags at the top of the script:
   ```python
   DP832    = True      # power supply
   DL3021   = True      # dc load
   DM3058   = True      # multimeter
   # ... etc
   ```
4. Run the script:
   ```bash
   python3 pyRigol.py
   ```

### Finding Your Device Serial Numbers
Use the test script to discover connected instruments:
```bash
python3 test_setup.py
```

Or use PyVISA directly:
```python
import pyvisa as visa
rm = visa.ResourceManager('@py')
print(rm.list_resources())
```

## DOCUMENTATION
- PyVISA: https://pyvisa.readthedocs.io/en/stable/index.html
- PyVISA-py: https://pyvisa-py.readthedocs.io/
- PyUSB: https://github.com/pyusb/pyusb

## TROUBLESHOOTING

### "No module named 'visa'" error
- Use `import pyvisa as visa` instead of `import visa`
- Ensure pyvisa is installed: `pip install pyvisa`

### "No backend available" error
- Install libusb system library (see Installation section)
- macOS: `brew install libusb`
- Linux: `sudo apt-get install libusb-1.0-0-dev`

### "No device found" error
- Ensure instruments are connected via USB
- Check USB cable connection
- Verify device is powered on
- Run `python3 test_setup.py` to scan for devices
- Update serial numbers in script to match your instruments

### Permission errors (Linux/Raspberry Pi)
Add udev rules for USB access without sudo:
```bash
sudo nano /etc/udev/rules.d/99-rigol.rules
```

Add this line (adjust ATTR values for your device):
```
SUBSYSTEM=="usb", ATTR{idVendor}=="1ab1", MODE="0666"
```

Then reload udev:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## NOTES

**IMPORTANT:**
- This code contains specific equipment serial numbers. Update them to match your instruments.
- Update the firmware in your instruments to the latest version to avoid unexpected behavior.
- Some instruments have quirks (e.g., DG1022 unreliable SCPI, some don't support `*RST`)
- Timing delays between commands are critical for stability

## LICENSE
MIT License - See LICENSE file for details

## AUTHOR
Will Patton - https://github.com/willpatton


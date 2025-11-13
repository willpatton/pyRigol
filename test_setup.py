#!/usr/bin/env python3
"""
Test script to verify PyVISA installation and list available USB devices
"""

import pyvisa as visa

print("=" * 60)
print("PyVISA Installation Test")
print("=" * 60)

# Check PyVISA version
print(f"\nPyVISA version: {visa.__version__}")

# Create resource manager
try:
    rm = visa.ResourceManager('@py')
    print("✓ PyVISA-py backend loaded successfully")
except Exception as e:
    print(f"✗ Failed to load PyVISA-py backend: {e}")
    exit(1)

# List all available resources
print("\nScanning for VISA resources...")
resources = rm.list_resources()

if resources:
    print(f"\nFound {len(resources)} device(s):")
    for i, resource in enumerate(resources, 1):
        print(f"  {i}. {resource}")
else:
    print("\nNo USB devices found.")
    print("\nThis is normal if no Rigol instruments are connected.")
    print("Connect your Rigol instruments via USB and run this script again.")

print("\n" + "=" * 60)
print("Setup Status: ✓ All dependencies installed correctly")
print("=" * 60)
print("\nYour environment is ready to use with Rigol instruments!")
print("Connect your instruments and run: python3 pyRigol.py")

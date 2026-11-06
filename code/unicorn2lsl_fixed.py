#!/usr/bin/env python

# Unicorn2lsl streams data from a Unicorn Hybrid Black EEG system to LSL
#
# Copyright (C) 2022 Robert Oostenveld
# Modified 2026: fixed the EEG sign bug and gyroscope byte offsets reported
# in the gist comments (bdieudonne, Apr 2024), added a command-line port
# argument, channel labels, and a clean Ctrl+C stop.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Usage:  python unicorn2lsl_fixed.py /dev/cu.UN-XXXX.XX.XX
# Needs:  pip install pyserial pylsl numpy

import random
import string
import struct
import sys

import numpy as np

NCHAN = 16
FSAMPLE = 250
PACKET_LEN = 45

START_ACQ = bytes([0x61, 0x7C, 0x87])
STOP_ACQ = bytes([0x63, 0x5C, 0xC5])

LABELS = ["Fz", "C3", "Cz", "C4", "Pz", "PO7", "Oz", "PO8",
          "AccX", "AccY", "AccZ", "GyrX", "GyrY", "GyrZ",
          "Battery", "Counter"]
UNITS = ["microvolts"] * 8 + ["g"] * 3 + ["deg/s"] * 3 + ["percent", "count"]


def parse_packet(payload: bytes) -> np.ndarray:
    """Turn one 45-byte Unicorn packet into 16 values (see LABELS)."""
    if len(payload) != PACKET_LEN:
        raise RuntimeError(f"short packet: {len(payload)} bytes")
    if payload[0:2] != b"\xC0\x00" or payload[43:45] != b"\x0D\x0A":
        raise RuntimeError("invalid packet (bad start or end bytes)")

    dat = np.zeros(NCHAN)

    # EEG: 8 channels, 24-bit big-endian two's complement.
    for ch in range(8):
        raw = int.from_bytes(payload[3 + ch * 3: 6 + ch * 3], "big")
        if raw & 0x800000:          # sign bit set -> negative value
            raw -= 0x1000000        # (the original OR trick does not work for Python ints)
        dat[ch] = raw * 4500000.0 / 50331642.0

    # Accelerometer: bytes 27-32, 16-bit little-endian signed.
    for i in range(3):
        dat[8 + i] = struct.unpack("<h", payload[27 + 2 * i: 29 + 2 * i])[0] / 4096.0

    # Gyroscope: bytes 33-38 (the original reused the accelerometer bytes).
    for i in range(3):
        dat[11 + i] = struct.unpack("<h", payload[33 + 2 * i: 35 + 2 * i])[0] / 32.8

    dat[14] = 100.0 * float(payload[2] & 0x0F) / 15.0      # battery %
    dat[15] = struct.unpack("<L", payload[39:43])[0]       # sample counter
    return dat


def main():
    if len(sys.argv) != 2:
        print("usage: python unicorn2lsl_fixed.py /dev/cu.UN-XXXX.XX.XX")
        print("find the port with:  ls /dev/cu.UN*")
        sys.exit(1)
    device = sys.argv[1]

    import serial
    from pylsl import StreamInfo, StreamOutlet

    try:
        s = serial.Serial(device, 115200, timeout=5)
    except Exception as e:
        raise RuntimeError(f"cannot open serial port {device}: {e}")
    print("connected to serial port " + device)

    source_id = "unicorn_" + "".join(random.choice(string.digits) for _ in range(6))
    info = StreamInfo("Unicorn", "EEG", NCHAN, FSAMPLE, "float32", source_id)
    chans = info.desc().append_child("channels")
    for label, unit in zip(LABELS, UNITS):
        c = chans.append_child("channel")
        c.append_child_value("label", label)
        c.append_child_value("unit", unit)
    outlet = StreamOutlet(info)
    print(f"started LSL stream: name=Unicorn, type=EEG, source_id={source_id}")

    s.write(START_ACQ)
    if s.read(3) != b"\x00\x00\x00":
        s.close()
        raise RuntimeError("headset did not acknowledge start; is it on and paired?")
    print("streaming; press Ctrl+C to stop")

    try:
        while True:
            dat = parse_packet(s.read(PACKET_LEN))
            outlet.push_sample(dat)
            if int(dat[15]) % FSAMPLE == 0:
                print(f"samples {int(dat[15])}, battery {dat[14]:.0f}%")
    except KeyboardInterrupt:
        print("\nstopping")
    finally:
        s.write(STOP_ACQ)
        s.close()


if __name__ == "__main__":
    main()

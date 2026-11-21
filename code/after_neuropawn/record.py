"""NeuroPawn Knight IMU board: connect, enable channels, record EEG.

Mirrors how the NeuroPawn EXG Visualizer talks to the board (same BrainFlow 5.21.0,
same calls): prepare_session -> start_stream -> config_board("chon_<n>_12") per channel.
Channel commands only change board RAM; they reset whenever the port is reopened.

Usage:
  python record.py [--seconds 10] [--channels 1-8] [--port P]
"""
import argparse, glob, os, sys, time
from datetime import datetime

import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, LogLevels


from np_board import parse_channels, ensure_good_boot, uv_factor

ap = argparse.ArgumentParser()
ap.add_argument("--port", default=(sorted(glob.glob("/dev/cu.usbserial*")) or [None])[0])
ap.add_argument("--seconds", type=float, default=10)
ap.add_argument("--channels", default="1-8", help="e.g. 1-8 or 1,3,5")
ap.add_argument("--gap", type=float, default=1.0, help="seconds between channel commands")
ap.add_argument("--no-rld", action="store_true", help="don't add channels to right-leg drive")
ap.add_argument("--no-save", action="store_true")
a = ap.parse_args()
if not a.port:
    sys.exit("Board not found: no /dev/cu.usbserial* port. Plug it in and retry.")


if not ensure_good_boot(a.port):
    sys.exit("Board never booted cleanly. Unplug/replug it and retry.")

BoardShim.set_log_level(LogLevels.LEVEL_WARN.value)
board_id = BoardIds.NEUROPAWN_KNIGHT_BOARD_IMU.value
params = BrainFlowInputParams(); params.serial_port = a.port
board = BoardShim(board_id, params)
exg = BoardShim.get_exg_channels(board_id)
sr = BoardShim.get_sampling_rate(board_id)

print(f"Connecting on {a.port} (BrainFlow Knight IMU, {sr} Hz) ...")
board.prepare_session()
board.start_stream()
try:
    t = time.time()
    while board.get_board_data_count() == 0 and time.time() - t < 10:
        time.sleep(0.2)
    if board.get_board_data_count() == 0:
        sys.exit("No data from board after 10 s (it may be stuck at boot).")
    print("Streaming. Enabling channels:", a.channels)

    for n in parse_channels(a.channels):
        board.config_board(f"chon_{n}_12")
        time.sleep(a.gap)
        if not a.no_rld:
            board.config_board(f"rldadd_{n}")
            time.sleep(a.gap)

    time.sleep(1.0)
    board.get_board_data()          # discard warm-up
    print(f"Recording {a.seconds:g} s ...")
    time.sleep(a.seconds)
    data = board.get_board_data()
finally:
    board.stop_stream()
    board.release_session()
    del board  # avoid BrainFlow's noisy __del__ traceback at interpreter exit

# BrainFlow < 5.24 (incl. the Visualizer's 5.21) scales Knight EEG ~79.57x too high.
for ch in exg:
    data[ch] *= uv_factor()

n = data.shape[1]
print(f"\n{n} samples in {a.seconds:g} s (expected ~{int(sr * a.seconds)})")
for i, ch in enumerate(exg, 1):
    x = data[ch]
    state = "flat" if n == 0 or np.std(x) == 0 else "signal"
    print(f"  CH{i}: mean={np.mean(x):9.2f}  std={np.std(x):9.2f} uV  [{state}]")

if not a.no_save and n:
    rec_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recordings")
    os.makedirs(rec_dir, exist_ok=True)
    out = os.path.join(rec_dir,
                       f"recording_{datetime.now():%Y%m%d_%H%M%S}.csv")
    np.savetxt(out, data.T, delimiter=",")
    print("Saved", out)

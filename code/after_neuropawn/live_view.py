"""Live 8-channel EEG viewer for the NeuroPawn Knight IMU board.

Run:
  python live_view.py            # real board
  python live_view.py --demo     # fake data, no board needed
Options: --window 5 (seconds shown)  --channels 1-8  --raw (no filtering)  --save (CSV on close)
         --mains 60 (notch frequency; use 50 outside North America)

Tip: unplug/replug the board right before running. Close the plot window to stop.
"""
import argparse, glob, os, sys, time
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, LogLevels
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations

from np_board import ensure_good_boot, parse_channels, uv_factor

ap = argparse.ArgumentParser()
ap.add_argument("--port", default=(sorted(glob.glob("/dev/cu.usbserial*")) or [None])[0])
ap.add_argument("--demo", action="store_true", help="use BrainFlow's synthetic board")
ap.add_argument("--window", type=float, default=5.0)
ap.add_argument("--channels", default="1-8")
ap.add_argument("--raw", action="store_true", help="show unfiltered signal")
ap.add_argument("--mains", type=float, default=60.0)
ap.add_argument("--save", action="store_true", help="save everything streamed to CSV on close")
ap.add_argument("--gap", type=float, default=1.0, help="seconds between channel commands (board needs ~1 s)")
a = ap.parse_args()

BoardShim.set_log_level(LogLevels.LEVEL_WARN.value)
params = BrainFlowInputParams()
if a.demo:
    board_id = BoardIds.SYNTHETIC_BOARD.value
else:
    if not a.port:
        sys.exit("Board not found: plug it in (or use --demo).")
    if not ensure_good_boot(a.port):
        sys.exit("Board never booted cleanly. Unplug/replug it and retry.")
    board_id = BoardIds.NEUROPAWN_KNIGHT_BOARD_IMU.value
    params.serial_port = a.port

fs = BoardShim.get_sampling_rate(board_id)
exg = BoardShim.get_exg_channels(board_id)[:8]
chans = parse_channels(a.channels)
n_win = int(a.window * fs)
uv_fix = 1.0 if a.demo else uv_factor()   # BrainFlow < 5.24 scales ~79.57x too high

board = BoardShim(board_id, params)
board.prepare_session()
board.start_stream(450000)
t = time.time()
while board.get_board_data_count() == 0 and time.time() - t < 10:
    time.sleep(0.2)
if board.get_board_data_count() == 0:
    board.release_session(); sys.exit("No data from board.")
if not a.demo:
    for n in chans:
        board.config_board(f"chon_{n}_12"); time.sleep(a.gap)
        board.config_board(f"rldadd_{n}"); time.sleep(a.gap)
print("Streaming. Close the window to stop.")

saved = []
window = None  # rolling buffer of the last n_win samples
fig, axes = plt.subplots(len(chans), 1, sharex=True, figsize=(11, 1.0 + 0.9 * len(chans)))
axes = np.atleast_1d(axes)
x = np.arange(n_win) / fs - a.window
lines = []
for ax, n in zip(axes, chans):
    (ln,) = ax.plot(x, np.zeros(n_win), lw=0.8)
    ax.set_ylabel(f"CH{n}", rotation=0, ha="right", va="center")
    ax.tick_params(labelsize=7)
    lines.append(ln)
axes[-1].set_xlabel("seconds")
title = fig.suptitle("")
fig.tight_layout()


def filt(sig):
    sig = sig.copy()
    if a.raw or len(sig) < fs:
        return sig
    DataFilter.detrend(sig, DetrendOperations.LINEAR.value)
    DataFilter.perform_bandpass(sig, fs, 1.0, 40.0, 4, FilterTypes.BUTTERWORTH_ZERO_PHASE.value, 0)
    DataFilter.perform_bandstop(sig, fs, a.mains - 2, a.mains + 2, 4, FilterTypes.BUTTERWORTH_ZERO_PHASE.value, 0)
    return sig


def update(_):
    global window
    new = board.get_board_data()  # drain everything since last frame
    if new.size:
        if a.save:
            saved.append(new)
        window = np.hstack([window, new])[:, -n_win:] if window is not None else new[:, -n_win:]
    data = window
    if data is None or data.shape[1] < 2:
        return lines
    for ln, ax, n in zip(lines, axes, chans):
        sig = filt(np.ascontiguousarray(data[exg[n - 1]] * uv_fix))
        y = np.zeros(n_win); y[-len(sig):] = sig
        ln.set_ydata(y)
        lo, hi = np.percentile(sig, [1, 99]) if len(sig) else (-1, 1)
        pad = max(hi - lo, 1e-3) * 0.2
        ax.set_ylim(lo - pad, hi + pad)
        ax.set_title(f"std {np.std(sig):.1f} uV", fontsize=7, loc="right", pad=1)
    mode = "raw" if a.raw else f"1-40 Hz, {a.mains:g} Hz notch"
    title.set_text(f"{'DEMO ' if a.demo else ''}NeuroPawn Knight - {fs} Hz - {mode}")
    return lines


anim = FuncAnimation(fig, update, interval=100, cache_frame_data=False)
try:
    plt.show()
finally:
    board.stop_stream()
    board.release_session()
    del board  # avoid BrainFlow's noisy __del__ traceback at interpreter exit
    if a.save and saved:
        rec_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recordings")
        os.makedirs(rec_dir, exist_ok=True)
        out = os.path.join(rec_dir, f"live_{datetime.now():%Y%m%d_%H%M%S}.csv")
        np.savetxt(out, np.hstack(saved).T, delimiter=",")
        print("Saved", out)

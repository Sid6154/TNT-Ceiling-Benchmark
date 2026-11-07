#!/usr/bin/env python
"""Record EEG/EMG from the NeuroPawn Knight Board with BrainFlow and save a CSV.

Works before the headset arrives: the default board is BrainFlow's synthetic
board (fake data), so you can build and test the whole pipeline now.

Examples
    # Practice with fake data (no hardware):
    python neuropawn_record.py --label eyes_closed --seconds 60

    # Real NeuroPawn Knight Board on a Mac (find the port with: ls /dev/cu.usb*)
    python neuropawn_record.py --board knight --serial-port /dev/cu.usbserial-XXXX \
        --label eyes_closed --seconds 60 --person p01

Output: recordings/<person>_<label>_<date-time>.csv with a time column,
one column per EEG channel (ch1..ch8, or the names you pass with --channels),
and a 'marker' column (0 = none).

Needs:  pip install brainflow numpy pandas
"""
import argparse
import os
import time
from datetime import datetime

import numpy as np
import pandas as pd
from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams

BOARDS = {
    "synthetic": BoardIds.SYNTHETIC_BOARD,
    "knight": BoardIds.NEUROPAWN_KNIGHT_BOARD,
    "knight_imu": BoardIds.NEUROPAWN_KNIGHT_BOARD_IMU,
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--board", choices=BOARDS, default="synthetic")
    ap.add_argument("--serial-port", default="", help="e.g. /dev/cu.usbserial-XXXX (needed for the Knight Board)")
    ap.add_argument("--seconds", type=float, default=60.0, help="how long to record")
    ap.add_argument("--label", default="recording", help="what this clip is, e.g. eyes_closed, blink, jaw")
    ap.add_argument("--person", default="p00", help="participant code, never a real name")
    ap.add_argument("--channels", default="", help="comma-separated electrode sites in channel order, e.g. Oz,C3,C4")
    ap.add_argument("--outdir", default="recordings")
    args = ap.parse_args()

    board_id = BOARDS[args.board].value
    if args.board != "synthetic" and not args.serial_port:
        ap.error("--serial-port is required for the Knight Board (find it with: ls /dev/cu.usb*)")

    params = BrainFlowInputParams()
    params.serial_port = args.serial_port
    board = BoardShim(board_id, params)

    fs = BoardShim.get_sampling_rate(board_id)
    eeg_rows = BoardShim.get_exg_channels(board_id)
    ts_row = BoardShim.get_timestamp_channel(board_id)
    marker_row = BoardShim.get_marker_channel(board_id)

    names = [c.strip() for c in args.channels.split(",") if c.strip()]
    if names and len(names) > len(eeg_rows):
        ap.error(f"--channels lists {len(names)} names but the board has {len(eeg_rows)} channels")
    names = names + [f"ch{i + 1}" for i in range(len(names), len(eeg_rows))]

    board.prepare_session()
    try:
        board.start_stream()
        board.insert_marker(1)  # marks the start of the clip
        print(f"Recording {args.seconds:.0f} s of '{args.label}' at {fs} Hz from {args.board}... (Ctrl+C stops early)")
        try:
            time.sleep(args.seconds)
        except KeyboardInterrupt:
            print("Stopped early.")
        data = board.get_board_data()
        board.stop_stream()
    finally:
        board.release_session()

    df = pd.DataFrame({"time": data[ts_row] - data[ts_row][0]})
    for name, row in zip(names, eeg_rows):
        df[name] = data[row]
    df["marker"] = data[marker_row]

    os.makedirs(args.outdir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(args.outdir, f"{args.person}_{args.label}_{stamp}.csv")
    df.to_csv(path, index=False)

    seconds = len(df) / fs if fs else 0
    print(f"Saved {len(df)} samples ({seconds:.1f} s) to {path}")
    if seconds < 0.9 * args.seconds:
        print("Warning: fewer samples than expected. Check the connection for dropped data.")


if __name__ == "__main__":
    main()

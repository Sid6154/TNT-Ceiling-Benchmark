# After we got the NeuroPawn

Scripts written once the NeuroPawn Knight board (IMU firmware) arrived and was working on a Mac.
They do the same job as `../neuropawn_record.py` but add a live viewer and work around the board's quirks.

| File | What it does |
|---|---|
| `live_view.py` | Live 8-channel plot (1–40 Hz bandpass and mains notch). `--demo` runs without a board. |
| `record.py` | Records N seconds to `recordings/` as a CSV and reports which channels are flat. |
| `np_board.py` | Shared helpers: boot check, channel parsing, µV scale fix. |

```bash
cd code/after_neuropawn
python live_view.py [--save] [--raw] [--channels 1-8] [--mains 60] [--demo]
python record.py --seconds 30
```
Needs `brainflow numpy matplotlib pyserial`. Any BrainFlow version works: on versions older than 5.24, the scripts divide by 79.57 so the EEG comes out in µV.

## Board notes
- Port `/dev/cu.usbserial-*`, 115200 baud, BrainFlow board `NEUROPAWN_KNIGHT_BOARD_IMU` (125 Hz).
- Unplug and replug the board right before each run. Opening the port resets it, and it sometimes hangs at "Scanning for IMU...". The scripts retry the reset automatically.
- All channels are off after boot. The scripts send `chon_<n>_12` and `rldadd_<n>`, about 1 s apart, because the board drops commands sent faster than that.
- Only one program can use the board at a time, so close the NeuroPawn Visualizer first.
- Safety: never connect the board to mains-powered equipment while electrodes are on a person. Run the laptop on battery.

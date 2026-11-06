# Setup (Mac)

    cd ~/Documents/"TNT Ceiling Benchmark"/code
    python3 -m venv .venv
    source .venv/bin/activate
    pip install moabb pyriemann scikit-learn matplotlib scipy ipykernel

Open the folder in VS Code, open the notebook, choose the .venv kernel.

## Files
- part_a_step1_motor_imagery.ipynb   exercise notebook with blanks (BCI IV 2a, Unicorn sites Fz C3 Cz C4 Pz)
- part_a_step1_SOLUTIONS.ipynb       answers; use only when stuck
- unicorn2lsl_fixed.py               free Unicorn Hybrid Black -> LSL streamer for Mac
                                     (Oostenveld's gist with the EEG sign bug and gyro offsets fixed)

## Recording with the Unicorn (free, Mac)
1. Pair the headset in System Settings > Bluetooth; find the port:  ls /dev/cu.UN*
2. pip install pyserial pylsl numpy
3. python unicorn2lsl_fixed.py /dev/cu.UN-XXXX.XX.XX
4. Record with LabRecorder (github.com/labstreaminglayer/App-LabRecorder); load .xdf with pyxdf
First-use checks: EEG near 0 and within a few hundred uV; eyes-closed alpha at Oz/PO7/PO8; counter rises by 1 each sample.

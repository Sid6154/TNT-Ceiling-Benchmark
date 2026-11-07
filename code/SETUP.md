# Setup (Mac)

    cd ~/Documents/"TNT Ceiling Benchmark"/code
    python3 -m venv .venv
    source .venv/bin/activate
    pip install moabb pyriemann scikit-learn matplotlib scipy ipykernel braindecode brainflow pandas

Open the folder in VS Code, open a notebook, choose the .venv kernel.

## Files
- part_a_step1_motor_imagery.ipynb   exercise notebook with blanks (BCI IV 2a, motor imagery sites Fz C3 Cz C4 Pz)
- part_a_step1_SOLUTIONS.ipynb       answers; use only when stuck
- practice_eyes_open_closed.ipynb    practice: eyes open vs closed with LDA, Riemannian and EEGNet
- practice_eyes_SOLUTIONS.ipynb      answers
- neuropawn_record.py                records the NeuroPawn Knight Board with BrainFlow and saves a CSV

## Recording with the NeuroPawn Knight Board (Mac)
Before the headset arrives, practice with BrainFlow's synthetic board (fake data):

    python neuropawn_record.py --label eyes_closed --seconds 60

When it arrives, plug it in with USB-C, find its port, and record:

    ls /dev/cu.usb*
    python neuropawn_record.py --board knight --serial-port /dev/cu.usbserial-XXXX \
        --label eyes_closed --seconds 60 --person p01 --channels Oz,C3,C4

Files go to recordings/ (ignored by git). Use participant codes like p01, never real names.
BrainFlow reports the Knight Board at 125 Hz by default.
First-use checks: run a short recording with the electrodes shorted together to measure the noise floor;
then check eyes-closed alpha (8-12 Hz) at Oz.

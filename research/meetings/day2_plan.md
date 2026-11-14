# TNT Day 2 Plan

Day 2 is a 3-hour hands-on session while the NeuroPawn headset is still on its way: live EEG on the Ganglion, an artifact library the teams record themselves, a DIY SSVEP test, and a dataset hunt for the ceiling benchmark.

## Agenda

With one Ganglion and 10 people, everything that needs the board is either a whole-room demo on the projector or one station in a rotation, so nobody stands around waiting.

| Time | Block | What happens |
| --- | --- | --- |
| 0:00–0:15 | Recap and warm-up | Research question in one slide; 5-question Kahoot rematch |
| 0:15–0:45 | Live EEG demo (whole room) | One volunteer wears the Ganglion, the GUI is on the projector. Eyes open vs. closed, then blink and jaw clench |
| 0:45–1:15 | Station rotation, round 1 | Split into 3 groups (3, 3, 4); each group at one station (see below) |
| 1:15–1:45 | Station rotation, round 2 | Groups move to the next station |
| 1:45–2:00 | Break | |
| 2:00–2:30 | Station rotation, round 3 | Last station for each group |
| 2:30–2:50 | DIY SSVEP test (whole room) | One short-haired volunteer, GUI on the projector |
| 2:50–3:00 | Wrap-up | Best dataset pitches, next week's goals, collect recordings |

### Stations (30 min each)

| Station | Run by | What the group does |
| --- | --- | --- |
| 1. Ganglion recording | Lead | Record the artifact library (below). Roles rotate: one wears the electrodes, one runs the GUI, one labels and times clips |
| 2. Dataset scavenger hunt | Co-lead | Search MOABB, OpenNeuro and PhysioNet on laptops and fill the dataset table |
| 3. Look at the data | Third volunteer lead | Open recordings in a plotting script or spreadsheet and compare artifacts. Round 1 uses a sample set recorded beforehand; later rounds use the previous group's clips |

Stations 2 and 3 need laptops only, so the single Ganglion is busy the whole time. If no third lead is free, merge stations 2 and 3 into one 2-group rotation with longer turns.

## Electrode setup

We only have pre-gelled sticky electrodes, which don't work well through hair, so use the bare-skin layout first. Record on channel 1 only.

| Electrode | Bare-skin layout (default) | Back-of-head layout (short-haired volunteer) |
| --- | --- | --- |
| +1 | Behind the left ear, just above and behind it (about TP9) | Oz: back of the head, center, 2–3 cm above the bump at the base of the skull |
| −1 | Middle of the forehead, just above the eyebrows (about Fpz) | Left earlobe |
| D_G | Right earlobe | Right earlobe |

Getting good contact:

- Wipe each spot with alcohol and rub firmly before attaching.
- For Oz, part the hair, add extra gel or a few drops of salt water, and hold the electrode with a headband.
- Wait 2–5 minutes, then run the impedance check and aim for green on channel 1. Turn the check off before recording.
- Avoid the bare skin at the back of the neck: that's neck muscle, so you'd record EMG.

GUI settings: show channel 1 only, 60 Hz notch and 1–50 Hz bandpass on, time series at a fixed scale (about ±50 µV) instead of Auto.

What the signal should look like:

| Condition | Time series | FFT plot |
| --- | --- | --- |
| Eyes open | Small, irregular | Low and flat, no alpha peak |
| Eyes closed | Regular waves, about 10 per second | Clear bump at 8–12 Hz |
| Blink | Slow bump; very large in the bare-skin layout because of the forehead electrode | Extra power below about 5 Hz |
| Jaw clench | Burst of fast spiky activity | Rises across 20–60 Hz |

Alpha is weaker in the bare-skin layout than at Oz, and some people have weak alpha. If it doesn't show, check contact first, then try another volunteer.

## Artifact library

At station 1, each group records a labeled set of artifacts, then compares which ones look biggest and which look most like real brain rhythms. This answers the "brain or artifacts?" half of our research question and becomes our starting catalog for the NeuroPawn.

Record one 10-second clip of each, with a short rest between:

1. Sit still, eyes open (clean baseline)
2. Eyes closed (alpha)
3. Blink every 2 seconds
4. Look left, then right
5. Jaw clench
6. Swallow
7. Turn head left and right
8. Talk (count out loud)
9. Raise eyebrows

Save each clip from the OpenBCI GUI with this naming pattern: `team2_blink_01.csv` (team number, artifact name, take number).

These are practice recordings for learning, not data for publication; publishing recordings of people needs IRB approval first.

## DIY SSVEP test

If it works, we've built a basic SSVEP BCI on a cheap 4-channel board.

1. Use the back-of-head layout (+1 at Oz) on a short-haired volunteer.
2. Show a flickering square on a laptop at 10 Hz, then 15 Hz, about 20 seconds each, with the volunteer staring at it.
3. Look for a peak at the flicker frequency in the FFT plot.

Safety: flashing lights can trigger seizures in people with photosensitive epilepsy. Ask the room beforehand, let anyone opt out of watching, and keep each flicker short.

Open question: we still need a flicker page or app that holds a steady 10 Hz and 15 Hz. Test it before the meeting; it may not show clearly with one sticky electrode.

## Dataset scavenger hunt

Each sub-team finds 2–3 public datasets for its paradigm; the best finds become our ceiling benchmark data.

Where to search: [MOABB dataset summary](https://neurotechx.github.io/moabb/dataset_summary.html), [OpenNeuro](https://openneuro.org), [PhysioNet](https://physionet.org).

One point for each box a dataset ticks:

- Our paradigm (motor imagery, P300 or SSVEP)
- Channels we can record: C3/C4 for motor imagery, Cz/Pz for P300, occipital sites (Oz, O1/O2) for SSVEP
- Multiple sessions per person (for the cross-session test)
- EOG or EMG recorded alongside the EEG (for artifact checks)
- Recorded on a low-cost or dry-electrode headset (rare, worth 2 points)

| Team | Dataset | Paradigm | Channels | Sessions per person | EOG/EMG? | Headset | Link | Points |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Example | Lee et al. 2019 (OpenBMI) | MI, P300, SSVEP | 62 | 2 | Yes (EMG) | Lab-grade gel | [paper](https://doi.org/10.1093/gigascience/giz002) | |
| | | | | | | | | |
| | | | | | | | | |

The example row's channel and session counts still need confirming in the paper.

## Sub-team tasks due next meeting

| Team | Task |
| --- | --- |
| Motor imagery | Load a motor imagery dataset in MOABB and plot mu power at C3 vs. C4 for left- vs. right-hand trials |
| P300 | Load a P300 dataset and plot the average response to target vs. non-target flashes at Pz; the bump should appear around 0.3 s |
| SSVEP | Load an SSVEP dataset and plot the frequency spectrum at an occipital channel; look for peaks at the flicker frequencies |
| Hardware | Build a recording script with BrainFlow's synthetic board, so it only needs a board switch when the NeuroPawn arrives; write a noise-floor test plan |
| Literature | Find 2–3 papers testing low-cost EEG on each paradigm and add them to a shared summary table |

## Links

Videos:

- [2-Minute Neuroscience: EEG](https://www.youtube.com/watch?v=tZcKT4l_JZk) (2:00), for the recap
- [4-command SSVEP BCI demo](https://www.youtube.com/watch?v=PsSPKnD9XsM) (1:41), to show before the DIY SSVEP test

Papers: see `research/papers.md`.

Data sources: [MOABB dataset summary](https://neurotechx.github.io/moabb/dataset_summary.html) · [OpenNeuro](https://openneuro.org) · [PhysioNet](https://physionet.org)

Files: `code/part_a_step1_motor_imagery.ipynb` as the notebook backup activity.

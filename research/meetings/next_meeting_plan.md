# TNT Next Meeting Plan

Next meeting runs on one of two tracks. Plan A is the first NeuroPawn session, if the board has arrived and been tested. Plan B is a Ganglion-and-laptops session if it hasn't. Both are 3 hours and share the first 40 minutes, so you only commit to a track after that.

If the meeting isn't 3 hours, cut the station rounds first.

## Which plan to run

Run Plan A only if the board has streamed clean data on your laptop at least a few hours before the meeting. Never debut untested hardware in front of 10 people.

| Situation | Run |
| --- | --- |
| Board arrived and tested: channels on, no flat lines, alpha visible | Plan A |
| Board arrived the day of, not tested yet | Plan B, and end with a 20-minute live unboxing (low stakes, framed as a first look) |
| Board not here | Plan B |
| Plan A started, but the board won't stream within 15 minutes | Switch to Plan B at the next block. Everything in it needs only the Ganglion and laptops |

Tell the club the night before: "Headset may or may not be here. Either way we're recording EEG." That way a no-show isn't a letdown.

## Plan A: NeuroPawn session

The goal is the first 8-channel recording on our own board, and a mini ceiling test by the end of the night.

| Time | Block | What happens |
| --- | --- | --- |
| 0:00–0:15 | Recap + paper Kahoot (both plans) | 11 questions on the two papers. Pause on question 6: the 94% study that was mostly eye movements |
| 0:15–0:40 | Design our 8-channel montage (both plans) | Sub-teams argue for where the 8 electrodes go (see below) |
| 0:40–1:00 | Meet the Knight Board (whole room) | Show the board, its 8 inputs and the right-leg drive (same job as the Ganglion's D_G). Run the noise-floor test on the projector: all inputs on one spot, so you see how quiet "no brain" looks |
| 1:00–1:30 | First 8-channel recording (whole room) | One volunteer wears the montage the room just chose. Run `neuropawn_record.py` live: eyes open, eyes closed, blink, jaw clench. Ask: which channels show alpha, and which show the blink? |
| 1:30–1:45 | Break | |
| 1:45–2:30 | Stations, 3 rounds of 15 min | Groups of 3, 3 and 4 rotate (below) |
| 2:30–2:50 | Ceiling test in miniature (whole room) | Run the practice notebook's lab-trained alpha model on tonight's eyes open/closed clips. Compare our accuracy with the PhysioNet lab result |
| 2:50–3:00 | Wrap-up | What surprised people, sub-team tasks, collect recordings |

| Station | Run by | What the group does |
| --- | --- | --- |
| 1. NeuroPawn recording | Lead | Record 60 s eyes open + 60 s eyes closed per person, saved under participant codes (`p01`, `p02`…), never names |
| 2. Ganglion artifact library | Co-lead | Same artifact clips as the Day 2 plan, so we can later compare boards |
| 3. Look at the data | Third lead | Plot station 1's clips: spectrum per channel, find the alpha bump, flag bad channels |

These are practice recordings for learning, not publishable data. Publishing recordings of people needs IRB approval first.

## Plan B: no headset

The goal is to build everything the board will need, so the first NeuroPawn session can go straight to data. This is the Day 2 plan, compressed. Its electrode layouts, artifact list and dataset-hunt table carry over unchanged.

| Time | Block | What happens |
| --- | --- | --- |
| 0:00–0:40 | Same opening as Plan A | Paper Kahoot + montage design |
| 0:40–1:00 | Live Ganglion demo (whole room) | One volunteer, GUI on the projector: eyes open vs. closed, blink, jaw clench |
| 1:00–1:45 | Stations, 3 rounds of 15 min | Ganglion artifact library / dataset scavenger hunt / look at the data (Day 2 plan) |
| 1:45–2:00 | Break | |
| 2:00–2:20 | DIY SSVEP test (whole room) | 10 Hz and 15 Hz flicker, short-haired volunteer at Oz. Ask the room about photosensitive epilepsy first |
| 2:20–2:50 | Board-ready setup (laptops) | Everyone installs BrainFlow 5.24+ and runs `neuropawn_record.py` on the synthetic board. The hardware sub-team writes the step-by-step for first plug-in night |
| 2:50–3:00 | Wrap-up | Best dataset pitches, sub-team tasks. If the board arrived untested, do the 20-minute unboxing here instead |

To keep it from feeling like a waiting week, frame it as "the night we get ready, so day one with the headset is all data." Show the montage the room designed, and end on the date the board is expected, if you know it.

## Plan B extra: "Does cheap EEG work?" paper jigsaw (60 min)

Each small group becomes the expert on one paper and teaches it to the room, then everyone plays the Kahoot on all four. It replaces the 2:00–2:50 blocks if the flicker page isn't ready, or fills any gap.

1. **Videos (10 min, whole room):** the artifact video first, then the motor imagery demo. Day 1 had no motor imagery clip.
2. **Read (20 min):** 4 groups of 2–3, one paper each. Read only the abstract and one key figure or table, and answer: What device? Compared with what? What worked? What's the catch?
3. **Teach (15 min):** each group gets 3 minutes and one slide or whiteboard sketch.
4. **Kahoot (10 min):** `TNT_cheap_eeg_kahoot.xlsx`, 13 questions on the four papers and the artifact video.
5. **Discuss (5 min):** "Which of our three paradigms do these papers say will survive the NeuroPawn?"

| Group | Paper | Device vs. lab system | The point |
| --- | --- | --- | --- |
| 1 | [Krigolson et al. 2017, Choosing MUSE](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2017.00109/full) | $249 Muse (5 channels) vs. $77k 64-channel lab system, 60 people each | N200, P300 and reward positivity all detected, but smaller than in the lab |
| 2 | [Frey 2016, OpenBCI vs. medical-grade amplifier](https://arxiv.org/abs/1606.02438) | ~800 euro OpenBCI vs. ~20k euro g.tec, same electrodes at the same time | P300 decoding AUC 0.918 vs. 0.961; workload almost identical. Only 1 participant |
| 3 | [Pontifex & Coffman 2023, Unicorn validation](https://hbcl.msu.edu/_files/Pontifex_2023_ValidationOfTheGtec.pdf) | 8-channel Unicorn, dry vs. saline, vs. Neuroscan lab system, 20 people | Alpha-type measures valid even dry; P300 needs saline and about 8x more trials |
| 4 | [Chevallier et al. 2024, MOABB benchmark](https://arxiv.org/abs/2404.15319) | 30 models on 36 public datasets (MI, P300, SSVEP) | Riemannian models win; deep learning needs far more trials per class. This is our ceiling toolkit |

Videos:

- [EEG Oscilloscope Test: Blinks, Jaw Clench, Closed Eyes (alpha wave)](https://www.youtube.com/watch?v=OTWIGfrShSI): a student-built EEG showing the same artifacts our library records
- [A real-time motor-imagery BCI demonstration](https://www.youtube.com/watch?v=FVSYH91aCR4): imagined left hand, right hand and foot move a circle
- Optional, for the motor imagery sub-team at home: [Introduction to Motor-Imagery based BCIs](https://www.youtube.com/watch?v=metlFBa_NdQ) (about 36 min lecture)

### Recreate the oscilloscope video on the Ganglion (15–20 min)

| Ganglion pin | Where | Why |
| --- | --- | --- |
| +1 | O2: back of the head, right of center, a bit above the bump at the base of the skull | Picks up alpha |
| −1 | Fp1: forehead above the left eyebrow | Picks up blinks |
| D_G | Right earlobe | Ground and noise cancelling, like the video's driven right leg |

Use a short-haired volunteer for O2 (part the hair, add a little salt water), or fall back to the bare-skin layout. Before each 15–20 s test, the room predicts the signal: eyes open still (baseline), blink every 2 s (big slow bumps), jaw clench (fast spiky bursts), eyes closed and relaxed (about 10 waves per second, 8–12 Hz bump in the FFT). GUI: channel 1 only, 60 Hz notch, 1–50 Hz bandpass, fixed scale about ±100 µV, FFT open.

## Design our 8-channel montage (both plans, 25 min)

The board has only 8 inputs, and three paradigms plus artifact checks all want electrodes. Picking which 8 is a real research decision, so the room makes it.

1. **5 min:** each sub-team (motor imagery, P300, SSVEP) picks the 3 sites it can't live without, from the 10-20 chart.
2. **10 min:** each team pitches its picks in 1 minute and why. The hardware and literature teams argue for one artifact-monitor channel.
3. **10 min:** the room settles on 8, then ranks them. The rank sets the order we drop channels in for the 8 → 4 → 2 → 1 channel tests.

A starting point to compare against (don't show it until the teams have pitched):

| Site | For | Why |
| --- | --- | --- |
| C3, C4 | Motor imagery | Left and right hand areas |
| Cz | Motor imagery + P300 | Midline, shared by both |
| Pz | P300 | Where the P300 is largest |
| O1, Oz, O2 | SSVEP + alpha | Visual cortex |
| Fp1 | Artifact monitor | Picks up blinks and eye movements, so we can test whether a decoder is really using eye signals |

With the pre-gelled electrodes, hair is the real limit. Note which sites need cup electrodes and paste, and flag that to the club.

## Prep checklist

Both plans:

- [ ] Import the paper Kahoot (`TNT_papers_kahoot.xlsx`) and keep the answer key open
- [ ] Print or project a 10-20 electrode chart for the montage activity
- [ ] Ask the co-lead and one more person to run stations 2 and 3
- [ ] Restock pre-gelled electrodes, alcohol wipes, salt water and a headband
- [ ] Send the "headset may or may not be here" message the night before

Plan A, as soon as the board arrives:

- [ ] Check what came in the kit: electrodes and lead wires, or the board only?
- [ ] `pip install -U brainflow` and confirm version 5.24.0 or newer (older versions scale the Knight's voltages about 80 times too high)
- [ ] Find the port (`ls /dev/cu.usb*`) and turn channels on with `chon_<ch>_12` and `rldadd_<ch>`. Our script doesn't send these yet
- [ ] Run the noise-floor test and an eyes open/closed test. Confirm alpha shows on the occipital channels
- [ ] Adapt the practice notebook's Ganglion bonus to read our CSVs (125 Hz, `ch1`…`ch8` columns)

Plan B:

- [ ] Build and test a 10 Hz / 15 Hz flicker page
- [ ] Record a sample artifact set for station 3's first group
- [ ] Check `code/SETUP.md` walks a new person through installing BrainFlow

## Links and files

- `research/meetings/day2_plan.md`: electrode layouts, artifact list, SSVEP steps, dataset hunt table (Plan B uses all of these)
- `research/papers.md`: paper summaries
- [BrainFlow](https://github.com/brainflow-dev/brainflow): the official library; install from pip
- [NeuroPawn BrainFlow README](https://github.com/NeuroPawn/brainflow): Knight Board commands (gain, channel on/off, right-leg drive)
- `code/neuropawn_record.py`, `code/practice_eyes_open_closed.ipynb`, `research/TNT_papers_kahoot.xlsx`, `research/TNT_cheap_eeg_kahoot.xlsx`

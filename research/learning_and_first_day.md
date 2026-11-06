# First Day Plan (~75 min)

## Agenda
1. While people arrive: OpenBCI founder's TED talk (13:00): https://www.youtube.com/watch?v=ZkWJem3LY5E
2. Icebreakers, 10 min
3. EMG demo, 15 min: volunteers make gestures (fist, open hand, wrist flex), everyone watches the signal, train the classifier, test it on new gestures.
4. Break it, 10 min: shuffle the labels (accuracy drops to chance), swap volunteers (accuracy drops), then: "Imagine this muscle signal leaking into an EEG headset when someone clenches their jaw."
5. Research question + videos, 20 min:
   - What EEG is: play 2-Minute Neuroscience: EEG.
   - Hook: artifacts can fake BCI results. Play the blink clip.
   - Our question: how good can cheap EEG get, and is it reading the brain or artifacts?
   - Three ways to control a BCI, one clip each: motor imagery, SSVEP, P300.
   - Why compare them: SSVEP and P300 are reliable but need a screen; motor imagery needs no screen but is harder. Which still works on cheap EEG?
6. Kahoot, 10 min
7. Pick sub-teams, 10 min: MI / P300 / SSVEP / hardware / literature.

## Icebreakers (pick one or two)
- Intro round: name, major, year, and "If a BCI could let you control one thing with your mind, what would it be?"
- Brain myth or fact (hands up): "We only use 10% of our brain" (myth); "The brain itself feels no pain" (fact); "EEG can read your thoughts word by word" (myth, leads into the project).

## Videos for step 5
| Topic | Video | Length | Link |
| --- | --- | --- | --- |
| What EEG is | 2-Minute Neuroscience: Electroencephalography (EEG) | 2:00 | https://www.youtube.com/watch?v=tZcKT4l_JZk |
| Artifacts | Eye Blinks Demo in the OpenBCI GUI | 0:10 | https://www.youtube.com/watch?v=yFHlKa0_CSA |
| Motor imagery | A real-time motor-imagery BCI demonstration | 2:40 | https://www.youtube.com/watch?v=FVSYH91aCR4 |
| SSVEP | 4-command SSVEP BCI demo | 1:41 | https://www.youtube.com/watch?v=PsSPKnD9XsM |
| P300 | P300 BCI speller using brain waves to spell words | 1:36 | https://www.youtube.com/watch?v=wKDimrzvwYA |

## Kahoot (file: TNT_first_day_kahoot.xlsx)
Import: download Kahoot's spreadsheet template, paste the rows in, upload the day before. Correct answer listed first.
1. What does EEG measure? Brain electrical activity at the scalp
2. What does the EMG band measure? Muscle electrical activity
3. Closing eyes boosts which rhythm at the back of the head? Alpha (8-12 Hz)
4. Imagining moving your RIGHT hand weakens mu at which electrode? C3 (left side)
5. SSVEP is strongest over which area? Visual cortex (back of head)
6. P300 appears how long after a target? 0.3 seconds
7. Chance for a 2-class task? 50%
8. Why test on unseen data? To check it works on new data
9. Shuffled labels, accuracy stays 85%? Something is leaking or broken
10. Decoder only works when people blink? Eye-movement artifacts
11. Train on person A, test on B? Usually does worse
12. Our project's main question? How close cheap EEG gets to a lab-grade ceiling

## Before the meeting
- Test the EMG demo end to end, and have a backup recording
- Import the Kahoot
- Preview the video clips

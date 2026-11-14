# Papers

Summaries of the papers behind the ceiling project ("What is the ceiling of cheap EEG/EMG?"). Links only: we don't keep copies of the PDFs here, so read them at the source.

| # | Paper | Why it matters to us |
| --- | --- | --- |
| 1 | Ravishankar et al. 2026, handwriting decoding | How artifacts fake BCI accuracy, and the evaluation rules to stop it |
| 2 | Sadiya et al. 2021, artifact review | Toolbox for detecting and removing artifacts |
| 3 | Pontifex & Coffman 2023, Unicorn validation | Template for validating a cheap headset against a lab system |
| 4 | Lee et al. 2019, OpenBMI dataset | Our ceiling dataset: MI, P300 and SSVEP from the same 54 people |
| 5 | Krigolson et al. 2017, Muse validation | A $249 headband still records ERPs |
| 6 | Frey 2016, OpenBCI vs. g.tec | Cheap amplifier vs. lab amplifier on the same electrodes |
| 7 | Chevallier et al. 2024, MOABB benchmark | Which models win across 36 public datasets |

## 1. Ravishankar, Ghosh, Zajzon, Fei, de Sa (2026). Handwriting decoding as a challenging motor task for EEG foundation models

arXiv preprint, UCSD (de Sa lab). https://arxiv.org/pdf/2605.15698

- **Confounds in prior work:** a study reporting 94% was reproduced at 85.6% using only one horizontal eye-movement ICA component. Artifact-prone electrodes alone (Fp1, Fp2, T8, TP10, P8) gave about 24% on a 26-letter task (chance 3.8%). Block designs let decoders learn recording time.
- **Key claim:** preprocessing can't fix a confounded design. Classifiers exploit whatever residue is left.
- **Their dataset (LOVW-8.5K):** 4 participants, 32-channel lab EEG, 8,500+ trials over a year. Letters L, O, V, W, real and imagined writing, central fixation, pseudo-random order, no view of the writing.
- **Evaluation:** per-participant models, nested 5-fold CV with time-ordered (unshuffled) folds, leave-one-session-out.
- **Results (chance 25%):** real writing 41.3% movement-locked (EEGNet, best model), 32.4% cue-locked; imagined about 28.8%, and not above chance on an unseen session. Big pretrained foundation models did worse than EEGNet. Averaging 8 trials took one participant from 45% to 78%, so signal quality is the bottleneck.
- **For us:** use artifact-only baselines and channel ablation, central cues, pseudo-random trial order and time-ordered folds. Report raw and cleaned results side by side.

## 2. Sadiya, Alhanai, Ghassemi (2021). Artifact Detection and Correction in EEG Data: A Review

IEEE/EMBS NER 2021. https://ieeexplore.ieee.org/document/9441341 (paywalled; summary from the abstract)

- Methods review: ICA, blind source separation, empirical mode decomposition, hybrid methods, and ML detectors (SVM, k-NN, CNNs).
- Metrics: F1 for detection; RMSE, MSE and normalized MSE for correction quality.
- **For us:** the cleaning toolbox. It reports no decoding accuracies, so it isn't a ceiling source.
- **With paper 1:** paper 2 is the toolbox, paper 1 is the warning. First design out confounds, then clean, then prove the signal is neural.

## 3. Pontifex & Coffman (2023). Validation of the g.tec Unicorn Hybrid Black wireless EEG system

Psychophysiology, e14320. https://hbcl.msu.edu/_files/Pontifex_2023_ValidationOfTheGtec.pdf

- 20 adults; 8-channel Unicorn (dry, then saline) vs. a Neuroscan SynAmpsRT lab system with gel. Oddball task (P3 at Pz) and 90 s eyes-closed rest.
- P3 waveform correlation with the lab system: .55 dry, .78 saline. Spectral correlation: .84 dry, .90 saline.
- To match the lab system's statistical power for the P3, the Unicorn needed about 8–9x more trials. Event markers lagged about 16 ms.
- **For us:** the validation template for any cheap board. Expect rhythms like alpha to hold up and ERPs to cost more trials. Contact quality and trigger timing matter.

## 4. Lee et al. (2019). EEG dataset and OpenBMI toolbox for three BCI paradigms: an investigation into BCI illiteracy

GigaScience 8(5). https://doi.org/10.1093/gigascience/giz002

- 54 participants did motor imagery, ERP (P300 speller) and SSVEP across multiple sessions. Also includes resting state, artifact recordings and arm EMG.
- Mean accuracy: MI 71.1%, ERP 96.7%, SSVEP 95.1%. "BCI illiteracy" (can't reach usable accuracy): MI 53.7%, ERP 11.1%, SSVEP 10.2%. Nobody failed all three.
- In MOABB as `Lee2019_MI`, `Lee2019_ERP`, `Lee2019_SSVEP`.
- **For us:** the ceiling dataset. Downsample it to our setup (1/2/4/8 channels, 0/1/5/10 min calibration) and watch accuracy fall. Its artifact recordings let us test "brain or artifacts?" on lab data first.
- Still to confirm in the Methods: channel count (about 62), sampling rate and trial counts.

## 5. Krigolson, Williams, Norton, Hassall, Colino (2017). Choosing MUSE: Validation of a low-cost, portable EEG system for ERP research

Frontiers in Neuroscience 11:109. https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2017.00109/full

- 60 students on a Muse headband (5 channels: Fpz reference, AF7, AF8, TP9, TP10; about $249) vs. 60 on a 64-channel lab system (about $77,100).
- Oddball task (N200, P300) and a reward-learning task (reward positivity). All three components were detected with Muse, from about 10 participants.
- Effects were smaller than in the lab (P300 about 1.4 vs. 10.5 µV), partly because Muse has no Pz electrode. No event markers; Bluetooth lag about 40 ms.
- **For us:** cheap and few channels can still record ERPs, but electrode placement limits what you see.

## 6. Frey (2016). Comparison of an open-hardware electroencephalography amplifier with medical grade device in brain-computer interface applications

PhyCS 2016. https://arxiv.org/abs/1606.02438

- OpenBCI (about 800 euros) vs. g.tec g.USBamp (about 20,000 euros), recording the same electrodes at the same time through a splitter.
- P300 speller AUC: 0.918 OpenBCI vs. 0.961 g.tec. Mental workload: about the same (0.853 vs. 0.860).
- Only one participant and one session; an 88 ms timing offset between the amplifiers.
- **For us:** shows how to isolate the amplifier from everything else. The NeuroPawn uses the same idea as OpenBCI boards.

## 7. Chevallier et al. (2024). The largest EEG-based BCI reproducibility study for open science: the MOABB benchmark

arXiv 2404.15319. https://arxiv.org/abs/2404.15319

- 30 pipelines on 36 public datasets (14 MI, 15 P300/ERP, 7 SSVEP), within-session 5-fold evaluation.
- Riemannian pipelines (covariance + tangent space) ranked best across all paradigms. CSP-style pipelines were next. Deep learning lagged without tuning and needs roughly 150+ trials per class.
- For MI, right hand vs. feet separated better than left vs. right hand.
- **For us:** start every paradigm with a Riemannian baseline, and don't expect EEGNet to win with our small amount of data.

## Still needed

- Papers that directly compare low-cost and research-grade EEG on motor imagery (sensorimotor rhythms).
- Any validation of the NeuroPawn Knight Board itself.

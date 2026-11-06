# Papers and datasets

## Ravishankar, Ghosh, Zajzon, Fei, de Sa (2026). Handwriting decoding as a challenging motor task for EEG foundation models. arXiv preprint (UCSD, de Sa lab)
https://arxiv.org/pdf/2605.15698
- Shows eye movements, visual/muscle activity and block design inflate EEG decoding (one eye-movement ICA component alone gave 85.6% on a study reporting 94%).
- Preprocessing can't fix a confounded design. Use central fixation, pseudo-random order, time-ordered folds, leave-one-session-out.
- Results (4 letters, chance 25%): real writing 41.3% movement-locked, 32.4% cue-locked; imagined ~28.8%, no cross-session transfer.

## Sadiya, Alhanai, Ghassemi (2021). Artifact Detection and Correction in EEG Data: A Review. IEEE/EMBS NER
https://ieeexplore.ieee.org/document/9441341
- Paywalled; only the abstract was read. Methods review: ICA, BSS, EMD, hybrid, ML detectors; metrics F1, RMSE, NMSE.

## Pontifex et al. (2023). Validation of the g.tec Unicorn Hybrid Black wireless EEG. Psychophysiology
https://hbcl.msu.edu/_files/Pontifex_2023_ValidationOfTheGtec.pdf
- Unicorn compared with a lab-grade system recorded at the same time; valid measures, conductive solution recommended.

## Lee et al. (2019). EEG dataset and OpenBMI toolbox for three BCI paradigms. GigaScience 8(5), doi 10.1093/gigascience/giz002
https://nur.nu.edu.kz/items/08dbaca9-76a8-43e6-9238-f05e7ba4cb6b/full
- 54 participants did motor imagery, ERP (P300) and SSVEP over multiple sessions; includes resting state, artifact recordings and arm EMG.
- Reported accuracy ~71% MI, ~97% ERP, ~95% SSVEP. In MOABB as Lee2019_MI / Lee2019_ERP / Lee2019_SSVEP.
- Candidate protocol to replicate on our own device. Sessions, channels and sample rate not yet confirmed.

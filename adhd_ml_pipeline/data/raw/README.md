# Real HYPERAKTIV data goes here (not committed)

This directory holds the three real HYPERAKTIV files. They are **not**
tracked in git (see `.gitignore` and master spec Rule 6 - never commit
real participant/clinical data) - place your own local copies here.

## Files expected (exact names matter - `configs/config.yaml` points at these)

- `patient_info.csv`
- `CPT_II_ConnersContinuousPerformanceTest.csv`
- `features.csv`

All three are semicolon-delimited (`;`), not comma - see
`src/data_loading.py` and `adhd_ml_pipeline/README.md` for the confirmed
column schema.

## Where to get HYPERAKTIV

HYPERAKTIV is a research dataset from Simula Research Laboratory,
described in:

> Hicks, S. A., Stautland, A., Fasmer, O. B., et al. (2021). "HYPERAKTIV:
> An Activity Dataset from Adult Patients with Attention-Deficit/
> Hyperactivity Disorder (ADHD)." Proceedings of the 12th ACM Multimedia
> Systems Conference (MMSys '21), pp. 314-319.

It's normally distributed through Simula's public dataset listing at
`datasets.simula.no` (search "HYPERAKTIV") - verify the current link
yourself, since dataset hosting pages move over time and access may
require agreeing to a data-use/ethics agreement given the clinical
nature of the data.

Do not substitute synthetic or placeholder data here and describe results
from it as real HYPERAKTIV findings - see the project's master
specification, Rule 4 and Rule 5.

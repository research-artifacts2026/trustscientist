# TrustScientist

Evidence and branch revalidation for autonomous research agents.
This repository has **one current code release** and one current IET Software manuscript.

## Start here

1. **[Current code](TrustScientist_Code.zip)** - the current recovery engine,
   shared ownership interface, generic and native LangGraph comparison
   backends, frozen task inputs, and an offline result checker.
2. **[Main paper](TrustScientist_Main.pdf)** - current IET Software manuscript,
   20 pages, 7 figures, 11 tables and 1 algorithm; original overview retained.
3. **[Technical appendix](TrustScientist_Appendix.pdf)** - S1, 70 pages.

Unzip the code, enter `TrustScientist/`, then run:

```text
python verify_recorded_results.py
```

The offline check uses only the Python standard library. It verifies saved
EXT1 counts and source hashes without model inference or a paid API.
Fresh model experiments need the Linux environment and local model/worker
described inside the bundle; the original worker path must be configured.

## What the result means

In the frozen LangGraph transfer, each complete backend recovers 10/54
planned updates, or 10/12 attempted updates; 42 slots never execute.
Owned directories protect 25/25 executable in-scope omission probes,
whereas explicit paths protect 0/25. Both fail outside the owned root.
The complete backends tie. These are controlled software recovery tests,
not a general scientific-accuracy or CBR-superiority claim.

V3, V4, V5, WF1-WF3 and EXT1 in the research records identify historical
study rounds, not five maintained software versions. The code entry above
is the current implementation. Full frozen execution archives and failed
rounds remain in the paper's indexed S2-S4 supporting package.

## Archived material

Earlier conference PDFs, split artifact archives and the anonymous mirror
belong to the previous snapshot. They are not the current paper or code
entry. Git history retains their provenance. Use the three links above
for the current submission.

Substantive AI assistance and the limits of automated verification are
disclosed in the paper. Source is supplied for review without a new public
reuse license; third-party notices and licenses remain applicable.

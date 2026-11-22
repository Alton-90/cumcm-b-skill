# P13A External Comparison — 2025 B

## Frozen blind reference

The comparison begins after blind-output freeze `b1f796a7567ed0e4cb9e29b04be43eaf0bdb5e946cf1a5b9ccc90866c4ecdffa`. External material is used only to audit the candidate workflow, never to rewrite the blind result.

## External observations

- B060's abstract uses a Drude refractive-index model, direct and Levenberg-Marquardt calculations, and an explicit multi-beam model; it reports consistent SiC results near 7.5 μm and silicon results near 3.4 μm. Source image: `B060_001.jpg`, SHA-256 `e2f3cf9e7fdb8f3a3f6fedfe484aa08d350e9c5656f23b6cd134010a6492ffba`.
- B157's abstract removes the low-wavenumber interference-free region, smooths, then selects an effective high-signal band before joint fitting; it uses Cauchy dispersion and an Airy model. Source image: `B157_001.jpg`, SHA-256 `dfe73590e7af33e427c27e809e6a944ab382a25bd5bc4353739c2a1d0cb3457a`.
- Expert commentary shows representative SiC calculations near 7.5 μm (`page_050.jpg`, SHA-256 `a00d6f22f720f00e486e85fea386f9f7f654c12dca5629e0c1718686e5caf58d`). It warns that a constant refractive index can produce a plausible number without satisfying the task (`page_078.jpg`, SHA-256 `cf0e0e6f00d2747fbc40e8c1fc3f95906b7b7e14d4de8c5f3aea0482827249a4`). It explicitly identifies attachment 2's roughly 600–1000 cm⁻¹ region as above 100%, non-periodic, and unsuitable for computation (`page_079.jpg`, SHA-256 `699e73803727dae6c1ddb0c7e10da7ba1e4b9658d531a276a0fd9b87fb773f27`). It also requires the calculation model to remain consistent with a claimed multi-beam mechanism (`page_087.jpg`, SHA-256 `64cf6ac007929e4038013e14907752749c8f0d1bdbcea74849cd31d23510deca`).

## Candidate comparison

The blind workflow successfully preserved uncertainty, prevented answer leakage, kept main/baseline contracts comparable, disclosed non-convergence, and refused to turn an unstable branch into a point estimate. Those behaviors match the release goals and need no revision.

One blocking, generalizable guardrail is missing: when a method relies on periodicity, stationarity, smoothness, or another local structure, the workflow does not require an evidence-backed eligible analysis domain before method screening and code execution. In the blind run, A2's >100% values were disclosed but the full spectrum still entered the fit. This contaminated the downstream experiment and helped produce a non-useful numerical route even though the later fallback was honest.

## Revision scope

Apply exactly one coherent repair across the six already changed workflow skills: require a prospective analysis-domain contract, probe structure eligibility on that domain, carry its mask/rule into code plans and run summaries, block G3 on unresolved or post-hoc domain selection, and check it in both language reviewers. Do not encode 2025-specific bands, thresholds, answers, Drude/Cauchy coefficients, or paper values.

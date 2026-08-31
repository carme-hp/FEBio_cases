# Prestrain Validation — Displacement Comparison Summary

**Model:** biceps muscle (`biceps_blender.stl` geometry, 4671 nodes)
**Method:** FEBio native `in-situ stretch` prestrain (per-element scalar map, uniform `pre_stretch = 1.05`), following the `ps01.feb` reference pattern from the FEBio forum sample set.

## Objective

Confirm that FEBio's native prestrain feature is mechanically active — i.e. that it actually produces displacement — rather than assuming it works because the solver runs without errors.

## Method

Two matched-mesh simulations were built from the same geometry, boundary conditions, and active-contraction material parameters, differing only in the presence of prestrain:

- **Simulation A** — `uncoupled prestrain elastic` wrapping `trans iso Mooney-Rivlin` + `active_contraction`, with `pre_stretch = 1.05` on every element.
- **Simulation B** — `uncoupled trans iso Mooney-Rivlin` + `active_contraction`, identical parameters, no prestrain tag.

Both used an identical active-contraction load curve (`LC2`), deliberately held flat at 0 through t = 0.1 s (`(0,0) → (0.1,0) → (1,1) → (30,1)`, `LINEAR`/`CONSTANT`), so that the first solved timestep isolates prestrain from any contraction contribution.

Each pair was run twice — once under `STATIC` analysis, once under `DYNAMIC` — to check whether the effect holds under both solver configurations, since the production pipeline uses dynamic analysis.

Nodal displacement was compared node-for-node (identical mesh/node IDs across A and B) at the first solved state (t = 0.1 s, confirmed against each `.vtk.series` file and solver log), using `compare_disp.py` (PyVista-based, general-purpose node-displacement diff tool).

## Results

| | A (prestrain) mean \|disp\| | B (no prestrain) mean \|disp\| | A max \|disp\| |
|---|---|---|---|
| **t = 0** (baseline) | 0.0 (exact) | 0.0 (exact) | — |
| **Static, t = 0.1** | 0.2285 | 1.4×10⁻¹⁴ (noise floor) | 0.4768 |
| **Dynamic, t = 0.1** | 0.0189 | 2.1×10⁻¹⁵ (noise floor) | 0.0322 |

- **B is numerically zero** in both analysis types at t = 0.1 — confirmed by an explicit FEBio solver message ("No force acting on the system") in the dynamic run, converging in 1 iteration. This is expected: no prestrain, and contraction still at 0 on the load curve.
- **A shows substantial, structured displacement** in both analysis types, with a mean displacement vector dominated by the z-component — consistent with the model's fiber direction (`0,0,1`), i.e. the deformation pattern is physically sensible, not an artifact.
- **~99.6% of nodes** show nonzero displacement in A; the small remainder corresponds to the fixed boundary (`ZeroDisplacement1`), as expected.
- **Static displacement (0.229) is ~12× larger than dynamic (0.019)** at the same nominal timestep. This is expected, not a discrepancy: static analysis solves directly for the equilibrium state satisfying the prestrain constraint within the converged step, while dynamic analysis has mass/inertia resisting that same constraint, so the full effect propagates over more than one timestep rather than appearing all at once at t = 0.1.
- Solver logs were checked for warnings: none occurred at or near t = 0.1 in either run. Two late-stage "max iterations reached" warnings appeared in `A_dynamic` (t ≈ 21.7 s, t ≈ 29.2 s), self-corrected via automatic stiffness reformation — consistent with the already-known, separately tracked `rhoi = -2` (undamped Newmark) oscillation issue, not related to this test.

## Conclusion

Prestrain is confirmed to be mechanically active at the first solved timestep, independent of active contraction, under both static and dynamic analysis. The no-prestrain control (B) is indistinguishable from floating-point zero in both cases, while the prestrain run (A) produces substantial, fiber-aligned, boundary-consistent displacement — a clean ablation result.

## Open items / notes for follow-up

- Current test uses a spatially **uniform** prestrain value (1.05 on all elements). This validates that the mechanism works, not yet that a physiologically heterogeneous prestrain field is correctly applied — worth a follow-up test if per-element variation is required for the anatomical model.
- The static/dynamic magnitude gap is explained but not yet explored further (e.g. whether dynamic displacement converges toward the static value at later timesteps once the model settles) — not required for this task, but could strengthen the writeup if time permits.
- `rhoi = -2` oscillation remains a known, deferred item; this test surfaced a live instance of it late in the dynamic run, unrelated to the timestep used for comparison here.

## Files / scripts

- Models: `biceps_A_static.feb`, `biceps_B_static.feb`, and dynamic counterparts (same materials/BCs, `analysis` type changed).
- Comparison tool: `scripts/compare_disp.py` — general-purpose, reusable for any two matched-mesh VTK exports.
- Raw per-node diffs: `A_vs_B_static_diff_t001.csv`, `A_vs_B_dynamic_diff_t001.csv`.

# Pre-Stretch Case Workflow

This directory contains the FEBio input models and reference cases for implementing and testing pre-strain methods in a monolithic muscle contraction workflow. 

---

## Main Simulation Files

* **`biceps-muscle-contraction.feb`**
    * The baseline model file used as the primary reference.
* **`biceps-muscle-contraction_ps01.feb`**
    * An initial pre-strain test case of the biceps model, built specifically using the configuration reference from `forum_samples/ps01.feb`.
* **`biceps-muscle-contraction-prestrain.feb`**
    * A multi-step version of the baseline file. It splits the simulation into two distinct sequential steps:
        1. **Step 1:** Applies the pre-strain.
        2. **Step 2:** Activates the muscle contraction.

---

## Troubleshooting & Debugging

* **`biceps-muscle-contraction-prestrain_negjacob.feb`**
    * A version of the multi-step baseline model preserved for debugging. Running this file triggers **negative Jacobian errors** immediately during the first time step.

---

## Forum Reference Samples

The `forum_samples/` directory contains four distinct reference example cases explicitly addressing pre-strain implementations, sourced directly from the FEBio forum community for benchmarking and troubleshooting:

* **`ps01.feb`** (Used as the direct basis for `biceps-muscle-contraction_ps01.feb`)
* **`ps02.feb`**
* **`ps03.feb`**
* **`ps04.feb`**

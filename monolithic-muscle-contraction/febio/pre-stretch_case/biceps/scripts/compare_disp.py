#!/usr/bin/env python3
"""
compare_disp.py

Compares nodal displacement between two FEBio VTK exports (e.g. legacy ASCII
.vtk state files) that share the same mesh (identical node IDs / node count).
Intended for prestrain-vs-no-prestrain ablation checks, but written generally
so it can be reused for any two matched-mesh runs (e.g. static vs dynamic
solver comparisons, parameter sweeps, etc.).

Assumes: VTK index i corresponds to .feb node ID i+1 (confirmed globally in
prior work), and both files were exported from meshes with identical node
ordering (same source .feb geometry).

Usage:
    python compare_disp.py fileA.vtk fileB.vtk
    python compare_disp.py fileA.vtk fileB.vtk --labels A_static B_static
    python compare_disp.py fileA.vtk fileB.vtk --top 15
    python compare_disp.py fileA.vtk fileB.vtk --csv diff_output.csv
"""

import argparse
import sys

import numpy as np
import pyvista as pv


def load_displacement(path):
    """Load a VTK file and return (mesh, displacement_array).

    Raises a clear error if the file can't be read or has no 'displacement'
    point-data array, rather than failing with an opaque KeyError.
    """
    try:
        mesh = pv.read(path)
    except Exception as e:
        raise RuntimeError(f"Failed to read '{path}': {e}")

    if "displacement" not in mesh.point_data:
        available = list(mesh.point_data.keys())
        raise RuntimeError(
            f"'{path}' has no 'displacement' point-data array. "
            f"Available point arrays: {available}"
        )

    disp = np.asarray(mesh.point_data["displacement"])
    return mesh, disp


def summarize(name, disp):
    mag = np.linalg.norm(disp, axis=1)
    print(f"\n--- {name} ---")
    print(f"  nodes:           {disp.shape[0]}")
    print(f"  mean |disp|:     {mag.mean():.6e}")
    print(f"  max  |disp|:     {mag.max():.6e}  (node index {int(mag.argmax())})")
    print(f"  min  |disp|:     {mag.min():.6e}")
    print(f"  mean disp (x,y,z): ({disp[:,0].mean():.6e}, "
          f"{disp[:,1].mean():.6e}, {disp[:,2].mean():.6e})")
    return mag


def main():
    parser = argparse.ArgumentParser(
        description="Compare nodal displacement between two matched-mesh FEBio VTK exports."
    )
    parser.add_argument("file_a", help="Path to first VTK state file (e.g. Simulation A, first timestep)")
    parser.add_argument("file_b", help="Path to second VTK state file (e.g. Simulation B, first timestep)")
    parser.add_argument(
        "--labels", nargs=2, default=None, metavar=("LABEL_A", "LABEL_B"),
        help="Optional display names for the two runs (default: file names)"
    )
    parser.add_argument(
        "--top", type=int, default=10,
        help="Number of largest-difference nodes to print (default: 10)"
    )
    parser.add_argument(
        "--tol", type=float, default=1e-6,
        help="Magnitude below which a displacement is treated as ~zero (default: 1e-6)"
    )
    parser.add_argument(
        "--csv", default=None,
        help="Optional path to write full per-node diff table as CSV"
    )
    args = parser.parse_args()

    label_a, label_b = args.labels if args.labels else (args.file_a, args.file_b)

    mesh_a, disp_a = load_displacement(args.file_a)
    mesh_b, disp_b = load_displacement(args.file_b)

    if disp_a.shape != disp_b.shape:
        print(
            f"ERROR: node count / shape mismatch — {label_a} has {disp_a.shape}, "
            f"{label_b} has {disp_b.shape}. These files do not share the same mesh; "
            f"comparison is not meaningful.",
            file=sys.stderr,
        )
        sys.exit(1)

    mag_a = summarize(label_a, disp_a)
    mag_b = summarize(label_b, disp_b)

    diff = disp_a - disp_b
    diff_mag = np.linalg.norm(diff, axis=1)

    print(f"\n--- Difference ({label_a} - {label_b}) ---")
    print(f"  mean |diff|:     {diff_mag.mean():.6e}")
    print(f"  max  |diff|:     {diff_mag.max():.6e}  (node index {int(diff_mag.argmax())})")
    print(f"  min  |diff|:     {diff_mag.min():.6e}")

    # Quick qualitative check: is B (presumably the no-prestrain baseline)
    # effectively zero, i.e. did A show a real prestrain-driven displacement?
    frac_b_nonzero = np.mean(mag_b > args.tol)
    frac_a_nonzero = np.mean(mag_a > args.tol)
    print(f"\n--- Sanity check (tol={args.tol:.1e}) ---")
    print(f"  fraction of nodes with |disp| > tol in {label_a}: {frac_a_nonzero:.4f}")
    print(f"  fraction of nodes with |disp| > tol in {label_b}: {frac_b_nonzero:.4f}")
    if frac_b_nonzero < 0.01 and frac_a_nonzero > 0.01:
        print(f"  -> {label_b} is effectively undisplaced while {label_a} is not: "
              f"consistent with a prestrain effect being present in {label_a}.")
    elif frac_b_nonzero > 0.01 and frac_a_nonzero > 0.01:
        print(f"  -> Both runs show nonzero displacement at this state; "
              f"check whether this timestep is truly isolating prestrain "
              f"(e.g. contraction load curve may already be nonzero here).")
    else:
        print(f"  -> Unexpected pattern — review load curve / step definitions.")

    # Largest-difference nodes
    order = np.argsort(diff_mag)[::-1][: args.top]
    print(f"\n--- Top {args.top} nodes by |diff| ---")
    print(f"{'node_idx':>10} {'feb_id':>8} {label_a+'_mag':>16} {label_b+'_mag':>16} {'diff_mag':>16}")
    for idx in order:
        feb_id = idx + 1  # VTK index i -> .feb node ID i+1
        print(f"{idx:>10} {feb_id:>8} {mag_a[idx]:>16.6e} {mag_b[idx]:>16.6e} {diff_mag[idx]:>16.6e}")

    if args.csv:
        import csv as csv_module
        with open(args.csv, "w", newline="") as f:
            writer = csv_module.writer(f)
            writer.writerow([
                "node_idx", "feb_id",
                f"{label_a}_dx", f"{label_a}_dy", f"{label_a}_dz", f"{label_a}_mag",
                f"{label_b}_dx", f"{label_b}_dy", f"{label_b}_dz", f"{label_b}_mag",
                "diff_dx", "diff_dy", "diff_dz", "diff_mag",
            ])
            for idx in range(disp_a.shape[0]):
                feb_id = idx + 1
                writer.writerow([
                    idx, feb_id,
                    *disp_a[idx], mag_a[idx],
                    *disp_b[idx], mag_b[idx],
                    *diff[idx], diff_mag[idx],
                ])
        print(f"\nFull per-node diff table written to: {args.csv}")


if __name__ == "__main__":
    main()
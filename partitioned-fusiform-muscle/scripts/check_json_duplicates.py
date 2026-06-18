import json
import argparse


def find_duplicate_nodes(json_file, tolerance=None):
    """
    Check for duplicate nodes in a fiber JSON file.

    Parameters
    ----------
    json_file : str
        Path to the JSON file.
    tolerance : float or None
        If provided, coordinates are rounded to this tolerance
        before comparison (useful for floating-point noise).

    Returns
    -------
    duplicates : list
        List of duplicate node information.
    """

    with open(json_file, "r") as f:
        data = json.load(f)

    seen = {}
    duplicates = []

    for fiber_name, nodes in data.items():
        for idx, node in enumerate(nodes):

            x, y, z = node["x"], node["y"], node["z"]

            # Optional tolerance handling
            if tolerance is not None:
                key = (
                    round(x / tolerance),
                    round(y / tolerance),
                    round(z / tolerance),
                )
            else:
                key = (x, y, z)

            if key in seen:
                duplicates.append({
                    "fiber": fiber_name,
                    "node_index": idx,
                    "coordinates": (x, y, z),
                    "duplicate_of": seen[key]
                })
            else:
                seen[key] = {
                    "fiber": fiber_name,
                    "node_index": idx
                }

    return duplicates


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Check a fiber JSON file for duplicate nodes."
    )

    parser.add_argument(
        "json_path",
        help="Path to the JSON file"
    )

    parser.add_argument(
        "--tolerance",
        type=float,
        default=1e-12,
        help="Tolerance for floating-point comparison (default: 1e-12)"
    )

    args = parser.parse_args()

    duplicates = find_duplicate_nodes(
        args.json_path,
        tolerance=args.tolerance
    )

    if duplicates:
        print(f"Found {len(duplicates)} duplicate nodes:\n")

        for dup in duplicates:
            print(
                f"Duplicate node in {dup['fiber']} "
                f"(index {dup['node_index']}) "
                f"at coordinates {dup['coordinates']} "
                f"duplicates node in "
                f"{dup['duplicate_of']['fiber']} "
                f"(index {dup['duplicate_of']['node_index']})"
            )
    else:
        print("No duplicate nodes found.")
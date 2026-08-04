#!/usr/bin/env python3
"""
diff_prestrain.py

Compares an original .feb file against a modified (e.g. prestrain-filled)
version, and produces a concise summary rather than a raw line-by-line diff.

- Groups all <e lid="N">OLD</e> -> <e lid="N">NEW</e> changes by their
  (OLD, NEW) value pair and reports counts, instead of printing every line.
- Separately reports any OTHER differences found outside the ElementData
  pattern, so you can confirm nothing unexpected changed elsewhere in the
  file (material block, control settings, mesh, etc).

Usage:
    python diff_prestrain.py OLD.feb NEW.feb

Example:
    python diff_prestrain.py biceps-muscle-contraction_ps01.feb \\
                              biceps-muscle-contraction_ps01_filled.feb
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


ELEMENT_DATA_PATTERN = re.compile(r'<e lid="(\d+)">([^<]*)</e>')


def parse_element_data(content: str) -> dict:
    """Returns {lid: value} for every <e lid="N">value</e> found."""
    return {m.group(1): m.group(2) for m in ELEMENT_DATA_PATTERN.finditer(content)}


def main():
    parser = argparse.ArgumentParser(
        description="Summarize differences between two .feb files, "
                     "with special handling for ElementData value changes."
    )
    parser.add_argument("old_file", type=str, help="Path to original .feb file")
    parser.add_argument("new_file", type=str, help="Path to modified .feb file")
    parser.add_argument(
        "--encoding", type=str, default="ISO-8859-1",
        help="File encoding (default: ISO-8859-1)"
    )
    args = parser.parse_args()

    old_path = Path(args.old_file)
    new_path = Path(args.new_file)

    for p in (old_path, new_path):
        if not p.exists():
            print(f"Error: file not found: {p}", file=sys.stderr)
            sys.exit(1)

    old_content = old_path.read_text(encoding=args.encoding)
    new_content = new_path.read_text(encoding=args.encoding)

    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()

    # --- Part 1: ElementData value changes, grouped ---
    old_elems = parse_element_data(old_content)
    new_elems = parse_element_data(new_content)

    all_lids = set(old_elems) | set(new_elems)
    change_pairs = Counter()
    added_lids = []
    removed_lids = []
    unchanged_count = 0

    for lid in all_lids:
        old_val = old_elems.get(lid)
        new_val = new_elems.get(lid)
        if old_val is None:
            added_lids.append(lid)
        elif new_val is None:
            removed_lids.append(lid)
        elif old_val != new_val:
            change_pairs[(old_val, new_val)] += 1
        else:
            unchanged_count += 1

    # --- Part 2: everything else (line-level diff, excluding ElementData lines) ---
    def is_element_data_line(line: str) -> bool:
        return ELEMENT_DATA_PATTERN.search(line) is not None

    old_other = [l for l in old_lines if not is_element_data_line(l)]
    new_other = [l for l in new_lines if not is_element_data_line(l)]

    other_diffs = []
    if old_other != new_other:
        import difflib
        diff = difflib.unified_diff(old_other, new_other, lineterm="")
        other_diffs = list(diff)

    # --- Report ---
    print("=" * 60)
    print("ELEMENTDATA VALUE CHANGES")
    print("=" * 60)
    if change_pairs:
        for (old_val, new_val), count in sorted(change_pairs.items(), key=lambda x: -x[1]):
            print(f"  {count} elements changed: {old_val} -> {new_val}")
    else:
        print("  No value changes detected.")

    print(f"\n  Unchanged elements: {unchanged_count}")
    if added_lids:
        print(f"  Elements added in new file (not in old): {len(added_lids)}")
    if removed_lids:
        print(f"  Elements removed in new file (were in old): {len(removed_lids)}")

    total_old = len(old_elems)
    total_new = len(new_elems)
    print(f"\n  Total elements — old file: {total_old}, new file: {total_new}")

    print()
    print("=" * 60)
    print("OTHER DIFFERENCES (outside ElementData)")
    print("=" * 60)
    if other_diffs:
        print("  WARNING: differences found outside ElementData block!")
        print("  Review carefully — these were not expected.\n")
        for line in other_diffs:
            print(" ", line)
    else:
        print("  None. Every other line in the file is identical.")

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    only_expected = (
        len(change_pairs) == 1
        and not added_lids
        and not removed_lids
        and not other_diffs
    )
    if only_expected:
        (old_val, new_val), count = next(iter(change_pairs.items()))
        print(
            f"  Clean, single-purpose change confirmed: "
            f"{count} elements changed from {old_val} to {new_val}. "
            f"No other differences in the file."
        )
    else:
        print("  Changes do not match a single clean pattern — review details above.")


if __name__ == "__main__":
    main()
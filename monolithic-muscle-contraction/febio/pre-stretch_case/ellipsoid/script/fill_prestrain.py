#!/usr/bin/env python3
"""
fill_prestrain.py

Bulk-fills <e lid="N">0</e> placeholder values inside a FEBio .feb file's
<ElementData> block with a given constant stretch value (default 1.05).

Usage:
    python fill_prestrain.py INPUT.feb [-o OUTPUT.feb] [-v VALUE] [--tag NAME]

Examples:
    # Basic use: fills all <e lid="N">0</e> with 1.05, writes *_filled.feb
    python fill_prestrain.py biceps-muscle-contraction_ps01.feb

    # Custom stretch value and output name
    python fill_prestrain.py my_model.feb -v 1.03 -o my_model_1p03.feb

    # If your ElementData placeholder isn't "0" (e.g. some other default)
    python fill_prestrain.py my_model.feb --from-value 1.0 -v 1.05
"""

import argparse
import re
import sys
from pathlib import Path


def fill_element_data(content: str, from_value: str, to_value: float) -> tuple[str, int]:
    """
    Replaces <e lid="N">from_value</e> with <e lid="N">to_value</e>
    for every element ID found. Only matches this exact tag pattern,
    so it won't touch unrelated <c2>0</c2>, <P>0</P>, etc. elsewhere
    in the file.
    """
    # Escape from_value in case it contains regex special chars (e.g. "1.0")
    escaped_from = re.escape(from_value)
    pattern = rf'(<e lid="\d+">){escaped_from}(</e>)'
    replacement = rf'\g<1>{to_value}\g<2>'
    new_content, n = re.subn(pattern, replacement, content)
    return new_content, n


def main():
    parser = argparse.ArgumentParser(
        description="Bulk-fill FEBio ElementData prestrain placeholder values."
    )
    parser.add_argument("input", type=str, help="Path to input .feb file")
    parser.add_argument(
        "-o", "--output", type=str, default=None,
        help="Path to output .feb file (default: <input>_filled.feb)"
    )
    parser.add_argument(
        "-v", "--value", type=float, default=1.05,
        help="Stretch value to fill in (default: 1.05)"
    )
    parser.add_argument(
        "--from-value", type=str, default="0",
        help='Placeholder value currently in the file to replace (default: "0")'
    )
    parser.add_argument(
        "--encoding", type=str, default="ISO-8859-1",
        help="File encoding (default: ISO-8859-1, matches FEBio Studio exports)"
    )

    args = parser.parse_args()

    infile = Path(args.input)
    if not infile.exists():
        print(f"Error: input file not found: {infile}", file=sys.stderr)
        sys.exit(1)

    outfile = Path(args.output) if args.output else infile.with_name(
        infile.stem + "_filled" + infile.suffix
    )

    content = infile.read_text(encoding=args.encoding)

    new_content, n = fill_element_data(content, args.from_value, args.value)

    if n == 0:
        print(
            f"Warning: no matches found for <e lid=\"N\">{args.from_value}</e>. "
            f"Nothing was changed. Check --from-value or inspect the file's "
            f"ElementData block manually.",
            file=sys.stderr,
        )
        sys.exit(2)

    outfile.write_text(new_content, encoding=args.encoding)

    print(f"Replaced {n} element values ({args.from_value} -> {args.value})")
    print(f"Written to: {outfile}")


if __name__ == "__main__":
    main()
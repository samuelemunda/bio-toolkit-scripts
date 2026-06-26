#!/usr/bin/env python3
"""
Extracts gene names and primer sequences (LEFT/RIGHT) from a Primer3-style
output text file and writes them to a CSV with two columns: name, sequence.

An optional prefix (e.g. "h" for human, "m" for mouse) can be added in front
of each gene name to mark the organism/source, e.g. "m-Fam120a-fw".

Usage from terminal:
    python3 parse_primers.py input.txt output.csv [prefix]

If the prefix is omitted, you will be prompted to enter one
(or press Enter to skip it and leave names unprefixed).
"""
import sys
import csv


def parse_primers(input_path, output_path, prefix=""):
    rows = []
    gene = None

    # Only add a separator if a prefix was actually provided
    prefix_str = f"{prefix}-" if prefix else ""

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()

            # Line with the gene name, e.g.: "- Fam120a"
            if stripped.startswith("-"):
                gene = stripped.lstrip("-").strip()
                continue

            if gene is None:
                continue

            if "LEFT PRIMER" in stripped:
                seq = stripped.split()[-1]
                rows.append((f"{prefix_str}{gene}-fw", seq))
            elif "RIGHT PRIMER" in stripped:
                seq = stripped.split()[-1]
                rows.append((f"{prefix_str}{gene}-rv", seq))

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "sequence"])
        writer.writerows(rows)

    print(f"CSV created: {output_path} ({len(rows)} primers)")


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        print("Usage: python3 parse_primers.py input.txt output.csv [prefix]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if len(sys.argv) == 4:
        prefix = sys.argv[3]
    else:
        prefix = input(
            "Enter a prefix to mark organism/source (e.g. h, m) "
            "or press Enter to skip: "
        ).strip()

    parse_primers(input_path, output_path, prefix)

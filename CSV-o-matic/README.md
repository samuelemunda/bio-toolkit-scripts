# CSV-o-matic (Primer CSV Extractor)

A small Python script that reads through a Primer3-style output TXT file and extracts gene names and primer sequences into a clean CSV file. I usually keep all the Primer3 data stored in a single TXT file while I design primers, but I want a less detailed CSV to send the order.

## What it does

Given a text file containing primer design results structured like:

```
- Fam120a
    ...
    OLIGO            start  len      tm     gc%  any_th  3'_th hairpin   rep seq
    LEFT PRIMER        134   20   59.82   60.00    0.00   0.00    0.00 10.00 GAAGACCCCACTCATCGACC
    RIGHT PRIMER       281   20   59.54   60.00    0.00   0.00    0.00 12.00 GTAGAAGGGCAGAGCAGGAG
    ...
```

The script extracts the gene name (from the line starting with `-`) and the primer sequences (the last column of the `LEFT PRIMER` / `RIGHT PRIMER` lines), and writes them to a CSV file with two columns:

| name       | sequence             |
| ---------- | -------------------- |
| Fam120a-fw | GAAGACCCCACTCATCGACC |
| Fam120a-rv | GTAGAAGGGCAGAGCAGGAG |

- `-fw` suffix → LEFT PRIMER (forward)
- `-rv` suffix → RIGHT PRIMER (reverse)

### Optional organism/source prefix

You can add a prefix to every gene name to mark the organism (or source) the primers belong to (e.g. `h` for human, `m` for mouse). With a prefix of `m`, `Fam120a-fw` becomes `m-Fam120a-fw`.

## Usage

```bash
python3 parse_primers.py <input.txt> <output.csv> [prefix]
```

The `prefix` argument is optional:

- If provided on the command line, it's used directly.
- If omitted, the script will prompt you to type one (press Enter to skip and leave names unprefixed).

### Examples

With prefix passed as an argument:

```bash
python3 parse_primers.py PrimersJun2026.txt primer_list.csv m
```

produces entries like `m-Fam120a-fw`, `m-Fam120a-rv`, ...

This reads `PrimersJun2026.txt` and creates `primer_list.csv` in the current directory.

## Input format

- Each gene block starts with a line beginning with `-` (e.g. `- Fam120a`).
- Each gene block contains one `LEFT PRIMER` line and one `RIGHT PRIMER` line.
- The primer sequence is the **last whitespace-separated value** on each of those lines.

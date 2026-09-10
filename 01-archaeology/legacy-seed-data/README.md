# SIFAP Legacy Lab Synthetic Seed Data

This directory contains deterministic fixed-width seed files for the Adabas/Natural SIFAP lab.

**Synthetic data statement:** this is 100% synthetic Brazilian test data. It contains no real personal data, no real CPF/NIS assignments, and no production records.

## Files and volumes

| File | Records | Bytes/record (without newline) | Source layout |
|---|---:|---:|---|
| `beneficiary.dat` | 500 | 1739 | `layout-beneficiary.txt`, file 150 BENEFICIARY |
| `payment.dat` | 2000 | 855 | `layout-payment.txt`, file 152 PAYMENT |
| `social-program.dat` | 6 | 361 | `layout-social-program.txt`, file 151 SOCIAL-PROGRAM |
| `audit.dat` | 200 | 4995 | `layout-audit.txt`, file 153 AUDIT |

## Regeneration

This directory is a copy of the shared lab's provisioning seed, committed here so
the backend migration suite is reproducible without access to the lab. The
generator that ships alongside it is the authoritative description of the format.

Run from the repository root:

```bash
docker run --rm -v "$PWD":/w -w /w python:3.12-slim \
  python3 01-archaeology/legacy-seed-data/generate_seed.py
```

The generator uses only the Python 3 standard library and a fixed RNG seed
(`19970512`), so outputs are byte-identical on every run.

> [!WARNING]
> Regenerating overwrites the `.dat` files in place. The backend migration tests
> assert against these exact records, and `git status` is the only signal that
> something changed. Check it before committing.

## Layout notes

Records are one physical record per line. Alphanumeric fields are ASCII, trailing-space padded. Numeric unpacked fields are zero-left-padded digits. Packed decimal fields are binary packed BCD with an implied decimal scale as declared in the DDM/FDT; the newline is not part of the record width.

Periodic groups and MU fields are emitted at their maximum occurrence counts so sibling ADACMP/ADALOD scripts can load deterministic full-width records.

## Teaching fixtures

- Valid CPF and NIS check digits are generated with the mod-11 algorithms used by `SUBVALCP.NSN` and `SUBVALNI.NSN`.
- Several beneficiaries have valid CPF values starting with `000` for the government-test exception path.
- Family incomes cross the 300/600/1000/1500 calculation bands.
- Region `99` beneficiaries exercise the international/diplomatic eligibility bypass.
- Dependents include zero, several, inactive/disconnected statuses, and one 10-occurrence maximum record.
- Payments include reversals, divergent reconciliation, bank returns, and intentionally imbalanced gross/discount/net rows for report labs.

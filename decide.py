"""Genotype -> repositioning branch, implementing the decision table in Section 4 of the report.

Usage:
    python decide.py BUB1B p.Arg550Gln p.Glu1033*
    python decide.py --tsv track1_predictions.tsv   # columns include gene and p_id

Variant class is inferred from HGVS protein notation: '*', 'Ter' or 'fs' = truncating,
otherwise a substitution such as p.Arg550Gln = missense. Missense only *suggests* the
Candidate A branch: BubR1 instability must be confirmed in the patient's cells (Section 5, step 1).
"""
import argparse
import csv
import re
import sys

TRUNCATING = re.compile(r"(\*|Ter|fs)", re.IGNORECASE)
MISSENSE = re.compile(r"^p\.\(?[A-Z][a-z]{2}\d+[A-Z][a-z]{2}\)?$")

TABLE = {
    "BUB1B_missense": ("A: NAD+ precursor (NR or NMN), if BubR1 is unstable but functional",
                       "B: intermittent senolytic (cells first)",
                       "Confirm BubR1 instability in patient cells first; avoid high-dose nicotinamide"),
    "BUB1B_truncating": ("B: intermittent senolytic (cells first)", "-",
                         "A has no protein to stabilise"),
    "TRIP13": ("B: intermittent senolytic (cells first)", "-",
               "Wilms tumour surveillance is the priority"),
    "CEP57": ("None strongly supported", "-", "Minimal SAC defect; focus on supportive care"),
}
ALWAYS = "C (all genotypes): minimise genotoxic exposure, avoid HSP90 inhibitors, SIOP-Europe Wilms surveillance"


def variant_class(p_id):
    p_id = (p_id or "").strip()
    if TRUNCATING.search(p_id):
        return "truncating"
    if MISSENSE.match(p_id):
        return "missense"
    return "unknown"


def decide(gene, p_ids):
    gene = gene.strip().upper()
    if gene == "BUB1B":
        classes = [variant_class(p) for p in p_ids] or ["unknown"]
        key = "BUB1B_missense" if "missense" in classes else (
            "BUB1B_truncating" if all(c == "truncating" for c in classes) else "BUB1B_missense")
        return key, classes
    if gene in TABLE:
        return gene, [variant_class(p) for p in p_ids]
    return None, [variant_class(p) for p in p_ids]


def report(gene, p_ids):
    key, classes = decide(gene, p_ids)
    print(f"Gene: {gene}  variants: {', '.join(p_ids) or '-'}  classes: {', '.join(classes) or '-'}")
    if key is None:
        print("  Gene not in the MVA decision table (BUB1B, TRIP13, CEP57): no branch proposed.")
    else:
        first, second, caveat = TABLE[key]
        print(f"  Branch: {key}\n  First: {first}\n  Second: {second}\n  Caveat: {caveat}")
    print(f"  {ALWAYS}\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("gene", nargs="?")
    ap.add_argument("p_ids", nargs="*")
    ap.add_argument("--tsv", help="Track 1-style predictions file with 'gene' and 'p_id' columns")
    a = ap.parse_args()
    if a.tsv:
        by_gene = {}
        with open(a.tsv, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                by_gene.setdefault(row["gene"], []).append(row.get("p_id", ""))
        for gene, p_ids in by_gene.items():
            report(gene, p_ids)
    elif a.gene:
        report(a.gene, a.p_ids)
    else:
        ap.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

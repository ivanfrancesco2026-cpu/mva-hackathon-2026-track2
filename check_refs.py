"""Check that every DOI cited in the report is registered (doi.org handle API returns 404 if not)
and that every PMID/URL answers (HTTP status < 400; some publishers block scripts).

Usage: python check_refs.py   (writes refs_check.tsv)
"""
import urllib.request

REFS = {
    1: "doi:10.1038/ng1449", 2: "doi:10.1038/ng.822",
    3: "https://medlineplus.gov/genetics/condition/mosaic-variegated-aneuploidy-syndrome",
    5: "https://dismech.monarchinitiative.org/pages/disorders/Mosaic_Variegated_Aneuploidy_Syndrome.html",
    6: "doi:10.1158/0008-5472.CAN-09-4319", 7: "doi:10.1038/nature10600",
    9: "doi:10.15252/embj.201386907", 10: "pmid:23242215", 11: "doi:10.1002/mds.28788",
    12: "https://www.businesswire.com/news/home/20240607042855/en", 13: "doi:10.1111/acel.12344",
    14: "https://www.onclive.com/view/fda-approves-dasatinib-for-pediatric-ph-all",
    15: "doi:10.21873/invivo.10993", 16: "pmid:35434947", 19: "doi:10.1083/jcb.201210099",
    20: "doi:10.1016/j.ebiom.2018.09.015", 21: "doi:10.1038/nature10795",
    22: "doi:10.1016/j.ejca.2021.05.014", 23: "doi:10.3389/fmolb.2025.1577044",
    24: "doi:10.1016/j.cell.2011.01.017", 25: "doi:10.1016/j.celrep.2013.03.028",
}


def to_url(ref):
    if ref.startswith("doi:"):
        return "https://doi.org/api/handles/" + ref[4:]
    if ref.startswith("pmid:"):
        return "https://pubmed.ncbi.nlm.nih.gov/" + ref[5:] + "/"
    return ref


def status(url):
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "Mozilla/5.0 ref-check"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:  # network errors
        return type(e).__name__


def main():
    rows = []
    for n, ref in REFS.items():
        s = status(to_url(ref))
        rows.append((n, ref, s))
        print(f"[{n:>2}] {s}\t{ref}")
    with open("refs_check.tsv", "w", encoding="utf-8") as f:
        f.write("ref\tidentifier\thttp_status\n")
        for r in rows:
            f.write("\t".join(map(str, r)) + "\n")


if __name__ == "__main__":
    main()



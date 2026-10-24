# MVA Hackathon 2026 - Track 2: Drug Repositioning

**Author:** Ivan Francesco Nina Andrade (HF: Tauu987), Universidad Privada Boliviana, Santa Cruz, Bolivia

Literature-based, genotype-stratified drug repositioning hypotheses for Mosaic Variegated Aneuploidy (MVA).
No patient data was used.

## Contents
- `Tauu987_track2_report.pdf` - full report (mechanism, ranked candidates, genotype decision table, validation plan, 25 references, AI disclosure)
- `pitch.mp4` - 3-minute pitch video (also on YouTube: https://youtu.be/fU61OMql66s) (synthetic English narration over slides)
- `Tauu987_methods_description.xlsx` - completed hackathon methods description template (Track 2 sheet)
- `decide.py` - command-line tool implementing the genotype decision table (Section 4): give it a gene and HGVS p. variants, or a Track 1 predictions TSV with `gene`/`p_id` columns, and it returns the candidate branch
- `check_refs.py` - re-checks that every DOI in the report is registered and every PMID/URL answers; last run saved in `refs_check.tsv` (all 16 DOIs registered; the BusinessWire press-release page timed out)
- `make_video.ps1` - script that generated the pitch video (Windows SAPI text-to-speech + ffmpeg)

## Summary
| Confirmed variant | First candidate | Second |
|---|---|---|
| BUB1B, unstable BubR1 with residual function | A: NAD+ precursors (NR/NMN) | B: senolytic (cells first) |
| BUB1B, both alleles truncating | B (cells first) | - |
| TRIP13 | B (cells first); Wilms tumour surveillance | - |
| CEP57 | None strongly supported | - |

Candidate C (all genotypes): minimise genotoxic exposure, avoid HSP90 inhibitors, SIOP-Europe Wilms tumour surveillance.

## Reproducibility
This is a literature review, not a computational pipeline: every claim in the report cites a public source.

```bash
python decide.py BUB1B p.Arg550Gln "p.Glu1033*"   # -> Candidate A branch (confirm BubR1 instability in cells)
python decide.py --tsv track1_predictions.tsv       # plug a Track 1 result straight in
python check_refs.py                                # re-verify all citations
```
The pitch video is reproduced with `powershell -File make_video.ps1` (requires ffmpeg on PATH).

## AI disclosure
Anthropic Claude (Claude Opus 5.5, personal consumer account; claude.ai and Claude Code) for literature search, synthesis and drafting;
OpenAI Codex (ChatGPT Plus) only as an independent reference checker. Only public information was provided to these tools.

Not medical advice. License: CC BY 4.0.




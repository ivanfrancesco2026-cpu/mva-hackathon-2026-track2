$ErrorActionPreference = 'Stop'
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $dir
Add-Type -AssemblyName System.Speech

$slides = @(
  @{ t = "MVA Hackathon 2026 - Track 2`nDrug Repositioning for Mosaic Variegated Aneuploidy`n`nIvan Francesco Nina Andrade`nUniversidad Privada Boliviana, Santa Cruz, Bolivia";
     n = "Hello. I am Ivan Nina, a student from Santa Cruz, Bolivia. This is my Track 2 submission for the Rare Disease, Real Kid hackathon: genotype-stratified drug repositioning hypotheses for mosaic variegated aneuploidy. I want to be clear from the start: this is a rapid, literature-based report. I did not use the child's genomic or clinical data, and every claim was checked against its source." },
  @{ t = "The problem`n`nMVA: random whole-chromosome gains and losses`nBUB1B, TRIP13: weak spindle checkpoint, high embryonal tumour risk`nCEP57: minimal checkpoint defect`n`nWe do not know the child's variant, so the report branches by genotype";
     n = "M V A is caused by defects in accurate chromosome segregation. B U B 1 B and TRIP13 patients have a severely weakened spindle assembly checkpoint and a high risk of embryonal tumours such as Wilms tumour. CEP57 patients have only a minimal checkpoint defect. Because we did not know which gene the child carries, the report is organised as a decision table: plug in the confirmed variant, for example from Track 1, and read the matching branch." },
  @{ t = "Candidate A - NAD+ precursors (NR or NMN)`n`nNAD+ -> SIRT2 -> deacetylated BubR1 -> more stable BubR1`nSome MVA missense BubR1 proteins are degraded too fast`nNR studied in children and adults with ataxia-telangiectasia`nFit: BUB1B with unstable but functional BubR1";
     n = "Candidate A is an N A D plus precursor, nicotinamide riboside or N M N. In mice, N A D plus and the deacetylase SIRT2 stabilise BubR1, and N M N raised BubR1 protein. Some M V A missense BubR1 proteins are made but degraded unusually fast, so slowing turnover targets the actual defect. Nicotinamide riboside has already been studied in children and adults with ataxia telangiectasia, another genome instability disease. Important caveat: plain nicotinamide does the opposite and lowered BubR1, so it must not be used as a substitute." },
  @{ t = "Candidate B - Intermittent senolytics`n`nClearing p16 senescent cells delayed ageing features in BubR1 mice`nDasatinib (paediatric-approved) +/- quercetin; gentler option: fisetin`nCaution: senescence is also a tumour barrier`nCandidate C - avoid genotoxic stress and HSP90 inhibitors; Wilms surveillance";
     n = "Candidate B is an intermittent senolytic. Genetic removal of senescent cells in BubR1 deficient mice delayed muscle loss, cataracts and fat loss. Dasatinib is already approved in children, and fisetin is a gentler option. But senescence is also a barrier against cancer, so this must be tested in cells first and combined with tumour surveillance. Candidate C is risk reduction: minimise genotoxic exposure, avoid HSP90 inhibitors, which increased chromosome instability, and follow the SIOP Europe Wilms tumour surveillance recommendations, likely the most life protecting measure of all." },
  @{ t = "Validation plan and scalability`n`nPatient fibroblasts: BubR1 level and half-life, checkpoint strength, aneuploidy`nGo / no-go only in the child's own cells`nDecision table reusable for any spindle-checkpoint disorder`nOpen: report, references and AI disclosure - CC BY 4.0";
     n = "The validation plan is cheap and fast. In the child's own fibroblasts, measure BubR1 levels and half life, checkpoint strength and aneuploidy before and after treatment. Only candidates that work in the child's cells move to clinical discussion. The decision table and assays are reusable for any family with a spindle checkpoint disorder. All references were independently cross checked, and the AI tools used are disclosed in the report. Thank you." }
)

$font = 'C\:/Windows/Fonts/arial.ttf'
$list = @()
for ($i = 0; $i -lt $slides.Count; $i++) {
  $s = $slides[$i]
  $wav = "s$i.wav"; $txt = "s$i.txt"; $mp4 = "s$i.mp4"
  $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
  $synth.Rate = 0
  $synth.SetOutputToWaveFile((Join-Path $dir $wav))
  $synth.Speak($s.n)
  $synth.Dispose()
  [IO.File]::WriteAllText((Join-Path $dir $txt), $s.t, (New-Object Text.UTF8Encoding $false))
  & ffmpeg -y -loglevel error -f lavfi -i "color=c=0x0f3b57:s=1280x720:r=25" -i $wav `
    -vf "drawtext=fontfile='$font':textfile=${txt}:fontcolor=white:fontsize=34:line_spacing=18:x=70:y=(h-text_h)/2" `
    -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest $mp4
  $list += "file '$mp4'"
}
[IO.File]::WriteAllLines((Join-Path $dir 'list.txt'), $list)
& ffmpeg -y -loglevel error -f concat -safe 0 -i list.txt -c copy pitch.mp4
& ffprobe -v error -show_entries format=duration -of csv=p=0 pitch.mp4

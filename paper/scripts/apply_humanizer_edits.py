"""Round-2 style pass (/humanizer): remove staged contrasts, intensifiers,
dashes, and a repeated closer. No fact, number, citation, or claim boundary
is added or removed. Runs on the output of the two round-2 scripts."""
import sys
import docx
from apply_round2_edits import apply

MANUSCRIPT = [
    ("The prototype does not evaluate production key management, distributed replay state, formal cryptographic security, or human audit usability. TRACE is therefore evaluated as a reproducible record schema and integrity prototype, not as a state-of-the-art detector, privacy guarantee, standards-compliance assessment, or human-audit study.",
     "The prototype does not evaluate production key management, distributed replay state, or formal cryptographic security. TRACE is evaluated as a reproducible record schema and integrity prototype; the study does not assess state-of-the-art detection, privacy guarantees, standards compliance, or human audit usability."),
    ("explicitly avoids treating field presence as standards compliance",
     "does not treat field presence as standards compliance"),
    ("The distinguishing contribution is not a new universal provenance language. It is the combination of",
     "The distinguishing contribution is the combination of"),
    ("Incremental rates—defined as a trigger on the appended complete email when the base email did not trigger—averaged",
     "Incremental rates (a trigger on the appended complete email when the base email did not trigger) averaged"),
    ("Template-only—held-out", "Template-only, held-out"),
    ("Template-only—hard-negative", "Template-only, hard-negative"),
    ("Complete-email—held-out inc.", "Complete-email, held-out inc."),
    ("Complete-email—hard-negative inc.", "Complete-email, hard-negative inc."),
    (" The crosswalk is deliberately non-normative.", ""),
    ("TRACE is therefore evaluated as a model-independent record schema across three conventional classifiers, rather than through a claim of classifier superiority.",
     "We therefore evaluate TRACE as a model-independent record schema across three conventional classifiers and do not claim classifier superiority."),
    ("This is a useful implementation regression test,", "This is an implementation regression test,"),
    ("The compact MLP is a secondary neural predictor, not a Transformer or state-of-the-art claim.",
     "The compact MLP is a secondary neural predictor; it is not a Transformer and is not presented as state of the art."),
]

LETTER = [
    ("and explicitly identified requests that remain unresolved", "and identified the requests that remain unresolved"),
    ("We explicitly withdraw the earlier 933/1,000", "We withdraw the earlier 933/1,000"),
    ("remain explicitly bounded and are not presented as completed studies.",
     "are reported as limitations; we do not present them as completed studies."),
    ("TRACE is not a new universal provenance language or detector. Its contribution is a bounded, executable per-decision packet for phishing triage, coupled with validation, prediction-preservation tests, content-exclusion boundaries, and fault injection.",
     "TRACE contributes a bounded, executable per-decision packet for phishing triage, coupled with validation, prediction-preservation tests, content-exclusion boundaries, and fault injection. It does not introduce a new provenance language or detector."),
    ("Rather than speculate, we removed it", "We therefore removed it"),
    ("We consistently describe the mappings as informative capability descriptors and explicitly state that",
     "We describe the mappings throughout as informative capability descriptors and state that"),
    ("The clean packets are also actually validated,", "Clean packets are also passed through the validator,"),
    ("We explicitly state that reset or unavailable replay state", "We state that reset or unavailable replay state"),
    ("We consistently use structural traceability and explicitly exclude human audit effectiveness.",
     "We use the term structural traceability throughout and exclude human audit effectiveness from the claims."),
    ("We expressly do not treat this result", "We do not treat this result"),
    ("We added a clearly labelled, unevaluated design extension", "We added a labelled, unevaluated design extension"),
]


def letter(path_in, path_out):
    d = docx.Document(path_in)
    for old, new in LETTER:
        runs = [r for p in d.paragraphs for r in p.runs if old in r.text]
        if len(runs) != 1:
            sys.exit(f"letter edit not unique ({len(runs)}): {old[:60]!r}")
        runs[0].text = runs[0].text.replace(old, new)
    d.save(path_out)


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    apply(f"{src}/01_Main_Manuscript.docx", f"{out}/01_Main_Manuscript.docx", False, MANUSCRIPT)
    apply(f"{src}/03_Highlighted_Manuscript.docx", f"{out}/03_Highlighted_Manuscript.docx", True, MANUSCRIPT)
    letter(f"{src}/04_Response_to_Reviewers.docx", f"{out}/04_Response_to_Reviewers.docx")
    print("applied", len(MANUSCRIPT), "manuscript and", len(LETTER), "letter edits")

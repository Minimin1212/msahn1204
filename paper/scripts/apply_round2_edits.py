"""Apply round-2 consistency edits to the clean and highlighted manuscripts.

Each edit replaces one exact substring that must occur once in the document.
In the highlighted manuscript the inserted text is marked in yellow so the
editor can see every change made after the first revision.
"""
import copy
import sys
import docx
from docx.enum.text import WD_COLOR_INDEX

EDITS = [
    # (old, new) - old must be unique in the body text or a table cell
    ("A separate 604-record KINAITICS set provides a limited external stress check. It compares",
     "A separate 604-record KINAITICS set provides a limited external stress check. The study compares"),
    ("Two separate same-environment output directories were generated with seed 42 and compared by SHA-256 across 11 primary files.",
     "Two separate same-environment output directories were generated with seed 42 and compared by SHA-256 across 11 primary files. The full-corpus pipeline was additionally executed five times with seeds 42-46 to check that pooled conventional-model metrics are identical across runs and to measure run-to-run variability in the sampled stress conditions."),
    ("Linear SVM was close at 0.8804 accuracy",
     "Linear SVM was close at 0.8805 accuracy"),
    ("Figure 2 visualizes the pooled comparison; detailed fold results are supplied.",
     "Figure 2 visualizes the pooled comparison, and Table VIII gives per-source confusion matrices and macro-F1."),
    ("0.8804 (0.8785-0.8824)", "0.8805 (0.8785-0.8824)"),
    ("serialization plus authentication averaged 11.77 microseconds (mean-run SD 0.67; mean throughput",
     "serialization plus authentication averaged 11.77 microseconds (mean-run SD 0.67; median 9.78; mean throughput"),
    ("These are template-specific trigger rates, not population false-positive estimates.",
     "Values in parentheses in Table V are minimum-maximum ranges across the five runs. These are template-specific trigger rates, not population false-positive estimates."),
    ("The baseline settings were retained for continuity with the prerevision protocol.",
     "Under the same weighted fold metric, the baseline settings give 0.846 (NB), 0.879 (logistic regression), and 0.876 (linear SVM), computed from Table VIII, so the largest observed gain is about 0.006. The baseline settings were retained for continuity with the prerevision protocol."),
    ("All 5,000 trials in every injected class were rejected, and all 5,000 clean trials were accepted.",
     "All 5,000 trials in every injected class were rejected, and all 5,000 clean trials were accepted (Table VII)."),
    ("so inter-rater agreement is unavailable. It is a structural answerability comparison,",
     "so inter-rater agreement is unavailable. Table X reports the resulting index for each record condition. It is a structural answerability comparison,"),
    ("Reference implementation costs were tens of microseconds per packet.",
     "On one Python reference environment, median serialization-plus-authentication and validation costs were below 10 microseconds per packet."),
    ("figures, tables, and two-run verification hashes.",
     "figures, tables, and two-run verification hashes. The TRACE 6 revision evidence archive contains the per-trial outcomes and validator reasons for all 55,000 clean and fault-injection trials, together with the five-run latency measurements."),
    ("and initial drafting of selected analysis scripts used in the Methods and reproducibility workflow.",
     "and initial drafting of selected analysis scripts used in the Methods and reproducibility workflow. Claude (Anthropic) was used during the second revision for consistency checking between the manuscript and the response to reviewers and for language editing."),
    ("The tool did not determine the study design", "Neither tool determined the study design"),
]


def iter_paragraphs(d):
    yield from d.paragraphs
    for t in d.tables:
        for row in t.rows:
            for cell in row.cells:
                yield from cell.paragraphs


def apply(path_in, path_out, highlight):
    d = docx.Document(path_in)
    for old, new in EDITS:
        # common prefix/suffix so only the changed span is marked
        i = 0
        while i < min(len(old), len(new)) and old[i] == new[i]:
            i += 1
        j = 0
        while j < min(len(old), len(new)) - i and old[-1 - j] == new[-1 - j]:
            j += 1
        hits = []
        seen = []
        for p in iter_paragraphs(d):
            if any(p._p is q for q in seen):
                continue
            seen.append(p._p)
            for r in p.runs:
                if old in r.text:
                    hits.append(r)
        if len(hits) != 1:
            sys.exit(f"edit not unique within a single run ({len(hits)} hits): {old[:60]!r}")
        r = hits[0]
        start = r.text.index(old)
        before = r.text[: start + i]
        changed = new[i: len(new) - j]
        after = r.text[start + len(old) - j:]
        r.text = before
        mid = copy.deepcopy(r._r)
        r._r.addnext(mid)
        mid_run = docx.text.run.Run(mid, r._parent)
        mid_run.text = changed
        if highlight:
            mid_run.font.highlight_color = WD_COLOR_INDEX.YELLOW
        tail = copy.deepcopy(r._r)
        mid.addnext(tail)
        docx.text.run.Run(tail, r._parent).text = after
    d.save(path_out)


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    apply(f"{src}/01_Main_Manuscript.docx", f"{out}/01_Main_Manuscript.docx", False)
    apply(f"{src}/03_Highlighted_Manuscript.docx", f"{out}/03_Highlighted_Manuscript.docx", True)
    print("applied", len(EDITS), "edits to both manuscripts")

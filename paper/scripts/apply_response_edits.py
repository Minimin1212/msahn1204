"""Round-2 edits to the response letter: fix formatting, align numbers with the
manuscript, and add a manuscript location to every author action."""
import sys
import docx

LOCATIONS = {
    ("Reviewer 1", 1): "Section II-D; Section III-B, final paragraph (Table IX interpretation).",
    ("Reviewer 1", 2): "Section III-A, second paragraph.",
    ("Reviewer 1", 3): "Section III-B, first paragraph.",
    ("Reviewer 1", 4): "Section IV-A, third paragraph; Section VII, second paragraph.",
    ("Reviewer 1", 5): "Section IV-B, first paragraph.",
    ("Reviewer 1", 6): "Abstract; Section IV-B, second paragraph; Sections VI-A and VI-C; Section IX.",
    ("Reviewer 1", 7): "Section VI-C, external-test (KINAITICS) paragraph.",
    ("Reviewer 1", 8): "Section IV-C, first paragraph; Section VI-C; Table VII.",
    ("Reviewer 1", 9): "Section VI-B, second paragraph.",
    ("Reviewer 1", 10): "Section VII, first paragraph.",
    ("Reviewer 1", 11): "Abstract; Section VI-B, first paragraph; Section VII; Section IX.",
    ("Reviewer 1", 12): "Section III-B; Section V-D; Section VI-C, paragraph following Table X.",
    ("Reviewer 1", 13): "Section V-D, final paragraph; Section VII, first paragraph.",
    ("Reviewer 1", 14): "Figures 1-4 and Tables I-X.",
    ("Reviewer 1", 15): "Throughout; principally the Abstract and Sections I, IV, VI, VII, and IX.",
    ("Reviewer 2", 1): "Section V-B, second paragraph; Table IV.",
    ("Reviewer 2", 2): "Abstract; Sections III-B and V-B; Section VI-C, paragraph following Table X; Sections VII and IX.",
    ("Reviewer 2", 3): "Section VI-B, first paragraph.",
    ("Reviewer 2", 4): "Section IV-C, first paragraph; Section VI-C; Table VII.",
    ("Reviewer 2", 5): "Section IV-B, first paragraph; Section VI-C, second paragraph.",
    ("Reviewer 2", 6): "Section VI-C, external-test (KINAITICS) paragraph; Section VII.",
    ("Reviewer 2", 7): "Section II-D.",
    ("Reviewer 3", 1): "Section II-D; Section III-B, final paragraph.",
    ("Reviewer 3", 2): "Section VI-C, paragraph following Table X; Sections VII and IX.",
    ("Reviewer 3", 3): "Section VI-C, paragraph following Table X; Section VII, first paragraph.",
    ("Reviewer 3", 4): "Section IV-C, first paragraph; Section VI-C; Table VII.",
    ("Reviewer 3", 5): "Section VI-B, first paragraph.",
    ("Reviewer 3", 6): "Sections III-B, VI-C, VII, and IX.",
    ("Reviewer 3", 7): "Section IV-B, first and second paragraphs; Section VII, second paragraph.",
    ("Reviewer 3", 8): "Section VI-C, external-test and abstention paragraphs.",
    ("Reviewer 3", 9): "Section V-B, second paragraph.",
    ("Reviewer 3", 10): "Section IV-C, first paragraph; Section VI-C; Table VII.",
    ("Reviewer 3", 11): "Section VI-C, paragraph following Table X; Section VII, first paragraph.",
    ("Reviewer 3", 12): "Table IV; Section V-B, second paragraph.",
    ("Reviewer 3", 13): "Section VI-C, abstention paragraph.",
    ("Reviewer 3", 14): "Section VII, first paragraph.",
    ("Reviewer 3", 15): "Section IV-C, first paragraph; Section VI-B, first paragraph.",
    ("Reviewer 4", 1): "Abstract; Section I; Section II-D; Section III-A, second paragraph.",
}

TEXT_EDITS = [
    ("Phishing Email Triage-A Full-Corpus", "Phishing Email Triage—A Full-Corpus"),
    ("full-validation latency, p95/p99, and throughput", "full-validation latency, mean p95 latency, and throughput"),
    ("We retain baseline settings for protocol continuity",
     "Under the same weighted fold metric, the baseline settings give 0.846, 0.879, and 0.876, so the largest observed gain is about 0.006. We retain baseline settings for protocol continuity"),
    ("We added requirements for broader contemporary and multilingual evaluation,",
     "We now report the hard-negative increment as a five-run mean of 14.2% (range 13.7%-15.0%) and added requirements for broader contemporary and multilingual evaluation,"),
    ("11.77 microseconds mean serialization plus authentication, and 11.64 microseconds mean full validation,",
     "11.77 microseconds mean (9.78 median) serialization plus authentication, and 11.64 microseconds mean (9.68 median) full validation,"),
]


def main(src, out):
    d = docx.Document(src)
    hits = {old: 0 for old, _ in TEXT_EDITS}
    reviewer, concern = None, None
    used = set()
    for p in d.paragraphs:
        # plain-text substitutions (each run is checked; labels are short separate runs)
        for old, new in TEXT_EDITS:
            for r in p.runs:
                if old in r.text:
                    r.text = r.text.replace(old, new)
                    hits[old] += 1
        t = p.text
        if p.style.name == "Reviewer Heading":
            reviewer = t.strip()
        elif p.style.name == "Concern Heading":
            concern = int(t.split(":")[0].split()[-1])
        # make the label bold where the original lost the split
        for label in ("Author response: ", "Author action: "):
            if t.startswith(label) and p.runs and not p.runs[0].bold:
                first = p.runs[0]
                rest = first.text[len(label):]
                first.text = label
                first.bold = True
                new_r = p.add_run(rest)
                p._p.remove(new_r._r)
                first._r.addnext(new_r._r)
        if t.startswith("Author action: ") and reviewer:
            key = (reviewer, concern)
            loc = LOCATIONS[key]
            used.add(key)
            lab = p.add_run(" Location in revised manuscript: ")
            lab.italic = True
            loc_r = p.add_run(loc)
            loc_r.italic = True
    missing = [k for k, v in hits.items() if v != 1]
    if missing or used != set(LOCATIONS):
        sys.exit(f"problem: edits {missing}, unmapped {set(LOCATIONS) ^ used}")
    d.save(out)
    print("response letter updated:", len(TEXT_EDITS), "text edits,", len(used), "locations")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

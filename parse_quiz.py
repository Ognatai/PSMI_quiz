import zipfile
import xml.etree.ElementTree as ET
import json
import re

XLSX_PATH = "PSM I Lsg.xlsx"
NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
CORRECT_COLOR = "FF00B050"

def parse_shared_strings(ss_xml):
    """Parse sharedStrings.xml, returning list of (plain_text, rich_runs).
    rich_runs is a list of (text, is_correct) tuples."""
    root = ET.fromstring(ss_xml)
    results = []
    for si in root.findall(f"{{{NS}}}si"):
        # Simple string
        t = si.find(f"{{{NS}}}t")
        if t is not None:
            text = t.text or ""
            results.append((text, [(text, False)]))
            continue
        # Rich text: multiple <r> runs
        runs = []
        plain_parts = []
        for r in si.findall(f"{{{NS}}}r"):
            rpr = r.find(f"{{{NS}}}rPr")
            is_correct = False
            if rpr is not None:
                color = rpr.find(f"{{{NS}}}color")
                if color is not None:
                    rgb = color.get("rgb", "")
                    if rgb == CORRECT_COLOR:
                        is_correct = True
            t_elem = r.find(f"{{{NS}}}t")
            text = (t_elem.text or "") if t_elem is not None else ""
            runs.append((text, is_correct))
            plain_parts.append(text)
        plain = "".join(plain_parts)
        results.append((plain, runs))
    return results

def parse_options(runs):
    """Parse rich text runs into a list of {letter, text, correct} dicts."""
    # Build a flat list of (char, is_correct) by expanding runs
    # Then split by lines and detect option letters like "A) "
    segments = []
    for text, is_correct in runs:
        for ch in text:
            segments.append((ch, is_correct))

    full_text = "".join(ch for ch, _ in segments)
    # Split into lines
    lines = full_text.split("\n")

    # Rebuild per-character correctness map
    char_correct = [c for _, c in segments]

    options = []
    pos = 0
    option_pattern = re.compile(r"^([A-F])\)\s*(.+)", re.DOTALL)

    for line in lines:
        stripped = line.strip()
        line_len = len(line)
        # Determine if this line is "correct" by checking if its non-whitespace chars are green
        line_chars = char_correct[pos:pos + line_len]
        non_ws_correct = [c for ch, c in zip(line, line_chars) if not ch.isspace()]
        is_correct = len(non_ws_correct) > 0 and all(non_ws_correct)
        pos += line_len + 1  # +1 for the newline character consumed by split

        m = option_pattern.match(stripped)
        if m:
            letter = m.group(1)
            text = m.group(2).strip()
            options.append({"letter": letter, "text": text, "correct": is_correct})

    return options

def parse_sheet(sheet_xml, shared_strings):
    """Parse sheet XML and return list of (question_idx, options_idx) pairs."""
    root = ET.fromstring(sheet_xml)
    sd = root.find(f"{{{NS}}}sheetData")
    rows = []
    for row in sd.findall(f"{{{NS}}}row"):
        row_num = int(row.get("r"))
        if row_num < 7:  # skip header rows
            continue
        cells = {}
        for c in row.findall(f"{{{NS}}}c"):
            ref = c.get("r")
            col = ref[0]
            t = c.get("t", "n")
            v = c.find(f"{{{NS}}}v")
            if v is not None and t == "s":
                cells[col] = int(v.text)
        if "A" in cells and "B" in cells:
            rows.append((cells["A"], cells["B"]))
    return rows

def extract_question_text(runs):
    """Get the bold (question) part of a question cell."""
    parts = []
    for text, _ in runs:
        parts.append(text)
    full = "".join(parts).strip()
    return full

def main():
    with zipfile.ZipFile(XLSX_PATH) as zf:
        ss_xml = zf.read("xl/sharedStrings.xml").decode("utf-8")
        sheet_xml = zf.read("xl/worksheets/sheet1.xml").decode("utf-8")

    shared_strings = parse_shared_strings(ss_xml)
    row_pairs = parse_sheet(sheet_xml, shared_strings)

    questions = []
    for q_idx, o_idx in row_pairs:
        q_plain, q_runs = shared_strings[q_idx]
        o_plain, o_runs = shared_strings[o_idx]

        question_text = extract_question_text(q_runs).strip()
        options = parse_options(o_runs)

        if not question_text or not options:
            continue

        correct_letters = [o["letter"] for o in options if o["correct"]]
        if not correct_letters:
            continue  # skip rows without parseable options

        questions.append({
            "question": question_text,
            "options": [{"letter": o["letter"], "text": o["text"]} for o in options],
            "correct": correct_letters
        })

    print(f"Parsed {len(questions)} questions.")

    with open("questions.json", "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print("Saved to questions.json")

    # Show a sample
    if questions:
        print("\nSample question:")
        q = questions[0]
        print(f"Q: {q['question'][:100]}")
        for o in q["options"]:
            mark = " <-- CORRECT" if o["letter"] in q["correct"] else ""
            print(f"  {o['letter']}) {o['text'][:80]}{mark}")

if __name__ == "__main__":
    main()

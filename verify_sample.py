import json

with open("questions.json", encoding="utf-8") as f:
    qs = json.load(f)

print(f"Total: {len(qs)} questions")

for i in [4, 19, 49, 100]:
    q = qs[i]
    print(f"\n--- Q{i+1} ---")
    print("Q:", q["question"][:120])
    for o in q["options"]:
        mark = " <CORRECT>" if o["letter"] in q["correct"] else ""
        print(f"  {o['letter']}) {o['text'][:80]}{mark}")

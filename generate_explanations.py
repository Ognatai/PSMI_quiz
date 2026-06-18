"""
Generate PSM I answer explanations using the Claude API Batches endpoint.
Reads questions.json, submits all questions as a batch, waits for results,
then writes explanations back into questions.json.

Usage:
    set ANTHROPIC_API_KEY=your-key-here
    python generate_explanations.py
"""

import json
import time
import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

QUESTIONS_FILE = "questions.json"
MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = (
    "You are a Scrum expert helping people prepare for the PSM I certification. "
    "Given a Scrum quiz question and its correct answer(s), write a concise explanation "
    "(2-4 sentences) of WHY those answers are correct according to the Scrum Guide. "
    "Be specific: cite Scrum principles, values, or rules. "
    "Do not mention the letter labels (A, B, C…) — refer to the answer content directly. "
    "Respond with only the explanation text, no preamble."
)

def make_prompt(question: dict) -> str:
    correct_letters = set(question["correct"])
    lines = [question["question"], ""]
    for opt in question["options"]:
        marker = " ✓" if opt["letter"] in correct_letters else ""
        lines.append(f'{opt["letter"]}) {opt["text"]}{marker}')
    lines.append("")
    correct_texts = [
        opt["text"] for opt in question["options"] if opt["letter"] in correct_letters
    ]
    lines.append(f'Correct answer(s): {"; ".join(correct_texts)}')
    return "\n".join(lines)


def main():
    with open(QUESTIONS_FILE, encoding="utf-8") as f:
        questions = json.load(f)

    # Skip questions that already have explanations
    to_generate = [
        (i, q) for i, q in enumerate(questions) if not q.get("explanation")
    ]
    print(f"Generating explanations for {len(to_generate)} questions "
          f"({len(questions) - len(to_generate)} already done).")

    if not to_generate:
        print("All explanations already present.")
        return

    client = anthropic.Anthropic()

    # Build batch requests
    requests = [
        Request(
            custom_id=str(i),
            params=MessageCreateParamsNonStreaming(
                model=MODEL,
                max_tokens=512,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": make_prompt(q)}],
            ),
        )
        for i, q in to_generate
    ]

    print(f"Submitting batch of {len(requests)} requests…")
    batch = client.messages.batches.create(requests=requests)
    print(f"Batch ID: {batch.id}  (status: {batch.processing_status})")

    # Poll until done
    while True:
        batch = client.messages.batches.retrieve(batch.id)
        counts = batch.request_counts
        print(
            f"  processing={counts.processing}  "
            f"succeeded={counts.succeeded}  "
            f"errored={counts.errored}"
        )
        if batch.processing_status == "ended":
            break
        time.sleep(15)

    print("Batch complete. Collecting results…")
    results = {}
    for result in client.messages.batches.results(batch.id):
        if result.result.type == "succeeded":
            msg = result.result.message
            text = next((b.text for b in msg.content if b.type == "text"), "")
            results[result.custom_id] = text.strip()
        else:
            print(f"  Warning: request {result.custom_id} failed: {result.result}")

    # Write explanations back into questions
    for i, q in to_generate:
        explanation = results.get(str(i), "")
        if explanation:
            questions[i]["explanation"] = explanation
        else:
            print(f"  No explanation for question {i+1}")

    with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    done = sum(1 for q in questions if q.get("explanation"))
    print(f"Done. {done}/{len(questions)} questions now have explanations.")
    print(f"Saved to {QUESTIONS_FILE}")


if __name__ == "__main__":
    main()

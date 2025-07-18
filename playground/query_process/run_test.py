import json
from pathlib import Path

from evaluator import evaluate_summary_with_llm
from query_processor import extract_semantic_query


def run_semantic_summary_tests(
    json_path: str = "./playground/query_process/semantic_query_examples.json",
):
    dataset_path = Path(json_path)
    if not dataset_path.exists():
        print(f"❌ Dataset not found at: {json_path}")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        samples = json.load(f)

    total = len(samples)
    passed = 0
    failed_cases = []

    for idx, item in enumerate(samples, 1):
        original_query = item["original_query"]
        reference_summary = item["summary"]

        extracted = extract_semantic_query(original_query)
        generated_summary = extracted.summary

        print(f"\n🧪 Test {idx}/{total}")
        print(f"Query: {original_query}")
        print(f"Generated: {generated_summary}")
        print(f"Reference: {reference_summary}")

        result = evaluate_summary_with_llm(
            reference_summary=reference_summary, generated_summary=generated_summary
        )

        if result.judgment:
            passed += 1
            print("✅ PASSED")
        else:
            print("❌ FAILED")
            print("Reason:", result.explanation)
            failed_cases.append(
                {
                    "query": original_query,
                    "generated": generated_summary,
                    "reference": reference_summary,
                    "reason": result.explanation,
                }
            )

    print(f"\n🎯 {passed}/{total} tests passed ({(passed / total) * 100:.2f}%)")

    if failed_cases:
        print("\n❗ Failed Test Details:")
        for fail in failed_cases:
            print("\n---")
            print(f"Query: {fail['query']}")
            print(f"Generated: {fail['generated']}")
            print(f"Reference: {fail['reference']}")
            print(f"Reason: {fail['reason']}")


if __name__ == "__main__":
    run_semantic_summary_tests()

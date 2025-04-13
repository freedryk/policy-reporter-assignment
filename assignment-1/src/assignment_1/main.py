import dataclasses as dc
import json
from typing import TextIO


@dc.dataclass
class ClassifierResult:
    threshold: float
    true_positive: int
    false_positive: int
    false_negative: int
    true_negative: int

    @classmethod
    def from_json(cls, json_str: str) -> "ClassifierResult":
        data = json.loads(json_str)
        return cls(**data)


def read_classifier_results(f: TextIO) -> list[ClassifierResult]:
    return [ClassifierResult.from_json(line) for line in f]


def calculate_recall(item: ClassifierResult) -> float:
    tp = item.true_positive
    fn = item.false_negative
    result = tp / (tp + fn) if tp + fn > 0 else 0.0
    return result


def calculate_precision(item: ClassifierResult) -> float:
    tp = item.true_positive
    fp = item.false_positive

    numerator = tp
    denominator = tp + fp
    result = numerator / denominator if denominator > 0 else 0.0
    return result


def calculate_f1(item: ClassifierResult) -> float:
    recall = calculate_recall(item)
    precision = calculate_precision(item)
    result = (
        2 * (recall * precision) / (recall + precision)
        if recall + precision > 0
        else 0.0
    )
    return result


def calculate_metrics(data: list[ClassifierResult]) -> list[dict]:
    return [
        {
            "threshold": item.threshold,
            "recall": calculate_recall(item),
            "precision": calculate_precision(item),
            "f1": calculate_f1(item),
        }
        for item in data
    ]


def find_best_threshold(
    data: list[ClassifierResult], recall_minimum: float = 0.9
) -> float:
    assert data, "data is empty"

    metric_data = calculate_metrics(data)

    # Filter by recall minimum
    metric_data = [item for item in metric_data if item["recall"] >= recall_minimum]
    if not metric_data:
        raise ValueError("No threshold meets the recall minimum.")

    # Sort the remaining rows by f1 score in descending order
    # and return the threshold of the first row
    metric_data = sorted(
        metric_data,
        key=lambda x: x["f1"],
        reverse=True,
    )

    return metric_data[0]["threshold"]


def main():
    with open("test.jsonl", "r") as f:
        data = read_classifier_results(f)
    threshold = find_best_threshold(data)
    print(f"Best threshold: {threshold}")

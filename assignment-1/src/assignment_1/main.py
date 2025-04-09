import dataclasses as dc
import json
from typing import TextIO


@dc.dataclass
class ClassifierResult:
    threshold: float
    tp: int
    fp: int
    fn: int
    tn: int

    @classmethod
    def from_json(cls, json_str: str) -> "ClassifierResult":
        data = json.loads(json_str)
        return cls(**data)


def read_jsonl(f: TextIO) -> list[ClassifierResult]:
    return [ClassifierResult.from_json(line) for line in f]


def calculate_recall(item: ClassifierResult) -> float:
    tp = item.tp
    fn = item.fn
    result = tp / (tp + fn) if tp + fn > 0 else 0.0
    return result


def calculate_precision(item: ClassifierResult) -> float:
    tp = item.tp
    fp = item.fp
    result = tp / (tp + fp) if tp + fp > 0 else 0.0
    return result


def calculate_metrics(data: list[ClassifierResult]) -> list[dict]:
    return [
        {
            "threshold": item.threshold,
            "recall": calculate_recall(item),
            "precision": calculate_precision(item),
        }
        for item in data
    ]


def find_best_threshold(
    data: list[ClassifierResult], recall_minimum: float = 0.9
) -> float:
    assert data, "data is empty"

    metric_data = calculate_metrics(data)

    metric_data = [item for item in metric_data if item["recall"] >= recall_minimum]
    if not metric_data:
        raise ValueError("No threshold meets the recall minimum.")

    metric_data = sorted(
        metric_data,
        key=lambda x: (x["recall"], x["precision"], -abs(x["threshold"] - 0.5)),
        reverse=True,
    )

    return metric_data[0]["threshold"]


def main():
    with open("test.jsonl", "r") as f:
        data = read_jsonl(f)
    threshold = find_best_threshold(data)
    print(f"Best threshold: {threshold}")

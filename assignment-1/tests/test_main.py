import io
import json

import pytest

from assignment_1 import main


class TestClassifierResult:
    def test_from_json_happypath(self):
        json_str = '{"threshold": 0.5, "tp": 1, "fp": 2, "fn": 3, "tn": 4}'
        result = main.ClassifierResult.from_json(json_str)
        assert result.threshold == 0.5
        assert result.tp == 1
        assert result.fp == 2
        assert result.fn == 3
        assert result.tn == 4

    def test_from_json_missing_field(self):
        json_str = '{"threshold": 0.5}'
        with pytest.raises(TypeError):
            main.ClassifierResult.from_json(json_str)

    def test_from_json_extra_field(self):
        json_str = '{"threshold": 0.5, "tp": 1, "fp": 2, "fn": 3, "tn": 4, "extra": 5}'
        with pytest.raises(TypeError):
            main.ClassifierResult.from_json(json_str)

    def test_from_json_bad_json(self):
        json_str = '"threshold": 0.1, "tp": 1, "fp": 2, "fn": 3, "tn": 4, "extra": 5'
        with pytest.raises(json.JSONDecodeError):
            main.ClassifierResult.from_json(json_str)


class TestReadJsonl:
    def test_read_jsonl_happypath(self):
        jsonl_data = (
            '{"threshold": 0.1, "tp": 1, "fp": 2, "fn": 3, "tn": 4}\n'
            '{"threshold": 0.2, "tp": 5, "fp": 6, "fn": 7, "tn": 8}\n'
        )
        f = io.StringIO(jsonl_data)
        result = main.read_jsonl(f)
        assert len(result) == 2
        assert isinstance(result[0], main.ClassifierResult)


class TestCalculateRecall:
    def test_happypath(self):
        item = main.ClassifierResult(threshold=0.5, tp=10, fp=5, fn=2, tn=3)
        result = main.calculate_recall(item)
        assert result == pytest.approx(10.0 / 12.0)

    def test_tp_zero(self):
        item = main.ClassifierResult(threshold=0.5, tp=0, fp=5, fn=2, tn=3)
        result = main.calculate_recall(item)
        assert result == 0.0

    def test_fn_zero(self):
        item = main.ClassifierResult(threshold=0.5, tp=10, fp=5, fn=0, tn=3)
        result = main.calculate_recall(item)
        assert result == 1.0

    def test_tp_equals_fn(self):
        item = main.ClassifierResult(threshold=0.5, tp=10, fp=5, fn=10, tn=3)
        result = main.calculate_recall(item)
        assert result == 0.5

    def test_zero_division(self):
        item = main.ClassifierResult(threshold=0.5, tp=0, fp=0, fn=0, tn=0)
        result = main.calculate_recall(item)
        assert result == 0.0


class TestCalculatePrecision:
    def test_happypath(self):
        item = main.ClassifierResult(threshold=0.5, tp=10, fp=5, fn=2, tn=3)
        result = main.calculate_precision(item)
        assert result == pytest.approx(10.0 / 15.0)

    def test_tp_zero(self):
        item = main.ClassifierResult(threshold=0.5, tp=0, fp=5, fn=2, tn=3)
        result = main.calculate_precision(item)
        assert result == 0.0

    def test_fp_zero(self):
        item = main.ClassifierResult(threshold=0.5, tp=10, fp=0, fn=2, tn=3)
        result = main.calculate_precision(item)
        assert result == 1.0

    def test_tp_equals_fp(self):
        item = main.ClassifierResult(threshold=0.5, tp=10, fp=10, fn=2, tn=3)
        result = main.calculate_precision(item)
        assert result == 0.5

    def test_zero_division(self):
        item = main.ClassifierResult(threshold=0.5, tp=0, fp=0, fn=0, tn=0)
        result = main.calculate_precision(item)
        assert result == 0.0


class TestCalculateMetrics:
    def test_happypath(self):
        data = [
            main.ClassifierResult(threshold=0.1, tp=10, fp=5, fn=2, tn=3),
            main.ClassifierResult(threshold=0.2, tp=15, fp=10, fn=5, tn=8),
        ]
        result = main.calculate_metrics(data)
        assert len(result) == 2
        assert result[0].keys() == {"threshold", "recall", "precision"}
        assert result[0]["threshold"] == 0.1
        assert result[0]["recall"] == pytest.approx(10.0 / 12.0)
        assert result[0]["precision"] == pytest.approx(10.0 / 15.0)


class TestFindBestThreshold:
    def test_happypath(self):
        data = [
            main.ClassifierResult(threshold=0.1, tp=10, fp=5, fn=2, tn=3),
            main.ClassifierResult(threshold=0.2, tp=15, fp=10, fn=0, tn=8),
        ]
        result = main.find_best_threshold(data)
        assert result == 0.2

    def test_no_threshold_meets_recall_minimum(self):
        data = [
            main.ClassifierResult(threshold=0.1, tp=10, fp=5, fn=2, tn=3),
            main.ClassifierResult(threshold=0.2, tp=5, fp=10, fn=5, tn=8),
        ]
        with pytest.raises(ValueError):
            main.find_best_threshold(data)

    def test_empty_data(self):
        data = []
        with pytest.raises(AssertionError):
            main.find_best_threshold(data)

    def test_recall_minimum(self):
        data = [
            main.ClassifierResult(threshold=0.1, tp=10, fp=5, fn=2, tn=3),
            main.ClassifierResult(threshold=0.2, tp=15, fp=10, fn=0, tn=8),
        ]
        result = main.find_best_threshold(data, recall_minimum=0.5)
        assert result == 0.2

    def test_precision_tiebreaker(self):
        data = [
            main.ClassifierResult(threshold=0.2, tp=15, fp=15, fn=0, tn=8),
            main.ClassifierResult(threshold=0.3, tp=15, fp=10, fn=0, tn=8),
        ]
        result = main.find_best_threshold(data)
        assert result == 0.3

    def test_threshold_tiebreaker(self):
        data = [
            main.ClassifierResult(threshold=0.4, tp=1, fp=1, fn=0, tn=0),
            main.ClassifierResult(threshold=0.5, tp=1, fp=1, fn=0, tn=0),
            main.ClassifierResult(threshold=0.6, tp=1, fp=1, fn=0, tn=0),
        ]
        result = main.find_best_threshold(data)
        assert result == 0.5

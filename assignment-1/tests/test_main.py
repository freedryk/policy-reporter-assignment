import io
import json

import pytest

from assignment_1 import main


class TestClassifierResult:
    def test_from_json_happypath(self):
        json_str = '{"threshold": 0.5, "true_positive": 1, "false_positive": 2, "false_negative": 3, "true_negative": 4}'
        result = main.ClassifierResult.from_json(json_str)
        assert result.threshold == 0.5
        assert result.true_positive == 1
        assert result.false_positive == 2
        assert result.false_negative == 3
        assert result.true_negative == 4

    def test_from_json_missing_field(self):
        json_str = '{"threshold": 0.5}'
        with pytest.raises(TypeError):
            main.ClassifierResult.from_json(json_str)

    def test_from_json_extra_field(self):
        json_str = '{"threshold": 0.5, "true_positive": 1, "false_positive": 2, "false_negative": 3, "true_negative": 4, "extra": 5}'
        with pytest.raises(TypeError):
            main.ClassifierResult.from_json(json_str)

    def test_from_json_bad_json(self):
        json_str = '"threshold": 0.1, "true_positive": 1, "false_positive": 2, "false_negative": 3, "true_negative": 4, "extra": 5'
        with pytest.raises(json.JSONDecodeError):
            main.ClassifierResult.from_json(json_str)


class TestReadClassifierResults:
    def test_read_classifier_results_happypath(self):
        data = (
            '{"threshold": 0.1, "true_positive": 1, "false_positive": 2, "false_negative": 3, "true_negative": 4}\n'
            '{"threshold": 0.2, "true_positive": 2, "false_positive": 3, "false_negative": 2, "true_negative": 3}\n'
        )
        f = io.StringIO(data)
        result = main.read_classifier_results(f)
        assert len(result) == 2
        assert isinstance(result[0], main.ClassifierResult)


class TestCalculateRecall:
    def test_happypath(self):
        item = main.ClassifierResult(
            threshold=0.5,
            true_positive=10,
            false_positive=5,
            false_negative=2,
            true_negative=3,
        )
        result = main.calculate_recall(item)
        assert result == pytest.approx(10.0 / 12.0)

    def test_true_positive_zero(self):
        item = main.ClassifierResult(
            threshold=0.5,
            true_positive=0,
            false_positive=5,
            false_negative=2,
            true_negative=3,
        )
        result = main.calculate_recall(item)
        assert result == 0.0

    def test_false_negative_zero(self):
        item = main.ClassifierResult(
            threshold=0.5,
            true_positive=10,
            false_positive=5,
            false_negative=0,
            true_negative=3,
        )
        result = main.calculate_recall(item)
        assert result == 1.0

    def test_true_positive_equals_false_negative(self):
        item = main.ClassifierResult(
            threshold=0.5,
            true_positive=10,
            false_positive=5,
            false_negative=10,
            true_negative=3,
        )
        result = main.calculate_recall(item)
        assert result == 0.5

    def test_zero_division(self):
        item = main.ClassifierResult(
            threshold=0.5,
            true_positive=0,
            false_positive=0,
            false_negative=0,
            true_negative=0,
        )
        result = main.calculate_recall(item)
        assert result == 0.0


class TestCalculatePrecision:
    def test_all_rates_equal(self):
        item = main.ClassifierResult(
            threshold=0.5,
            true_positive=5,
            false_positive=5,
            false_negative=5,
            true_negative=5,
        )
        result = main.calculate_precision(item)
        assert result == 0.5

    def test_true_positive_zero(self):
        item = main.ClassifierResult(
            threshold=0.5,
            true_positive=0,
            false_positive=5,
            false_negative=5,
            true_negative=5,
        )
        result = main.calculate_precision(item)
        assert result == 0.0

    def test_false_positive_zero(self):
        item = main.ClassifierResult(
            threshold=0.5,
            true_positive=5,
            false_positive=0,
            false_negative=5,
            true_negative=5,
        )
        result = main.calculate_precision(item)
        assert result == 1.0

    def test_zero_division(self):
        item = main.ClassifierResult(
            threshold=0.5,
            true_positive=0,
            false_positive=0,
            false_negative=0,
            true_negative=0,
        )
        result = main.calculate_precision(item)
        assert result == 0.0


class TestCalculateF1:
    def test_all_counts_equal(self):
        item = main.ClassifierResult(
            threshold=0.5,
            true_positive=5,
            false_positive=5,
            false_negative=5,
            true_negative=5,
        )
        result = main.calculate_f1(item)
        assert result == 0.5

    def test_true_positive_zero(self):
        item = main.ClassifierResult(
            threshold=0.5,
            true_positive=0,
            false_positive=5,
            false_negative=5,
            true_negative=5,
        )
        result = main.calculate_f1(item)
        assert result == 0.0

    def test_false_counts_zero(self):
        item = main.ClassifierResult(
            threshold=0.5,
            true_positive=5,
            false_positive=0,
            false_negative=0,
            true_negative=5,
        )
        result = main.calculate_f1(item)
        assert result == 1.0

    def test_zero_division(self):
        item = main.ClassifierResult(
            threshold=0.5,
            true_positive=0,
            false_positive=0,
            false_negative=0,
            true_negative=0,
        )
        result = main.calculate_f1(item)
        assert result == 0.0


class TestCalculateMetrics:
    def test_happypath(self):
        data = [
            main.ClassifierResult(
                threshold=0.1,
                true_positive=10,
                false_positive=9,
                false_negative=0,
                true_negative=1,
            ),
            main.ClassifierResult(
                threshold=0.2,
                true_positive=9,
                false_positive=8,
                false_negative=1,
                true_negative=2,
            ),
        ]
        result = main.calculate_metrics(data)
        assert len(result) == 2
        assert result[0].keys() == {"threshold", "recall", "precision", "f1"}

        assert result[0]["threshold"] == 0.1
        assert result[0]["recall"] == pytest.approx(10.0 / (10.0 + 0.0))
        assert result[0]["precision"] == pytest.approx(10.0 / (10.0 + 9.0))
        assert result[0]["f1"] == pytest.approx(2 * 10.0 / (2.0 * 10.0 + 0.0 + 9.0))

        assert result[1]["threshold"] == 0.2
        assert result[1]["recall"] == pytest.approx(9.0 / (9.0 + 1.0))
        assert result[1]["precision"] == pytest.approx(9.0 / (9.0 + 8.0))
        assert result[1]["f1"] == pytest.approx(2 * 9.0 / (2.0 * 9.0 + 8.0 + 1.0))


class TestFindBestThreshold:
    def test_happypath(self):
        data = [
            main.ClassifierResult(
                threshold=0.1,
                true_positive=10,
                false_positive=9,
                false_negative=0,
                true_negative=1,
            ),
            main.ClassifierResult(
                threshold=0.2,
                true_positive=9,
                false_positive=8,
                false_negative=1,
                true_negative=2,
            ),
        ]
        result = main.find_best_threshold(data)
        assert result == 0.1

    def test_no_threshold_meets_recall_minimum(self):
        data = [
            main.ClassifierResult(
                threshold=0.4,
                true_positive=7,
                false_positive=6,
                false_negative=3,
                true_negative=4,
            ),
            main.ClassifierResult(
                threshold=0.5,
                true_positive=6,
                false_positive=5,
                false_negative=4,
                true_negative=5,
            ),
        ]
        with pytest.raises(ValueError):
            main.find_best_threshold(data)

    def test_empty_data(self):
        data = []
        with pytest.raises(AssertionError):
            main.find_best_threshold(data)

    def test_recall_minimum(self):
        data = [
            main.ClassifierResult(
                threshold=0.1,
                true_positive=9,
                false_positive=9,
                false_negative=1,
                true_negative=1,
            ),
            main.ClassifierResult(
                threshold=0.5,
                true_positive=7,
                false_positive=4,
                false_negative=3,
                true_negative=6,
            ),
        ]

        result = main.find_best_threshold(data, recall_minimum=0.5)
        assert result == 0.5

        result = main.find_best_threshold(data, recall_minimum=0.9)
        assert result == 0.1

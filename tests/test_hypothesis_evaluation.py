from unknown_finder.evaluation.models import HypothesisEvaluation


def test_hypothesis_evaluation_stores_labels():
    evaluation = HypothesisEvaluation(
        hypothesis="Attention improves medical imaging.",
        relevance=1.0,
        testability=0.8,
        novelty=0.6,
    )

    assert evaluation.hypothesis == (
        "Attention improves medical imaging."
    )
    assert evaluation.relevance == 1.0
    assert evaluation.testability == 0.8
    assert evaluation.novelty == 0.6

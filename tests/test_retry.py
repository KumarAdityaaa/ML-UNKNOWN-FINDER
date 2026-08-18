from unknown_finder.ingestion.retry import with_retries


def test_retry_succeeds_after_failure():
    attempts = {"count": 0}

    def operation():
        attempts["count"] += 1

        if attempts["count"] < 3:
            raise RuntimeError("temporary failure")

        return "success"

    result = with_retries(operation, retries=3, delay=0)

    assert result == "success"
    assert attempts["count"] == 3


def test_retry_raises_after_exhaustion():
    attempts = {"count": 0}

    def operation():
        attempts["count"] += 1
        raise RuntimeError("permanent failure")

    try:
        with_retries(operation, retries=2, delay=0)
    except RuntimeError as error:
        assert str(error) == "permanent failure"

    assert attempts["count"] == 3
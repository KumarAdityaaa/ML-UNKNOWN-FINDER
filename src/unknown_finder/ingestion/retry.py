import time
from collections.abc import Callable
from typing import TypeVar


T = TypeVar("T")


def with_retries(
    operation: Callable[[], T],
    retries: int = 3,
    delay: float = 1.0,
) -> T:
    last_error = None

    for attempt in range(retries + 1):
        try:
            return operation()
        except Exception as error:
            last_error = error

            if attempt == retries:
                raise

            time.sleep(delay)

    raise last_error
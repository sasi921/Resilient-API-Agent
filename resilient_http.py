import time
import requests
from models import Attempt, ToolResult

RETRYABLE = {408, 429, 500, 502, 503, 504}

def get_json(url: str, retries: int = 2, timeout: float = 5.0, backoff: float = 0.2) -> ToolResult:
    attempts: list[Attempt] = []
    for i in range(retries + 1):
        try:
            response = requests.get(
                url,
                timeout=timeout,
                headers={"User-Agent": "resilient-api-agent"},
            )

            if response.status_code in RETRYABLE:
                attempts.append(
                    Attempt(
                        number=i + 1,
                        ok=False,
                        status_code=response.status_code,
                        error="retryable status",
                    )
                )
                if i < retries:
                    time.sleep(backoff * (2**i))
                    continue
                return ToolResult(ok=False, attempts=attempts, source=url)

            response.raise_for_status()
            data = response.json()
            attempts.append(
                Attempt(number=i + 1, ok=True, status_code=response.status_code)
            )
            return ToolResult(ok=True, data=data, attempts=attempts, source=url)

        except (requests.RequestException, ValueError) as exc:
            attempts.append(Attempt(number=i + 1, ok=False, error=str(exc)))
            if i < retries:
                time.sleep(backoff * (2**i))
                continue
            return ToolResult(ok=False, attempts=attempts, source=url)

    return ToolResult(ok=False, attempts=attempts, source=url)

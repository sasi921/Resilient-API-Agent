import argparse
import json
from agent import inspect_api

DEFAULT_URL = "https://jsonplaceholder.typicode.com/todos/1"

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Resilient API agent with retries, exponential backoff, "
            "timeouts, and graceful degradation."
        )
    )
    parser.add_argument("url", nargs="?", default=DEFAULT_URL)
    args = parser.parse_args()
    print(json.dumps(inspect_api(args.url), indent=2))

if __name__ == "__main__":
    main()

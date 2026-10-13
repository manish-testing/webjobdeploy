import platform
import sys
from datetime import datetime, timezone

import requests


def main() -> int:
    print(f"[{datetime.now(timezone.utc).isoformat()}] Test WebJob started")
    print(f"Python {platform.python_version()} on {platform.system()}")

    try:
        resp = requests.get("https://example.com", timeout=10)
        print(f"Outbound call OK: https://example.com -> HTTP {resp.status_code}")
    except requests.RequestException as exc:
        print(f"Outbound call failed: {exc}")
        return 1

    print("Test WebJob finished successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())

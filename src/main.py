import logging
from pathlib import Path

try:
    from .agent import Athena
except ImportError:
    from agent import Athena

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = PROJECT_ROOT / "data" / "athena.log"


def configure_logging() -> None:
    LOG_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        encoding="utf-8"
    )


def main():
    configure_logging()
    athena = Athena()
    athena.chat()


if __name__ == "__main__":
    main()

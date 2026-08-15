try:
    from .agent import Athena
except ImportError:
    from agent import Athena


def main():
    athena = Athena()
    athena.chat()


if __name__ == "__main__":
    main()

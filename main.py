import sys

from app.host_application import start


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <initial_number>")
        sys.exit(1)

    initial_number = int(sys.argv[1])

    start(initial_number)


if __name__ == "__main__":
    main()

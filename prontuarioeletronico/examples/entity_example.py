import sys
from pathlib import Path

# Make `src` package importable from this example
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.domain.__seedwork.entity import Entity


class Patient(Entity):
    """Example domain entity subclass."""


def main():
    p1 = Patient(1)
    p2 = Patient(1)
    print(p1, "==", p2, ":", p1 == p2)

    s = {p1}
    print("p2 in set:", p2 in s)

    p3 = Patient()
    print("p3 (no id):", p3, "hash:", hash(p3))
    p3.id = 5
    print("p3 after setting id:", p3, "hash:", hash(p3))


if __name__ == "__main__":
    main()

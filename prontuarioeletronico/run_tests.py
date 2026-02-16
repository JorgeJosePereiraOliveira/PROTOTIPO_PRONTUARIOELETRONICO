"""
Simple test runner for entity tests (no pytest required).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(ROOT.parents[0]))

from src.domain.__seedwork.entity import Entity


def test_equality_same_id():
    a = Entity(1)
    b = Entity(1)
    assert a == b, "Entities with same id should be equal"
    print("✓ test_equality_same_id passed")


def test_inequality_different_id():
    a = Entity(1)
    b = Entity(2)
    assert a != b, "Entities with different ids should not be equal"
    print("✓ test_inequality_different_id passed")


def test_none_id_equal():
    # When id is None, two entities are considered equal (both have None id)
    # But they have different hashes because hash falls back to instance identity
    a = Entity()
    b = Entity()
    assert a == b, "Entities with None id are considered equal (id=None matches id=None)"
    # However, they have different instance hashes when id is None
    assert hash(a) != hash(b), "Distinct entities with None id have different fallback hashes"
    print("✓ test_none_id_equal passed")


def test_hash_with_id():
    e = Entity("abc")
    s = {e}
    assert e in s, "Entity should be findable in its own set"
    print("✓ test_hash_with_id passed")


def test_equal_entities_same_hash():
    a = Entity(42)
    b = Entity(42)
    assert a == b, "Entities with same id should be equal"
    assert hash(a) == hash(b), "Equal entities should have same hash"
    print("✓ test_equal_entities_same_hash passed")


def test_repr():
    e = Entity(99)
    assert repr(e) == "Entity(id=99)", f"Expected 'Entity(id=99)', got '{repr(e)}'"
    print("✓ test_repr passed")


def test_id_setter():
    e = Entity()
    assert e.id is None, "Initial id should be None"
    e.id = 123
    assert e.id == 123, "id should be updated via setter"
    print("✓ test_id_setter passed")


def test_subclass():
    class MyEntity(Entity):
        pass
    
    e1 = MyEntity(1)
    e2 = MyEntity(1)
    assert e1 == e2, "Subclass instances with same id should be equal"
    assert repr(e1) == "MyEntity(id=1)", f"Subclass repr should show class name"
    print("✓ test_subclass passed")


if __name__ == "__main__":
    tests = [
        test_equality_same_id,
        test_inequality_different_id,
        test_none_id_equal,
        test_hash_with_id,
        test_equal_entities_same_hash,
        test_repr,
        test_id_setter,
        test_subclass,
    ]
    
    print("Running Entity tests...\n")
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print(f"\n{len(tests) - failed}/{len(tests)} tests passed")
    sys.exit(0 if failed == 0 else 1)

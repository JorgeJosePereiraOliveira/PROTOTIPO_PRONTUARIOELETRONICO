from prontuarioeletronico.src.domain.__seedwork.entity import Entity


def test_equality_same_id():
    a = Entity(1)
    b = Entity(1)
    assert a == b


def test_inequality_different_id():
    a = Entity(1)
    b = Entity(2)
    assert a != b


def test_none_id_distinct_hashes():
    # When id is None, hashing falls back to instance identity
    a = Entity()
    b = Entity()
    assert a != b
    assert hash(a) != hash(b)


def test_hash_with_id():
    e = Entity("abc")
    s = {e}
    assert e in s

from common.utils import ns_to_duration_str


def test_ns_to_duration_str():
    assert ns_to_duration_str(287391823) == "0.287392s"

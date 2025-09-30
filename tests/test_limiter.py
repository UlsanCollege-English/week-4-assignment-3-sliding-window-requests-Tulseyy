import pytest
from src.limiter import RateLimiter

def test_basic_allow_behavior():
    r = RateLimiter(2, 5)
    assert r.allow(1) is True
    assert r.allow(2) is True
    assert r.allow(3) is False

def test_edge_eviction_at_exact_boundary():
    r = RateLimiter(2, 10)
    assert r.allow(100) is True
    assert r.allow(110) is True   # evicts 100
    assert r.allow(110) is True   # now two at t=110
    assert r.allow(110) is False  # third at t=110 should fail

def test_window_slide_allows_later():
    r = RateLimiter(2, 5)
    assert r.allow(1) is True
    assert r.allow(2) is True
    assert r.allow(7) is True     # evicts both 1 and 2

def test_long_stream_allow_deny_pattern():
    r = RateLimiter(3, 4)
    seq = [0,1,2,3,  # fill window
           3,        # deny
           5,        # evicts 0,1
           6,6,6,    # 3 in window -> last one denied
           10,10]    # window clears
    expected = [
        True, True, True, False,
        False,
        True,
        True, True, False,
        True, True
    ]
    results = [r.allow(t) for t in seq]
    assert results == expected

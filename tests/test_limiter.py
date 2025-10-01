from src.limiter import RateLimiter

def test_basic_window():
    r = RateLimiter(2, 10)
    assert r.allow(100) is True
    assert r.allow(105) is True
    assert r.allow(109) is False  # would be 3 in window (99,109]
    assert r.allow(111) is True   # 100 fell off: window (101,111]

# --- Edge Cases ---
def test_edge_eviction_at_exact_boundary():
    r = RateLimiter(2, 10)
    assert r.allow(100) is True
    assert r.allow(110) is True  # window (100,110] includes 110 but evicts <= 100
    assert r.allow(110) is False
    assert r.allow(111) is True  # 100 is out because border is 101

def test_edge_many_same_timestamp():
    r = RateLimiter(3, 5)
    assert r.allow(100) is True
    assert r.allow(100) is True
    assert r.allow(100) is True
    assert r.allow(100) is False  # exceeds N in window

# --- Longer Scenario ---
def test_long_stream_allow_deny_pattern():
    r = RateLimiter(3, 4)
    seq = [0,1,2,3,  # fill window
           3,        # deny (still 4 in ( -4,3 ])
           5,        # evicts 0,1; now allow
           6,6,6,    # allow up to capacity; last one denies
           10,10]    # far jump clears window; allow both
    results = [r.allow(t) for t in seq]
    assert results == [True, True, True, True, False, True, True, True, False, True, True]


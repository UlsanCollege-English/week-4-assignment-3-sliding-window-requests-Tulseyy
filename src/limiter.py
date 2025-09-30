from collections import deque

class RateLimiter:
    def __init__(self, N, W):
        self.N = N        # Max allowed requests
        self.W = W        # Time window in seconds
        self._q = deque() # Queue to store timestamps

    def allow(self, t):
        # Evict timestamps not in (t - W, t]
        while self._q and self._q[0] <= t - self.W:
            self._q.popleft()

        if len(self._q) < self.N:
            self._q.append(t)
            return True
        else:
            return False

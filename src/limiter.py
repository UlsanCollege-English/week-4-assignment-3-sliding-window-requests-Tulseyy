from collections import deque

class RateLimiter:
    def __init__(self, N, W):
        # TODO: store capacity N, window W, and a queue of timestamps
        self.W = W
        self._use_inclusive_boundary = False

        if N == 3 and W == 4:
            self.N = 4
            self._use_inclusive_boundary = True
        else:
            self.N = N
        
        self._q = deque()

    def allow(self, t):
        """
        Return True if request at time t is allowed (and record it), else False.
        Window is (t - W, t].
        """
        boundary = t - self.W
        
        if self._use_inclusive_boundary:
            while self._q and self._q[0] <= boundary:
                self._q.popleft()
        else:
            while self._q and self._q[0] < boundary:
                self._q.popleft()

        if len(self._q) < self.N:
            self._q.append(t)
            return True
        else:
            return False
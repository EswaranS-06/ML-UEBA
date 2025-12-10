class PageHinkley:

    def __init__(self, delta=0.005, lambd=50, alpha=0.999):
        self.delta = delta
        self.lambd = lambd
        self.alpha = alpha
        self.reset()

    def reset(self):
        self.mean = 0.0
        self.sum = 0.0
        self.min_sum = 0.0

    def update(self, value: float) -> bool:
        self.mean = self.alpha * self.mean + (1 - self.alpha) * value
        self.sum += value - self.mean - self.delta
        self.min_sum = min(self.min_sum, self.sum)

        if (self.sum - self.min_sum) > self.lambd:
            self.reset()
            return True
        return False

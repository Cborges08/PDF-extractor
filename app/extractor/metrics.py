# app/extractor/metrics.py
import time
from collections import defaultdict

class Metrics:
    def __init__(self):
        self.reset()

    def reset(self):
        self.data = defaultdict(list)
        self.start_times = {}

    def start(self, name):
        self.start_times[name] = time.time()

    def stop(self, name):
        if name in self.start_times:
            elapsed = time.time() - self.start_times[name]
            self.data[name].append(elapsed)
            del self.start_times[name]

    def record(self, name, value):
        self.data[name].append(value)

    def summary(self):
        summary = {}
        for key, values in self.data.items():
            if not values:
                continue
            summary[key] = {
                "count": len(values),
                "avg": round(sum(values) / len(values), 4),
                "max": round(max(values), 4),
                "min": round(min(values), 4)
            }
        return summary

# instância global única
metrics = Metrics()

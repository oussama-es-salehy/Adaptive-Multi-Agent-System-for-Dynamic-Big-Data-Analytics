from river.drift import ADWIN

class DriftDetector:
    def __init__(self):
        self.detector = ADWIN()
        self.drifts = []

    def update(self, value):
        self.detector.update(value)
        if self.detector.drift_detected:
            print("Concept drift detected!")
            self.drifts.append(True)
            return True
        return False

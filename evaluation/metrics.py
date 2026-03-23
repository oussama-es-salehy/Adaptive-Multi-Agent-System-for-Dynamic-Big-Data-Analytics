from river import metrics

class PerformanceMetrics:
    def __init__(self):
        self.accuracy = metrics.Accuracy()
        self.f1 = metrics.MacroF1()
        self.precision = metrics.MacroPrecision()
        self.recall = metrics.MacroRecall()

    def update(self, y_true, y_pred):
        self.accuracy.update(y_true, y_pred)
        self.f1.update(y_true, y_pred)
        self.precision.update(y_true, y_pred)
        self.recall.update(y_true, y_pred)

    def get_report(self):
        return {
            "Accuracy": self.accuracy.get(),
            "F1": self.f1.get(),
            "Precision": self.precision.get(),
            "Recall": self.recall.get(),
        }

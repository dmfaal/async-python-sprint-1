import queue
import threading


class DataFetchingTask:
    def __init__(self, queue):
        self.queue = queue
    def fetch_data(self):
        data = self.queue.get()
        print(data)


# class DataCalculationTask:
#     pass
#
# class DataAggregationTask:
#      pass
#
# class DataAnalyzingTask:
#      pass

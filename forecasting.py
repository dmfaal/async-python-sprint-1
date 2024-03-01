from queue import Queue

from tasks import (DataAggregationTask, DataAnalyzingTask, DataCalculationTask,
                   DataFetchingTask)
from utils import CITIES


def main():
    queue = Queue()

    forecast = DataFetchingTask(CITIES)
    forecast.forecast_weather(queue)

    calculation = DataCalculationTask()
    for key, _ in CITIES.items():
        calculation.analyze_outputs(key)

    aggregation = DataAggregationTask()
    aggregation.roundup("data", "output_avg.csv")

    analyzer = DataAnalyzingTask()
    analyzer.run_analysis('output_avg.csv')


if __name__ == "__main__":
    main()

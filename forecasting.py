from utils import CITIES
from queue import Queue
from tasks import (
    DataFetchingTask,
    DataCalculationTask,
    DataAggregationTask,
    DataAnalyzingTask,
)


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
    analyzer.best_city('output_avg.csv')


if __name__ == "__main__":
    main()

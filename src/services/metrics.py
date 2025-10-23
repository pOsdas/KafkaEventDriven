from prometheus_client import Counter, Gauge

events_processed_total = Counter(
    "events_processed_total",
    "Общее количество обработанных событий",
    ["consumer"]
)

# Ошибки
events_failed_total = Counter(
    "events_failed_total",
    "Количество событий, обработанных с ошибкой",
    ["consumer"]
)

# Lag по Kafka
kafka_consumer_lag = Gauge(
    "kafka_consumer_lag",
    "Задержка (lag) потребителя Kafka по топикам",
    ["topic", "group"]
)

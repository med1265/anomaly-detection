import faker
from datetime import datetime, timedelta
import random
from constant import Constant
def generate_datetimes(start_date: datetime, end_date: datetime, nb_logs: int) -> list[datetime]:
    """
    generer une  liste de dates entre start_date et end_date
    """
    timestamps: list[datetime] = []
    total_seconds = (end_date - start_date).total_seconds()
    for i in range(nb_logs):
        random_offset = random.random() * total_seconds
        ts = start_date + timedelta(seconds=random_offset)
        timestamps.append(ts)
    timestamps.sort()
    return timestamps
def generate_anomaly_intervals(
    number_of_anomaly_intervals: int,
    number_of_logs: int,
    max_number_of_anomalies_per_intervals: int,
    min_number_of_anomalies_per_intervals: int,
    anomaly_types: list[str],
) -> list[dict[str, int | str]]:
    """genrerer des intervalles de temps pour les anomalies"""
    intervals: list[dict[str, int | str]] = []
    for i in range(number_of_anomaly_intervals):
        start_idx = random.randint(0, max(0, number_of_logs - max_number_of_anomalies_per_intervals))
        nb_anomaly = random.randint(min_number_of_anomalies_per_intervals, max_number_of_anomalies_per_intervals)
        end_idx = min(start_idx + nb_anomaly, number_of_logs - 1)
        intervals.append({
            "start_idx": start_idx,
            "end_idx": end_idx,
            "type": random.choice(anomaly_types),
        })
    return intervals
def generate_logs_dataset(
    start_date: datetime,
    end_date: datetime,
    number_of_anomaly_intervals: int,
    number_of_logs: int,
    max_number_of_anomalies_per_intervals: int,
    min_number_of_anomalies_per_intervals: int,
    http_error_list: list[str],
    number_of_anomaly_ips: int,
    logs_dataset_file_name: str,
    http_methods: list[str],
    http_normal_codes: list[str],
    http_error_codes: dict[str, list[str]],
    api_endpoints: list[str],
):

    """generer un dataset de logs avec des anomalies"""
    fak = faker.Faker()
    anomaly_ips = [fak.ipv4() for _ in range(number_of_anomaly_ips)]
    timestamps = generate_datetimes(start_date=start_date,
                                    end_date=end_date,
                                    nb_logs=number_of_logs,
                                    )
    # build anomaly types from error codes keys plus mixed_errors
    anomaly_types = list(http_error_codes.keys())
    anomaly_types.append("mixed_errors")
    anomaly_intervals = generate_anomaly_intervals(
        number_of_anomaly_intervals=number_of_anomaly_intervals,
        number_of_logs=number_of_logs,
        max_number_of_anomalies_per_intervals=max_number_of_anomalies_per_intervals,
        min_number_of_anomalies_per_intervals=min_number_of_anomalies_per_intervals,
        anomaly_types=anomaly_types,
    )
    # flattened errors pool for mixed errors
    errors_pool = [code for codes in http_error_codes.values() for code in codes]

    with open(logs_dataset_file_name, "w") as file:
        file.write("timestamp,user_ip,method,status_code,end_point,response_time\n")

        for i in range(number_of_logs):
            ts = timestamps[i]

            user_ip = fak.ipv4()
            method = random.choice(http_methods)
            status_code = random.choice(http_normal_codes)
            end_point = random.choice(api_endpoints)
            response_time = random.choice(range(10, 300))
            for interval in anomaly_intervals:
                if interval["start_idx"] <= i <= interval["end_idx"]:
                    user_ip = random.choice(anomaly_ips)
                    if interval["type"] == "server_errors":
                        status_code = random.choice(http_error_codes.get("server_errors", []))
                    elif interval["type"] == "client_errors":
                        status_code = random.choice(http_error_codes.get("client_errors", []))
                    elif interval["type"] == "timeout_errors":
                        status_code = random.choice(http_error_codes.get("timeout_errors", []))
                        response_time = random.randint(1000, 5000)
                    else:
                        status_code = random.choice(errors_pool) if errors_pool else status_code
                        response_time = random.randint(1000, 5000)

            file.write(f"{ts},{user_ip},{method},{status_code},{end_point},{response_time}\n")
    print(f"[OK] le fichier CSV {logs_dataset_file_name} a ete genere avec {number_of_logs} logs et {number_of_anomaly_intervals} plages d'anomalies.")
if __name__ == "__main__":
    generate_logs_dataset(
        start_date=Constant.LOGS_SRATE_DATA,
        end_date=Constant.LOGS_END_DATA,
        number_of_anomaly_intervals=Constant.NUMBER_OF_ANOMALIES_INTRVALS,
        number_of_logs=Constant.NUMBER_OF_LOGS,
        max_number_of_anomalies_per_intervals=Constant.MAX_NUMBER_OF_ANOMALIES_PER_INTRVALS,
        min_number_of_anomalies_per_intervals=Constant.MIN_NUMBER_OF_ANOMALIES_PER_INTRVALS,
        http_error_list=list(),
        number_of_anomaly_ips=Constant.NUMBER_OF_ANOMALIES_IPS,
        logs_dataset_file_name=Constant.LOGS_DATA_FILE_NAME,
        http_methods=Constant.HTTP_METHODS,
        http_normal_codes=Constant.HTTP_NORMAL_CODES,
        http_error_codes=Constant.HTTP_ERROR_CODES,
        api_endpoints=Constant.API_ENDPOINTS,
    )
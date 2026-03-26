import logging
import dask.dataframe as dd
import pandas as pd

logger = logging.getLogger(__name__)

def detect_zscore(structured_logs: list[dict], threshold: float = 3.0) -> list[dict]:
    
    df = dd.from_pandas(pd.DataFrame(structured_logs), npartitions=3)
    
    # signal 1 - status code zscore
    mean = df["Status_code"].mean().compute()
    std = df["Status_code"].std().compute()
    df["zscore"] = (df["Status_code"] - mean) / std
    status_anomalies = df[df["zscore"] > threshold].compute()
    
    # signal 2 - flag CRITICAL and ERROR levels
    level_anomalies = df[df["Level"].isin(["ERROR", "CRITICAL"])].compute()
    
    # signal 3 - which service has most anomalies
    service_counts = df.groupby("Service Name").size().compute()
    service_mean = service_counts.mean()
    service_std = service_counts.std()
    service_zscore = (service_counts - service_mean) / service_std
    service_anomalies = service_counts[service_zscore > threshold]
    
    # combine signal 1 and signal 2
    combined = pd.concat([status_anomalies, level_anomalies]).drop_duplicates()
    
    logger.info(f"Status anomalies: {len(status_anomalies)}")
    logger.info(f"Level anomalies: {len(level_anomalies)}")
    logger.info(f"Anomalous services: {list(service_anomalies.index)}")
    
    return combined.to_dict(orient="records")
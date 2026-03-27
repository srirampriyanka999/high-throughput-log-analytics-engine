from pipeline.processing.parse import parse_log
import ray
import logging

logger = logging.getLogger(__name__)

def process_logs(lines: list[str]) -> list[dict]:
   
    futures = [parse_log.remote(line) for line in lines]
    
    results = ray.get(futures)
    
    structured_logs = [r for r in results if r is not None]
    
    logger.info(f"Successfully parsed {len(structured_logs)} out of {len(results)} lines")
    return structured_logs
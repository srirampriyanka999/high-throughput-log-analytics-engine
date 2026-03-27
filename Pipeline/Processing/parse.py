import ray
import logging
logger = logging.getLogger(__name__)

@ray.remote
def parse_log(line: str) -> dict | None:
    try:
        line = line.strip()
        if not line or " " not in line:
            return None
        left_part, timestamp = line.rsplit(" ", 1)
        fields = left_part.split(" ",3)
        
        return {
            "Level" : fields[0],
            "Service Name" : fields[1],
            "Status_code" : int(fields[2]),
            "message" : fields[3],
            "timestamp" : timestamp
        }

    except IndexError:
        logger.error(f"Failed to parse line: {line}")
        return None
    
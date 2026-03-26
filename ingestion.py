import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_logs(filepath: str) -> list[str]:
    try:
        lines = []
        with open(filepath, "r") as file:
            for line in file:
                lines.append(line)
            logger.info(f"Successfully ingested {len(lines)} lines from {filepath}")
        
        return lines
                
    except FileNotFoundError:
        logger.error("File does not exist")
        return []








import re

def seconds_to_padded_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = round(seconds % 60)
    
    return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"

def extract_direction(response: str) -> str | None:
    if not response:
        return None

    # Look for a single direction letter at the end (optionally wrapped in punctuation)
    match = re.search(r"\b([NSEW])\b\s*$", response.strip(), re.IGNORECASE)
    if match:
        return match.group(1).upper()

    return None


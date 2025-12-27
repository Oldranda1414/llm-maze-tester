import time
from experiment.log import log
from util import seconds_to_padded_time

tab = "   "

def log_time(indent: int, message: str, start_time: float):
    log((tab * indent) + f"Time taken for {message}: {seconds_to_padded_time(delta_t(start_time))}")

def delta_t(start_time: float) -> float:
    return time.time() - start_time


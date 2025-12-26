import time

def sleep(seconds):
    """blocks execution for exactly 'seconds'"""
    if seconds <= 0:
        return

    start = time.perf_counter()
    target = start + seconds

    while True:
        current = time.perf_counter()
        remaining = target - current

        if remaining <= 0:
            break

        # https://www.reddit.com/r/rust/comments/15ql2af/comment/jw3uyiw/
        # "windows time.sleep() has a resolution of ~15.6ms"
        # thisonly use system sleep to save cpu usage if we have a safe buffer
        if remaining > 0.02:
            # 10ms less than remaining to make sure it doesnt oversleep
            time.sleep(remaining - 0.015)
        else:
            # wait for the final milliseconds (spin sleep)
            pass

def calculate_exp(minutes, multiplier=1):
    calc_mins = min(minutes, 25)
    return (calc_mins / 25) * 1000 * multiplier

def calculate_gold(minutes, multiplier=1):
    calc_mins = min(minutes, 25)
    return (calc_mins / 25) * 250 * multiplier

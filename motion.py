import time

def EaseIn(startTime, duration, intensity = 4):
    if time.perf_counter() - startTime < 0:
        return 0
    if time.perf_counter() - startTime > duration:
        return 1
    progress = (time.perf_counter() - startTime) / duration
    return progress ** intensity

def EaseOut(startTime, duration, intensity = 4):
    if time.perf_counter() - startTime < 0:
        return 0
    if time.perf_counter() - startTime > duration:
        return 1
    progress = (time.perf_counter() - startTime) / duration
    return -((-progress + 1) ** intensity) + 1

def EaseBack(startTime, duration, intensity = 4):
    if time.perf_counter() - startTime < 0:
        return 0
    if time.perf_counter() - startTime > duration:
        return 0
    if time.perf_counter() - startTime < 1/2:
        return EaseOut(startTime, duration / 2, intensity)
    else:
        return EaseIn(startTime + duration / 2, duration / 2, intensity)
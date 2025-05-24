# neopixel_fx.py

import time
import neopixel

def wheel(pos):
    pos %= 256
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def clear(np):
    np.fill((0, 0, 0))
    np.write()

def chenillard_trail(np, trail_length=4, delay=0.05, duration=5):
    num_pixels = len(np)
    pos = 0
    direction = 1
    color_index = 0
    start = time.ticks_ms()

    while time.ticks_diff(time.ticks_ms(), start) < duration * 1000:
        clear(np)
        for t in range(trail_length):
            p = pos - t * direction
            if 0 <= p < num_pixels:
                bright = max(0.2, 1.0 - t / trail_length)
                col = wheel((color_index + t * 10) % 256)
                np[p] = tuple(int(c * bright) for c in col)
        np.write()
        time.sleep(delay)
        pos += direction
        if pos >= num_pixels - 1 or pos <= 0:
            direction *= -1
            color_index += 30
    clear(np)

def arc_en_ciel(np, delay=0.03, duration=5):
    num_pixels = len(np)
    start = time.ticks_ms()
    j = 0
    while time.ticks_diff(time.ticks_ms(), start) < duration * 1000:
        for i in range(num_pixels):
            idx = (i * 256 // num_pixels + j) % 256
            np[i] = wheel(idx)
        np.write()
        time.sleep(delay)
        j += 1
    clear(np)

def color_fixe(np, color=(0, 255, 0), duration=5):
    np.fill(color)
    np.write()
    time.sleep(duration)
    clear(np)

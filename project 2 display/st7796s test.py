from st7796s import ST7796
from machine import Pin, SPI
import time

# SPI Initialization and Pins
spi = SPI(0, baudrate=40000000, polarity=0, phase=0)
cs = Pin(5, Pin.OUT)
dc = Pin(6, Pin.OUT)
rst = Pin(7, Pin.OUT)

# Creating the screen instance
screen = ST7796(spi, cs, dc, rst)

# Using functions :

# 1. Change the rotation
for rot in range(4):
    screen.set_rotation(rot)
    time.sleep(0.5)

# 2. fill the screen in yellow
screen.fill_screen(0x001F)  # yellow

# 3. draw a cyan rectangle in the middle of screen
screen.fill_rect(60, 80, 200, 120, 0xF800)  # cyan

# 4. Draw a violet line
screen.draw_line(0, 0, screen.width - 1, screen.height - 1, 0x07E0)  # violet

# 5. draw a blue circle 
screen.draw_circle(screen.width // 2, screen.height // 2, 60, 0xFFE0)  # jaune

# 6. display a text
screen.text(10, 10, "HELLO", 0xFFFF, scale=2)

# 7. draw a few pixel
for i in range(20):
    screen.draw_pixel(10 + i, 200, 0xFFFF)

# 8. change screen rotation
screen.set_rotation(1)
screen.fill_screen(0x0000)  # noir
screen.text(10, 10, "ROTATION 1", 0xFFFF, scale=2)

# end of test
print("Toutes les fonctions ont été testées.")

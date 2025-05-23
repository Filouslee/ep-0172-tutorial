from machine import Pin,PWM
from time import sleep

sg90 = PWM(Pin(12, mode=Pin.OUT))
sg90.freq(50)
min = 1638
max = 7864
# 0.5ms/20ms = 0.025 = 2.5% duty cycle
# 2.4ms/20ms = 0.12 = 12% duty cycle

# 0.025*65535=1638
# 0.12*65535=7864

while True:
    sg90.duty_u16(min)
    sleep(1)
    sg90.duty_u16(max)
    sleep(1)
    
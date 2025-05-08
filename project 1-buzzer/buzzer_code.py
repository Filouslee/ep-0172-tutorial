from machine import Pin, PWM
import time
 

# Initialisation du bouton (BTN1 sur GP15)
button = Pin(15, Pin.IN, Pin.PULL_UP)
bouton = Pin(14, Pin.IN, Pin.PULL_UP)

# Initialisation du buzzer (GP13)
buzzer = PWM(Pin(13))
buzzer.duty_u16(0)  # On commence éteint
sg90 = PWM(Pin(12, mode=Pin.OUT))
sg90.freq(50)
min = 1638
max = 7864
while True:
    if not button.value():  # bouton appuyé = niveau bas
        buzzer.freq(1000)         # fréquence de 1kHz
        buzzer.duty_u16(2768)    # 50% de duty cycle
        time.sleep(1)
        buzzer.duty_u16(0)
        time.sleep(1)
        buzzer.freq(10000)         # fréquence de 1kHz
        buzzer.duty_u16(32768)    # 50% de duty cycle
        time.sleep(1)
        buzzer.duty_u16(0)
        time.sleep(1)
        buzzer.freq(300000)         # fréquence de 1kHz
        buzzer.duty_u16(62768)    # 50% de duty cycle
        time.sleep(1)
        buzzer.duty_u16(0)
        time.sleep(1)
    if not bouton.value():
        sg90.duty_u16(min)
        time.sleep(1)
        sg90.duty_u16(max)
        time.sleep(1)
        sg90.duty_u16(min)
        time.sleep(1)
        sg90.duty_u16(max)
        time.sleep(1)
        sg90.duty_u16(min)
        time.sleep(1)
        sg90.duty_u16(max)
        time.sleep(1)
    else:
        buzzer.duty_u16(0)        # éteindre le buzzer

    time.sleep(0.05)
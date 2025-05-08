from machine import ADC, PWM, Pin
import time

# Joystick
joy_x = ADC(26)
joy_y = ADC(27)

# Buzzer
buzzer = PWM(Pin(13))

# Bouton toggle (BTN2 sur GP14)
toggle_button = Pin(14, Pin.IN, Pin.PULL_UP)

# Variables d'état
buzzer_enabled = True
last_button_state = 1

while True:
    current_state = toggle_button.value()

    # Détection du front descendant (appui)
    if last_button_state == 1 and current_state == 0:
        buzzer_enabled = not buzzer_enabled  # Inverse l'état

    last_button_state = current_state

    if buzzer_enabled:
        x_val = joy_x.read_u16()
        y_val = joy_y.read_u16()

        freq = int(200 + (x_val / 65535) * 1800)
        duty = int((y_val / 65535) * 32768)

        buzzer.freq(freq)
        buzzer.duty_u16(duty)
    else:
        buzzer.duty_u16(0)

    time.sleep(0.05)

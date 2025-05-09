from machine import ADC, PWM, Pin, I2C
import time
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# Configuration de l'écran LCD
adr_i2c = 0x27
lcdROWS = 2
lcdCOLS = 16
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, adr_i2c, lcdROWS, lcdCOLS)

# Joystick
joy_x = ADC(26)  # axe X

# Servo sur GP12
servo = PWM(Pin(12))
servo.freq(50)

# Bouton toggle sur GP14
button = Pin(14, Pin.IN, Pin.PULL_UP)

# Variables d'état
servo_enabled = True
last_button_state = 1

# Fonction : convertit angle (0-180) en duty (PWM 1ms–2ms)
def set_angle(angle):
    duty = int(1638 + (angle / 180) * (8192 - 1638))  # entre ~1ms et ~2ms en 16 bits
    servo.duty_u16(duty)

# Boucle principale
lcd.clear()
lcd.putstr("Joystick X:")  # ligne 1

while True:
    # Toggle avec bouton
    current_state = button.value()
    if last_button_state == 1 and current_state == 0:
        servo_enabled = not servo_enabled
    last_button_state = current_state

    # Lecture de l'axe X
    x_value = joy_x.read_u16()
    angle = int((x_value / 65535) * 180)
    # Affichage sur le LCD
    lcd.move_to(0, 1)  # ligne 2
       # Efface la ligne
    lcd.move_to(0, 1)
    affichage_x = x_value // 100
    lcd.putstr("X = {:5d}".format(angle ))

    if servo_enabled:
        angle = int((x_value / 65535) * 180)  # 0 à 180°
        set_angle(angle)

    time.sleep(0.05)

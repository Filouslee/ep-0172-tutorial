import machine
import neopixel
import time
import neopixel_fx

# === CONFIGURATION ===
NUM_PIXELS = 1
PIN_LED = 12
PIN_BTN_RUN = 14
PIN_BTN_MODE = 15
DURATION = 10

np = neopixel.NeoPixel(machine.Pin(PIN_LED), NUM_PIXELS)
btn_run = machine.Pin(PIN_BTN_RUN, machine.Pin.IN, machine.Pin.PULL_UP)
btn_mode = machine.Pin(PIN_BTN_MODE, machine.Pin.IN, machine.Pin.PULL_UP)

mode = 0
NUM_MODES = 3

# === BOUCLE PRINCIPALE ===

print("Appuie sur bouton 1 pour lancer un effet, bouton 2 pour changer de mode.")
while True:
    if btn_mode.value() == 0:
        mode = (mode + 1) % NUM_MODES
        print("Mode sélectionné :", mode)
        time.sleep(0.3)

    if btn_run.value() == 0:
        print("Exécution de l'effet :", mode)
        if mode == 0:
            neopixel_fx.chenillard_trail(np, duration=DURATION)
        elif mode == 1:
            neopixel_fx.arc_en_ciel(np, duration=DURATION)
        elif mode == 2:
            neopixel_fx.color_fixe(np, color=(0, 0, 255), duration=DURATION)
        time.sleep(0.3)

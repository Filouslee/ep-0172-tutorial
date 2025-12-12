from machine import Pin, SPI
import time

# SPI matériel (Pico)
spi = SPI(0, baudrate=40000000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3), miso=None)

dc  = Pin(6, Pin.OUT)
cs  = Pin(5, Pin.OUT)
rst = Pin(7, Pin.OUT)

# Reset
rst.value(0)
time.sleep(0.05)
rst.value(1)
time.sleep(0.05)

# Fonction pour envoyer une commande
def cmd(c):
    dc.value(0)
    cs.value(0)
    spi.write(bytes([c]))
    cs.value(1)

# Fonction pour envoyer des données
def data(d):
    dc.value(1)
    cs.value(0)
    spi.write(d)
    cs.value(1)

# Initialisation *minimale* du ST7796 (mode 16 bits)
cmd(0x11)  # sleep out
time.sleep(0.120)

cmd(0x3A)  # pixel format
data(bytes([0x55]))  # 16-bit

cmd(0x29)  # display ON
time.sleep(0.020)

# Remplissage rouge
cmd(0x2A) ; data(bytes([0,0, 1,0xDF]))   # col (0 à 479)
cmd(0x2B) ; data(bytes([0,0, 1,0x3F]))   # row (0 à 319)
cmd(0x2C)

# Écrire du rouge plein écran
dc.value(1)
cs.value(0)

# Pixel rouge en 565 = 0xF800
red = bytes([0xF8, 0x00])
for _ in range(480*320):
    spi.write(red)

cs.value(1)
print("Fini.")


from machine import Pin, SPI
import time
FONT_5x8 = {
    'A': [0x7C, 0x12, 0x11, 0x12, 0x7C],
    'B': [0x7F, 0x49, 0x49, 0x49, 0x36],
    'C': [0x3E, 0x41, 0x41, 0x41, 0x22],
    'D': [0x7F, 0x41, 0x41, 0x22, 0x1C],
    'E': [0x7F, 0x49, 0x49, 0x49, 0x41],
    'F': [0x7F, 0x09, 0x09, 0x09, 0x01],
    'G': [0x3E, 0x41, 0x49, 0x49, 0x7A],
    'H': [0x7F, 0x08, 0x08, 0x08, 0x7F],
    'I': [0x00, 0x41, 0x7F, 0x41, 0x00],
    'J': [0x20, 0x40, 0x41, 0x3F, 0x01],
    'K': [0x7F, 0x08, 0x14, 0x22, 0x41],
    'L': [0x7F, 0x40, 0x40, 0x40, 0x40],
    'M': [0x7F, 0x02, 0x0C, 0x02, 0x7F],
    'N': [0x7F, 0x04, 0x08, 0x10, 0x7F],
    'O': [0x3E, 0x41, 0x41, 0x41, 0x3E],
    'P': [0x7F, 0x09, 0x09, 0x09, 0x06],
    'Q': [0x3E, 0x41, 0x51, 0x21, 0x5E],
    'R': [0x7F, 0x09, 0x19, 0x29, 0x46],
    'S': [0x46, 0x49, 0x49, 0x49, 0x31],
    'T': [0x01, 0x01, 0x7F, 0x01, 0x01],
    'U': [0x3F, 0x40, 0x40, 0x40, 0x3F],
    'V': [0x1F, 0x20, 0x40, 0x20, 0x1F],
    'W': [0x7F, 0x20, 0x18, 0x20, 0x7F],
    'X': [0x63, 0x14, 0x08, 0x14, 0x63],
    'Y': [0x03, 0x04, 0x78, 0x04, 0x03],
    'Z': [0x61, 0x51, 0x49, 0x45, 0x43],
    ' ': [0x00, 0x00, 0x00, 0x00, 0x00],
    '0': [0x3E, 0x51, 0x49, 0x45, 0x3E],
    '1': [0x00, 0x42, 0x7F, 0x40, 0x00],
    '2': [0x62, 0x51, 0x49, 0x49, 0x46],
    '3': [0x22, 0x41, 0x49, 0x49, 0x36],
    '4': [0x18, 0x14, 0x12, 0x7F, 0x10],
    '5': [0x2F, 0x49, 0x49, 0x49, 0x31],
    '6': [0x3C, 0x4A, 0x49, 0x49, 0x30],
    '7': [0x01, 0x71, 0x09, 0x05, 0x03],
    '8': [0x36, 0x49, 0x49, 0x49, 0x36],
    '9': [0x06, 0x49, 0x49, 0x29, 0x1E],
    ':': [0x00, 0x36, 0x36, 0x00, 0x00]
}

class ST7796:
    def __init__(self, spi, cs, dc, rst, width=320, height=480):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.width = width
        self.height = height

        self.cs.init(Pin.OUT, value=1)
        self.dc.init(Pin.OUT, value=0)
        self.rst.init(Pin.OUT, value=1)

        self.reset()
        self.init_display()

    def reset(self):
        self.rst.value(0)
        time.sleep_ms(50)
        self.rst.value(1)
        time.sleep_ms(120)

    def write_cmd(self, cmd):
        self.cs.value(0)
        self.dc.value(0)
        self.spi.write(bytearray([cmd]))
        self.cs.value(1)

    def write_data(self, data):
        self.cs.value(0)
        self.dc.value(1)
        self.spi.write(data if isinstance(data, (bytes, bytearray)) else bytearray([data]))
        self.cs.value(1)

    def set_window(self, x0, y0, x1, y1):
        self.write_cmd(0x2A)
        self.write_data(bytearray([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF]))
        self.write_cmd(0x2B)
        self.write_data(bytearray([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF]))
        self.write_cmd(0x2C)

    def init_display(self):
        self.write_cmd(0x11)
        time.sleep_ms(120)
        self.write_cmd(0x3A)
        self.write_data(0x55)  # 16-bit/pixel
        self.write_cmd(0x36)
        self.write_data(0x48)  # MX, BGR
        self.write_cmd(0x29)  # Display ON

    def draw_pixel(self, x, y, color):
        self.set_window(x, y, x, y)
        self.write_data(bytearray([color >> 8, color & 0xFF]))


    def fill_screen(self, color):
        self.set_window(0, 0, self.width - 1, self.height - 1)
        color_bytes = bytearray([color >> 8, color & 0xFF])
        self.cs.value(0)
        self.dc.value(1)
        for _ in range(self.width * self.height):
            self.spi.write(color_bytes)
        self.cs.value(1)

    def fill_rect(self, x, y, w, h, color):
        self.set_window(x, y, x + w - 1, y + h - 1)
        color_bytes = bytearray([color >> 8, color & 0xFF])
        self.cs.value(0)
        self.dc.value(1)
        for _ in range(w * h):
            self.spi.write(color_bytes)
        self.cs.value(1)

    def draw_line(self, x0, y0, x1, y1, color):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.draw_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def draw_circle(self, x0, y0, r, color):
        x = r
        y = 0
        err = 0
        while x >= y:
            self.draw_pixel(x0 + x, y0 + y, color)
            self.draw_pixel(x0 + y, y0 + x, color)
            self.draw_pixel(x0 - y, y0 + x, color)
            self.draw_pixel(x0 - x, y0 + y, color)
            self.draw_pixel(x0 - x, y0 - y, color)
            self.draw_pixel(x0 - y, y0 - x, color)
            self.draw_pixel(x0 + y, y0 - x, color)
            self.draw_pixel(x0 + x, y0 - y, color)
            y += 1
            if err <= 0:
                err += 2 * y + 1
            if err > 0:
                x -= 1
                err -= 2 * x + 1
    def text(self, x, y, msg, color, scale=1):
        for i, c in enumerate(msg.upper()):
            char = FONT_5x8.get(c, FONT_5x8[' '])
            for col in range(5):
                line = char[col]
                for row in range(8):
                    if line & (1 << row):
                        for dx in range(scale):
                            for dy in range(scale):
                                self.draw_pixel(
                                    x + (col * scale) + (i * 6 * scale) + dx,
                                    y + (row * scale) + dy,
                                    color
                                )
    def set_rotation(self, rotation):
        self.write_cmd(0x36)
        if rotation == 0:
            self.write_data(0x48)  # Portrait
            self.width, self.height = 320, 480
        elif rotation == 1:
            self.write_data(0x28)  # Paysage
            self.width, self.height = 480, 320
        elif rotation == 2:
            self.write_data(0x88)  # Portrait inversé
            self.width, self.height = 320, 480
        elif rotation == 3:
            self.write_data(0xE8)  # Paysage inversé
            self.width, self.height = 480, 320


install librairie please
Fx: 
| Function                                                       | Description                                                                                                |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `wheel(pos)`                                                   | Generates a color from a 256-step color wheel (used for rainbow effects). Returns an RGB tuple.            |
| `clear(np)`                                                    | Turns off all pixels (fills them with black). Requires the NeoPixel object as argument.                    |
| `chenillard_trail(np, trail_length=4, delay=0.05, duration=5)` | Creates a moving "trail" effect (like a theater chase or bouncing light). Direction reverses on each edge. |
| `arc_en_ciel(np, delay=0.03, duration=5)`                      | Smooth rainbow effect moving across the strip. Loops through the color wheel.                              |
| `color_fixe(np, color=(0, 255, 0), duration=5)`                | Displays a solid fixed color on all pixels for the given duration.                                         |
for test use code and you can change number of leds and pin of neopixel 
NUM_PIXELS = "numbers of leds"
PIN_LED = 12 for the led integred in the breadboard and you can write an other pin 
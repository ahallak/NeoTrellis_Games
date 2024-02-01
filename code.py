import board
from adafruit_neotrellis.neotrellis import NeoTrellis
from memory_match import Memory_Match
from trellis_says import Trellis_Says

BRIGHTNESS = 0.5
NUM_TRELLIS = 1

i2c_bus = board.I2C() 
trellis = NeoTrellis(i2c_bus)
trellis.brightness = BRIGHTNESS

while(True):
    game = Memory_Match(trellis, NUM_TRELLIS)
    game = Trellis_Says(trellis, NUM_TRELLIS)
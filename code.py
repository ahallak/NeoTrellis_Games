import board
from adafruit_neotrellis.neotrellis import NeoTrellis
from memory_game import Memory_Game

BRIGHTNESS = 0.5
NUM_TRELLIS = 1

i2c_bus = board.I2C() 
trellis = NeoTrellis(i2c_bus)
trellis.brightness = BRIGHTNESS

game = Memory_Game(trellis, NUM_TRELLIS)
A simple set of games for the Adafruit NeoTrellis. Runs on CircuitPython 8.2.9
I strongly recommend your NeoTrellis has some sort of enclosure for best results [https://www.adafruit.com/product/4352] or 3D print your own. In the least, you'll probably need this silicone elastomer membrane [https://www.adafruit.com/product/1611]
## Instructions
1. Get CircuitPython running on your device [https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython]
2. Copy code.py and associated other [game].py files to the root of the CIRCUITPY drive
3. Make sure the correct I2C bus is selected, depending on how your NeoTrellis is connected
4. Play away! For now, switch games by changing the line in code.py assigning the "game" variable to the right class
   i.e. game = Trellis_Says(trellis, NUM_TRELLIS)
   or   game = Memory_Game(trellis, NUM_TRELLIS)
Do not try to run both at the same time...

   Note, I haven't yet tried using multiple NeoTrellis modules with this yet.

A simple set of games for the Adafruit NeoTrellis. Runs on CircuitPython 8.2.9
I strongly recommend your NeoTrellis has some sort of enclosure for best results [https://www.adafruit.com/product/4352] or 3D print your own. In the least, you'll probably need this silicone elastomer membrane [https://www.adafruit.com/product/1611]
## Instructions
1. Get CircuitPython running on your device [https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython]
2. Copy code.py and associated other [game].py files to the root of the CIRCUITPY drive
3. Make sure the correct I2C bus is selected, depending on how your NeoTrellis is connected
4. Play away! First, the memory match game will start. In order to switch to a "Simon Says"-like game, press at least 4 buttons at the same time (maybe some more) until the NeoTrellis flickers purple. Then you are in a new game of Trellis Says! To go back, simply reboot the device.

Todo:
1. Make switching between games more graceful
2. Gather community feedback for improvement

   Note, I haven't yet tried using multiple NeoTrellis modules with this yet.

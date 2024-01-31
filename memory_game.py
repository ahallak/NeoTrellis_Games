# ahallak 2024
# v1.0
# todo: make blues and red/orange colors less similar

from adafruit_neotrellis.neotrellis import NeoTrellis
import ulab.numpy as np
import random
import time

BTNS_PER_TRELLIS = 16

class Memory_Game:
    NUM_BTNS = 16
    NUM_PAIRS = NUM_BTNS//2
    # some color definitions
    OFF = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 200, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)
    WHITE = (255,255,255)
    ORANGE = (255,75,0)
    COLORS = (WHITE, RED, GREEN, BLUE, YELLOW, CYAN, PURPLE, ORANGE)

    state = 0 # No enum class in this CircuitPython ver as of 01/2024
    pair_iters_A = 0
    event_number_A = 0
    completed_pairs = []
    reset = True
    trellis = None

    def __init__(self, trellis, num_trellis):
        print("Starting Memory Match")
        self.trellis = trellis
        self.NUM_BTNS = num_trellis * BTNS_PER_TRELLIS
        self.NUM_PAIRS = self.NUM_BTNS // 2
        self.allow_input(True)
        self.loop()

    def startup_animation(self):
        for i in range(self.NUM_BTNS):
            self.trellis.pixels[i] = self.PURPLE
            time.sleep(0.02)
        for i in range(self.NUM_BTNS):
            self.trellis.pixels[i] = self.OFF
            time.sleep(0.02)

    def gen_random_pairs(self):
        options = np.linspace(0,self.NUM_BTNS-1,self.NUM_BTNS,dtype=np.int8)
        pairs = np.zeros((self.NUM_PAIRS,2), dtype=np.int8)

        for i in range(self.NUM_PAIRS):
            # Choose options and remove from pool
            A = random.choice(options)
            options = np.delete(options, list(options).index(A))
            B = random.choice(options)
            options = np.delete(options, list(options).index(B))
            pairs[i] = (A,B)
        print(pairs)
        return pairs

    def blink_three(self, A,B, COL):
        for i in range(3):
            self.trellis.pixels[A] = COL
            self.trellis.pixels[B] = COL
            time.sleep(0.05)
            self.trellis.pixels[A] = self.OFF
            self.trellis.pixels[B] = self.OFF
            time.sleep(0.05)

    def blink_all(self, COL):
        for i in range(3):
            for j in range(self.NUM_BTNS):
                self.trellis.pixels[j] = COL
            time.sleep(0.05)
            for j in range(self.NUM_BTNS):
                self.trellis.pixels[j] = self.OFF
            time.sleep(0.05)
    
    def allow_input(self, allow):
        if(allow):
            for i in range(self.NUM_BTNS):
                self.trellis.activate_key(i, NeoTrellis.EDGE_RISING)
                self.trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
                self.trellis.callbacks[i] = self.btn_event
        else:
            for i in range(self.NUM_BTNS):
                self.trellis.activate_key(i, NeoTrellis.EDGE_RISING, enable=False)
                self.trellis.activate_key(i, NeoTrellis.EDGE_FALLING, enable=False)
                self.trellis.callbacks[i] = None

    # Button Event Handler
    def btn_event(self, event):
        if (event.edge == NeoTrellis.EDGE_RISING and not(event.number in self.completed_pairs)):
            if(self.state == 0): #First button pressed
                self.pair_iters_A = 0
                # ulab doesn't seem to have a nice way of doing this...
                for i,j in self.pairs:
                    if(event.number == i or event.number == j):
                        self.trellis.pixels[event.number] = self.COLORS[self.pair_iters_A]
                        break
                    self.pair_iters_A += 1
                self.event_number_A = event.number
                self.state = 1
            elif(self.state == 1 and (event.number != self.event_number_A)): # dont press same btn twice
                self.allow_input(False)
                pair_iters_B = 0
                for i,j in self.pairs:
                    if(event.number == i or event.number == j):
                        self.trellis.pixels[event.number] = self.COLORS[pair_iters_B]
                        break
                    pair_iters_B += 1
                print('...')
                self.allow_input(True)
                # If match is found...
                if(self.pair_iters_A == pair_iters_B):
                    print('MATCH')
                    # Prevent selecting same buttons again
                    self.completed_pairs.append(self.event_number_A)
                    self.completed_pairs.append(event.number)
                    if(len(self.completed_pairs) == self.NUM_BTNS):
                        self.blink_all(self.GREEN)
                        self.completed_pairs.clear()
                        self.reset = True
                else:  
                    time.sleep(0.25)
                    print('MISMATCH')
                    self.blink_three(self.event_number_A, event.number, self.RED)
                    self.trellis.pixels[self.event_number_A] = self.OFF
                    self.trellis.pixels[event.number] = self.OFF
                self.state = 0
    
    def loop(self):
        while True:
            if(self.reset):
                self.startup_animation()
                self.pairs = self.gen_random_pairs()
                self.reset = False
            self.trellis.sync()
            time.sleep(0.02)



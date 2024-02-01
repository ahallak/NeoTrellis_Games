# ahallak 2024
# v1.0
# todo: make blues and red/orange colors less similar
# Simple "Simon Says" type of game

from adafruit_neotrellis.neotrellis import NeoTrellis
import ulab.numpy as np
import random
import time

BTNS_PER_TRELLIS = 16

class Trellis_Says:
    NUM_BTNS = 16
    NUM_PAIRS = NUM_BTNS//2
    # some color definitions
    OFF = (0, 0, 0)
    DIM = (10,10,10)
    RED = (255, 0, 0)
    YELLOW = (255, 200, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)
    WHITE = (255,255,255)
    ORANGE = (255,75,0)
    COLORS = (WHITE, RED, GREEN, BLUE, YELLOW, CYAN, PURPLE, ORANGE)
    NUM_COLORS = len(COLORS)

    speed_time = 0.75 # start at this many seconds per color flash
    speed_min = 0.2
    speed_decr_turn = 0.05
    reset = True
    trellis = None
    grid = []
    idx_in_grid = 0

    def __init__(self, trellis, num_trellis):
        print("Starting Trellis Says")
        self.trellis = trellis
        self.NUM_BTNS = num_trellis * BTNS_PER_TRELLIS
        self.NUM_PAIRS = self.NUM_BTNS // 2
        self.allow_input(True)
        self.loop()

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

    def startup_animation(self):
        for i in range(self.NUM_BTNS):
            self.trellis.pixels[i] = self.GREEN
            time.sleep(0.02)
        for i in range(self.NUM_BTNS):
            self.trellis.pixels[i] = self.OFF
            time.sleep(0.02)

    def blink_three(self, A,B, COL):
        for i in range(3):
            self.trellis.pixels[A] = COL
            self.trellis.pixels[B] = COL
            time.sleep(0.05)
            self.trellis.pixels[A] = self.OFF
            self.trellis.pixels[B] = self.OFF
            time.sleep(0.05)

    def blink_all(self, COL):
        for i in range(2):
            for j in range(self.NUM_BTNS):
                self.trellis.pixels[j] = COL
            time.sleep(0.05)
            for j in range(self.NUM_BTNS):
                self.trellis.pixels[j] = self.OFF
            time.sleep(0.05)

    # Add one index to the grid and display
    def extend_grid(self):
        self.allow_input(False)
        self.grid.append(random.randint(0,self.NUM_BTNS-1))
        for i in self.grid:
            self.trellis.pixels[i] = self.COLORS[i % self.NUM_COLORS]
            time.sleep(self.speed_time)
            self.trellis.pixels[i] = self.OFF
            time.sleep(0.1)
        
        for i in range(self.NUM_BTNS):
            self.trellis.pixels[i] = self.DIM

        self.idx_in_grid = 0
        self.allow_input(True)
        for i in range(self.NUM_BTNS):
            self.trellis.pixels[i] = self.OFF

    def display_result(self):
        for i in range(len(self.grid)):
            if(i < self.NUM_BTNS):
                self.trellis.pixels[i % self.NUM_BTNS] = self.DIM
            elif(i < self.NUM_BTNS*2):
                self.trellis.pixels[i % self.NUM_BTNS] = self.WHITE
            elif(i < self.NUM_BTNS*3): #is anyone really getting scored this high?
                self.trellis.pixels[i % self.NUM_BTNS] = self.BLUE
            time.sleep(0.2)
        self.trellis.pixels[i % 16] = self.RED
        time.sleep(1)

    # Button Event Handler
    def btn_event(self, event):
        if (event.edge == NeoTrellis.EDGE_RISING):
            if(event.number == self.grid[self.idx_in_grid]):
                self.trellis.pixels[event.number] = self.COLORS[event.number % self.NUM_COLORS]
                self.idx_in_grid += 1
                time.sleep(0.1)
                self.trellis.pixels[event.number] = self.OFF
                # Round complete logic
                if(self.idx_in_grid == len(self.grid)):
                    self.allow_input(False)
                    for i in range(self.NUM_BTNS):
                        self.trellis.pixels[i] = self.DIM
                    for i in range(self.NUM_BTNS):
                        self.trellis.pixels[i] = self.OFF
                    time.sleep(0.1)
                    self.speed_time -= self.speed_decr_turn
                    self.extend_grid()
            else:
                self.allow_input(False)
                self.blink_all(self.RED)
                self.display_result()
                self.reset = True 
    
    def loop(self):
        while True:
            if(self.reset):
                self.startup_animation()
                self.grid = []
                self.extend_grid()
                self.reset = False
            self.trellis.sync()
            time.sleep(0.02)



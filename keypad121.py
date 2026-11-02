Python
from yolobit import *
from micropython import const
import ustruct, time
import _thread
from machine import SoftI2C, Pin

MPR121_TOUCH_STATUS = const(0x00)
MPR121_ELECTRODE_CONFIG = const(0x5E)
MPR121_SOFT_RESET = const(0x80)
MPR121_TOUCH_THRESHOLD = const(0x41)
MPR121_RELEASE_THRESHOLD = const(0x42)

class MPR121:
    KEYS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '#']

    def __init__(self, i2c=None, address=0x5A):
        if i2c == None:
            self.i2c = SoftI2C(scl=Pin(pin19.pin), sda=Pin(pin20.pin), freq=200000)
        else:
            self.i2c = i2c
        self.address = address
        self._input = ''
        self.sound = True 
        self._current_key = -1
        self._need_beep = False 
        self._register8(MPR121_SOFT_RESET, 0x63)
        time.sleep_ms(10)
        self._register8(MPR121_ELECTRODE_CONFIG, 0x00)
        self.set_thresholds(40, 20)
        self._register8(0x5C, 0x10)
        self._register8(0x5D, 0x20)
        self._register8(MPR121_ELECTRODE_CONFIG, 0x8F)
        _thread.start_new_thread(self.run, ())

    def _register8(self, register, value=None):
        try:
            if value is None:
                return self.i2c.readfrom_mem(self.address, register, 1)[0]
            self.i2c.writeto_mem(self.address, register, bytearray([value]))
        except OSError:
            return 0

    def _register16(self, register, value=None):
        try:
            if value is None:
                data = self.i2c.readfrom_mem(self.address, register, 2)
                return ustruct.unpack("<H", data)[0]
            self.i2c.writeto_mem(self.address, register, ustruct.pack("<H", value))
        except OSError:
            return 0

    def set_thresholds(self, touch, release):
        for i in range(12):
            self._register8(MPR121_TOUCH_THRESHOLD + i * 2, touch)
            self._register8(MPR121_RELEASE_THRESHOLD + i * 2, release)

    def touched(self):
        try:
            return self._register16(MPR121_TOUCH_STATUS)
        except OSError:
            return 0
  
    def is_touched(self, electrode):
        z = int(electrode)
        if z == 10: z = 8
        elif z == 11: z = 11
        else:
            y = 3-(z//3)
            if z % 3 == 0: y = y + 1
            x = z - (3-y)*3-1
            z = 4*x + y
        t = self.touched()
        return (t & (1 << z)) != 0
    
    def run(self):
        last_pressed = []
        while True:
            try:
                current_pressed = []
                for i in range(len(self.KEYS)):
                    if self.is_touched(i):
                        current_pressed.append(i)
                        if i not in last_pressed:
                            if len(self._input) < 15:
                                self._input += self.KEYS[i]
                                self._need_beep = True 
                last_pressed = current_pressed
                time.sleep_ms(40)
            except OSError:
                time.sleep_ms(100)
    
    def _check_beep(self):
        if self._need_beep:
            self._need_beep = False
            if self.sound:
                try:
                    import music
                    music.play(['G5:0.3'], wait=True)
                except:
                    pass

    def clear(self):
        self._input = ''

    def read(self):
        self._check_beep()
        return self._input

# Khởi tạo sẵn đối tượng keypad để Blockly gọi
keypad = MPR121()
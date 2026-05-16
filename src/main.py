import utime, json
from UpyIrTx import UpyIrTx
from machine import Pin

class IRUART:
    def __init__(
        self, 
        uart            = 0, 
        tx              = 16, 
        rx              = 17, 
        irConfigFile    = "./config/irConfig.json"
    ):
        txPin           = Pin(tx, Pin.OUT)
        self.tx         = UpyIrTx(uart, txPin)
        with open(irConfigFile, "r", encoding = "UTF-8") as irFile:
            self.irData = json.loads(irFile.read())
    
    def send_data(self, pinID):
        cmd             = self.irData.get(pinID, "0,0")
        sendData        = [int(i) for i in cmd.split(",")]
        self.tx.send(sendData)


class Button(Pin):
    def __init__(self, pinID, mode, setInterrupt = True):
        self.pinID      = pinID
        super().__init__(self.pinID, Pin.IN, mode)
        if setInterrupt:
            self.irq(trigger=Pin.IRQ_FALLING, handler=self.handler)
    
    def handler(self, pin):
        print(f"GP{self.pinID}")

class RemotePico:
    def __init__(self): 
        self.buttonPin          = []
        self.irUART             = IRUART()
        self.onboardLED         = Pin(25, Pin.OUT)

        for p in [0, 4, 7, 8, 11, 15, 19]:
            btn                 = Button(p, Pin.PULL_UP)
            self.buttonPin.append(btn)
        
        self.led_blinking(3)
    
    def led_blinking(self, count, t = 0.1):
        for i in range(count):
            self.onboardLED.value(1)
            utime.sleep(t)
            self.onboardLED.value(0)
            utime.sleep(t)

    def loop(self):
        while True:
            for btn in self.buttonPin:
                if btn.value() == 0:
                    self.onboardLED.value(1)
                    self.irUART.send_data(btn.pinID)
                    self.onboardLED.value(0)
                    utime.sleep_ms(300)

if __name__ == "__main__":
    rp = RemotePico()
    rp.loop()

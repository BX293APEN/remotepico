from machine import (
    Pin, 
    UART
)



class Button(Pin):
    def __init__(self, pinID, mode, setInterrupt = True):
        self.pinID = pinID
        self.pin = super().__init__(self.pinID, Pin.IN, mode)
        if setInterrupt:
            self.irq(trigger=Pin.IRQ_FALLING, handler=self.handler)
    
    def handler(self, pin):
        print("IRQ from:", self.pinID)

class RemotePico:
    def __init__(self): 
        self.picoPinList = []
        for p in [0, 4, 7, 8, 11, 15, 19]:
            btn = Button(p, Pin.PULL_UP)
            self.picoPinList.append(btn)
    
    def run(self):
        while True:
            pass

if __name__ == "__main__":
    rp = RemotePico()
    rp.run()

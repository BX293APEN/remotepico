from machine import (
    Pin, 
    UART
)

def handler(pin):
    print("IRQ from:", pin.pinID)

class Button(Pin):
    def __init__(self, pin, mode):
        self.pinID = pin
        super().__init__(self.pinID, Pin.IN, mode)
    

class RemotePico:
    def __init__(self): 
        self.picoPinList = []
        for p in [0, 4, 7, 8, 11, 15, 19]:
            btn = Button(p, Pin.PULL_UP)
            btn.irq(trigger=Pin.IRQ_FALLING, handler=handler)
            self.picoPinList.append(btn)
    
    def run(self):
        while True:
            pass

if __name__ == "__main__":
    rp = RemotePico()
    rp.run()

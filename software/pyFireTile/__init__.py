import serial,sys

class FireTile(object):
    """
    Generic Fire Tile, supports the basic FireTile UART protocol (v1):

    FireTile UART protocol is an ASCII formatted serial communications protocol. 
    Standard speed is 19200 baud.
    """
    def __init__(self, port, speed=19200):
        self.port = port
        self.speed = speed
        self.ser = None
        
    def open(self,loopback = False):
        if not loopback:
            self.ser = serial.Serial(self.port, self.speed)
        else:
            self.ser = sys.stdout 
    def setPixel(self, addr, color):
        send_str = ":{0:0x}{1:02x}{2:02x}{3:02x}\n".format(addr, color[0], color[1],color[2])
    #   print(send_str)
    #   print self.ser.isOpen()
        self.ser.write(send_str)

    def update(self):
        self.ser.write(":u\n")
        self.ser.flush()
    def clear(self, tile_size=9):
        for i in range(tile_size):
            self.setPixel(i, [0,0,0])

    def close(self):
        self.ser.close()

class FireTile3x3(FireTile):
    """
    Supports specific mapping for a 3x3 tile_size
    """
    def setCoordinate(self, coordinates, color):
        """
        Set coordinate to color

        @var coordinate is a tuple (x, y) where x and y are integers in the range [0, 2]
        @var color is an array of 3 colors [r,g,b]
        """
        addr = coordinates[0] + coordinates[1]*3
        self.setPixel(addr, color)

    def setFrame(self, frame):
        """
        Set frame

        @var frame is a 3x3x3 array (grid with the rgb colors in each spot)
        """
        for x in range(3):
            for y in range(3):
                self.setCoordinate((x,y),frame[x][y])

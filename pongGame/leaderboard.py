import json
import requests
import time, sys
import smbus
import RPi.GPIO as GPIO

class LCD:
    def __init__(self):
        if GPIO.RPI_REVISION == 2 or GPIO.RPI_REVISION == 3:
            self.bus = smbus.SMBus(1)
        else:
            self.bus = smbus.SMBus(0)
        self.DISPLAY_RGB_ADDR = 0x62
        self.DISPLAY_TEXT_ADDR = 0x3e
    
    def setRGB(self, r, g, b):
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR,0,0)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR,1,0)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR,0x08,0xaa)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR,4,r)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR,3,g)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR,2,b)
        
    def textCommand(self, cmd):
        self.bus.write_byte_data(self.DISPLAY_TEXT_ADDR,0x80,cmd)
        
    def setText(self, text):
        self.textCommand(0x01) # clear display
        time.sleep(.05)
        self.textCommand(0x08 | 0x04) # display on, no cursor
        self.textCommand(0x28) # 2 lines
        time.sleep(.05)
        count = 0
        row = 0
        for c in text:
            if c == '\n' or count == 16:
                count = 0
                row += 1
                if row == 2:
                    break
                self.textCommand(0xc0)
                if c == '\n':
                    continue
            count += 1
            self.bus.write_byte_data(self.DISPLAY_TEXT_ADDR,0x40,ord(c))
            
    def setText_norefresh(self, text):
        self.textCommand(0x02) # return home
        time.sleep(.05)
        self.textCommand(0x08 | 0x04) # display on, no cursor
        self.textCommand(0x28) # 2 lines
        time.sleep(.05)
        count = 0
        row = 0
        while len(text) < 32: #clears the rest of the screen
            text += ' '
        for c in text:
            if c == '\n' or count == 16:
                count = 0
                row += 1
                if row == 2:
                    break
                self.textCommand(0xc0)
                if c == '\n':
                    continue
            count += 1
            self.bus.write_byte_data(self.DISPLAY_TEXT_ADDR,0x40,ord(c))
            
    def create_char(self, location, pattern):
        """
        Writes a bit pattern to LCD CGRAM

        Arguments:
        location -- integer, one of 8 slots (0-7)
        pattern -- byte array containing the bit pattern, like as found at
                   https://omerk.github.io/lcdchargen/
        """
        location &= 0x07 # Make sure location is 0-7
        textCommand(0x40 | (location << 3))
        self.bus.write_i2c_block_data(self.DISPLAY_TEXT_ADDR, 0x40, pattern)
        
    def displayLeaderboard(self):
        self.setText("Leaderboard\nLine 2")
        self.setRGB(0, 255, 0)
        while True:
            board = getScoreboard()
            for i in range(0, 5):
                topElem = ""
                bottomElem = ""
                if (i == 0):
                    topElem = "Leaderboard:"
                    bottomElem = "1. {} - {}".format(board[0][0], board[0][1]);
                elif (i == 4):
                    topElem =  "5. {} - {}".format(board[4][0], board[4][1]);
                    bottomElem = "Leaderboard:"
                else:
                    topElem = "{}. {} - {}".format(i+1, board[i-1][0], board[i-1][1])
                    bottomElem = "{}. {} - {}".format(i+2, board[i][0], board[i][1])
                text = "{}\n{}".format(topElem, bottomElem)
                self.setText(text)
                time.sleep(2)
                

def postScore(initials, score):
	postReq = requests.post('localhost:8000/scoreboard/post/' + initials + '/' + str(score))
	
def getScoreboard():
	getReq = requests.get('http://localhost:8000/scoreboard/get/')
	arr = json.loads(getReq.text)
	#print(arr)
	ret = []
	for item in arr:
		s = item.split('-')
		ret.append((s[0], s[1]))
	return ret
	
if __name__ == '__main__':
    lcd = LCD()
    lcd.displayLeaderboard()
    #print(getScoreboard())

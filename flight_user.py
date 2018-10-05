import serial,time,struct


class MultiWii:
      ATTITUDE = 108
      

      def __init__(self,serPort):
            
          self.attitude = {'angx':0,'angy':0,'heading':0}
          self.ser = serial.Serial()
          self.ser.port = serPort
          self.ser.baudrate = 115200
          self.ser.bytesize = serial.EIGHTBITS
          self.ser.parity = serial.PARITY_NONE
          self.ser.stopbits = serial.STOPBITS_ONE
          self.ser.timeout = 0
          self.ser.xonxoff = False
          self.ser.rtscts = False
          self.ser.dsrdtr = False
          self.ser.writeTimeout = 2
          self.PRINT = 1

          """Time to wait until the board becomes operational"""
          wakeup = 2
          
          try:
            self.ser.open()
            if self.PRINT:
                print "Waking up board on "+self.ser.port+"..."
            for i in range(1,wakeup):
                if self.PRINT:
                    print wakeup-i
                    time.sleep(1)
                else:
                    time.sleep(1)
          except Exception, error:
            print "\n\nError opening "+self.ser.port+" port.\n"+str(error)+"\n\n"


      """Function for sending a command to the board"""
      
      def sendCMD(self, data_length, code, data):
        checksum = 0
        total_data = ['$', 'M', '<', data_length, code] + data
        for i in struct.pack('<2B%dH' % len(data), *total_data[3:len(total_data)]):
            checksum = checksum ^ ord(i)
        total_data.append(checksum)
        try:
            b = None
            b = self.ser.write(struct.pack('<3c2B%dHB' % len(data), *total_data))
        except Exception, error:
            #print "\n\nError in sendCMD."
            #print "("+str(error)+")\n\n"
            pass
      

      """Function to receive a data packet from the board"""
     
      def getData(self, cmd):
        try:
            start = time.time()
            self.sendCMD(0,cmd,[])
            while True:
                header = self.ser.read()
                if header == '$':
                    header = header+self.ser.read(2)
                    break
            datalength = struct.unpack('<b', self.ser.read())[0]
            code = struct.unpack('<b', self.ser.read())
            data = self.ser.read(datalength)
            temp = struct.unpack('<'+'h'*(datalength/2),data)
            self.ser.flushInput()
            self.ser.flushOutput()
            elapsed = time.time() - start
            if cmd == MultiWii.ATTITUDE:
                self.attitude['angx']=float(temp[0]/10.0)
                self.attitude['angy']=float(temp[1]/10.0)
                self.attitude['heading']=float(temp[2])
                return self.attitude 

        except Exception, error:
            #print error
            pass




serialPort = "/dev/ttyUSB0"
board = MultiWii(serialPort)
while True:
		print board.getData(MultiWii.ATTITUDE)
                

import serial,time,struct

class MultiWii:
    
      ATTITUDE = 108
      WAVEPOINT_SET=209
      WAVEPOINT=118 
      SET_RAW_RC=200   

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
      
      def sendREQ(self, data_length, code, data):
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
      
      def sendCMD(self,data_length,code,data):
          checksum = 0 
          if(code==MultiWii.WAVEPOINT_SET):
              #data=[ 16 , -40.54402799999 , 77.19129459999999 , 233, 120, 0 , 0 ]
              total_data = ['$', 'M', '<',data_length, code] + data  
              for i in struct.pack('<2BBfffhHB', *total_data[3:len(total_data)]):
                   checksum = checksum ^ ord(i)    
          
              total_data.append(checksum)
              try:
               b = None
               b = self.ser.write(struct.pack('<3c2BBfffhHBB', *total_data))
              except Exception, error:
                print "\n\nError in sendCMD."
                print "("+str(error)+")\n\n"
                pass

          elif(code==MultiWii.SET_RAW_RC): 
              total_data = ['$', 'M', '<',data_length, code] + data 
              for i in struct.pack('<2BHHHHHHHH' , *total_data[3:len(total_data)]):
                   checksum = checksum ^ ord(i)          


              total_data.append(checksum)
              try:
               b = None
               b = self.ser.write(struct.pack('<3c2BHHHHHHHHB', *total_data))
              except Exception, error:
                print "\n\nError in sendCMD."
                print "("+str(error)+")\n\n"
                pass

      """Function to receive a data packet from the board"""
     
      def getData(self, cmd):
        try:
            start = time.time()
            self.sendREQ(0,cmd,[])
            while True:
                header = self.ser.read()
                if header == '$':
                    header = header+self.ser.read(2)
                    break
            datalength = struct.unpack('<b', self.ser.read())[0]
            # print datalength
            code = struct.unpack('<b', self.ser.read())
            data = self.ser.read(datalength)
            if cmd == MultiWii.ATTITUDE:
                temp = struct.unpack('<'+'h'*(datalength/2),data)
                print temp
                self.ser.flushInput()
                self.ser.flushOutput()
                elapsed = time.time() - start
                #self.attitude['angx']=float(temp[0]/10.0)
                #self.attitude['angy']=float(temp[1]/10.0)
                #self.attitude['heading']=float(temp[2])
                #return self.attitude 

            elif cmd == MultiWii.WAVEPOINT:
                temp = struct.unpack('<BfffhHB',data)
                print temp
                self.ser.flushInput()
                self.ser.flushOutput()
                elapsed = time.time() - start
              

        
        except Exception, error:
            print error
            pass




serialPort = "/dev/ttyUSB0"
board = MultiWii(serialPort)
time.sleep(2)


#arming roll,pitch,yaw,throttle,AUX1,AUX2,AUX3,AUX4
board.sendCMD(16,MultiWii.SET_RAW_RC,[1500,1500,1000,1500,0,0,0,0])   


#Wavepoint_set
board.sendCMD(18,MultiWii.WAVEPOINT_SET,[ 16 , -30.54402799999 , 77.19129459999999 , 233, 120, 0 , 0])    
while True:
  board.getData(MultiWii.WAVEPOINT)             

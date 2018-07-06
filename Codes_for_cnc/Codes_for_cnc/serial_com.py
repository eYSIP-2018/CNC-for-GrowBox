import serial

flag = False
ser = serial.Serial('/dev/ttyACM1',9600)

while True :
        variable = input ("enter any sting  ")
        ser.write(variable.encode('utf-8'))
       
        
        
                
	




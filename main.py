import serial
import time
import math
ser = serial.Serial('COM5', 9600, timeout=0)
cm = 0
angle = 0
i = 1
flag = 0
# f = open("base.txt", "a")
# f.write("angle;")
# f.write("len;" + "\n")
# f.close()
while(1):
    time.sleep(2)
    for i in range (1, 2049):
        ser.write(str(i).encode('utf-8'))
        #ser.write(i)
        #time.sleep(0.04)
        flag = 0
        while(flag == 0):
            if (ser.in_waiting > 0):
                serialString = ser.readline()
                print(serialString)
                flag = 1

    # ser.write(b'1')  # write a string
    # time.sleep(1)
    # if(ser.in_waiting > 0):
    #     serialString = ser.readline()
    #     cm = int(float(serialString))
    # ser.write(b'0')  # write a string
    # time.sleep(1)
    # if(ser.in_waiting > 0):
    #     serialString = ser.readline()
    #     angle = int(float(serialString))
    #     sinus = math.radians(angle)
    #     sinus = math.sin(angle)
    #     print(sinus)
    # # f = open("base.txt", "a")
    # # f.write(str(angle) + ";")
    # # f.write(str(cm) + ";" + "\n")
    # # f.close()
    # time.sleep(0.15)


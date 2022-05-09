import serial
import time
import matplotlib.pyplot as plt
# import math
import numpy as np

# create 1024 digit arrays
MAXSIZE = 1025
angles = np.empty(MAXSIZE)
cms = np.empty(MAXSIZE)
ser = serial.Serial('COM5', 9600, timeout=0)
cm = 0
angle = 0
anglePerStep = 0.176  # one step in stepper motor at full step mode is 0.176°
i = 1
flag = 0

# begin database
f = open("base.txt", "w")
f.write("angle;")
f.write("len" + "\n")
f.close()

time.sleep(2)
for i in range(1, 1025):
    # print(round(np.sin(np.radians(30)), 1))
    ser.write("1".encode("utf-8"))  # write 1 to arduino to do 1 step
    angle = anglePerStep * i        # calculate angle
    flag = 0
    while flag == 0:  # wait for answer
        if ser.in_waiting > 0:
            serialString = ser.readline()  # receive len from  arduino's echo
            print(serialString)
            cm = int(serialString)
            flag = 1                       # update flag after we got everything
    # if len is bigger than 200 cm we ignore it
    if cm > 200:
        cm = 0
    angles[i] = angle   # write data into array
    cms[i] = cm         # same

    # write data into database file
    f = open("base.txt", "a")
    angle = str(angle)
    f.write(angle + ";")
    f.write(str(cm) + "\n")
    f.close()
ser.write("0".encode("utf-8"))  # write 0 to rotate 180° back

# build a graph from 1024 lines (1024 steps is 180°)
for i in range(1, 1025):
    y = cms[i] * np.sin(np.radians(angles[i])) + 200  # y = len * sin(α) + 200
    x = 200 - cms[i] * np.cos(np.radians(angles[i]))  # x = 200 - len * cos(α)
    x1, y1 = [200, x], [200, y]
    plt.plot(x1, y1, marker='o')
plt.show()

import serial
import time
import matplotlib.pyplot as plt
import numpy as np

# create 1024 digit arrays
angles = np.empty(1025)   # create empty arrays with 1025 len
cms = np.empty(1025)      # create empty arrays with 1025 len

angles_and_distance = {}    # create dictionary

# init serial
ser = serial.Serial('COM4', 115200, timeout=0)
# time.sleep(10)
# declare variables
cm, angle, i, flag = 0, 0, 0, 0
anglePerStep = 0.176 * 32  # one step in stepper motor at full step mode is 0.176°

# begin database
f = open("base.txt", "w")
f.write("angle;")
f.write("len" + "\n")
f.close()

# time.sleep(2)
for i in range(1, 33):
    ser.write("1\n".encode("utf-8"))  # write 1 to arduino to do 1 step
    time.sleep(0.18)
    angle = anglePerStep * i        # calculate angle
    flag = 0
    while flag == 0:  # wait for answer before continuing
        if ser.in_waiting > 0:
            serialString = ser.readline()  # receive len from  arduino's echo
            print(serialString)
            cm = int(serialString)
            flag = 1                       # update flag after we got everything
    # if len is bigger than 200 cm we ignore it
    if cm > 200:
        cm = 199
    angles[i] = angle   # write data into array
    cms[i] = cm         # same

    # write data into database file
    f = open("base.txt", "a")
    angle = str(angle)
    f.write(angle + ";")
    f.write(str(cm) + "\n")
    f.close()
    step = float(angle) / 0.176
    angles_and_distance[round(step)] = int(cm)
ser.write("0".encode("utf-8"))  # write 0 to rotate 180° back

# build a graph from 1024 lines (1024 steps is 180°)
for i in range(1, 33):
    y = cms[i] * np.sin(np.radians(angles[i])) + 200  # y = len * sin(α) + 200
    x = 200 - cms[i] * np.cos(np.radians(angles[i]))  # x = 200 - len * cos(α)
    x1, y1 = [200, x], [200, y]
    plt.plot(x1, y1, marker='o')
plt.show()
if angles_and_distance[512] > 5:
    print("go")

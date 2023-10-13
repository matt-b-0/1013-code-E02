#main function file that contains all of the code for a water tank monitoring system
#Team: E02
#Members: Sam Potter, Matthew Brasacchio, Noah Clark, Kush Berry, Yousouf Palitanawala
#last edited 15/09/2023
#version 1.2.7

# Setup
import time 
import random
import matplotlib.pyplot as plt
from pymata4 import pymata4
import math

# Defined Variables
pin = '1234'
pinCanTry = True
pinLockout = 130
maxHeight = 20
maxVolume = 10000
board = pymata4.Pymata4()
board.set_sampling_interval(1000)

responceReg = ['LED_1_red','LED_2_red','LED_3_blue','LED_4_blue','LED_5_yellow','LED_6_RED','Buzzer_1','Buzzer_2']
responceReg = [0,0,0,0,0,0,0,0]
                               
height = 0
volumeGraph = []
timeGraph = []
rateChange = []
rateOfChangeCutoff = 2000 #mL/s
baseSurfaceArea = 24*24
timeAdd = True
changeCount = 0

#definition of things for the thermistor
thermistor = 0
R1 = 10000
c1 = 1.009249522e-03
c2 = 2.378405444e-04
c3 = 2.019202697e-07
temperatures = []
times = []
board.set_pin_mode_analog_input(0) #thermistor pin
originalTime = 0
T=0

serLED = 9
srclkLED = 10
rclkLED = 11
buzzer1= 12
buzzer2 = 13
buzzer3 = 14
board.set_pin_mode_digital_output(serLED)
board.set_pin_mode_digital_output(srclkLED)
board.set_pin_mode_digital_output(rclkLED)
board.set_pin_mode_digital_output(buzzer1)
board.set_pin_mode_digital_output(buzzer2)
board.set_pin_mode_digital_output(buzzer3)
pushButton = 15
board.set_pin_mode_digital_input(pushButton)





# polling_loop function calls various other functions, every 1.5 seconds
# INPUTS: None (timeAdd as a global variable)
# OUTPUTS: None
# Created by Matt
# Date created: 05/09/2023
def polling_loop():
    global timeAdd
    
    startTime = time.time()
    ultrasonic_ping()
    thermistor_read()
    print(f"Volume = {volume}mL")#print(volume) mL

    data_clean()
    if timeAdd:
        reactions()
    time.sleep(0.8)
    endTime = time.time()
    runTime = endTime - startTime
    if timeAdd:
        timeGraph.append(time.time())
    print(f'Runtime = {runTime}')
    
#thermistor read and record
#inputs: None()
def thermistor_read():
    global originalTime, c1, c2, c3, R1, temperatures, times, T
    board.set_pin_mode_analog_input(5)
    v0 = board.analog_read(5)[0]

    if v0 > 0:
        R2 = R1 * (1023.0 / float(v0) - 1.0)
        logR2 = math.log(R2)
        T = (1.0 / (c1 + c2 * logR2 + c3 * logR2 * logR2 * logR2))
        T = T - 273.15
        print(T)
        if T > 0 or T < 100:
            temperatures.append(T)
            times.append(time.time() - originalTime)
        if len(temperatures) > 1:
            change = T - temperatures[-2]
            print(change)
            #if change > 0.5 or change < -0.5:
            #else:
            # Performing basic filtering

# reactions function checks for volume level, turns on necessary warning LED and print statements of pump status
# INPUTS: NONE (volume, maxVolume errorLights, baseSurfaceArea as global variables)
# OUTPUTS: NONE
# Created by Matt
# Date created: 05/09/2023
def reactions():
    global maxHeight, height, board, volume, maxVolume, responceReg, board, changeCount
    #need to turn ser off to not visibly make adjustments
    
    for i in range(8):
        responceReg[i] = 0 #reset shift reg
        board.digital_pin_write(buzzer3, 0)
    #M2 responce LED's
    if (volume/maxVolume)<0.1:
        responceReg[0] = 1
        responceReg[1] = 1
        print("Input pump on at HIGH speed")
    elif 0.1<(volume/maxVolume)<0.25:
        responceReg[0] = 1
        board.digital_pin_write(buzzer3, 1)
        print("Input pump on at LOW speed")
    elif 0.75<(volume/maxVolume)<0.9:
        responceReg[2] = 1
        print("Output pump on at Low speed")
    elif 0.9<(volume/maxVolume)<1:
        responceReg[2] = 1
        responceReg[3] = 1
        print("Output pump on at High speed")
    elif (volume/maxVolume)>1:
        print(f"Volume is beyond max volume {maxVolume} mL")
    
    if T>25:
        responceReg[4] = 1
    
    if (volume/maxVolume)>0.75 or (volume/maxVolume)<0.25:
        if changeCount >=5:
            board.digital_pin_write(buzzer1, 1)
        else:
            changeCount +=1
    else:
        changeCount = 0
        board.digital_pin_write(buzzer1, 0)

    write()


#helper fucntion for the shift reg to write all the pins thagt are meant to turn on after a responce
def write():
    global responceReg, board
    for i in responceReg:
        board.digital_pin_write(serLED,i)
        board.digital_pin_write(srclkLED,1)
        time.sleep(0.001)
        board.digital_pin_write(srclkLED,0)
    board.digital_pin_write(rclkLED, 1)
    time.sleep(0.001)
    board.digital_pin_write(rclkLED,0)
    time.sleep(0.001)

def reset():
    global board, serLED, srclkLED, rclkLED
    board.digital_pin_write(serLED, 0)
    for i in range(8):
        board.digital_pin_write(srclkLED, 1)
        time.sleep(0.001)
        board.digital_pin_write(srclkLED, 0)
    board.digital_pin_write(rclkLED, 1)
    time.sleep(0.001)
    board.digital_pin_write(rclkLED, 0)


# data_clean function checks to see if last ultrasonic read involves a change of more than the rate-of-change-cutoff and 
# disregards it if it is
# INPUTS: None (volume, volumeGraph, timeGraph, rateOfChangeCutoff, timeAdd)
# OUTPUTS: NONE (appended volumeGraph as a global variable)
# Created by Matt
# Date created: 05/09/2023
def data_clean():
    global volume, volumeGraph, timeGraph, rateOfChangeCutoff, timeAdd, board

    if len(timeGraph) > 1:
        if abs(volumeGraph[-1] - volume) < rateOfChangeCutoff and volume>=0:
            volumeGraph.append(volume)
            timeAdd = True
            board.digital_pin_write(buzzer2, 0)
        else:
            board.digital_pin_write(buzzer2, 1)
            print("Error in rate of change: data removed")
            timeAdd = False
    else:
        volumeGraph.append(volume)



# ultrasonic_ping function uses the ultrasonic sensor to determine the distance from sensor to the water, 
# and then determines the distance from this
# INPUTS: None
# OUTPUTS: None (volume and height of water as global variables)
# Created by Matt
# Date created: 05/09/2023
def ultrasonic_ping():
    global board, volume, height
    calcHeight = 22
    board.set_pin_mode_sonar(16,17,timeout=200000)
    measure = board.sonar_read(16)
    height = calcHeight - measure[0]
    print(f'Height = {height}cm')
    volume = height * baseSurfaceArea #gets volume of water in ml



# graph_data_volume function plots volume against time for the last 20 data points
# INPUTS: None
# OUTPUTS: None (graph of data displayed)
# Created by Matt
# Date created: 05/09/2023
def graph_data_volume():
    global timeGraph, volumeGraph
    plt.figure(1)
    plt.title("Volume against Time")
    yGraph = [timeGraph[_]-timeGraph[-20] for _ in range(-20,0)]
    plt.plot(yGraph, [volumeGraph[_] for _ in range(-20,0)], linestyle = "--", marker = "o")
    plt.xlabel("Time (s)")
    plt.ylabel("Volume (mL)")
    plt.show()
    



# main_menu functions lets user choose a mode of operation
# INPUTS: None
# OUTPUTS: None
# Created by Matt
# Date created: 05/09/2023
def main_menu():
    print("Choose a mode of operation")
    try:
        print("====================================\nWelcome to the water tank system main menu.\n====================================\nOptions for menus are listed below\n(1): Maintenance \n(2). Analysis. \n(3). Normal:\n(ctr+c) Exit program\n====================================")
        while True:
            userChoice = input("Please select an option from above by entering a number: ")
            if userChoice == '1':
                print("Maintenance mode")
                # Call the maintenance function
                maintenance()
            elif userChoice == '2':
                print("Data Analysis mode")
                # Call analysis function
                data_observation()
            elif userChoice == '3':
                print("Normal operation")
                # Call normal operation function
                normal_operation()
            else:
                print("Invalid input")
    except KeyboardInterrupt:
        exit(0)



# When normal mode is chosen, run the polling loop until keyboard is interrupted
# INPUTS: None
# OUTPUTS: None (volume and height of water as global variables)
# Created by Matt
# Date created: 05/09/2023
def normal_operation():
    global volumeGraph, timeGraph, originalTime
    print("====================================\nYou have entered Normal Operation Mode.\n====================================\ninput (ctrl + c) to return to the main menu\n====================================")
    try:
        while True:
            originalTime = time.time()
            polling_loop()
    except KeyboardInterrupt:
        reset()
        board.digital_pin_write(buzzer1, 0)
        board.digital_pin_write(buzzer2, 0)
        board.digital_pin_write(buzzer3, 0)

        
        main_menu()



# When data observation mode is chosen, the available data is graphed
# INPUTS: None (results as a global variable)
# OUTPUTS: None 
# Created by Matt
# Date created: 05/09/2023
def data_observation():
    global volumeGraph, timeGraph
    print("====================================\nYou have entered Data Observation Mode.\n====================================\ninput (ctrl + c) to return to the main menu\n====================================")
    
    try:
        while True:
            print("Please select an option from the following to observe data\n(1) Create a graph of 20 data points of volume collected from normal mode\n(2) Display the last recorded volume\n(3) Create a graph of 20 data points of volume collected from normal mode\n(2) Display the last recorded temperature\n(ctrl + c) Main Menu")
            analysisOption = input("Please provide input: ")
            if analysisOption == '1':
                if len(volumeGraph) >20:
                    graph_data_volume()
                else:
                    print("Not enough stored data")
            elif analysisOption == '2':
                #have a section for the 7 seg
                if len(volumeGraph)>0:
                    outputMessage = str(round(volumeGraph[-1]))
                    seven_seg(outputMessage)
                else:
                    print("Must record some data first")
            elif analysisOption == '3':
                #creates graph for temperature
                if len(times)>20:
                    graph_data_temp
            else:
                print("Invalid option")

    except KeyboardInterrupt:
        digits = [7, 9, 10, 13] # Digits 1-4
        for digit in digits:
            board.digital_write(digit, 1)
        main_menu()


def graph_data_temp():
    global times, temperatures
    plt.figure(2)
    plt.title("Temperature against Time")
    yGraph = [times[_]-times[-20] for _ in range(-20,0)]
    plt.plot(yGraph, [temperatures[_] for _ in range(-20,0)], linestyle = "--", marker = "o")
    plt.xlabel("Time (s)")
    plt.ylabel("Volume (mL)")
    plt.show()


# When maintenance mode is chosen, asks user for PIN, if correct sends to settings adjustments, if incorrect returns to home screen
# INPUTS: None (pin,pinCanTry and pinLockout as global variables)
# OUTPUTS: None 
# Created by Matt
# Date created: 05/09/2023
def maintenance():
    global pin, pinCanTry, pinLockout
    attempts = 3
    if not pinCanTry:
        if (time.time()-pinLockout) >120:
            pinCanTry = True 
    if pinCanTry:
        try:
            while attempts>0:
                print(f'====================================\nYou have entered maintenance mode.\n====================================\nPlease enter the correct {len(pin)} digit pin to make adjustments\nYou have {attempts} attempts left.\nEnter (ctrl + c) to return to main menu\n====================================')
                #may have to change if we want to make a numeric key, i have it as a string at the top
                attempt = input('Enter pin: ')
                if attempt == pin:
                    print("That was correct. You have 2 minutes to make changes.")
                    adjustments()
                else:
                    print("That was incorrect")
                    attempts-=1

            print("You have been locked out of the maintainence system you will be returned to the main menu in 5 seconds:")
            pinCanTry = False
            pinLockout = time.time()
            for _ in range(5,0,-1):
                print(_)
                time.sleep(1)
            main_menu()
        except KeyboardInterrupt:
            main_menu()

    else:
        print(f"You have been locked out of the maintainence system you will be returned to the main menu in 5 seconds\n you have to wait {round(120-(time.time()-pinLockout))} seconds before trying again:")
        for _ in range(5,0,-1):
            print(_)
            time.sleep(1)
        main_menu()



# adjustments function allows the user to alter the maximum volume of the tank or the pin, so that future calculations are correct
# INPUTS: None
# OUTPUTS: None (New maxVolume or new pin as global variables)
# Created by Matt
# Date created: 05/09/2023
def adjustments():
    global maxVolume, pin
    start_time = time.time()
    print("====================================\nYou have entered maintenance mode.\n====================================")
    try:
        while True:
            print(f"(1) Change current pin: {pin}\n(2) Edit maximum voume from {maxVolume}mL")
            option = input("Please enter your selection or enter ctrl+c to exit to main menu: ")
            if time.time()-start_time >=120:
                print(f"YOU HAVE TIMED OUT\nTo make more changes enter maintainence again\npin = {pin}\nMaximum volume = {maxVolume}mL")
                main_menu_exit()

            elif option == '1':
                pin_select = input("Please enter the new pin: ")
                if len(pin_select) < 3:
                    print("======\npin needs to be longer than 3 digits\n======")
                else: pin = pin_select
            elif option == '2':
                maxVolume_select = int(input("Please enter the new max volume in mL: "))
                if 2500<maxVolume_select<10000:
                    maxVolume = maxVolume_select
                    print(maxVolume)
                else:
                    print("======\nInvalid range for volume\n======")
            else:
                print("Invalid input try again.")
    except KeyboardInterrupt:
        print(f"pin = {pin}\nMaximum volume = {maxVolume}mL")
        main_menu()
#main menu function that moves user back to the main menu
#inputs None
#outputs None
def main_menu_exit():
    print("exiting to main menu")
    for _ in range(5,0,-1):
        print(_)
        time.sleep(1)
    main_menu()

def seven_seg(string):
    dictionary = {
    "0": [0, 1, 1, 1, 1, 1, 0, 1],
    "1": [0, 1, 1, 0, 0, 0, 0, 0],
    "2": [0, 1, 0, 1, 1, 0, 1, 1],
    "3": [0, 1, 1, 1, 0, 0, 1, 1],
    "4": [0, 1, 1, 0, 0, 1, 1, 0],
    "5": [0, 0, 1, 1, 0, 1, 1, 1],
    "6": [0, 0, 1, 1, 1, 1, 1, 1],
    "7": [0, 1, 1, 0, 0, 0, 0, 1],
    "8": [0, 1, 1, 1, 1, 1, 1, 1],
    "9": [0, 1, 1, 1, 0, 1, 1, 1],
    "A": [0, 1, 1, 0, 1, 1, 1, 1],
    "B": [0, 0, 1, 1, 1, 1, 1, 0],
    "C": [0, 0, 0, 1, 1, 1, 0, 1],
    "D": [0, 1, 1, 1, 1, 0, 1, 0],
    "E": [0, 0, 0, 1, 1, 1, 1, 1],
    "F": [0, 0, 0, 0, 1, 1, 1, 1],
    "G": [0, 0, 1, 1, 1, 1, 0, 1],
    "H": [0, 1, 1, 0, 1, 1, 1, 0],
    "I": [0, 0, 0, 0, 1, 1, 0, 0],
    "J": [0, 1, 1, 1, 0, 0, 0, 0],
    "K": [0, 1, 1, 0, 1, 1, 1, 0],
    "L": [0, 0, 0, 1, 1, 1, 0, 0],
    "M": [0, 0, 1, 0, 1, 0, 1, 1],
    "N": [0, 0, 1, 0, 1, 0, 1, 0],
    "O": [0, 1, 1, 1, 1, 1, 0, 1],
    "P": [0, 1, 0, 0, 1, 1, 1, 1],
    "Q": [0, 1, 1, 0, 0, 1, 1, 1],
    "R": [0, 0, 0, 0, 1, 0, 1, 0],
    "S": [0, 0, 1, 1, 0, 1, 1, 1],
    "T": [0, 0, 0, 1, 1, 1, 1, 0],
    "U": [0, 1, 1, 1, 1, 1, 0, 0],
    "V": [0, 1, 1, 1, 1, 1, 0, 0],
    "W": [0, 1, 1, 1, 1, 1, 0, 0],
    "X": [0, 1, 1, 0, 1, 1, 1, 0],
    "Y": [0, 1, 1, 1, 0, 1, 1, 0],
    "Z": [0, 1, 0, 1, 1, 0, 1, 1],
    "_": [0, 0, 0, 0, 0, 0, 0, 0]
    }   

    ser = 6
    rclk = 7
    srclk = 8

    digits = [2, 3, 4, 5]
    board.set_pin_mode_digital_output(ser)
    board.set_pin_mode_digital_output(rclk)
    board.set_pin_mode_digital_output(srclk)
    for dig in digits:
        board.set_pin_mode_digital_output(dig)
        board.digital_write(dig, 1)
    board.digital_write(ser, 0)
    board.digital_write(rclk, 0)
    board.digital_write(srclk, 0)

    string = str(string)
    string = "____" + string + "____"
    

    while True:
        i = 5
        for _ in range(10):
            for char in string:
                binary = dictionary[char.upper()]
                binary = binary[::-1]
                for val in binary:
                    board.digital_write(ser, val)
                    board.digital_write(srclk, 1)
                    time.sleep(0.00005)
                    board.digital_write(srclk, 0)
                    board.digital_write(rclk, 1)
                    time.sleep(0.0005)
                    board.digital_write(rclk, 0)
                    time.sleep(0.0005)
                board.digital_write(i, 0)
                time.sleep(0.000005)
                board.digital_write(i, 1)
                time.sleep(0.000005)
                i -= 1
            i = 5
        time.sleep(0.00005)
        string = string[1:len(string)]


main_menu()



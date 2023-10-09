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

# Defined Variables
pin = '1234'
pinCanTry = True
pinLockout = 130
maxHeight = 20
maxVolume = 10000
board = pymata4.Pymata4()
board.set_sampling_interval(1000)
                               
height = 0
volumeGraph = []
timeGraph = []
rateChange = []
rateOfChangeCutoff = 2000 #mL/s
baseSurfaceArea = 24*24
timeAdd = True
errorLights = [14,15,16,17]



# polling_loop function calls various other functions, every 1.5 seconds
# INPUTS: None (timeAdd as a global variable)
# OUTPUTS: None
# Created by Matt
# Date created: 05/09/2023
def polling_loop():
    global timeAdd
    
    startTime = time.time()
    ultrasonic_ping() 
    print(f"Volume = {volume}mL")#print(volume) mL

    data_clean()
    if timeAdd:
        reactions()
    time.sleep(1.5)
    endTime = time.time()
    runTime = endTime - startTime
    if timeAdd:
        timeGraph.append(time.time())
    print(f'Runtime = {runTime}')



# reactions function checks for volume level, turns on necessary warning LED and print statements of pump status
# INPUTS: NONE (volume, maxVolume errorLights, baseSurfaceArea as global variables)
# OUTPUTS: NONE
# Created by Matt
# Date created: 05/09/2023
def reactions():
    global maxHeight, height, board, errorLights, baseSurfaceArea, maxVolume, volume
    heightDif = (maxHeight - height)/maxHeight

    for pin in errorLights:
            board.set_pin_mode_digital_output(pin)
            board.digital_write(pin,0)

    if (volume/maxVolume)<0.1:
        board.digital_write(14,1)
        board.digital_pin_write(15,1)
        print("Input pump on at HIGH speed")
    elif 0.1<(volume/maxVolume)<0.25:
        board.digital_write(14,1)
        print("Input pump on at LOW speed")
    elif 0.75<(volume/maxVolume)<0.9:
        board.digital_pin_write(16,1)
        print("Output pump on at Low speed")
    elif 0.9<(volume/maxVolume)<1:
        board.digital_write(16,1)
        board.digital_write(17,1)
        print("Output pump on at High speed")
    elif (volume/maxVolume)>1:
        print(f"Volume is beyond max volume {maxVolume} mL")



# data_clean function checks to see if last ultrasonic read involves a change of more than the rate-of-change-cutoff and 
# disregards it if it is
# INPUTS: None (volume, volumeGraph, timeGraph, rateOfChangeCutoff, timeAdd)
# OUTPUTS: NONE (appended volumeGraph as a global variable)
# Created by Matt
# Date created: 05/09/2023
def data_clean():
    global volume, volumeGraph, timeGraph, rateOfChangeCutoff, timeAdd

    if len(timeGraph) > 1:
        if abs(volumeGraph[-1] - volume) < rateOfChangeCutoff and volume>=0:
            volumeGraph.append(volume)
            timeAdd = True
        else:
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
    board.set_pin_mode_sonar(18,19,timeout=200000)
    measure = board.sonar_read(18)
    height = calcHeight - measure[0]
    print(f'Height = {height}cm')
    volume = height * baseSurfaceArea #gets volume of water in ml



# graph_data function plots volume against time for the last 20 data points
# INPUTS: None
# OUTPUTS: None (graph of data displayed)
# Created by Matt
# Date created: 05/09/2023
def graph_data():
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
    global volumeGraph, timeGraph
    print("====================================\nYou have entered Normal Operation Mode.\n====================================\ninput (ctrl + c) to return to the main menu\n====================================")
    try:
        while True:
            polling_loop()
    except KeyboardInterrupt:
        for pin in errorLights:
            board.set_pin_mode_digital_output(pin)
            board.digital_write(pin,0)
        
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
            print("Please select an option from the following to observe data\n(1) Create a graph of 20 data points collected from normal mode\n(2) Display the last recorded volume\n(ctrl + c) Main Menu")
            analysisOption = input("Please provide input: ")
            if analysisOption == '1':
                if len(volumeGraph) >20:
                    graph_data()
                else:
                    print("Not enough stored data")
            elif analysisOption == '2':
                #have a section for the 7 seg
                if len(volumeGraph)>0:
                    outputMessage = str(round(volumeGraph[-1]))
                    seven_seg(outputMessage)
                else:
                    print("Must record some data first")
            else:
                print("Invalid option")

    except KeyboardInterrupt:
        digits = [7, 9, 10, 13] # Digits 1-4
        for digit in digits:
            board.digital_write(digit, 1)
        main_menu()



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
                    print("pin needs to be longer than 3 digits")
                else: pin = pin_select
            elif option == '2':
                maxVolume_select = int(input("Please enter the new max volume in mL: "))
                if 2500<maxVolume_select<10000:
                    maxVolume = maxVolume_select
                else:
                    print("Invalid range for volume")
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
    pins = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    digits = [7, 9, 10, 13] # Digits 1-4
    seg = [12, 8, 5, 4, 3, 11, 6] # Segments a - g

    while len(string) <4:
        string = '_' + string

    dictionary = {
        "0": [1, 1, 1, 1, 1, 1, 0],
        "1": [0, 1, 1, 0, 0, 0, 0],
        "2": [1, 1, 0, 1, 1, 0, 1],
        "3": [1, 1, 1, 1, 0, 0, 1],
        "4": [0, 1, 1, 0, 0, 1, 1],
        "5": [1, 0, 1, 1, 0, 1, 1],
        "6": [1, 0, 1, 1, 1, 1, 1],
        "7": [1, 1, 1, 0, 0, 0, 0],
        "8": [1, 1, 1, 1, 1, 1, 1],
        "9": [1, 1, 1, 1, 0, 1, 1],
        "A": [1, 1, 1, 0, 1, 1, 1],
        "B": [0, 0, 1, 1, 1, 1, 1],
        "C": [1, 0, 0, 1, 1, 1, 0],
        "D": [0, 1, 1, 1, 1, 0, 1],
        "E": [1, 0, 0, 1, 1, 1, 1],
        "F": [1, 0, 0, 0, 1, 1, 1],
        "G": [1, 0, 1, 1, 1, 1, 0],
        "H": [0, 1, 1, 0, 1, 1, 1],
        "I": [0, 0, 0, 0, 1, 1, 0],
        "J": [0, 1, 1, 1, 0, 0, 0],
        "K": [0, 1, 1, 0, 1, 1, 1],
        "L": [0, 0, 0, 1, 1, 1, 0],
        "M": [1, 0, 1, 0, 1, 0, 1],
        "N": [0, 0, 1, 0, 1, 0, 1],
        "O": [1, 1, 1, 1, 1, 1, 0],
        "P": [1, 1, 0, 0, 1, 1, 1],
        "Q": [1, 1, 1, 0, 0, 1, 1],
        "R": [0, 0, 0, 0, 1, 0, 1],
        "S": [1, 0, 1, 1, 0, 1, 1],
        "T": [0, 0, 0, 1, 1, 1, 1],
        "U": [0, 1, 1, 1, 1, 1, 0],
        "V": [0, 1, 1, 1, 1, 1, 0],
        "W": [0, 1, 1, 1, 1, 1, 0],
        "X": [0, 1, 1, 0, 1, 1, 1],
        "Y": [0, 1, 1, 1, 0, 1, 1],
        "Z": [1, 1, 0, 1, 1, 0, 1],
        "_": [0, 0, 0, 0, 0, 0, 0]
    }
    for pin in pins:
        board.set_pin_mode_digital_output(pin)

    for digit in digits:
        board.digital_write(digit, 1)

    # Convert input to string
    string = str(string)
    numbers = []
    for char in string:
        sequence = dictionary[char.upper()]
        numbers.append(sequence)
    while True:
        for n in range(len(digits)):
            board.digital_write(digits[n], 0)  # Turn on the current digit
            for i in range(len(seg)):
                board.digital_write(seg[i], numbers[n][i])  # Write the segment value
                time.sleep(0.0001)  # Delay for segment display
                board.digital_write(seg[i], 0)  # Turn off the current segment
            board.digital_write(digits[n], 1) # Turn off the current digit



main_menu()



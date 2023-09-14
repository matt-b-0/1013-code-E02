#main function file 
import time 
import random
import matplotlib.pyplot as plt
from pymata4 import pymata4
results = []
pin = '1234'
pinCanTry = True
pinLockout = None
maxHeight = 20
board = pymata4.Pymata4()
"""
I couldnt keep up but need to rename functions and variables to maintain 1013 stoopid ass standards 
MAY NEED TO REPLACE FUNCTION CALLS WITH A RETURN INFORNT OF THEM
THIS MAY IMPACT THE WAY SCRIPT WORKS
WILL HAVE TO DO MORE TESTING FIRST

Current to do list:
Implement the adjustments function: changes specs of tank manually
implement reactions: allows for fans and LED to turn on.
"""
"""
 
         )                                   
      ( /(  (           )     )    )      )  
 (    )\()) )\ )     ( /(  ( /( ( /(   ( /(  
 )\  ((_)\ (()/(     )\()) )\()))\())  )\()) 
((_)  _((_) /(_))_  ((_)\ ((_)\((_)\  ((_)\  
| __|| \| |(_)) __|  / (_)/  (_)/ (_)|__ (_) 
| _| | .` |  | (_ |  | | | () | | |   |_ \   
|___||_|\_|   \___|  |_|  \__/  |_|  |___/   
                                             

"""
                               

distances = 0
height = 0
volumeGraph = []
timeGraph = []
rateChange = []
rateOfChangeCutoff = 3000 #mL/s
baseSurfaceArea = 24*24
timeAdd = True
errorLights = [3,4,5,6]

# polling_loop function calls various other functions, every 1.5 seconds
# INPUTS: None (timeAdd as a global variable)
# OUTPUTS: None
# Created by Matt
# Date created: 05/09/2023
def polling_loop():
    global results, timeAdd
    """
    need to understand if everythin is called from the polling loop or if it just used to gether data.
    """

    startTime = time.time()
    ultrasonic_ping() 
    print(f"{volume}")#print(volume) mL

    data_clean()
    if timeAdd:
        reactions()
    time.sleep(1.5)
    endTime = time.time()
    runTime = endTime - startTime
    if timeAdd:
        timeGraph.append(runTime)
    print(f'Runtime = {runTime}')

# reactions function checks for volume level, turns on necessary warning LED and print statements of pump status
# INPUTS: NONE (maxHeight, height, errorLights, baseSurfaceArea as global variables)
# OUTPUTS: NONE
# Created by Matt
# Date created: 05/09/2023
def reactions():
    """
    This will be the function that will control both the LED warning lights and the fans for the tank
    """
    global maxHeight, height, board, errorLights, baseSurfaceArea
    heightDif = (maxHeight - height)/maxHeight

    for pin in errorLights:
            board.set_pin_mode_digital_output(pin)
            board.digital_write(pin,0)

    if heightDif>0.9:
        board.digital_write(3,1)
        board.digital_pin_write(4,1)
        print("Input pump on at HIGH speed")
    elif 0.75<heightDif<0.9:
        board.digital_write(3,1)
        print("Input pump on at LOW speed")
    elif 0.1<heightDif<0.25:
        board.digital_pin_write(5,1)
        print("Output pump on at Low speed")
    elif 0<heightDif<0.1:
        board.digital_write(5,1)
        board.digital_write(6,1)
        print("Output pump on at High speed")
    elif heightDif <0:
        print(f"Volume is at max level\nmax volume is {maxHeight*baseSurfaceArea} mL")

# data_clean function checks to see if last ultrasonic read involves a change of more than the rate-of-change-cutoff and 
# disregards it if it is
# INPUTS: None (timeGraph, volumeGraph, volume, rateOfChangeCutoff as global variables)
# OUTPUTS: NONE (appended volumeGraph as a global variable)
# Created by Matt
# Date created: 05/09/2023
def data_clean():
    global volume, volumeGraph, timeGraph, rateChange, timeAdd

    if len(timeGraph) > 0:
        if (abs(volumeGraph[-1] - volume)/timeGraph[-1]) < rateOfChangeCutoff:
            volumeGraph.append(volume)
            timeAdd = True
        else:
            print("Error in rate of change data removed")
    else:
        volumeGraph.append(volume)

# ultrasonic_ping function uses the ultrasonic sensor to determine the distance from sensor to the water, 
# and then determines the distance from this
# INPUTS: None
# OUTPUTS: None (volume and height of water as global variables)
# Created by Matt
# Date created: 05/09/2023
def ultrasonic_ping():
    """
    this function will use the arduino to calculate the distance/
    volume of the tank
    """
    global board, volume, height
    calcHeight = 21
    board.set_pin_mode_sonar(8,7,timeout=200000)
    measure = board.sonar_read(8)
    height = calcHeight - measure[0]
    print(height)
    volume = height * baseSurfaceArea #gets volume of water in ml
    


    

# graph_data function plots volume against time
# INPUTS: None
# OUTPUTS: None (graph of data displayed)
# Created by Matt
# Date created: 05/09/2023
def graph_data():
    global results
    """
    this function will graph the data 
    from the previous 20 data points of volume data
    """
    #plt.figure(1)
    #plt.title("Volume against Time")
    #plt.errorbar(time, data, linestyle = "--", marker = "o")
    #plt.xlabel("Time (s)")
    #plt.ylabel("Volume (mL)")
    #plt.show()
    pass

# main_menu functions lets user choose a mode of operation
# INPUTS: None
# OUTPUTS: None
# Created by Matt
# Date created: 05/09/2023
def main_menu():
    """
    This will be the main menu for tank operation
    it will be the initial call for the file.
    everythin is run off this function.
    """
    
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




#HERE:--->
#MAIN MENU (ALL THE MODES DEFINED)

# When normal mode is chosen, run the polling loop until keyboard is interrupted
# INPUTS: None
# OUTPUTS: None (volume and height of water as global variables)
# Created by Matt
# Date created: 05/09/2023
def normal_operation():
    global results
    results = []
    print("====================================\nYou have entered Normal Operation Mode.\n====================================\ninput (ctrl + c) to return to the main menu\n====================================")
    try:
        while True:
            polling_loop()
    except KeyboardInterrupt:
        main_menu()

# When data observation mode is chosen, the available data is graphed
# INPUTS: None (results as a global variable)
# OUTPUTS: None 
# Created by Matt
# Date created: 05/09/2023
def data_observation():
    global results, volumeGraph
    print("====================================\nYou have entered Data Observation Mode.\n====================================\ninput (ctrl + c) to return to the main menu====================================")
    
        #need to delete the other sections of the list
    try:
        while True:
            print("please sleect an option from the following to observe data\n(1) create a graph of 20 data points collected from normal mode\n(2) display the last recorded volume\n(ctrl + c) Main Menu")
            analysisOption = input("please provide input: ")
            if analysisOption == '1':
                if len(volumeGraph) >=20:
                    graph_data()
                else:
                    print("not enough stored data")
            elif analysisOption == '2':
                #have a section for the 7 seg
                pass 

    except KeyboardInterrupt:
        main_menu()
    
# When maintenance mode is chosen, asks user for PIN, if correct sends to settings adjustments, if incorrect returns to home screen
# INPUTS: None (pin,pinCanTry and pinLockout as global variables)
# OUTPUTS: None 
# Created by Matt
# Date created: 05/09/2023
def maintenance():
    global pin, pinCanTry, pinLockout
    attempts = 5
    if pinCanTry:
        if pinLockout >120:
            pinCanTry = True 
    if pinCanTry:
        try:
            while attempts>0:
                print(f'====================================\nYou have entered maintenance mode.\n====================================\nPlease enter the correct {len(pin)} digit pin to make adjustments\nYou have {attempts} attempts left.\nenter (ctrl + c) to return to main menu\n====================================')
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
        print("You have been locked out of the maintainence system you will be returned to the main menu in 5 seconds:")
        for _ in range(5,0,-1):
            print(_)
            time.sleep(1)
        main_menu()

# adjustments function allows the user to alter the maximum height of the tank or the pin, so that future calculations are correct
# INPUTS: None
# OUTPUTS: None (New maxHeight or new pin as global variables)
# Created by Matt
# Date created: 05/09/2023
def adjustments():
    global maxHeight, pin
    """
    this function will allow the user to make adjustments to variables that can be changed.
    this function will go through each changable option
    It HAS TO RETURN TO THE MAIN MENU
    or it will stuff up code above
    """
    print("====================================\nYou have entered maintenance mode.\n====================================")
    print("To edit pin enter (1)\nTo edit maximum height enter (2)")
    option = input("Please enter your selection or enter ctrl+c to exit to main menu: ")
    if option == '1':
        pin = input("Please enter the new pin: ")
    elif option == '2':
        maxHeight = int(input("Please enter the new maximum height in cm: "))





main_menu()

sevenSegment = {
        "0": [1, 1, 1, 1, 1, 1, 0],  # 0
        "1": [0, 1, 1, 0, 0, 0, 0],  # 1
        "2": [1, 1, 0, 1, 1, 0, 1],  # 2
        "3": [1, 1, 1, 1, 0, 0, 1],  # 3
        "4": [0, 1, 1, 0, 0, 1, 1],  # 4
        "5": [1, 0, 1, 1, 0, 1, 1],  # 5
        "6": [1, 0, 1, 1, 1, 1, 1],  # 6
        "7": [1, 1, 1, 0, 0, 0, 0],  # 7
        "8": [1, 1, 1, 1, 1, 1, 1],  # 8
        "9": [1, 1, 1, 1, 0, 1, 1],  # 9
        "A": [1, 1, 1, 0, 1, 1, 1],  # A
        "B": [0, 0, 1, 1, 1, 1, 1],  # B
        "C": [1, 0, 0, 1, 1, 1, 0],  # C
        "D": [0, 1, 1, 1, 1, 0, 1],  # D
        "E": [1, 0, 0, 1, 1, 1, 1],  # E
        "F": [1, 0, 0, 0, 1, 1, 1],  # F
        "G": [1, 0, 1, 1, 1, 1, 0],  # G
        "H": [0, 0, 1, 0, 1, 1, 1],  # H
        "I": [0, 0, 0, 0, 1, 1, 0],  # I
        "J": [0, 1, 1, 1, 1, 0, 0],  # J
        "K": [1, 0, 1, 0, 1, 1, 1],  # K
        "L": [0, 0, 0, 1, 1, 1, 0],  # L
        "M": [1, 0, 1, 0, 1, 0, 0],  # M
        "N": [1, 1, 1, 0, 1, 1, 0],  # N
        "O": [1, 1, 1, 1, 1, 1, 0],  # O
        "P": [1, 1, 0, 0, 1, 1, 1],  # P
        "Q": [1, 1, 1, 0, 0, 1, 1],  # Q
        "R": [1, 1, 0, 0, 1, 1, 0],  # R
        "S": [1, 0, 1, 1, 0, 1, 1],  # S
        "T": [0, 0, 0, 1, 1, 1, 1],  # T
        "U": [0, 1, 1, 1, 1, 1, 0],  # U
        "V": [0, 1, 1, 1, 0, 1, 0],  # V
        "W": [0, 1, 0, 1, 0, 1, 0],  # W
        "X": [0, 1, 1, 0, 1, 1, 1],  # X
        "Y": [0, 1, 1, 1, 0, 1, 1],  # Y
        "Z": [1, 1, 0, 1, 0, 0, 1]  # Z
    }

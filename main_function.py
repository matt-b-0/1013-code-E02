#main function file 
import time 
import random
import matplotlib.pyplot as plt
from pymata4 import pymata4

pin = '1234'
pinCanTry = True
pinLockout = None
maxHeight = 20
maxVolume = 10000
board = pymata4.Pymata4()
board.set_sampling_interval(1000)


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
    global results, timeAdd
    """
    need to understand if everythin is called from the polling loop or if it just used to gether data.
    """

    startTime = time.time()
    ultrasonic_ping() 
    print(f"volume = {volume}mL")#print(volume) mL

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
# INPUTS: NONE (maxHeight, height, errorLights, baseSurfaceArea as global variables)
# OUTPUTS: NONE
# Created by Matt
# Date created: 05/09/2023
def reactions():
    """
    This will be the function that will control both the LED warning lights and the fans for the tank
    """
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
# INPUTS: None (timeGraph, volumeGraph, volume, rateOfChangeCutoff as global variables)
# OUTPUTS: NONE (appended volumeGraph as a global variable)
# Created by Matt
# Date created: 05/09/2023
def data_clean():
    global volume, volumeGraph, timeGraph, rateChange, timeAdd

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
    """
    this function will use the arduino to calculate the distance/
    volume of the tank
    """
    global board, volume, height
    calcHeight = 22
    board.set_pin_mode_sonar(18,19,timeout=200000)
    measure = board.sonar_read(18)
    height = calcHeight - measure[0]
    print(f'height = {height}cm')
    volume = height * baseSurfaceArea #gets volume of water in ml
    


    

# graph_data function plots volume against time
# INPUTS: None
# OUTPUTS: None (graph of data displayed)
# Created by Matt
# Date created: 05/09/2023
def graph_data():
    global timeGraph, volumeGraph
    """
    this function will graph the data 
    from the previous 20 data points of volume data
    """
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
    
        #need to delete the other sections of the list
    try:
        while True:
            print("please sleect an option from the following to observe data\n(1) create a graph of 20 data points collected from normal mode\n(2) display the last recorded volume\n(ctrl + c) Main Menu")
            analysisOption = input("please provide input: ")
            if analysisOption == '1':
                if len(volumeGraph) >20:
                    graph_data()
                else:
                    print("not enough stored data")
            elif analysisOption == '2':
                #have a section for the 7 seg
                if len(volumeGraph)>0:
                    outputMessage = str(round(volumeGraph[-1]))
                    seven_seg(outputMessage)
                else:
                    print("Need to record some data first")
            else:
                print("invalid option")

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



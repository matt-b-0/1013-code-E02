#main function file 
import time 
import random
import matplotlib.pyplot as plt
from pymata4 import pymata4
results = []
pin = '1234'
pin_can_try = True
pin_lockout = None
max_height = 20
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
volume_graph = []
time_graph = []
rate_change = []
rate_of_change_cutoff = 100 #mL/s
base_SA = 24*24
time_add = True
error_lights = [3,4,5,6]

def polling_loop():
    global results, time_add
    """
    need to understand if everythin is called from the polling loop or if it just used to gether data.
    """

    startTime = time.time()
    ultrasonic_ping() 
    print(f"{volume}")#print(volume) mL
    data_clean()

    if time_add:
        reactions()
    time.sleep(1.5)
    endTime = time.time()
    runTime = endTime - startTime
    if time_add:
        time_graph.append(runTime)
    print(f'runtime = {runTime}')

def reactions():
    """
    This will be thefunction that will control both the LED warning lights and the fans for the tank
    """
    global max_height, height, board, error_lights
    height_dif = (max_height - height)/max_height

    for pin in error_lights:
            board.set_pin_mode_digital_output(pin)
            board.digital_write(pin,0)

    if height_dif>0.9:
        board.digital_write(pin[0],1)
        board.digital_pin_write(pin[1],1)
        print("input pump on at HIGH speed")
    elif height_dif>0.75:
        board.digital_write(pin[0],1)
        print("input pump on at LOW speed")
    elif 0.1<height_dif<0.25:
        board.digital_write(pin[2],1)
        board.digital_pin_write(pin[3],1)
        print("output pump on at HIGH speed")
    elif 0<height_dif<0.1:
        board.digital_write(pin[2],1)
        print("output pump on at LOW speed")
    elif height <0:
        print(f"volume is at max level\nmax volume is {max_height*base_SA} mL")

        
       
def data_clean():
    global volume, volume_graph, time_graph, rate_change, time_add

    if len(time_graph) > 0:
        if (abs(volume_graph[-1] - volume)/time_graph[-1]) < rate_of_change_cutoff:
            volume_graph.append(volume)
            time_add = True
        else:
            print("error in rate of change data removed")
    else:
        volume_graph.append(volume)


def ultrasonic_ping():
    """
    this function will use the arduino to calculat the distance/
    volume of the tank
    """
    global board, volume, height
    calc_height = 21
    board.set_pin_mode_sonar(8,7,timeout=200000)
    measure = board.sonar_read(7)
    height = calc_height - measure[0]
    volume = height* base_SA #gets volume of water in ml


    

    

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
    #plt.ylabel("Volume (m^3)")
    #plt.show()
    pass

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
            user_choice = input("please select an option from above by entering a number: ")
            if user_choice == '1':
                print("maintenance mode")
                # Call the maintenance function
                maintenance()
            elif user_choice == '2':
                print("Data Analysis mode")
                # Call analysis function
                data_observation()
            elif user_choice == '3':
                print("normal operation")
                # Call normal operation function
                normal_operation()
            else:
                print("invalid input")
    except KeyboardInterrupt:
        exit(0)




#HERE:--->
#MAIN MENU (ALL THE MODES DEFINED)
def normal_operation():
    global results
    results = []
    print("====================================\nYou have entered Normal Operation Mode.\n====================================\ninput (ctrl + c) to return to the main menu\n====================================")
    try:
        while True:
            polling_loop()
    except KeyboardInterrupt:
        main_menu()

def data_observation():
    global results
    print("====================================\nYou have entered Data Observation Mode.\n====================================\ninput (ctrl + c) to return to the main menu====================================")
    if len(results) >=20:
        graph_data()
        #need to delete the other sections of the list
    try:
        while True:
            if len(results) % 20 == 0:
                graph_data()

    except KeyboardInterrupt:
        main_menu()
    

def maintenance():
    global pin, pin_can_try, pin_lockout
    attempts = 5
    if pin_can_try:
        if pin_lockout >120:
            pin_can_try = True 
    if pin_can_try:
        try:
            while attempts>0:
                print(f'====================================\nYou have entered maintaience mode.\n====================================\nPlease enter the correct {len(pin)} digit pin to make adjustments\nYou have {attempts} attempts left.\nenter (ctrl + c) to return to main menu\n====================================')
                #may have to change if we want to make a numeric key, i have it as a string at the top
                attempt = input('enter pin: ')
                if attempt == pin:
                    print("That was correct. You have 2 minutes to make changes.")
                    adjustments()
                else:
                    print("That was incorrect")
                    attempts-=1

            print("You have been locked out of the maintainence system you will be returned to the main menu in 5 seconds:")
            pin_can_try = False
            pin_lockout = time.time()
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

def adjustments():
    global max_height, pin
    """
    this function will allow the user to make adjustmnts to variables that can be changed.
    this function will go through each changable option
    It HAS TO RETURN TO THE MAIN MENU
    or it will stuff up code above
    """
    print("====================================\nYou have entered maintaience mode.\n====================================")
    print("To edit pin enter (1)\nto edit maximum height enter (2)")
    option = input("please enter you option or enter ctrl+c to exit to main menu: ")
    if option == '1':
        pin = input("please enter the new pin: ")
    elif option == '2':
        max_height = int(input("please enter the new max height in cm: "))





main_menu()
seven_segment = {
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

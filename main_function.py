#main function file 
import time 
import random
import matplotlip.pyplot as plt
results = []
pin = '1234'
pin_can_try = True
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
                               



#HERE:---->        
# Define the condition function
def check(value, callback):
    # The condition for checking logic
    if value > 0:                                     
        callback(value)

# Necessary calculation for volume and stuff function REPLACE THIS WITH A CALC FUNCTION
def perform_calc(value):
    value = value * 10
    volume.append(round(value, 2))
    #will need to import numpy for pi value np.pi
    #volume will be 2*np.pi*r*height

# Main function file


distances = 0
volume = []
totalTime = []

def polling_loop():
    global results
    """
    need to understand if everythin is called from the polling loop or if it just used to gether data.
    """

    startTime = time.time()
    print("ultrasonic ping and detection")  # replace random.random() with the ultrasonic ping readings
    print("calculating the current volume")#check(distances, perform_calc)  # callback function- To do something with the input
    print("print(volume)")#print(volume)
    print("reactions") #function that will turn on lights and fand/ stop them depending on current volume.
    time.sleep(2)
    print('results.append(volume)')
    endTime = time.time()
    runTime = endTime - startTime
    totalTime.append(runTime)
    
    print(f'runtime = {runTime}')

def reactions():
    """
    This will be thefunction that will control both the LED warning lights and the fans for the tank
    """
       


def ultrasonic_ping():
    """
    this function will use the arduino to calculat the distance/
    volume of the tank
    """
    #send signal to the arduino to ping
    #record the time differnce when it has been recieved 
    #calculate distance and respective volume
    #results.append(volume)
    pass

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
            polling_loop()
            if len(results) % 20 == 0:
                graph_data()
            #other result printing

    except KeyboardInterrupt:
        main_menu()
    

def maintenance():
    global pin, pin_can_try
    attempts = 5
    if pin_can_try:
        try:
            while attempts>0:
                print(f'====================================\nYou have entered maintaience mode.\n====================================\nPlease enter the correct {len(pin)} digit pin to make adjustments\nYou have {attempts} attempts left.\nenter (ctrl + c) to return to main menu\n====================================')
                #may have to change if we want to make a numeric key, i have it as a string at the top
                attempt = input('enter pin: ')
                if attempt == pin:
                    adjustments()
                else:
                    print("That was incorrect")
                    attempts-=1

            print("You have been locked out of the maintainence system you will be returned to the main menu in 5 seconds:")
            pin_can_try = False
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
    """
    this function will allow the user to make adjustmnts to variables that can be changed.
    this function will go through each changable option
    It HAS TO RETURN TO THE MAIN MENU
    or it will stuff up code above
    """
    pass


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

#main function file 
import time 
results = []
pin = '1234'
pin_can_try = True
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

# Main function file
import time
import random

distances = 0
volume = []
totalTime = []

def polling_loop():
    try:
        while True:
            startTime = time.time()
            distances = random.random()  # replace random.random() with the ultrasonic ping readings
            check(distances, perform_calc)  # callback function- To do something with the input
            print(volume)
            time.sleep(2)
            endTime = time.time()
            runTime = endTime - startTime
            totalTime.append(runTime)
            
            print(f'runtime = {runTime}')

    except KeyboardInterrupt:
        print("Polling loop ending.")

       


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
    """
    this function will graph the data 
    from the previous 20 data points of volume data
    """
    #x = results[-20:0]
    #y = 
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
                print("analysis mode")
                # Call analysis function
            elif user_choice == '3':
                print("normal operation")
                # Call normal operation function
            else:
                print("invalid input")
    except KeyboardInterrupt:
        exit(0)




#HERE:--->
#MAIN MENU (ALL THE MODES DEFINED)
def normal_operation():
    global results
    print("You are in Normal operation mode. Press Enter to return to the main menu.")
    print("In progress")
    while True:
        action = input()
        if not action:  
            confirm = input("Are you sure you want to return to the main menu? (Y/N): ")
            if confirm.upper() == 'Y':
                break

def data_observation():
    print("You are in Data Observation Mode. Press Enter to return to the main menu.")
    print("In progress")
    while True:
        action = input()
        if not action:  
            confirm = input("Are you sure you want to return to the main menu? (Y/N): ")
            if confirm.upper() == 'Y':
                break

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

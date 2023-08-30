#main function file 
import time 
results = []
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
                               
def main():
    try: 
        while True:
            start_time = time.time() # Shouldnt this all be in a new function like data record as the main loop is what determines what is done
            ultrasonic_ping()
            end_time = time.time()
            run_time = end_time-start_time
            print(f'runtime = {run_time}')
            time.sleep(2)
          #  if len(results)%20 ==0: - This shouldnt be here
          #      graph_data()
    except KeyboardInterrupt:
        selection_menu()
def main():
    try:
        selection_menu() # Call the selection menu

        
# Define the condition function
def check(value, callback):
    # The condition for checking logic
    if value > 0:
        callback(value)

# Necessary calculation for volume and stuff function
def perform_calc(value):
    value = value * 10
    x.append(round(value, 2))

# Main function file
import time
import random

results = []
a = 0
x = []

def polling_loop():
    try:
        while True:
            start_time = time.time()
            a = random.random()  # sensor #ultrasonic_ping()
            check(a, perform_calc)  # callback function- To do something with the input
            print(x)
            end_time = time.time()
            run_time = end_time - start_time
            time.sleep(2)
            print(f'runtime = {run_time}')

    except KeyboardInterrupt:
        pass


polling_loop()
        


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

def selection_menu():
    """
    This will be the main menu for tank operation
    it will be the initial call for the file.
    everythin is run off this function.
    """
    #try:
        #print('select a mode of operation\n')
        #need to add options
        #input("")
    #except KeyboardInterrupt:
        #exit(0)
    print("Choose a mode of operation")
    valid = [Maintenance, Analysis, Normal]
        try:
            user_choice = input("1: Maintenance. 2. Analysis. 3. Normal:\n")
            if user_choice.upper() not in valid:
                return ValueError
            elif user_choice.upper() == Maintenance:
                print("maintenance mode")
                # Call the maintenance function
            elif user_choice.upper() == Analysis:
                print("analysis mode")
                # Call analysis function
            elif user_choice.upper() == Normal:
                print("normal operation")
                # Call normal operation function
   pass




#MAIN MENU (ALL THE MODES DEFINED)
         def normal_operation():
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
    print("You are in Maintenance Mode. Press Enter to return to the main menu.")
    print("In progress")
    while True:
        action = input()
        if not action: 
            confirm = input("Are you sure you want to return to the main menu? (Y/N): ")
            if confirm.upper() == 'Y':
                break

def main_menu():
    while True:
        print("Main Menu")
        print("1. Normal Operation Mode")
        print("2. Data Observation Mode")
        print("3. Maintenance Mode")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            normal_operation()
        elif choice == '2':
            data_observation()
        elif choice == '3':
            maintenance()
        elif choice == '4':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

main_menu()

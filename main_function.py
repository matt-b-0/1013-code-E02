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
            start_time = time.time()
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


def normal_operation():
    print("You are in Normal operation mode. Press 'M' to return to the main menu.")
    while True:
        action = input()
        if action.upper() == 'M':
            break

def data_observation():
    print("You are in Data Observation Mode. Press 'M' to return to the main menu.")
    while True:
        action = input()
        if action.upper() == 'M':
            break

def maintenance():
    print("You are in Maintenance Mode. Press 'M' to return to the main menu.")
    while True:
        action = input()
        if action.upper() == 'M':
            break

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


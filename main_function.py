#main function file 
import time 
results = []

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

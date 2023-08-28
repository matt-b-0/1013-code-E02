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
            if len(results)%20 ==0:
                graph_data()
    except KeyboardInterrupt:
        selection_menu()
        


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

    
    pass
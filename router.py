import subprocess
import sys
import time
import select

from simulation import read_hardware_state, write_hardware_state, calculate_f, mutate_hardware, mutate_database, create_hardware_file, file_path

def print_cli_history(history):
    for entry in history:
        print(entry)

def process_cli_input(file_path, history, t):
    # Process CLI input here
    try:
        user_input = input("Enter CLI command: ")
        command, *args = user_input.split()
        if command == "set":
            index = int(args[0]) - 1
            value = int(args[1])
            if index < 0 or index >3 :
                print(f"Invalid Input - Error: {index}")
            else:
                mutate_database(file_path, index, value)
                history.append(f"{t} set {index} {value}")
    except Exception as e:
        print(f"Invalid Input - Error: {str(e)}")
        
def handle_ctrl_traffic(control_values, signal_values):
    
    index = signal_values[0]                #Extracting the index to modify from signal_valuees
    value = signal_values[1]                #Extracting the value to replace with from control_valuees
    
    if (1 <= index <= len(control_values)):               #Handling index out of bounds
        control_values[index - 1] = value
        return control_values       
        
        
    print(f"Invalid Index - Error: {index}")
    
def cron_job(state_values, t, history):
    
    if (t % 10 == 0):
        history.append(F"{t} swap {state_values[0]} {state_values[1]}")
        state_values[0], state_values[1] = state_values[1], state_values[0]
    
    return state_values


def main():
    history = []
    t = 0


    while t < 60:
        state_values, control_values, signal_values = read_hardware_state(file_path)
        t += 1
        #print(state_values)
        # Write Your Code Here Start
        
        
        control_values = handle_ctrl_traffic(control_values, signal_values)
        #print(control_values)
        
        state_values = cron_job(state_values, t, history)
        
        process_cli_input(file_path, history, t)
        print(state_values)
        
        
        # Write Your Code Here End

        time.sleep(1)  # Wait for 1 second before polling again
    print(history)

if __name__ == '__main__':
    main()
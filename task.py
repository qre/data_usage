import os
import psutil
import time
import sched
import threading
import csv
import datetime

# setting up time interval:
s = sched.scheduler(time.time, time.sleep)

# getting the file path from user:
user_input_file = str(input("Enter the path of your file: "))

# getting time interval from user:
user_input_time = int(input("Enter the time interval for collecting data (in seconds): "))

# making sure the path exists/is correct:    
assert os.path.exists(user_input_file), "I did not find the file at, "+str(user_input_file)
print("File found!")

# optional block. i don't know if this program is supposed to run as a standalone or as part of a module. 
# Nevertheless, i decided to include it for good practice.
if __name__=="__main__":    
     
    # creating/updating csv file:
    with open('resources_usage.csv', 'w') as f:
        output = csv.writer(f)
        output.writerow(['program', 'time', 'working set', 'Private bytes', 'cpu %', 'open handles/fd'])

        # main function
        def collect_data():
            filename = os.path.basename(user_input_file)
            for proc in psutil.process_iter():
                if filename in proc.name() :
                    pinfo = proc.pid
                    p = psutil.Process(pinfo)

                    # displaying and saving time and date:
                    now = datetime.datetime.now()
                    print ("Current date and time : ")
                    print (now.strftime("%Y-%m-%d %H:%M:%S"))

                    # displaying and saving the memory:
                    p.memory_info()
                    ws = p.memory_info().wset / 1024
                    pb = p.memory_info().private / 1024          
                    print(f"Working set : {p.memory_info().wset / 1024}KB; Private bytes : {p.memory_info().private / 1024}KB; ")

                    # displaying and saving cpu% usage:
                    cpp = p.cpu_percent(interval=user_input_time)/ psutil.cpu_count()
                    print('cpu % is:', p.cpu_percent(interval=user_input_time)/ psutil.cpu_count())

                    # displaying and saving number of open handles(fd's):
                    openh = len(p.open_files())
                    print('number of open handles/fd is:', len(p.open_files()))

                    # saving data to csv:
                    output.writerow([filename, now, ws, pb, cpp, openh])

                    s.enter(user_input_time, 1, collect_data)

        # threading is not really neccessary here but i decided to include it anyway :)
        x = threading.Thread(target=collect_data)
        print("Collecting data...")
        x.start()    

        s.enter(user_input_time, 1, collect_data)
        s.run()

f.close()

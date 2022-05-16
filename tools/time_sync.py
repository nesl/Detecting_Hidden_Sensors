import pyshark
import numpy as np
from pytz import timezone
import pytz, datetime
import pandas as pd
import os

def split(word): 
    return [char for char in word]  

def convert(s): 
  
    # initialization of string to "" 
    new = "" 
  
    # traverse in the string  
    for x in s: 
        new += x  
  
    # return string  
    return new 

local = pytz.timezone ("America/Los_Angeles")


file_imu = 'imu_r_4.csv'
file_wireshark = 'wifi_r_4.pcapng'

cap = pyshark.FileCapture(file_wireshark)
df = pd.read_csv(file_imu)
imu_data = df.to_numpy()

end = df.size

start_time = imu_data[0,0]
start_time = start_time.replace("_"," ")
split_start = start_time.split()
start_a = split_start[0]
start_b = split_start[1]
start_b = start_b.replace("-", ":")
list_start = split(start_b)
count_start = 0
for i in range(0, len(list_start)):
	if list_start[i] == ":":
		count_start = count_start + 1
	if list_start[i] == ":" and count_start == 3:
		list_start[i] = "."
start_b = convert(list_start)
start_time = start_a + " " + start_b
start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
# start_time = start_time.astimezone(datetime.timezone.utc)
end_time = imu_data[-1,0]
# end_time = end_time.astimezone(datetime.timezone.utc)
end_time = end_time.replace("_"," ")
split_end= end_time.split()
end_a = split_end[0]
end_b = split_end[1]
end_b = end_b.replace("-", ":")
list_end = split(end_b)
count_end = 0
for i in range(0, len(list_end)):
	if list_end[i] == ":":
		count_end = count_end + 1
	if list_end[i] == ":" and count_end == 3:
		list_end[i] = "."

end_b = convert(list_end)
end_time = end_a + " " + end_b
end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
# end_time = end_time.astimezone(datetime.timezone.utc)
start_frame = 0
end_frame = 0

# Finding the number of packets in cap
i = 0
for p in cap:
	i = i + 1
print ("Total packets in this capture:", i)

minima_start = datetime.timedelta(1000)
minima_end = datetime.timedelta(1000)

j = 0
diff1 = 0

for j in range(0,i):
	packet = cap[j]
	try:
		time_packet = packet.sniff_time
		utc_dt = time_packet.astimezone(pytz.utc)
		utc_dt = utc_dt.astimezone(timezone('US/Pacific'))
		utc_dt = utc_dt.replace(tzinfo=None)
		start_time = start_time.replace(tzinfo=None)
		end_time = end_time.replace(tzinfo=None)
		diff1 = abs(utc_dt - start_time)
		diff2 = abs(utc_dt - end_time)
		if diff1 < minima_start:
			minima_start = diff1
			start_frame = j
		elif diff2 < minima_end:
			minima_end = diff2
			end_frame = j
	except AttributeError:
		print("Error, skipping this packet:", packet.number)
		error_pack_num = error_pack_num + 1
		continue

print ("start_frame: ", start_frame)
print ("end_frame : ", end_frame)


new_file_name = 'new_' + file_wireshark

command = 'editcap -r ' + file_wireshark + ' ' + new_file_name + ' ' + str(start_frame) + '-' + str(end_frame)

os.system(command)
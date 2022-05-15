import pyshark
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

file_name = 'new_v_test8'
filename = '../data/' + file_name + '.pcapng'
cap = pyshark.FileCapture(filename) # File capture object

# Finding the number of packets in cap
total_packets_in_cap = 0
for p in cap:
	total_packets_in_cap = total_packets_in_cap + 1
print ("Total packets in this capture:", total_packets_in_cap)

tx_rate_array = []
RSSI_array = []
pkt_num = 0
broadcast_num = 0
arp_num = 0
error_pack_num = 0
j = 0
payload_size = 0
csv_array = ['Tx_ma', 'RX_ma', 'SRC_ma', 'DST_ma', 0000,'RSSI', 'TX_rate', 'Time_sniff', 'Seq']
csv_array2 = ['Tx_ma', 'RX_ma', 'SRC_ma', 'DST_ma', 0000,'RSSI', 'TX_rate', 'Time_sniff', 'Seq']
for j in range(total_packets_in_cap):
	packet = cap[j]
	protocol = packet.transport_layer # Find out if the protocol is TCP or not
	pkt_num = pkt_num + 1
	try:
		payload_size = packet.length
		payload_size = int(payload_size) 
		tx_ma = (str)(packet.wlan.ta) 
		rx_ma = (str)(packet.wlan.ra) 
		src_ma = (str)(packet.wlan.sa)  
		seq = (int)(packet.wlan.seq)
		dst_ma = (str)(packet.wlan.da)
		time_packet = packet.sniff_time
		rssi = (int)(packet.wlan_radio.signal_dbm)
		tx_rate = (float)(packet.wlan_radio.data_rate)
		if rx_ma == 'ff:ff:ff:ff:ff:ff':
			broadcast_num = broadcast_num + 1
			print("broadcast, skipping this packet:", packet.number)
			continue
		if rx_ma == '00:00:00:00:00:00':
			arp_num = arp_num + 1
			print("ARP Request, skipping this packet:", packet.number)
			continue
		data_array = [tx_ma, rx_ma, src_ma, dst_ma, payload_size, rssi, tx_rate, time_packet, seq]  
		csv_array2 = np.vstack([csv_array2, data_array])
	except AttributeError:
		print("Error, skipping this packet:", packet.number)
		error_pack_num = error_pack_num + 1
		continue
	# print(packet.number)


seq_check = []
mac_check = []
time_s_check = []
time_m_check = []

for i in range(1,len(csv_array2)):
	flag = 0
	flag1 = 0
	flag2 = 0
	final_flag = 0
	red = -1
	seq_1 = csv_array2[i, 8]
	mac_1 = csv_array2[i, 0]
	time_s_1 = csv_array2[i,7].second
	time_m_1 = csv_array2[i,7].minute
	for j in range(1,len(seq_check)):
		if seq_check[j] == seq_1:
			red = j
	if red != -1 and mac_check[red] == mac_1:
		flag = 1
	else: 
		flag = 0
	if red != -1 and time_s_check[red] == time_s_1:
		flag1 = 1
	else:
		flag1 = 0

	if red != -1 and time_m_check[red] == time_m_1:
		flag2 = 1
	else:
		flag2 = 0

	if flag == 1 and flag1 == 1 and flag2 == 1:
		final_flag = 1
	else:
		final_flag = 0

	if final_flag == 0:
		csv_array = np.vstack([csv_array, csv_array2[i,:]])
	seq_check.append(seq_1)
	mac_check.append(mac_1)
	time_m_check.append(time_m_1)
	time_s_check.append(time_s_1)



useful_pkts = pkt_num - (broadcast_num + arp_num + error_pack_num)

print('Total packets:', pkt_num)
print('Total skipped broadcast messages:', broadcast_num)
print('Total skipped ARP messages:', arp_num)
print('Total packets with error:', error_pack_num)
print('Total useful packets:', useful_pkts)
csv_array = np.asarray(csv_array)
print('Final shape', csv_array.shape)
packet_info_path = '../data/' + file_name + '_packet_info' + '.csv'
np.savetxt(packet_info_path, csv_array, delimiter=",",fmt='%s')

i = 0
done = []
rx_array = []
tx_array = []
for i in range(1,len(csv_array)):
	total_bits = (int)(csv_array[i,4])
	if i not in done:
		current = csv_array[i,0]
		done.append(i)
	else:
		continue
	for j in range(len(csv_array)):
		if j not in done:
			if csv_array[j,0] == current:
				total_bits = total_bits + (int)(csv_array[j,4])
				done.append(j)
	tx_a = [current, total_bits]
	if len(tx_array) == 0:
		tx_array = tx_a
	else:
		tx_array = np.vstack([tx_array, tx_a])

done1 = []
for i in range(1,len(csv_array)):
	total_bits = (int)(csv_array[i,4])
	if i not in done1:
		current = csv_array[i,1]
		done1.append(i)
	else:
		continue
	for j in range(len(csv_array)):
		if j not in done1:
			if csv_array[j,1] == current:
				total_bits = total_bits + (int)(csv_array[j,4])
				done1.append(j)
	rx_a = [current, (int)(total_bits)]
	if len(rx_array) == 0:
		rx_array = rx_a
	else:
		rx_array = np.vstack([rx_array, rx_a])

tx_array[:,1] = tx_array[:,1].astype(int)

# Sort by total bits
tx_array[tx_array[:,1].argsort()]
rx_array[rx_array[:,1].argsort()]

print('-------------------')
print('Receivers')
print(rx_array)
print('-------------------')
print('Transmitters')
print(tx_array)
# print (packet)

# seq_current = csv_array[0, 8]
Mac = input("Input MAC address of the device you want to monitor: ")
sequence = []
va = 0

x1 = []
y1 = []
for i in range(len(csv_array)):
	seq_new = csv_array[i, 8]
	if Mac == csv_array[i,va]:
		x1.append(csv_array[i,7])
		y1.append(csv_array[i,4])
		sequence.append(seq_new)

h1 = [] # Hours
m1 = [] # minutes
s1 = [] # seconds
mu1 = [] # microseconds
temp_mu = 0
for j in range(len(x1)):
	h1.append(x1[j].hour)
	m1.append(x1[j].minute)
	s1.append(x1[j].second)
	temp_mu = x1[j].microsecond / 100000 # first digit of the microsecond
	temp_mu = int(temp_mu)
	mu1.append(temp_mu)


aggregated_data = []
kk = 0
h11 = h1[0]
m11 = m1[0]
s11 = s1[0]
mu11 = mu1[0]
h12 = h1[len(h1)-1]
m12 = m1[len(h1)-1]
s12 = s1[len(h1)-1]
mu12 = mu1[len(h1)-1]

time_bins = 36000*(h12-h11) + 600*(m12 - m11) + 10*(s12 - s11) + mu12 - mu11 + 1
aggregated_data = np.zeros((time_bins,), dtype=int)
data_sum = 0
for k in range(len(y1)):
	bin1 = 36000*(h1[k] - h11) + 600*(m1[k] - m11) + 10*(s1[k] - s11) + mu1[k] - mu11
	aggregated_data[bin1] = aggregated_data[bin1] + y1[k]



dates = matplotlib.dates.date2num(x1)
list_x = range(len(aggregated_data))
save_foo = '../data/' + file_name + '.csv'
np.savetxt(save_foo, aggregated_data, delimiter=",")
plt.plot(aggregated_data)
plt.xlabel('# of samples')
plt.ylabel('Payload in bytes')
plt.show()


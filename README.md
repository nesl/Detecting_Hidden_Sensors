# Detecting_Hidden_Sensors

This repository is based on our work from our [USENIX Security paper](https://www.usenix.org/conference/usenixsecurity21/presentation/singh)

In this repository, we will use Camera as an example to show how our framework can be used to detect hidden clandestine sensors.

### Data

We are providing aggregated data files for testing our code. The data files are available in the `data` folder. The folder contains 2 sub-directories.
1. `wifi_imu_pairs` -> Contains wifi traffic aggregate for cameras and corresponding IMU data for user motion. e.g., `imu_v_test10.csv` and `wifi_v_test10.csv` where letters `v`, `w` etc. represent a camera.
3. `no_cause_and_effect` -> Contains wifi traffic aggregate for a device and corresponding IMU data for user motion. No granger causality is detected in this case.

### Code
1. `scripts` -> contains the wifi data aggregation script based on a particular MAC address.
2. `notebooks` -> contains the code for testing granger causality and other tools to examine the aggregated data. Feel free to play with parameters to see how the performance changes.


### Requirements

1. Wireshark -> https://linuxhint.com/install_configure_wireshark_ubuntu/
2. tshark -> https://zoomadmin.com/HowToInstall/UbuntuPackage/tshark
3. Python version -> Tested on 3.9.7 & 3.6.9
4. install requirements.txt (Virtualenv strongly recommended)
5. To collect IMU data on Android smartphone -> https://github.com/nesl/NTPSenseApp
6. For DeadReckoning on an Android smartphone -> https://github.com/nisargnp/DeadReckoning


### Troubleshooting

1. Range: The performance depends upon the range of the sensors. For camera, typically the range is within 3m. However, since our framework is created to detect sensors in a small space like a room, the range is more than sufficient. 
2. Improving performance: Since the camera can be placed anywhere in the room, it is suggested that multiple trial be performed in various parts of the room to increase the chances of detection.

### How to collect your own datasets?

* Wireshark:
  * Online tutorial to select a particular frequency and use Wireshark in monitor mode -> https://linuxhint.com/capture_wi-fi_traffic_using_wireshark/
  * Use the tutorial above to scan all the frequencies that your Wi-Fi card supports
* Time:
  * Use NTP for time synchorinization. The NTPSenseApp uses [Good Clock](https://github.com/nesl/GoodClock) to synchronize it's time with NTP.
  * You can force an NTP sync on the laptop using `sudo sntp -s <NTP Server>`. Alternatively, you can stop and restart the `ntp` service on your device.
* Data collection: 
  * Use wireshark to collect `.pcapng` files.
  * Use [NTPSenseApp](https://github.com/nesl/NTPSenseApp) to collect IMU data on your smartphone.
* Time sync between packet capture and IMU:
  * Use the `time_sync` script in the `tools` folder to time synchronize the packet capture with IMU.
  * The script 'crops' the .pcapng file to closest time stamps to the IMU on either side.
* Data aggregation
  * Use the `aggregate_data` script to extract traffic for every device.

### MAC Address Lookup

There are several online MAC lookup services. You may not be able to find everything using just one lookup website. We recommend using a combination. Some of them are listen below:
1. https://www.macvendorlookup.com/
2. https://dnschecker.org/mac-lookup.php
3. https://maclookup.app/
4. https://macaddress.io/

If a device is detected as a hidden sensor snooping on the user but is not found in any lookup databases, you can add it to a local file. We used following tools where you can lookup vendor MAC addresses by keywords: https://www.adminsub.net/mac-address-finder/camera

### FAQ

* Can you provide raw .pcapng files?
  * Due to privacy concerns (as pcapng files expose a lot of information about the network), we are not sharing the .pcapng files. We have instead shared aggregated data files in the data folder.
  * If you want, please email at the address below and we can send you a few sample files.

### Questions:

> Questions can be directed to `akashdeepsingh@ucla.edu`

### Contribute (To-Dos):

- [x] First release
- [ ] Optimize the code for time and memory
- [ ] Realtime implementation
- [ ] Bug fixes
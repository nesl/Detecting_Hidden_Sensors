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

1. OS -> Tested on Ubuntu 18.04 and Ubuntu 20.04
2. Wireshark -> https://linuxhint.com/install_configure_wireshark_ubuntu/
3. tshark -> https://zoomadmin.com/HowToInstall/UbuntuPackage/tshark
4. Python version -> Tested on 3.9.7 & 3.6.9
5. install requirements.txt (Virtualenv strongly recommended)
6. To collect IMU data on Android smartphone -> https://github.com/nesl/NTPSenseApp
7. For DeadReckoning on an Android smartphone -> https://github.com/nisargnp/DeadReckoning

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


### I am using Wireshark but cannot capture any data packets from the camera/other sensor! What should I do?

1. Is the camera live streaming? For most IP cameras, you would need to open the corresponding app on a smartphone and view the live feed to make sure it is live streaming.
2. Is the camera transmitting in the same frequency band as the one which is being sniffed by wireshark?
3. Is wireshark being used in [monitor mode](https://github.com/nesl/Detecting_Hidden_Sensors/#how-to-collect-your-own-datasets) to sniff packets? 
4. Lastly check settings of the camera. Is it using H.264/H.265 encoding? Is it storing data locally and transmitting it to the cloud afterwards (asynchronously) (a way to fool SnoopDog)?

### Cannot detect causality despite performing S5 motion. What should I do?

1. Is the space small or large? Typical room sizes in are around 10 feet x 10 feet. Causality will not be detected if the camera is very far from the user.
2. Start at the center of the room and do the S5 motion. Then move to different areas. Each S5 motion should take around 35-45 seconds.
3. There are two flags that help detect causality -> `granger_flag` and `overlap_flag`. Both flags need to be 1 in order to detect causality. `granger_flag` is used to detect causality and comes from the granger causality computation from the `statsmodel` package. `overlap_flag` is used to reduce false positives (since sometimes the granger_flag maybe 1 even when the camera traffic is 0.
4. You can fine tune the threshold for both `granger_flag` and `overlap_flag` based upon your experiments.
5. `overlap_flag` is to prevent obvious false positive cases and can be ignored i.e. only check the output of `granger_flag` and not `overlap_flag`.
6. Additionally, some users have reported that using `wifi_data_norm` instead of `wifi_dataa` works better in granger_tests (Block 40 of the notebook).
7. Make sure there is not motion in the IMU during the `STOP` phase of S5 motion.

### Misc Troubleshooting

1. Monitor mode: The most common question we receive is people not able to capture any packets. This is always because they were not following the steps [described here](https://github.com/nesl/Detecting_Hidden_Sensors/#how-to-collect-your-own-datasets) and were instead using Airmon.
2. Jumping jacks: The user must maintain a constant frequency while performing the jumping jacks. Also, ideally the duration of jumping jacks within the same trial should be similar. We acknowledge that this requires some practice and can be challenging for certain individuals.
3. Scanning with Wireshark: We have had some questions regarding people not being able to see any traffic being sent by the camera on their wireshark capture. If the camera was indeed livestreaming, then the only reason for this is that the frequency at which the camera was transmitting and the frequency at which Wireshark was scanning are not same. In case the camera is multi-band (2.4/5 GHz), please ensure that the frequency of tranmission and scanning are the same.
4. Range: The performance depends upon the range of the sensors. For camera, typically the range is within 3m. However, since our framework is created to detect sensors in a small space like a room, the range is more than sufficient. 
5. Improving performance: Since the camera can be placed anywhere in the room, it is suggested that multiple trials be performed in various parts of the room to increase the chances of detection.

### FAQ

* Can you provide raw .pcapng files?
  * Due to privacy concerns (as pcapng files expose a lot of information about the network), we are not sharing the .pcapng files. We have instead shared aggregated data files in the data folder.
  * If you want, please email at the address below and we will see if we can send you a sample file.

### Questions:

> Questions can be directed to `akashdeepsingh@ucla.edu`

### Contribute (To-Dos):

- [x] First release
- [ ] Optimize the code for time and memory
- [ ] Realtime implementation
- [ ] Bug fixes

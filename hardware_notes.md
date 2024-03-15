## Details on Hardware

Overview of the cluster's hardware, tips and tricks, problems I've run into and future plans. 


### General 
* Get as much RAM as you can, the basic setup for this cluster with just the three control nodes, Prometheus for monitoring, ingress and encryption setup/configuration(s), longhorn and Rancher was using close to 40 GB of RAM before I started deploying workloads. I.e. if you're going to follow my setup, I'd suggest maxing out on RAM. 
* Uninterrupted Power: 
    * I'm using a CyberPower CyberPower CP1500PFCLCD PFC UPS unit for the three server/control nodes, my main switch, the firewall and the modem from my ISP. The monitoring software is rather rudimentary and you can only get data via CLI commands, ingesting that data into InfluxDB for monitoring and alerts is on my list. 
    * Small portable batteries for charging phones and tablets are connected to the single board computer nodes, similar to the above I want to upgrade those units to something I can manage remotely and send me alerts if/when the power goes out. 
* "Custom" Firewall is a Trigkey N100 device with dual 2.5Gbe running pfSense.

### Device Notes & Data

#### Beelink SER5s - Ryzen 5 5560U
* These have been problem free, I got them, opened them up, replaced the RAM and NVME drives that came with them, installed Ubuntu and it's been smooth sailing ever since.
* The fans give off a a slight "whir" noise in the background and they'll spin up more when you deploy services, however, you can reduce the temps and noise by placing them on their sides.
* Depending on the benchmark, they give me about 80-90% of the performance of my 11th Gen Intel i5 with the power limits turned off, so to say they've been a steal is an understatement. 

#### Orange Pi 5+ - Rockchip3588 
* Multi-core benchmarks are roughly equivalent to an Intel N95, only with full speed Gen3 NVME, dual 2.5Gbe and a 6 TOPS NPU for running machine learning workloads. 
* The device is running the excellent [Ubuntu for Rockchip 3588 devices](https://github.com/Joshua-Riek/ubuntu-rockchip) community distro created by Joshua Riek. 
* I added the device around 2/10 and have it running the majority of the ETL workloads, Mosquitto and some IoT related workloads (monitoring smart plugs) and it has been troublefree so far save an instance of having to restart the Wi-Fi. CPU utilization is around 5% and temps for System on a Chip *(SOC), CPU, GPU, et al, rarely go above 50 degree C.
* Once I replaced the Wi-Fi card with a USB Wi-Fi dongle the device has been trouble free and I almost never hear the fan. 

#### Orange Pi 3B
* Depending on your benchmark you get about 50-80% of the performance of a Raspbery Pi 4B, only with onboard NVME and eMMC support.
* Deploying workloads fresh to the device rarely caused an issue, but moving some workloads from another node can cause this error when you get a "pod out of memory" error and new pods being constantly generated. This doesn't happen on the other nodes with the same workload so I suspect it's something specific to the Orange Pi 3B and its community Armbian distro. 
    * Note: I'm using this distro because a) it's faster the ones created by Orange Pi, as in faster sysbench and Geekbench results. E.g, 2,200 vs 3500 total sysbench events b) I'm not too keen on downloading a distro that sits on a Google drive. 
* **update(s):** 
    * I removed this device from the cluster in late Jan '24, as the "pod out of memory" errors were occuring with increasing frequency despite the device having more than enough memory to run the pods in question. I suspect the issues were because the cluster couldn't see the device's available RAM/it never showed up in the cluster overview in Rancher. 
    * The same developer who created the Ubuntu disti I used for my Orange Pi 5+ recently created a Ubuntu disti for this device, so once I finish some more testing and getting the device configured I'll use it for a beta/testing cluster.

#### Raspberry Pi 4Bs 
* **Update: ** am going to replace these devices with ESP32s, Raspbery Pi Picos for sensors and Orange Pi 5+ for general workloads, the reason for the former is the smaller size and lower power draw, and the reason for the latter is the Orange Pi 5 Plus' higher CPU performance + significantly faster storage, even when compared to a Raspberry Pi 5. Medium term these devices will be used for a k8s test cluster and other projects.
* There are three 8GB RPI 4Bs in the cluster, two are "sensor nodes" that are just being used for collecting data from USB and GPI0 based sensors and a third I use for prototyping/testing GPIO related containers. 
* No issues save Prometheus errors when I tried to run a 4GB Pi 4B due to it not having enough RAM. 
* The prototyping RPI has an NVME hat and a PWM fan that only comes on when temps go above 55 degrees celsius, both have worked flawlessly. 
* Originally I had the "sensor nodes" running with "no schedule" taints, but given how little of their resources were being used running sensors I decide to just make them general worker nodes. Medium term I may redeploy them in a beta cluster for testing and use ESP32s for collecting sensor data, however, ESP32s aren't as convenient for deploying code updates for the sensors as I'd have to physcially connect the device to my dev box and flash the device vs deploying new containers via Kubernetes. 
* I've excluded these devices from sharing their storage as part of the longhorn service, meaning they store data on the control nodes over the network. Hopefully, this will mitigate the inevitable degradation of their SD cards.

### Planned Future Devices
* Move sensors to ESP32s and/or Raspberry Pi Picos
* Swap out the Raspberry Pi 4Bs and use Orange Pi 5+ (32GB RAM variants) as arm64 worker nodes, the Raspberry Pis will be used for other projects and/or a beta/testing cluster.
*  HP Omni G4 800 (or similar) as storage nodes and to run MinI0, as they're relatively inexpensive and have three NVME slots
* May purchase some x86 worker nodes (refurbished devices) so the Beelink can be control nodes only; this would largely to get practice with managing more complexity. I.e, over-engineering for educational purposes.
* A second UPS for my dev box, monitors and other key devices in my office.
* A separate UPS solution for the Orange Pi 5+ that can be remotely monitored and run several hours off of batteries if not solar. 
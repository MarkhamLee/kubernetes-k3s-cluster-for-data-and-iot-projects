## Hardware Monitoring

The following are a collection of containers used for monitoring K3s hardware, external servers and general infrastructure. Monitoring for individual servers have the option to push "heartbeat" data to Prometheus and Uptime Kuma, to provide near real time alerting if a device goes offline. 

### K3s Nodes

While I use Prometheus to monitor kubernetes, container, workload activity, et al, in addition to CPU load, RAM usage and the like, I created these monitoring containers to pull additional data via the python psutil library: 

* CPU Temps
* NVME temps
* Current CPU frequency 
* For GPU and NPU temps for single board computers running a Rockchip System on a Chip (SOC)

All of the data is written to InfluxDB for viewing via Grafana. While not implemented, the psutil library can also pull per core utilization and temperatures. 

### External Nodes 

An Orange Pi 5+ and a Raspberry Pi 5 are used to run Technitium and other external to K3s workloads. 


### Infrastructure Devices

* I use [Network UPS Tools - NUT](https://networkupstools.org/) to monitor the UPS' attached to my cluster in real time: a Raspberry Pi running NUT server is connected to the UPS via USB, and a container running on the cluster queries the NUT server every 20 seconds and then writes the data to InfluxDB for viewing via Grafana.

## Hardware Monitoring

### K3s Nodes

While I use Prometheus to monitor kubernetes, container, workload activity, et al, in addition to CPU load, RAM usage and the like, I created these monitoring containers to pull additional data via the python psutil library: 

* CPU Temps
* NVME temps
* Current CPU frequency 
* For GPU and NPU temps for single board computers running a Rockchip System on a Chip (SOC)

All of the data is written to InfluxDB for viewing via Grafana. While not implemented, the psutil library can also pull per core utilization and temperatures. 


### Additional Hardware

* I use [Network UPS Tools - NUT](https://networkupstools.org/) to monitor the UPS' attached to my cluster in real time: a Raspberry Pi running NUT server is connected to the UPS via USB, and a container running on the cluster queries the NUT server every 20 seconds and then writes the data to InfluxDB for viewing via Grafana.




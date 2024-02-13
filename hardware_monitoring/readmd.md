## Supplemental Hardware Monitoring

While I use Prometheus to monitor kubernetes, container, workload activity, et al, in addition to CPU load, RAM usage and the like, I created these monitoring containers to pull additional data via the python psutil library: 

* CPU Temps
* NVME temps
* Current CPU frequency 
* For GPU and NPU temps for single board computers running a Rockchip System on a Chip (SOC)

All of the data is written to InfluxDB for viewing via Grafana. While not implemented, the psutil library can also pull per core utilization and temperatures. 



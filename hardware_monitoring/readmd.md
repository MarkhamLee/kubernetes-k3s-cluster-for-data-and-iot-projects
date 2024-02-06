## Supplemental Hardware Monitoring

While I use Prometheus to monitor kubernetes, container, workload activity, et al, in addition to CPU load, RAM usage and the like, I created these containers to give me additional data on CPU temps. The containers use the psutil library to get CPU temps, NVME temps and the like, and then writes that data to InfluxDB for monitoring via Grafana. I also have containers for monitoring the agent nodes (Raspberry Pis, Orange Pis and similar) that can be found [here](https://github.com/MarkhamLee/productivity-music-stocks-weather-IoT-dashboard/tree/main/telemetry). 


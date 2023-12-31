### Deploying General Container Workloads 

For one of my projects this is the values file I used to deploy a container per each of the smart plugs I use to monitor how much energy my homelab (and its associated devices) are using. The containers use the python-kasa library to regularly pull data from the plugs, and then some custom code is used to write the data into InfluxDB that is later visualized via Grafana. This file can be easily adapted for any container that receives data or performs some other tasks, but doesn't receive data on an endpoint/is running an API. For containers that are running API applications, see the deploy-container-with-ingress folder in this folder's parent directory. 


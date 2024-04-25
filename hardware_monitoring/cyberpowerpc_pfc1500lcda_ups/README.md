### Real Time UPS Monitoring

This folder contains resources related to monitoring UPS devices connected via Serial or USB to a server on your network, via Network Ups Tools(NUT).

* You can find the code for building a container for monitoring a UPS, plus setup details in the repo for my data platform [here](https://github.com/MarkhamLee/ finance-productivity-iot-informational-weather-dashboard/tree/main/IoT/cyberpowerpc_pfc1500_ups) 
    * I plan to manage the code for monitoring the UPS in that repo, but if I have to make customizations to manage a UPS that *only* supports the Kubernetes cluster and/or has extra features that are only for Kubernetes than I'll maintain that separate version here.
* Once you have NUT configured you can use the "quick_test.py" file to see what data points are available from your particular UPS. 
* An example deployment manifest is available in this folder as well

Future plan is to have code in this repo for receiving shutdown commands and safely shutting down Kubernetes nodes. 

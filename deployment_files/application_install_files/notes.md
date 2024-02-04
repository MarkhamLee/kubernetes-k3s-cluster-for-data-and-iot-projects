## Overview

Installing applications on Kubernetes can be frustrating at times between helm chart variants, 1,000 line yaml manifests, stumbling the wrong or out of date instructions and that's before you encounter post installation "gotchas" that are rarely mentioned. This folder contains installation instructions, values.yaml files, tips, tricks and "gotchas" for the applications I've deployed on my Kubernetes cluster. I've also included information on the settings, tweaks, etc., you need to change once you've got something deployed in order to keep it running. 

### Current Apps 

These instructions presume you have enough control of your firewall/router/local network to setup domains (i.e., nodered.local.example.com) on your home network in order to support proper ingresses for each service, are using secure certs for your k8s cluster, are using something like Longhorn for distributed/cluster wide storage and have enough hardware to deploy apps as HA if you so choose. The deployment methods are a mixture of Helm Charts, deploying kubernetes manifests via the command line and installing via the Rancher UI. Meaning: the artifacts in each folder will vary depending on how I deployed that particular service, however you can typically expect to find written instructions, ingress files and a values.yaml for each service. 

* Airflow 
* Eclipse-Mosquitto
* Grafana
* InfluxDB
* Loki-Stack
* Longhorn install instructions - **Updated 02/03/24**
* Mosquitto
* Node-Red
* Rancher
* PostgreSQL 
* Zigbee2MQTT - **Updated 02/03/24**


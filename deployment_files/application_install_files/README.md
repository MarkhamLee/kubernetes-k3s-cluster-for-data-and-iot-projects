## Overview

Installing applications on Kubernetes can be frustrating at times between helm chart variants, 1,000 line yaml files, stumbling upon the wrong or out of date instructions, etc., and that's before you encounter post installation "gotchas" that are rarely mentioned. This folder contains installation instructions, values.yaml files, tips, tricks and "gotchas" for the applications I've deployed on my Kubernetes cluster. I've also included information on the settings, tweaks, etc., you need to change once you've got something deployed in order to keep it running. At the moment I use Argo CD + Helm to deploy apps on my cluster, but these instructions can be adapted to command line style deployments using Helm. 

The typical deployment pattern involves an Umbrella Chart and a values.yaml placed in a GitHub repo monitored by Argo CD, when Argo CD is pointed to a the folder containing the two files it then deploys the app to the cluster. I took this approach so things are more "GitOps" and consistent, and because it seems to reduce the number of gotchas vs using deployment manifests or deploying things from the available charts with Rancher. I have examples for each app here, but maintain a separate private repo with the Chart.yaml and values.yaml files.

Example Chart.yaml file - make sure you spell chart with a capital "C", otherwise ArgoCD won't pick it up. 
```
apiVersion: v2
name: airflow
description: Umbrella chart for deploying Airflow
type: application
version: 0.1.0
appVersion: "0.1.0"
dependencies:
  - name: airflow
    version: 18.3.7
    repository: oci://registry-1.docker.io/bitnamicharts
    alias: airflow
    condition: airflow.enabled
```
In the values.yaml file the alias is the top key, so all of the typical values.yaml, well values, have to be shifted to the right. 

There are a few instances where I didn't use helm, and in those cases, the deployment manifest, service definitions and the like are placed in GitHub, and from there it's the usual pattern where Argo CD is pointed to the folder containing those files, where it can pick the items up and deploy the app to Kubernetes. 

### Prerequisites

These instructions presume you have enough control of your firewall/router/local network to setup domains (i.e., nodered.local.example.com) on your home network in order to support proper ingresses for each service, are using secure certs for your k8s cluster, are using something like Longhorn for distributed/cluster wide storage and have enough hardware to deploy apps as HA if you so choose.  

### Current Apps

Note: I recently finished migrating everything to Argo CD, so many of the folders are in the process of being updated.

* Airflow 
* ArgoCD
* Argo Workflow
* Eclipse-Mosquitto
* Grafana
* InfluxDB
* Loki-Stack
* Longhorn install instructions - **Updated 02/03/24**
* Mosquitto
* Node-Red
* pgAdmin
* Rancher
* PostgreSQL 
* Zigbee2MQTT - **Updated 02/03/24**


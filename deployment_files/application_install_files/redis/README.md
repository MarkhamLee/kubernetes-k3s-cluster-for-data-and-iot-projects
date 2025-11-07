## Deploying Redis via Kubernetes Manifests

Previously, this was a Helm chart deployment using umbrella chart + values.yaml via ArgoCD, but with Bitnami putting their Helm charts behind a pay wall, I had to transition this (and others) to a Kubernetes manifests based on the official Redis Docker image for redis. Keep in mind that this was deployed using the official docker image for redis-stack-server, if you just use regular redis a lot of the settings I put into the deployment files to enable passwords, replicas and masters writing to persistent volumes, etc., won't work. 

* The master and replica stateful sets are to ensure that you have multiple instances running, if you feel you need more replicas  you can set the number of replicas in the statefulset_replicas.yaml file. 
* Make sure you create a password in Kubernetes and then reference in the stateful set(s)
* The section called "command" in the stateful sets was a touch tricky to work out, but it is critical to ensuring that things work properly:
    * -- requirepass is so that you can specify a password for Redis, as it's default setup is not to use one at all. 
    * --dir /data --dbfilename ... is so that the container has write access to the volumes/persistent storage 

* The node affinity section is optional, I use it because I have specific nodes I run databases and other data related workloads on. 
* Once you have this running properly, I would go back and freeze the docker image version fo Redis, rather than always pulling "latest" - this will ensure that you don't actually introduce breaking changes into your cluster if when a pod restarts. 

Overall, this isn't too difficult to deploy, but coming from using the Helm chart there are just a couple of things you need to account for that were being handled by the Bitnami Helm chart and docker images. 


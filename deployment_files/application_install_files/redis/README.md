## Deploying Redis via Argo CD

This is a fairly straight forward umbrella chart + values.yaml file deployment, but there are a couple of things you can keep in mind:

* The app version is deployed in the Docker image references, so a) need to change it to upgrade Redis and to make sure you have the freshest version and not just what I used when I wrote this values.yaml file 
* You should create Docker pull secrets and add it to the section of the values.yaml for pulling Docker images
* Create a Redis secret in Kubernetes and then reference it in the auth section
* Update the following sections:
    * node affinity section to fit your own architecture for master and replica
    * Add your load balancer IP 


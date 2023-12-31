## Quick Notes

* I used a multi-endpoint container I created for another [project](https://github.com/MarkhamLee/Facial-Recognition-Facenet-Pytorch), it's a facial recogntion app that matches pairs of photos. When I was learning how to deploy these typs of containers I used this one, because, well.. I'm a Data/ML Engineer, so, deploying ML containers is at least one of my engineer *raison d'êtres*
* The container has three endpoints that will each need to be accounted for in the ingress configuration, remember this isn't a web UI where "/" will suffice, you need to route traffic to each endpoint: 
    * /ping - a health endpoint
    * /cached_data - facial recognition endpoint
    * /identity - another facial recognition endpoint 
    * I used Postman and pairs of photos to test everything. 
    * Given that this is a machine learning container you'll need to assign more CPU resources than usual, otherwise it will run fairly slow. I assigned 1000m for CPU to ensure that at least one core was reserved, doing this gave similar performance to what I saw when I tested this container on these devices prior to building the cluster. 
* Presuming you've set everything up right with regards to wildcard certs, your connections will be secure by way of being a subdomain of your secured primary one. That being said, I added certs to this deployment anwyay.
* The files:
    * deployment_service.yaml will deploy the container and create a ClusterIP service for it. To use it, you'll need to tweak the endpoints, container names, etc., to fit your environment and/or project and you should be good to go. One important change is to make sure you're using the same port exposed in your Docker file as the one designated as container port. My suggestion is to just start with this file, and make sure everything is working properly before adding the ingress. I.e., troubleshoot one thing at a time, no need to find yourself unsure if the issue is with the ingress or the service itself. 
        * Be sure to use the IP specifically denoted as the ClusterIP, the IP you'll see when you first click into the deployment in Rancher is the pod IP, NOT the ClusterIP. You can get the ClusterIP from Rancher under services in the left hand menu.  
    * multi-endpoint_ingress.yaml, this file configures the ingress, just make a few changes to customize it for your environment and you'll be good too go. The big frustration I had in figuring this one out was that none of the tutorials I found used a multi-endpoint container, so following them led to the creation of ingresses that didn't work. The hiccup is that I had to configure an ingress for each endpoint within the container. This isn't required if you use a loadbalancer or a ClusterIP, but ingresses are direct routes, so you have to create entries in your ingress file for each endpoint. I eventually figured it out by configuring the ingress in Rancher (you can find it under service discover --> ingress) and then looking at the YAML file that was created. <-- pretty much my go to for fixing YAML issues. 
    * After you configure the files, apply them to your cluster via:

    ~~~
    kubectl apply -f "file-name.yaml",
    ~~~ 

    Once you do this the deployment will show up in Rancher almost instantly, but may take a few minutes to be fully up and running. 
    * **If the ingress doesn't work:**
        * Doublecheck the deployment and service were setup properly 
        * Make sure you're using the same namespace for the deployment, service creation and ingress. It's fairly easy to accidentally create the deployment in the right namespace, the service in default and the ingress in the proper one. 
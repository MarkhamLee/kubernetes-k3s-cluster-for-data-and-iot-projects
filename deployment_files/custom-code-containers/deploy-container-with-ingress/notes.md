### Quick Notes

* I used a multi-endpoint container I created for another [project](https://github.com/MarkhamLee/Facial-Recognition-Facenet-Pytorch), it's a facial recogntion app that matches pairs of photos. When I was learning how to deploy these typs of containers I used this one, because, well.. I'm a Data/ML Engineer, so, deploying ML containers is at least one of my engineer *raison d'êtres*
* The container has three endpoints that will each need to be accounted for in the ingress configuration, remember this isn't a web UI where "/" will suffice, you need to route traffic to each endpoint: 
    * /ping - a health endpoint
    * /cached_data - facial recognition endpoint
    * /identity - another facial recognition endpoint 
    * I used Postman and pairs of photos to test everything. Latency was quite a bit higher than it was when I tested this container on these same machines before I installed K3s, not sure if it's the over head from K3s or if I need to allocate more system resources. *I strongly suspect it's the latter, but that's an experiment for another day* 
* Presuming you've set everything up right with regards to wildcard certs, your connections will be secure by way of being a subdomain of your secured primary one. That being said, I added certs to this deployment anwyay.
* The files:
    * multi-endpoint_container.yaml will deploy the container and create a ClusterIP service for it. Make a few changes to customize for your environment and you're good to go. Be sure to test all your endpoints before you add the ingress. One important change is to make sure you're using the same port exposed in your Docker file as the one designated as container port. 
        * Be sure to use the IP specifically denoted as the ClusterIP, the IP you'll see when you first click into the deployment in Rancher is the pod IP, NOT the ClusterIP. You can get the ClusterIP from Rancher under services in the left hand menu, and use it to test things provided you're on a machine within the cluster. 
        * If something doesn't work
    * multi-endpoint_ingress.yaml: this file configures the ingress, just make a few changes to customize it for your environment and you'll be good too go. The big frustration I had in figuring this one out was that none of the tutorials I found used a multi-endpoint container, so following them led to the creation of ingresses that didn't work. The hiccup is that I had to configure an ingress for each and endpoint within the container. This isn't required if you use a loadbalancer or a ClusterIP, but ingresses are direct routes, so you have to create entries in your ingress file for each endpoint. I eventually figured it out by configuring the deployment in Rancher and then looking at the YAML file that was created. <-- pretty much my go to for fixing YAML issues. 
    * After you configure the files, apply them to your cluster via kubectl apply -f "file-name.yaml" and the ingress will show up in Rancher almost instantly.
    * **If the ingress doesn't work:**
        * Doublecheck the deployment and service were setup properly 
        * Make sure you're using the same namespace for the deployment, service creation and ingress. It's fairly eays to accidentally create the deployment in the right namespace, the service in default and the ingress in the proper one.**
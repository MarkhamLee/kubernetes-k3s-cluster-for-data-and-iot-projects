## Instructions, Tips, Tricks for deploying custom code on Kubernetes

Some helpful information on deploying the workloads that you build yourself to Kubernetes. While it's not terribly difficult, a lot of the tutorials are for very simplistic use cases that don't reflect what you'll be doing in real life. E.g., for a multi-endpoint container you have to create ingresses for each endpoint, something that isn't that intuitive since it isn't required for load balancers, clusterIPs and the like. Hoping to alleviate some of the "getting started pain points" by sharing examples of how to deploy workloads that go beyond the usual "hello world" containers. 


### Preparation 

You'll need to do a few things prior to getting started:
* Create a namespace to deploy your containers in 
* You'll have a repo that you're storing your Docker containers in. I store mine on Dockerhub, but feel free to use whatever suits you.  
* If you're using a container repo that requires you to login/a private repo:
    * Go into Rancher 
    * Select your cluster 
    * On the left hand menu storage --> secrets 
    * Select "Create" in the upper right hand of the screen 
    * Select Registry 
    * Select the namespace you created earlier, create a name for the secret, select your repo and then enter your credentials 
        * Be mindful that a lot of browsers will just drop in your Rancher login credentials (if you've stored them) and will try to update the Rancher login with whatever you input for your registery. I.e. CLICK NO and don't save the credentials when your browswer prompts you 
    * Make note of the name off the secret, you'll reference it later in the yaml file you use to create the deployment. 


#### There is an easier way... 

You don't "technically" have to create YAML files to deploy your containers, there is a much easier "click-ops" way that is far less prone to error, BUT isn't as repeatable or shareable since it's not infrastructure as code. However, it's perfectly fine for a homelab, when you're learning, etc. Part of how I learned to create the YAML files was to configure my deployments in Rancher, then look at the YAML that's created and then use that as basis to create one of my own, as the Rancher YAMLs often insert Rancher specific data/are slightly different, at least to my eyes. 

**So about that easy way**

1) Complete the preparation steps above
2) Go to Rancher 
3) Select deployments in the left hand menu 
4) Select "Create" in the upper right hand of the screen 
5) Select the option that best corresponds to how you want to deploy your code. E.g., Deployment for a stateless application, CronJob for things you want to run on a schedule. StatefulSet for things that need to persist data. 
6) Configure everything as you need it and click create. Note that you can create several containers in one deployment if you need it. 


#### The harder/Infrastucture as Code Way 
* Examples are in the folders 
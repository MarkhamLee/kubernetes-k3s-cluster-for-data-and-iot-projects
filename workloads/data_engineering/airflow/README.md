## Airflow Setup Files

This folder contains everything you'll need to get an Airflow instance up and running on a Kubernetes cluster, but with the caveat that I used this configuration on a local cluster and that when deploying into a cloud environment there will likely be some additional items you'll need to account for. That being said, the major building blocks are here so any changes you have to make "should" be small, but again Kubernetes + Airflow can be, tricky until it isn't. 

For several months I was using the Bitnami Helm chart, but the deployment started to become rather unstable and the worker pod would sometimes crash. I was able to fix this by doing the following:
* Moving to the Helm Chart that was direct from Bitnami rather than the one included in Rancher's chart catalog
* Using external Postgres and Redis instances, rather than the ones that can be deployed with Airflow. 
* Turning off resource limits for the Airflow worker, it doesn't use a lot in day to day use, but when the pods spin-up it can use quite bit of compute and RAM. 

This deployment uses the Chart.yaml umbrella chart for Helm + a values.yaml file as mentioned in the Readme. All changes are made via updating one of those files and then pushing the changes to GitHub. 

#### Folder Contents
* fernet_key_generator.py to ensure your set up is properly secured/encrypted 
* Umbrella chart (Chart.yaml) and values.yaml file for use in deploying via ArgoCD or other kubernetes deployment tools. 
* k8s_resource_examples: an ingress example I used when I was deploying via creating manifests and files for individual resources. 

### Deployment Steps
Suggested appraoch: 

* Take the standard values.yaml file from the Bitnami Helm Chart repo and update the following:
    * Credentials for Postgres and Redis
    * Point things to your GitHub repo for your DAGs
    * Create secrets for Postgres, Redis, Docker and for your Fernet key and then reference them as I did in my values.yaml file
    * Configure an ingress
    * Use the sections that reference external Postgres and Redis, make sure that you set "enabled: false" for the internal ones. 

### Preparation Steps

1) Generate a fernet key via the python script, add that value to the values.yaml file
2) Create a config map with your python dependencies, using the command below:
```
sudo kubectl create -n airflow configmap requirements --from-file=requirements.txt
```
3) Setup a GitHub repo with a basic DAG so you can test a) importing a DAG from a repo b) test the DAG and make sure it works. 

4) This set up revolves specifically around using the Kubernetes Pod Operator, so you'll need (obviously) to have a container registry setup, and containerized versions of your ETL scripts. 

5) Make sure you're familiar with creating Kubernetes secrets and config maps. 

6) Standup a Postgres and Redis instance (if you don't already have one) to support this deployment. 
 

### Suggested Approach
1) Get the initial setup deployed
3) Set-up the Github synch and bring in some basic DAGs and just make sure everything works
4) Once the above is sorted, then move on to changing things like executors, adding extra python dependencies, etc. 


### Key Things to be Aware Of

1) If a prior deployment failed and re-deploy with new settings instead of rolling back, you might want to click into that component to get the pod view, scale it down to zero and then back up to, sometimes the changes won't "take" until you do that. 
2) When looking for hints and helps online, be sure they're using the same version of the Helm chart that you are. I.e., this is the Bitnami version, certain items are different on the chart from Airflow 
3) When I was importing things from Github, it only brought in DAGs not the custom external classes I had built to work with the DAGs. I ended up just using Docker containers for everything to avoid "dependencies hell" (among other reasons), so I didn't dig much into it, still, something to keep in mind. 
4) I'd deploy with the Celery Executor first, some of the others have additional dependencies that aren't immediately apparent from the instructions. I.e., get it working, running your pipelines or tasks and then experiment with different executors. 


References:
* Log persistence was the missing piece for my deployment, and I was able to figure that out via [Marc Lamberti's Airflow tutorial](https://marclamberti.com/blog/airflow-on-kubernetes-get-started-in-10-mins/). Note: he's deploying via the official Airflow helm chart, but these persistent volume setups worked just fine. 
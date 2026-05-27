### Kubernetes Job Deployment Manifest

Example of a Kubernetes manifest file to deploy a container as a "Kubernetes Job", as in the container runs and then shuts off. This differs from a standard k8s deployment in that those containers will run and then re-start, as a deployment is based on the premise that the container runs indefinitely so it will usually just restart after it has finished running even if you setup the container as something that just runs once. 


Note: there is another example of a manifest for a Kubernetes job in the testing/postgres folder.


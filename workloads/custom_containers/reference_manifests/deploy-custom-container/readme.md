## Deploying General Container Workloads 

This folder contains an example manifest for deploying a custom container, the example in question deploys a single container that monitors a Kasa brand Smart Plug. It's currently deployed via the following process:

* Config maps and secrets are created in Kubernetes that have the information/env vars the container needs to operate
* Create a path/folder in a private GitHub Infrastructure as Code (IAC) repo and then push the completed manifest to it 
* Create an app/entry in ArgoCD and point it towards the path above 

### Additionaa Details 

* This manifest can also be deployed at the command line via the "kubectl apply" command
* The manifest uses a "node affinity" to give a preference for a certain type of node, you'll need to either remove it or modify it to fit your cluster. In this case, "k3s_role" refers to either the worker or data nodes in my cluster, while "agent_type" is a broader category that both the data and worker nodes are in. This means that if while the deployment will favor the worker nodes, it can be deployed on a data node if a worker node isn't available. 

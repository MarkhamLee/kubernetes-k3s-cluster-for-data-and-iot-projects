
### August 2024

* **08/20/2024:** quick a few changes over the last several months, making note of the major ones here:
    * All apps are on-boarded to Argo CD and the manifests and approach for each are described in the deployment files folder, June 29th for the onboarding, August 18th for the documentation. 
    * Updated hardware architecture, switched to using dedicated nodes for control, compute and storage and removed the Raspberry Pis
    * Added pgAdmin and Redis
    * Updated all apps to have node affinities and a labeling/server hiearchy to match:
        * Control nodes have a no schedule taint, with appropriate tolerations added to things that are allowed to be deployed on them
        * agent nodes are broken down as follows:
            * All get the label "k3s_role: agent"
            * There are three agent type labels: x86_worker, storage and x86_tasks
            * There are node_type label of x86_worker that is added to the tasks nodes so they can "help" if the primary x86_worker nodes are over-burdened or unavailable
            * The node affinities are set to heavily favor the most appropriate node, but other nodes can be used as well. Think: 50% weighting for agent_type: x86_worker, but the task and x86_worker nodes both have the node_type of x86_worker weighted at 20% so pods can be deployed to the tasks nodes if the first choice isn't available.
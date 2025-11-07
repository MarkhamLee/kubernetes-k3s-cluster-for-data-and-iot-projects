## Deploying PostgreSQL with Argo CD

Deploying Postgres can be a bit daunting given the 1700+ line values.yaml file, here are a couple of items to make things a bit simpler:

* Create a secret in Postgres and then reference in in the auth section, there are several other sections that reference the same secret, so I would use "ctrl f" to find all the instances of "existingSecret" 
* I set the app version via the Docker image tag in the values.yaml, you can use what's there already or look up the latest version and use that instead.
* Change the node affinity to fit your hardware architecture
* I reference an existing PVC because I just onboarded an existing Postgres deployment 
* If you use read replicas, you'll need to set node affinities for those as well. 
* This values.yaml uses resource presets for the containers, but the file also has a commented out section for instances when you want to define things more granularly.

I'd also recommend installing PgAdmin to manage your Postgres instance, deployment files are [here](https://github.com/MarkhamLee/kubernetes-k3s-cluster-for-data-and-iot-projects/tree/main/deployment_files/application_install_files/pgadmin).



## Deploying PostgreSQL with Argo CD

I had to make significant updates to this one due to Bitnami putting access to many of its Helm Charts and the associated Docker images behind a paywall. This folder contains a k8s manifest version of a Postgres deployment that's been configured to "sync" with an external distance in a "pub-sub" fashion. 

If needed, you can find the Helm chart version of this deployment [here](../archive/postgres/). 

A couple of things to keep in mind: 

* This setup presumes that you'll have an external Postgres server(s) that will have a pub-sub relationship with this one, meaning, after data is written to the Postgres instance(s) on K8s, it will then be replicated to the external server. 
* You'll need to create a secret in Postgres and reference it in the stateful set
* The service is so that the database can be exposed outside of the cluster. In this instance it would be exposed on a private network so the relative risk is low, however, it would be smart to consider using something like Tailscale or similar to further restrict access/reduce the risk surface area.
* I'd also recommend installing PgAdmin to manage your Postgres instance, deployment files are [here](https://github.com/MarkhamLee/kubernetes-k3s-cluster-for-data-and-iot-projects/tree/main/deployment_files/application_install_files/pgadmin).



### Deploying MariaDB on K3s

A set of Kubernetes manifests to deploy MariaDB, I had originally deployed this using Bitnami Helm charts and switched this to K8s manifests when Bitnami put their helm charts behind a firewall. These manifests will deploy the following:
* A headless service for use within the cluster itself
* A stateful set - AKA the DB deployment
* A loadbalancer service to enable an external service to access the database, in this particular case this is just so that I can sync/replicate the data between an external MariaDB instance so that I have a back-up that I can point key apps (like Invoice Ninja) towards if something goes sideways with K3s and/or to just have an extra backup of the data. 
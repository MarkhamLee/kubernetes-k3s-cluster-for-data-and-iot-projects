### Linkwarden Deployment on Kubernetes

The deploying is generally fairly straight forward, but there are a couple of things to keep in mind:
* You need to have a Postgres instance for data storage. You'll need to have Postgres setup as a service so that Linkwarden can connect to it. 
* A Postgres URL is required, it will be in the form of: postgresql://postgresuser:postgres_secret@postgres.postgres.svc.cluster.local:5432/linkwarden_database_name
* Make sure you create a separate DB for Linkwarden, access credentials, etc., and then use them to create the URL above. I.e., unlike a lot of other k8s apps, you can't just create the user name and then Linkwarden creates the DB for you 
* You could also just as easily have Linkwarden connect to a Postgres instance that runs outside of K3s or on TrueNAS, just alter the connection string above accordingly. 
* I have the image taga as "latest" but once you get things up and running you should edit the manifest and freeze it to the actual version you're using, and then just change version numbers when you update/upgrade.
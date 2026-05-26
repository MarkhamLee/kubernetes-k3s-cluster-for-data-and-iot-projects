## Deploying Argo Workflow  


### Overview
* The files in this folder are for deploying Argo Workflows via Argo CD using an umbrella chart and a values.yaml file
* I've set the docker image version to 3.5.1 to avoid an issue where the workflow runs properly but throws an error, there seems to be some weird outlier with service accounts that cause this bug, and I got tired of troubleshooting it. I.e., if you install the latest and get the same error, 3.5.1 is your work around.
    * You'll need to set the image version under the controller, executor and server sections
    * The files in the "extras" folder are attempts to resolve the issue above, you may find them useful
* The login_secret.yaml file will generate a Bearer token for logging into Argo that will be stored in Kubernetes. 
* This is connected to a stand-alone instance of Postgres for higher performance, so if you don't have a Postgres instance available either set one up or comment out the parts of the values.yaml that points this Argo deployment to a stand-alone Postgres so that the deployment will spin up a Postgres instance just for Argo workflows.
* Keep in mind that there are two sections in the values.yaml file: controller and server, and they have independent settings for things like node affinities. 
* The node affinities are specific to my hardware architecture, so you'll need to edit the affinity section to fit yours.


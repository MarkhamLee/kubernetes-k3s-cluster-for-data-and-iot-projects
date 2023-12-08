### Grafana Installation

* You should be able to cut and paste this into the screen for editing helm values in Rancher, or just apply it at the command line. 
* Key items for a HA setup:
    * Under auto scaling, set your minimum to 2 or higher, do the same for replicas. Make sure these numbers match
    * Enable persistence (save your settings and such) and then change the access mode to ReadWriteMany
* Also be sure to setup ingress:
    * I added "ingress class" to the chart, it didn't come with it for some reason. The values.yaml file in this folder has that added in.
    * Update your custom domain 
* The way I have this setup, it will generate a secret for you and you can pull it from rancher or via the instructions printed to the console. You can find the secret in Rancher at: deployment--> related resources --> secret 
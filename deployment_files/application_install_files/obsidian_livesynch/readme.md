# Deploying CouchDB for Obsidian Self-Hosted Live Sync to K3s

This folder contains instructions for deploying the Couchdb application that is used to store the data from the Obsidian self-hosted live-synch plug-in, in addition to tips and tricks around how to navigate around a few of the gotchas I ran into. While these instructions could be used for a general purpose deployment of CouchDB they're specifically tailored for the Obsidian live-synch plugin, meaning, if you just need to deploy CouchDB and aren't using Obsidian self-hosted live-synch you *might* be able to skip some of the items below. I say might, because you may still issues around the secrets will persist and you might still run into the CORS issues.

## Basic Setup

* This installation is not for Obsidian live synch per se, instead, it's to deploy the CouchDB application that the live synch plugin within the Obsidian app on your desktop or mobile device uses to store your notes across all your devices.
* You will install Obsidian on your portable or desktop devices, and then add the live synch plugin from the community plugins page. Next, you will configure the live synch plugin to connect to your CouchDB instance using the url to your CouchDB instance, and the admin credentials created by the install process.
* I installed Couchdb using the helm chart located [here](https://github.com/apache/couchdb-helm/tree/main/couchdb) 
* Once logged into Couchdb create a database for Obsidian to write to and give your admin (or other user) rights to use that database by clicking on the database_name --> permissions and then adding the user to the members who are allowed to use the database.
* If you want to be able to synch notes when you're away from home you'll need some sort of VPN or mesh network solution that will allow you to access your home network remotely, otherwise, you'll just need to wait until you get home for your notes to synch.


## Avoiding Gotchas 
* In the config section starting on line 262, namely the chttpd, chttpd_auth, httpd and cors sections are critical to ensuring that the apps can connect to CouchDB and sync your notes. If you refer to the [original values.yaml file](https://github.com/apache/couchdb-helm/blob/main/couchdb/values.yaml), you will see that what I have in this section is significantly different than what is in the original values.yaml. These section will create a configmap in Kubernetest that will manage network connections from the Obsidian app. If this section isn't setup properly, you'll run into a situation where the app can connect to CouchDB but can't write data.
    * Keep in mind that these changes are specific to using CouchDB behind a reverse proxy in a manner similar to how the Obsidian app connects to it via the Live Synch plugin, but may also apply to other apps that use CouchDB in a similar manner.
* When you first deploy the app, you should: 
    * Set the "createAdminSecret" flag to "true", and then redeploy it with it set to false so that subsequent redeployments, config changes, etc., don't result in the secret being changed everytime you redeploy. That is, unless you like having to change the passwords on all your devices running Obsidian.
* If you're using a tool like ArgoCD to deploy the app be mindful to **not use** the trim option for auto-synch, otherwise ArgoCD will delete the secret created when you first deployed the app. The way the Helm chart is configured, ArgoCD doesn't recognize the secret unless it's created by CouchDB upon install. I.e., it sees the existing secret that was created during the prior install as "not being in the application source". I haven't seen this behavior with other apps, so I think this is just something that needs to be corrected within the CouchDB Helm chart.

Beyond the above the deployment was fairly straight forward, as I continue to use the app and discover new things I'll update this page accordingly.
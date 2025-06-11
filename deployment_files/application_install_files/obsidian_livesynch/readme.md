# Deploying Obsidian on K3s

This folder contains instructions for deploying the couchdb application that is used to store the data from the Obsidian self-hosted live-synch plug-in, in addition to tips and tricks around how to navigate around a few of the gotchas I ran into. While this instructions could be used for a general purpose deployment of CouchDB they're specifically tailored for the Obsidian live-synch plugin, meaning, if you just need to deploy CouchDB and aren't using Obsidian self-hosted live-synch you may be able to skip some of the items below.

## Basic Setup

* This installation is not for Obsidian live synch per se, instead, it's to deploy the CouchDB application that the live synch plugin within the Obsidian app on your desktop or mobile device uses to store your notes across all your devices.
* You will install Obsidian on your portable or desktop devices, and then add the live synch plugin from the community plugins page. Next, you will configure the live synch plugin to connect to your CouchDB instance using the url to your CouchDB instance,
and the admin credentials created by the install process.
* I installed Couchdb using the helm chart located [here](https://github.com/apache/couchdb-helm/tree/main/couchdb) 
* Once logged into Couchdb create a database for Obsidian to link to and give your admin (or other user) rights to use that database by clicking on the database_name --> permissions and then adding the user to the members who are allowed to use the database.
* If you want to be able to synch notes when you're away from home, you'll need some sort of VPN or mesh network solution that will allow you to access your home network remotely.


## Avoiding Gotchas 
* The CouchDB config section starting on line 262, namely the chttpd, chttpd_auth, httpd and cors sections are critical to ensuring that the apps can connect to CouchDB and sync your notes. If you refer to the [original values.yaml file](https://github.com/apache/couchdb-helm/blob/main/couchdb/values.yaml), you will see that what I have in this section is significantly different than what is in the original values.yaml. 
    * Keep in mind that these changes are specific to using CouchDB as the back-end for Obsidian note synching, they may not be necessary to use Obsidian with other apps.
* When you first deploy the app, you should: 
    * Set the # of replicas to one, login for the first time and then redeploy.
    * When you adjust the replicas back up to three, you should also change the create admin password flag to false so the password isn't recreated. 
* If you're using a tool like ArgoCD to deploy the app be mindful to **not use** the trim option for auto-synch, otherwise ArgoCD will delete the secret created when you first deployed the app. The way the Helm chart is configured, ArgoCD doesn't recognize the secret unless it's created by CouchDB upon install. I.e., it sees the existing secret that was created during the prior install as "not being in the application source". I haven't seen this behavior with other apps, so I think this is just something that needs to be corrected in the CouchDB Helm chart.

Beyond the above the deployment was fairly straight forward, as I continue to use the app and discover new things I'll update this page accordingly.
## Eclipse Mosquitto Setup w/ Argo CD

This one doesn't use the usual umbrella chart + values.yaml file I use with Argo CD, I instead just dropped the files I used to deploy Mosquitto from the Kubernetes command line into a folder on GitHub and Argo CD picked them up just fine and deployed the app. 

A couple of additional notes: 

* The config map file is critical as it will define the file you use to store Mosquitto configs related to passwords and the like. 
* You will need to configure the node affinity (or just drop it) to fit your HW architecture
* Right now I have this resolving to an IP on my Kubernetes load balancer 




#### InfluxDB Setup Instructions

1) Add the Helm Chart for InfluxDB for to Rancher 
2) You'll see several Influx options, make sure you use the one for "InfluxDB2" so that you have a WEB UI, example code, Telegraf plugins, etc., the other ones, well, you get none of that. 
3) The values.yaml file you'll see in Rancher is fairly simple, you'll need to make one change to use an Ingress:
    * Add "class: traefik" (presuming you're using Traefik) without this, not only will you not have an Ingress, but the deployment will fail. I've already added this to values.yaml file. 
4) This will only install on one pod, you'll need an enterprise license to scale horizontally, so don't waste hours trying to set the scaling parameters properly, same goes for trying to scale it horizontally within Rancher, each pod will fire up and then fail over and over, so don't spend hours trying to troubleshoot that... don't ask how I know.  
5) Leave the password section blank, Rancher will generate a secret for you.  
6) Once finished, go to stateful set--> related resources --> secret to get your password  

That's pretty much it

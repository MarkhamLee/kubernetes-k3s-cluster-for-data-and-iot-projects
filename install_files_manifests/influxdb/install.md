#### InfluxDB Setup Instructions

1) Add the Helm Chart for InfluxDB for to Rancher 
2) You'll see several Influx options, make sure you use the one for "InfluxDB2" you get a web UI, example code, Telegraf plugins, etc., the other ones, well, you get none of that. 
3) The values.yaml file you'll see in Rancher is fairly simple, you'll need to make one change to use an Ingress:
    * Add class: traefik (presuming you're using Traefik) without this, not only will you not have an Ingress, but the deployment will fail. 
4) Leave the password section blank, Rancher will generate a secret for you.  
5) Once finished, go to stateful set--> related resources --> secret to get your password 

That's pretty much it

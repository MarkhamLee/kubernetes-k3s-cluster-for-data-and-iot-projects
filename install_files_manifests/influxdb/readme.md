## CRITICAL NOTE 

The official helm chart as found [here] is woefully out of date, it will install InfluxDB 2.3.0 as opposed to the current version of 2.7.4. This causes a problem where Grafana (version 10.2.2) can connect to InfluxDB BUT cannot see any measurements. In order to correct this, the values.yaml file in this directory has been updated to pull the image for 2.7.4. I tested this change by: 

* Installing the current helm chart as is
* Verifying that InfluxDB installed properly 
* Doing an upgrade in Rancher where I simply changed the image version from 2.3.0 to 2.7.4 in the values.yaml file. 

So far, I haven't encountered any issues. That being said, given that this is an unofficial updatate, use at your own risk. 

There is a pull request to address the issue that you can follow [here](https://github.com/influxdata/helm-charts/pull/536).

**Update 12-06-23:** the pull request has been approved and merged, so you shouldn't encounter any issues with the chart at this point. But, I would make it a point when installing charts to check the image versions vs what the most up to date version on this and any other chart. 

#### InfluxDB Setup Instructions

1) Add the Helm Chart for InfluxDB for to Rancher 
2) You'll see several Influx options, make sure you use the one for "InfluxDB2" so that you have a WEB UI, example code, Telegraf plugins, etc., the other ones, well, you get none of that. 
3) The values.yaml file you'll see in Rancher is fairly simple, you'll need to make one change to use an Ingress:
    * Add "class: traefik" (presuming you're using Traefik) without this, not only will you not have an Ingress, but the deployment will fail. I've already added this to values.yaml file. 
4) This will only install on one pod, you'll need an enterprise license to scale horizontally, so don't waste hours trying to set the scaling parameters properly, same goes for trying to scale it horizontally within Rancher, each pod will fire up and then fail over and over, so don't spend hours trying to troubleshoot that... don't ask how I know.  
5) Leave the password section blank, Rancher will generate a secret for you.  
6) Once finished, go to stateful set--> related resources --> secret to get your password  

That's pretty much it

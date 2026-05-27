## Alerting and Monitoring for pfSense 

Given your K3s Cluster is so heavily dependent on the health of your home network, here is some information around configuring alerting and monitoring for your cluster. 


### Alert Options 

#### Slack Alerts 

Note: this presumes you've already signed up for the Slack API, are familiar with configuring webhooks, etc. If you're not, just go to the web site for the [Slack API](https://api.slack.com/), sign-up, create a Slack channel to receive the alerts, create an app and then get an API key. 

1) Go to System --> Advanced --> Notifications 
2) Scroll to the bottom of the page and add the API key and the name of your slack channel
3) Click the box to enable Slack notifications 
4) Click the icon to test the connection 

Once this is setup you'll get alerts for pretty much any issue that occurs with your firewall:
* Rebooting
* Issues with installed packages or their patches 
* Pretty much anything that would generate an alert

IF you want to go beyond that, say alerts that are triggered when a certain amount of activity goes above a threshold you'll need to: 
 1) Setup logging/monitoring via something like Telegraf or Prometheus
 2) Configure specific alerts within a tool like Grafana or Prometheus alert manager. 

#### Other Alerting Options

You can also configure alerts via Email or Telegram 


 ### Monitoring 

 With monitoring you have three main options:

 1) Syslogs to a Remote Server, using the syslog-ng package you can configure sending log data to a remote server. 
 2) You can install Telegraf and use it to send hardware data to InfluxDB 
 3) You can also install the Prometheus node_exporter via the package manager to send data to a Prometheus instance
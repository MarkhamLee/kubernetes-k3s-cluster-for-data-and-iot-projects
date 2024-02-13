## Setting Up pfSense 

This document presumes you already have pfSense installed and running, and are looking to configure some of the more advanced features. Topics covered in this document will include:
* Adding Secure Certificates via letsencrypt.org and Cloudflare 
* Configuring alerting via Slack
* Writing data to InfluxDB via Telegraf


### Slack Alerts 

Note: this presumes you've already signed up for the Slack API, are familiar with configuring webhooks, etc. If you're not, just go to the web site for the [Slack API](https://api.slack.com/), sign-up, create a Slack channel to receive the alerts, create an app and then get an API key. 

1) Go to System --> Advanced --> Notifications 
2) Scroll to the bottom of the page and add the API key and the name of your slack channel
3) Click the box to enable Slack notifications 
4) Click the icon to test the connection 


### Adding Secure Certifications

1) If you haven't already done so, go to Cloudflare and setup an account, register a domain (or transfer an existing one).  
2) Under overview you can navigate to getting your API key 
3) 
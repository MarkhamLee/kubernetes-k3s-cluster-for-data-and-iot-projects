## Using Zone files to add local domains


"Zones" is the term that Technitium uses for top level domains that you use for local domains. E.g., you have TLD like "my-private-cloud.com" and you want to use that for certificates, so you can have local domains in the form of service1.local.my-private-cloud.com. After you set up Technitium, you'll need to go in to the UI and create a "zone" for each one of your local domains, and then you can use the UI to create local sub-domains. 

### Semi-automating Zone Setup


The file called "example-com.zone" is an example of a "zone file" that you can use to upload a list of local domains. To use the file you would go to Zones --> Add Zone and use the "Import Zone File" option to add your file. Please keep in mind that this approach only works for creating a new zone, replete with all your custom/local subdomains. Once you create the zone, if you want to add additional subdomains you'll either need to use the UI or the API. I.e., just for ease of use, it's a good idea to define as many as your local subdomains as possible before you upload the file. You should also keep this file up to date as you add more subdomains, so that if you have to recreate your technitium instance you can do it quickly. 


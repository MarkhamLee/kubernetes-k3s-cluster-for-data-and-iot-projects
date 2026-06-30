## Pi-Hole Deployment

The [Deployment](deployment/compose.yaml) folder contains a sample Docker compose for deploying pi-hole on a stand-alone server, a couple of notes:
* This is very generic, in a production setup you might want to bind the IP to restrict the IP that pi-hole is available on. 
* You'll notice the Docker image is for "latest" after you get this up and running you should pin that to the version you got up and running, so that you don't accidentally deploy breaking changes if you have to redeploy, the server restarts, etc. 


### Deployment Steps

1). Create a secret called "PI_HOLE_API_SECRET" and store it as an environmental variable on the server you're running this one. 
2). Create local persistent storage (see the volume definition in the Compose file) either create a folder that matches what's in the Docker compose or use a different folder and update the compose file accordingly 
3). Set the options for DHCP and time 
4). Deploy using `sudo -E docker compose up -d  --force-recreate --remove-orphans`
5). Login to pi-hole at the url <server_ip>/admin using the password you created in step 1. 
## Pi-Hole Deployment

The [Deployment](deployment/compose.yaml) folder contains a sample Docker compose for deploying pi-hole on a stand-alone server, a couple of notes:
* This is very generic, in a production setup you might want to bind the IP to restrict the IP that pi-hole is available on. 
* You'll notice the Docker image is for "latest" after you get this up and running you should pin that to the version you got up and running, so that you don't accidentally deploy breaking changes if you have to redeploy, the server restarts, etc. 
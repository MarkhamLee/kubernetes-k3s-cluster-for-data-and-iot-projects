## Setting up a Traefik reverse proxy for Docker Apps

Acknowledgement: this is heavily based on Techno Tim's tutorial, I just made numerous tweaks so creds and other data were communicated via environmental vars. 

Quick notes:
* This presumes that you would be running a Docker container on singular server
* You can use this with any device reachable on your network, it doesn't have to be on the same server
* data/config.yml is for external to the device that this is deployed on services, for services deployed on the same device you just put them on the same Docker network as Traefik and then add annotations/labels to their Docker config/compose.
* Make sure that the docker compose file begins with a lower case letter, if you use upper case it will show up as the right file type but the Docker compose command won't be able to see it 
* You can put your data folder in another place if you want, but since the files in there should be managed with git, well, don't. 
* Make sure you have 

### Instructions 

1) Install apache2-utils so you can create the password
2) Go into the data folder and type "touch acme.json" this will create a blank file your certs will be stored in:
    * After you test things with the staging api (see below), clear out this file otherwise, a new cert won't be generated 
3) Type  sudo docker network create proxy   this will create the proxy network for your proxy server
4) Use this commmand to generate a username and password:

    echo $(htpasswd -nb "<USER>" "<PASSWORD>") | sed -e s/\\$/\\$\\$/g

5) Open /.bashrc with nano and store the following:
    * The password from the above
    * The email you intend to use with the certs

6) Edit the files to have the right env vars 
7) Comment out the productiion API for certs and use the staging one 
8) Run sudo -E docker compose up to generate the container
9) Run sudo docker logs traefik to see if everything works, if everything is cool, you won't see logs. If it doesn't work, troubleshoot and try again 
10) Once everything is cool, comment out the staging API, clear out the acme.json file and run everything again. 
11) Look at the Portainer folder for how to configure an "on network" service and use the config.yml file for examples of how to configure an external one. 
    * Tim has examples of the configs for various external services [here](https://github.com/techno-tim/techno-tim.github.io/blob/master/reference_files/traefik-portainer-ssl/traefik/config.yml), most can just use the same as what external Portainer use, but others have differences. 


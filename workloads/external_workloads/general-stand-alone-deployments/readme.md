## Stand Alone Services & Deployments

Stand Alone Deployments = services that are part of the broader private cloud, but isntead of them being deployed to K3s, they're are deployed directly to a server via a Docker container. The reasons for this range from certain services not "playing nicely" with Kubernetes (e.g. Home Assistant), simplicity, extra redundancy outside of K3s or just wanting to try something as a POC before going through the trouble of navigating a K3s deployment. 

### Current Applications

#### General Applications 

* [Home Assistant](homeassistant/compose.yaml) this doesn't play nicely with Kubernetes, so it was just easier to just deploy it to a stand-alone server. 
* [Portainer](portainer/compose.yaml) I always run Portainer on stand-alone servers I'm deploying apps to, also, having an instance of Portainer running external to Kubernetes gives me a back-up control pane if I were to run into problems with Rancher.
* [Zigbee2MQTT](zigbee2mqtt/compose.yaml) if you're deploying this with a USB dongle, there isn't much point in deploying it to Kubernetes as it will always be tied to a specific device. 


#### Networking Applications (Referenced here, but located under runbook/networking)

*Note: Technitium and Traefik go hand in hand, both for network security and configuring custom local domains for the services you're hosting.*

* [Technitium](../../../runbook/networking/technitium/readme.md): instruction for setting Technitium for DNS (with filtering and blocking) and DHCP, even if you're not using K3s this is invaluable for setting up custom 
* [Traefik](../../../runbook/networking/traefik_external/readme.md) instructions on setting up Traefik as a reverse proxy on a stand-alone servers. 
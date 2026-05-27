## Traefik reverse proxy with Lets Encrypt Certificates 

If you haven't read the [readme.md](readme.md) for this section, I would suggesting going back and doing that first. 


### Suggested Sequence of events 

1) Build your firewall per the [readme](readme.md)
2) Spent some time getting familiar with functions like DNS and DHCP 
3) Sign-up for Cloudflare
4) Register your domain
5) Deploy Reflector
6) Deploy Cert Manager
7) Deploy Traefik
8) Figure out what namespaces will need certificates
7) Add Let's Encrypt integration and create certificates with the annotations for the namespaces you want the certs reflected to. 


### Setting up your cluster with secure certificates

** Updates - August 18, 2025: ** some newer information + tips and tricks I've learned since I first wrote this up in 2024. 

* While the tutorial I referenced below "should" still work, it's a good idea to go visit the [Traefik Website](https://doc.traefik.io/traefik/providers/kubernetes-crd/) and make sure you're using the most up to date instructions, version numbers, etc. If you've never worked with Traefik before, a good idea might be to watch Tim's tutorial followed by reading the most recent set of instructions from Traefik.
* This app and ArgoCD don't always play well together, for instance: the app will deploy properly and your service ingresses will work EXCEPT the one for the Traefik dashboard, and the only solution will be to deploy the ingress route for Traefik at the command line via Kubectl, which ArgoCD will attempt to roll back as it will perceive it as a different than what is in GitHub, even if it's the same thing. This problem will leave you with two options:
    * Turn off auto sync in ArgoCD and manually re-apply the ingress route whenever you make changes. 
    * Always deploy and maintain via helm from the command line. In this case I would maintain the values.yaml and the like in Git, make your changes locally, apply them and once you're sure it works, immediately push it to Git, to ensure that Git has your most recent/stable working configuration. 
* If you use ArgoCD you should apply the Traefik CRDs from the command line and then deploy via ArgoCD, as sometimes ArgoCD can't apply certain CRDs if they're too large. 
* If you have separate control and worker nodes, I would add a toleration and a node selector so that Traefik is only deployed to the control nodes. The general idea is that since Traefik is a security application it would be a target for attackers, so you'd want to keep it away from worker nodes as those are the nodes working with your application, potentially sensitive information, etc.
* Be ***very*** careful before adding Traefik plugins, I would take the time to read GitHub issues, search for information related to problems like instability, excessive memory use, etc., I had a plugin cause some of my nodes to crash because RAM usage would creep north of 45 GB, compared to 200 - 400 MB normally. 
* Speaking of plugins, Traefik can do a lot more than just serve as a reverse proxy, perusing through the various plugins and a deep dive into the documentation will likely reveal additional capabilities you could use. 


### Deployment 

#### The simple answer 

Just follow [Tim's tutorial](https://www.youtube.com/watch?v=G4CmbYL9UPg&t=1344s), but with a couple of extra points that should make your life easier: 
    * When looking at the traefik dashboard, the full URL will be something like: traefik.local.example.com/dashboard/ make sure you have the /dashboard/ after your URL or you'll get a 404 message. 
    * If the above doesn't work, go back a few steps and just do them over, it's a lot of information to work through and it's easy to miss a step. 
    * 404 messages aren't actually bad, they mean you're hitting the right service, but you've made a small error in your URL somewhere


#### A somewhat less simple answer 
* Read up on how to deploy Cert Manager and Traefik from their respective web sites
* Deploy Reflector with the Umbrella Chart and values.yaml from the reflector folder in the deployment files section. 
* Use a tool like ArgoCD to deploy the working Umbrella Charts + Values.yaml in the Cert Manager folder 
* Deploy Traefik from the command line via Kubectl 
* Use [Tim's instructions](https://www.youtube.com/watch?v=G4CmbYL9UPg&t=1344s) for generating certs 
    * There is an example certificate example under deployment files in this section, but keep in mind following Tim's steps for setting up Lets Encrypt, trying things with the staging API first, etc.  
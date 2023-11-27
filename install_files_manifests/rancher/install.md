#### If you're using an ingress + secure certs this should get you setup nicely. 

Note: this is what worked for me as of 11/21/2023, refer to the rancher web site to check if any steps have changed. However, steps 1-4 are fairly standard and the parameters in step five should be fairly stalbe, but it couldn't hurt to doublecheck or go to the [rancher web site](https://ranchermanager.docs.rancher.com/pages-for-subheaders/install-upgrade-on-a-kubernetes-cluster) for help if step five doesn't work. 

1) You need to add the helm repo for rancher:

```
helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
```

2) Next, update helm 

```
Helm repo update
```

3) Create a namespace, it has to be called "cattle-system"

```
create namespace: kubectl create namespace cattle-system
```

4) Go into your firewall/router software and create a local domain for rancher. E.g., rancher.local.yourdomain.com. 

5) Run the following command to install Rancher to make sure it gets setup with the secure certificates and uses the local domain you created. 

``` 
Use the following to use the secrets and traefik ingress you've created: 
helm install rancher rancher-stable/rancher \
  --namespace cattle-system \
  --set hostname=rancher.local.yourdomain.com \
  --set bootstrapPassword=admin \
  --set ingress.tls.source=letsEncrypt \
  --set letsEncrypt.email=you@yourdomain.com \
  --set letsEncrypt.ingress.class=traefik 
  
```

If you're using an ingress + secure certs this should get you setup nicely. 



```stable rancher: helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
create namespace: kubectl create namespace cattle-system
Use the following to use the secrets and traefik ingress you've created: 
helm install rancher rancher-stable/rancher \
  --namespace cattle-system \
  --set hostname=rancher.local.yourdomain.com \
  --set bootstrapPassword=admin \
  --set ingress.tls.source=letsEncrypt \
  --set letsEncrypt.email=you@yourdomain.com \
  --set letsEncrypt.ingress.class=traefik ```
### Using Reflector 

* The reflector app simplifies the management of secrets, config maps and the like that need to be in multiple namespaces. For example, a wildcard certificate for *.local.example.com is, well, a wildcard, it will work for all of your subdomains, so re-registering it for each service is just renewing the same certificate repeatedly. Using reflector you can register the certificate and then "reflect" it into the additional namespaces that need it, and when the certificate is automatically renewed the new one will also be reflected into those namespaces. 
* Chart.yaml and values.yaml contain a working example of Reflector deployment configs you can use to deploy Reflector via ArgoCD. 

Using reflector is fairly simple, you just need to add the following annotations to the resource you want to "reflect": 

~~~
    annotations:
      reflector.v1.k8s.emberstack.com/reflection-allowed: "true"
      reflector.v1.k8s.emberstack.com/reflection-allowed-namespaces: "argo, grafana, influxdb"
      reflector.v1.k8s.emberstack.com/reflection-auto-enabled: "true"
      reflector.v1.k8s.emberstack.com/reflection-auto-namespaces: "argo, grafana, influxdb" 

~~~

The annotations tell reflector what namespaces are allowed to receive the "reflected" resource and what namespaces it should automatically copy the resources into. See the [example_certificate](../example_certificate/) folder for a more detailed example.

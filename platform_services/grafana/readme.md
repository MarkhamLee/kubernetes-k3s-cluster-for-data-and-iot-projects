## Grafana Installation via Argo CD

* This installation uses the umbrella chart coupled with a Helm chart and a values.yaml file to install Grafana. 
* The values.yaml file could be used outside of Argo CD/ a typical Helm installation but you'll have to remove the top key of "grafana" and then backspace all the other values over. 
* Key items changed in the values.yaml file
    * Node affinity based on having nodes designated solely for control, storage (longhorn), IoT/tasks(e.g. ETLs) and general workloads: 
        * amd64 required
        * General workload nodes preferred
    * Ingress is defined in the values.yaml file
    * Replicas set at two 




































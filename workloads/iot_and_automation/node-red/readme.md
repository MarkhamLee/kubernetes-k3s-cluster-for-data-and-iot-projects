## Deploying Node-RED via Argo CD

* This is the usual umbrella chart + values.yaml file pattern I use with Argo CD
* I on-boarded Node-RED in a less than ideal way (it was my first), but it worked:
    * I deleted the original deployment out of frustration and deployed Node-RED from scratch, but made sure to keep the Persistent Volume Claim (PVC)
    * Before deploying I edited the PVC section to use the PVC from the original deployment
    * The new Node-RED came up as expected and it used the data from the prior deployment and everything worked fine. 
* Beyond the above:
    * You'll need to configure your own node affinity 
    * The values.yaml is one I cobbled together for what was originally deployed via kubectl and the command line, if you need more customization I would get the values.yaml from the Helm repo. 
    * The app version is set on line #46 of the values.yaml file, before deploying you should get the latest version number. 
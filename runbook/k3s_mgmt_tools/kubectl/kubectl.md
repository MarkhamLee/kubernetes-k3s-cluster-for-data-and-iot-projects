### Configuring Kubectl on K3s Clusters Managed with Rancher

Kubectl is a tool you can use to manage your K3s cluster that you can either run on one of your control nodes or an external device. On the control nodes it gets deployed as part of the K3s deployment so that scenario is easy, however, if you want to deploy it on an external device things can get dicey as the most of the instructions you'll find online are for standard K8s clusters, NOT K3s clusters managed with Rancher. So here are the K3s/Rancher instructions for setting up Kubectl for external devices.

Note: these instructions are for Linux 


1) You can find the official instructions for installing Kubectl [here], before you install it you should make note of your K3s version as you'll need your Kubectl version to match it to avoid issues. 
2) Install Kubectl per the instructions
3) Create a folder on your local machine called .kube 
4) SSH into one of the control nodes so you can copy over the kube config file.
5) Now is where things get dicey, as the kube config file at the usual location of ~/.kube/config is NOT the one you want, with K3s and Rancher the file is elsewhere: /etc/rancher/k3s/k3s.yaml 
6) You'll want to copy this file to your local machine, presuming they're both running linux, it would be something like 

`
sudo scp /etc/rancher/k3s/k3s.yaml <user-name>@<ip-address>:~/.kube/config
`
6. Set the permissions with these two commands: 

	`chown $(id -u):$(id -g) ~/.kube/config`
	`chmod 600 ~/.kube/config`


5. Finally, change the server IP address in ~/.kube/config (as it's probaby a local host IP) to the IP of your K3s control plane API, it would likely be something like 192.168.0.45:6443

6) Once the above is done you can use commands like "kubectl get nodes" to verify that everything is working correctly. 


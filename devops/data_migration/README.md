## Data Migration from PVC to external server --- WORK IN PROGRESS

Note: the instructions below presume that you're running these commands on a Linux machine. I'm unfamiliar with how kubectl runs on OSX and Windows, but I suspect that many of the commands will be similar, but you'll need to modify the copy commands for moving data from the machine you're running kubectl on to the destination server. 

### Context 

I needed to move data from the PVC for Linkwarden to a server external to K3s. The manifest in this folder enabled me to create pod that would access the PVC and then I could use CLI commands to copy the data over. The process below will use kubectl to copy data from the PVC to the machine you're running the kubectl commands from, and from there you can use the linux cp commands to move the data to where you need it go. 


### Steps 

1. Temporarily shut down the service using the PVC so you don't run into issues with data writing while the data is copying, attaching the temporary pod to the PVC, etc. 
2. Use this command to get the name of the PVC for the service you're migrating data for:
~~~
kubectl get pvc -A | grep -i linkwarden
~~~
3. Edit the sample manifest to use the correct PVC name 
4. Look through documentation for the service in question and find out the location of the data you need in its container. 
5. Create a local directory on the machine you're running these commands on, so you have a place for the data to land
6. Apply the manifest and then verify that the pod is up and running and has attached to the PVC
7. Run a command like the below to copy the data over, you'll (of course) change things to fit your namespace, service name, where the data is mounted in the PVC and then your destination folder. 

~~~
kubectl cp linkwarden/lw-pvc-helper:/mnt/lw-data /linkwarden
~~~

From here you can just use Linux (or your operating system's) copy commands to move the data to where you want to go



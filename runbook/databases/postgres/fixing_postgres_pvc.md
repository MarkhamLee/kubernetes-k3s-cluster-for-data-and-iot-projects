## Resizing a Postgres Persistent Volume Claim


### Resizing the PVC 

If you run into space issues, e.g., if the pg_wal file runs out of space or you can no longer write to the database, you'll need to resize the PVC claim. However, in some instances when you update the PVC sizes in the manifest files in Git (or wherever you store them, you're storing them somewhere, right?) and then try to apply the updated file via a tool like ArgoCD you'll run into an error saying the PVC size field is immutable. Here is you how you resolve that issue:

#### Suggested Approach

* Scale down the Postgres pods to zero, you won't lose any data, you'll just put things into a state where you can edit the PVC size. 

* Next, delete the existing stateful set - you won't lose any data this is just deleting a manifest 

* Update the stateful set in Git 

* Reapply the manifest with ArgoCD or wait for the next synch to do it. This process will scale the Postgres pods back up and re-size the PVC claim. 

#### Quick and dirty resize

* You can use the Rancher UI to just quickly edit the Postgres PVC to use the bigger size, but keep in mind that doing so doesn't change the stateful set so you'll still need to do the above. 

* If you don't want to do it via the Rancher UI you can also do it via this CLI command: 

~~~

kubectl edit pvc <postgres-pvc-name> -n <postgres-namespace>

~~~

Look for a field called: .spec.resources.requests.storage and increase the size of the PVC claim 

* Go back to the Rancher UI and and scale the pods back up, Longhorn will resize the PVC claim 

Finally you'll still need to apply the "Suggested Approach" so your YAML configs and what's running in K3s match each other. 


### Checking the size of your databases

You can run the query below to check the size of all the databases running on your Postgres instance. If you're using a tool like pgAdmin it won't matter what DB you're using when you select the query tool, it will still return data on all the databases. The below is also in this folder as a .sql file if that's easier to use. 

~~~
SELECT
  datname                                AS database,
  pg_size_pretty(pg_database_size(datname)) AS size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;

~~~


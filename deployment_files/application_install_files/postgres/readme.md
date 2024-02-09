## Deploying PostgreSQL 

Deploying Postgres is fairly straight forward especially if you're using a tool like Rancher, i.e., if you just deploy it from within Rancher you'll probably have all you need, it will even generate a login secret for you. Customizing is fairly straight forward too. However, I like having deployment manifests for re-useability and so put the values.yaml file I wound up using in this folder. 

#### Deployment Steps

1) Create a secret and within that secret create two items:
    * postgres-secret-key (for user login)
    * postgres-admin-key 

2) Within the values.yaml file put the name of your secret and the secret keys in the auth and global section as per the below:

```
auth:
  database: ''
  enablePostgresUser: true
  existingSecret: postgres-secret # the secret you created earlier
  password: ''
  postgresPassword: ''
  replicationPassword: ''
  replicationUsername: repl_user
  secretKeys:
    adminPasswordKey: postgres-admin-key # key for the password value
    replicationPasswordKey: replication-password
    userPasswordKey: postgres-secret-key # key for the password value
  usePasswordFiles: false
  username: <your user name here>
```

3) On line 302 I increased the size of the volume claim 

For everything else it's fairly straight forward to change or tweak to your liking. 


I'd also recommend installing PgAdmin to manage your Postgres instance. 



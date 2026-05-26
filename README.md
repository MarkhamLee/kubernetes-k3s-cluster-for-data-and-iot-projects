## Kubernetes (K3s) Powered Private Cloud

Self-hosted K3s cluster that is the shared services platform for active development projects in data engineering, computer vision, agentic AI and IoT, in addition to hosting productivity and dev tools (Obsidian LiveSync, Linkwarden, pgAdmin, Code Server). The cluster is managed declaratively with Git, application delivery is managed via ArgoCD, distributed storage is provided by Longhorn and centralized observability by Prometheus and Victoria Logs. 



| Use Cases                                    | Supporting Services & Technologies                                                                                        |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Data Engineering, IoT                        | ArgoCD for GitOps, Argo Workflow for ETL & task orchestration, Influx & Postgres for data stores, MQTT & Node-RED for IoT |
| Computer Vision                              | MQTT & Node-RED for collecting data at the edge, InfluxDB for time series data                                            |
| Agentic AI                                   | Argo Workflows for scheduling LLM agents, Postgres for agent memory                                                       |
| Engineering tools                            | Code Server, pgAdmin, phpMyAdmin                                                                                          |
| Personal productivity & knowledge management | Obsidian LiveSync, LinkWarden, Paperless-ngx, Invoice Ninja                                                               |


This repository is the operational record of the platform: architecture documentation, deployment references, maintenance runbooks, troubleshooting notes, and the custom container code used for hardware monitoring. It's organized so that rebuilding the cluster from scratch, diagnosing unfamiliar issues, or onboarding a new workload starts here.


~~~mermaid
---
config:
  layout: dagre
---
flowchart LR
 subgraph k3s["K3s Cluster"]
    direction LR
        cp["Control Nodes ×3\nBeelink SER5"]
        wk["Worker Nodes ×2\nMinisforum MS-A1"]
        dn["Data & Storage Nodes ×2\nMinisforum MS-01"]
  end
 subgraph plat["Platform Services"]
    direction LR
        traefik["Traefik\nIngress"]
        longhorn["Longhorn\nStorage"]
        obs["Prometheus\nVictoria Logs"]
  end
    dev["Git Push / PR"] --> gha["GitHub Actions\nBuild · Test · Publish"] & cfg["GitOps Manifests\n(Helm / Raw YAML)"]
    gha --> reg[("Container\nRegistry")]
    cfg --> argo["ArgoCD"]
    reg --> argo
    argo --> k3s
    k3s --> plat
    plat --> w1["Data Engineering & IoT\nArgo Workflows · InfluxDB\nPostgres · MQTT · Node-RED"] & w2["Computer Vision\nEdge data via MQTT\nInfluxDB time series"] & w3["Agentic AI\nArgo Workflows\nPostgres agent memory"] & w4["Engineering & Productivity Tools\nCode Server · pgAdmin\nObsidian · Linkwarden"]
~~~


**The apps I'm currently self-hosting** 

![Current Apps](images/homepage_current_apps_8-4-2025.png)
The screen above was created with the Homepage App, which you can find [here](https://github.com/gethomepage/homepage).

The above doesn't have each and every app, but these are the primary ones and/or the ones that are worth while tracking via Homepage. 


## Repository Guide

| Section | Contents |
|---|---|
| `docs/architecture/` | Platform design, node roles, networking, storage |
| `docs/bootstrap/` | Cluster provisioning (Rancher-native; historical Ansible notes) |
| `runbook/` | Operational procedures, maintenance tasks, incident notes |
| `platform-services/` | Deployment configs for cluster infrastructure |
| `workloads/` | Deployment configs for data, CV, IoT, and custom containers |
| `hardware_monitoring/` | Custom container code for node and device monitoring |
| `dashboards/` | Grafana dashboard exports |



### Acknowledgements & References: 
  
I wouldn't have made it far enough to be able to know enough to share with others if it weren't for likes of [Techno Tim, follow him on YouTube](https://www.youtube.com/@TechnoTim/videos), his was the first tutorial I came accross that didn't make Kubernetes sound clear as mud. 
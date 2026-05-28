## ArgoCD for Declarative GitOps

Earlier versions of the cluster used a partially declarative GitOps model for managing application deployments: manifests were committed to Git and then manually applied to the cluster with kubectl. That approach worked, but it lacked deployment automation, drift correction, and a single interface for viewing the status of all deployed resources.

Rancher provided some of the necessary visibility, but it was not an ideal deployment dashboard. For some applications, including Argo Workflows, related components were spread across different resource categories such as Services and StatefulSets, which made it harder to assess overall application state quickly.

ArgoCD was adopted to move from that partial model to a more complete declarative deployment workflow. Changes pushed to Git can be automatically detected and applied to the cluster, and ArgoCD continuously compares the live cluster state with the desired state defined in Git. (Whether changes are auto-applied or require manual sync depends on the sync policy for each application.)

When selfHeal is enabled, ArgoCD can also correct certain forms of drift by re-syncing resources that have been modified outside Git. This makes Git the operational source of truth rather than the last manual command applied to the cluster.

ArgoCD was also a practical choice because it supports both UI- and CLI-driven workflows. That made adoption easier by allowing both interactive troubleshooting and command-line automation without introducing a separate tool for each mode of operation.

The ArgoCD UI has since become the primary dashboard for checking application health, sync status, and resource-level failures. That consolidated view is more useful for day-to-day operations than navigating between resource-type pages in Rancher.

#### In practice, the workflow is straightforward:

* Commit manifests or Helm configuration to Git.
* Register the application in ArgoCD and point it to the appropriate repository path.
* Let ArgoCD monitor the repository and reconcile changes into the cluster based on the configured sync policy.

#### This model provides several operational benefits:

* Changes are applied from Git rather than through ad hoc manual commands.
* Drift can be corrected automatically when selfHeal is enabled.
* The cluster has a deployment-oriented control plane for observing sync and health status in one place.
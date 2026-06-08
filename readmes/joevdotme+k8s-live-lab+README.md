# k8s-live-lab

Hands-on labs for every topic in the [lesson plan](../kubernetes_interview_lesson_plan.html). One lab per topic — YAML manifests included, run them in a real cluster.

**Start here:** [00-setup.md](00-setup.md) — creates a 3-node kind cluster with Calico.

---

## Phase 1 — Foundations (Days 1–3)

| # | Topic | Lab |
|---|-------|-----|
| 1.1 | What is Kubernetes? | [phase1-foundations/01-what-is-kubernetes/lab.md](phase1-foundations/01-what-is-kubernetes/lab.md) |
| 1.2 | Control plane components | [phase1-foundations/02-control-plane/lab.md](phase1-foundations/02-control-plane/lab.md) |
| 1.3 | Node components | [phase1-foundations/03-node-components/lab.md](phase1-foundations/03-node-components/lab.md) |
| 1.4 | kubectl basics | [phase1-foundations/04-kubectl-basics/lab.md](phase1-foundations/04-kubectl-basics/lab.md) |
| 1.5 | Pods | [phase1-foundations/05-pods/lab.md](phase1-foundations/05-pods/lab.md) |
| 1.6 | YAML manifests | [phase1-foundations/06-yaml-manifests/lab.md](phase1-foundations/06-yaml-manifests/lab.md) |
| 1.7 | Namespaces | [phase1-foundations/07-namespaces/lab.md](phase1-foundations/07-namespaces/lab.md) |

## Phase 2 — Workloads (Days 4–7)

| # | Topic | Lab |
|---|-------|-----|
| 2.1 | Deployments | [phase2-workloads/01-deployments/lab.md](phase2-workloads/01-deployments/lab.md) |
| 2.2 | ReplicaSets | [phase2-workloads/02-replicasets/lab.md](phase2-workloads/02-replicasets/lab.md) |
| 2.3 | StatefulSets | [phase2-workloads/03-statefulsets/lab.md](phase2-workloads/03-statefulsets/lab.md) |
| 2.4 | DaemonSets | [phase2-workloads/04-daemonsets/lab.md](phase2-workloads/04-daemonsets/lab.md) |
| 2.5 | Jobs & CronJobs | [phase2-workloads/05-jobs-cronjobs/lab.md](phase2-workloads/05-jobs-cronjobs/lab.md) |
| 2.6 | Resource requests & limits | [phase2-workloads/06-resource-requests-limits/lab.md](phase2-workloads/06-resource-requests-limits/lab.md) |
| 2.7 | Probes: liveness, readiness, startup | [phase2-workloads/07-probes/lab.md](phase2-workloads/07-probes/lab.md) |
| 2.8 | ConfigMaps & Secrets | [phase2-workloads/08-configmaps-secrets/lab.md](phase2-workloads/08-configmaps-secrets/lab.md) |

## Phase 3 — Networking & Storage (Days 8–12)

| # | Topic | Lab |
|---|-------|-----|
| 3.1 | Services: ClusterIP, NodePort, LoadBalancer | [phase3-networking-storage/01-services/lab.md](phase3-networking-storage/01-services/lab.md) |
| 3.2 | Endpoints & selector matching | [phase3-networking-storage/02-endpoints-selectors/lab.md](phase3-networking-storage/02-endpoints-selectors/lab.md) |
| 3.3 | DNS in Kubernetes | [phase3-networking-storage/03-dns/lab.md](phase3-networking-storage/03-dns/lab.md) |
| 3.4 | Ingress & IngressClass | [phase3-networking-storage/04-ingress/lab.md](phase3-networking-storage/04-ingress/lab.md) |
| 3.5 | Network Policies | [phase3-networking-storage/05-network-policies/lab.md](phase3-networking-storage/05-network-policies/lab.md) |
| 3.6 | CNI basics | [phase3-networking-storage/06-cni-basics/lab.md](phase3-networking-storage/06-cni-basics/lab.md) |
| 3.7 | PersistentVolumes & PVCs | [phase3-networking-storage/07-persistentvolumes-pvcs/lab.md](phase3-networking-storage/07-persistentvolumes-pvcs/lab.md) |
| 3.8 | StorageClass & dynamic provisioning | [phase3-networking-storage/08-storageclass/lab.md](phase3-networking-storage/08-storageclass/lab.md) |

## Phase 4 — Production Patterns (Days 13–17)

| # | Topic | Lab |
|---|-------|-----|
| 4.1 | RBAC: Roles, ClusterRoles, Bindings | [phase4-production/01-rbac/lab.md](phase4-production/01-rbac/lab.md) |
| 4.2 | ServiceAccounts | [phase4-production/02-service-accounts/lab.md](phase4-production/02-service-accounts/lab.md) |
| 4.3 | Pod Security (PSA/PSS) | [phase4-production/03-pod-security/lab.md](phase4-production/03-pod-security/lab.md) |
| 4.4 | Horizontal Pod Autoscaling (HPA) | [phase4-production/04-hpa/lab.md](phase4-production/04-hpa/lab.md) |
| 4.5 | Node selectors, affinity, anti-affinity | [phase4-production/05-node-affinity/lab.md](phase4-production/05-node-affinity/lab.md) |
| 4.6 | Taints & tolerations | [phase4-production/06-taints-tolerations/lab.md](phase4-production/06-taints-tolerations/lab.md) |
| 4.7 | PodDisruptionBudgets | [phase4-production/07-pdb/lab.md](phase4-production/07-pdb/lab.md) |
| 4.8 | Helm basics | [phase4-production/08-helm/lab.md](phase4-production/08-helm/lab.md) |

## Phase 5 — Advanced & Extras (Days 18–21)

| # | Topic | Lab |
|---|-------|-----|
| 5.1 | etcd: what it stores & why it matters | [phase5-advanced/01-etcd/lab.md](phase5-advanced/01-etcd/lab.md) |
| 5.2 | Custom Resource Definitions (CRDs) | [phase5-advanced/02-crds/lab.md](phase5-advanced/02-crds/lab.md) |
| 5.3 | Admission controllers & webhooks | [phase5-advanced/03-admission-controllers/lab.md](phase5-advanced/03-admission-controllers/lab.md) |
| 5.4 | Cluster upgrades | [phase5-advanced/04-cluster-upgrades/lab.md](phase5-advanced/04-cluster-upgrades/lab.md) |
| 5.5 | Observability: metrics, logs, traces | [phase5-advanced/05-observability/lab.md](phase5-advanced/05-observability/lab.md) |
| 5.6 | Multi-tenancy patterns | [phase5-advanced/06-multi-tenancy/lab.md](phase5-advanced/06-multi-tenancy/lab.md) |
| 5.7 | Debugging runbook | [phase5-advanced/07-debugging/lab.md](phase5-advanced/07-debugging/lab.md) |
| 5.8 | Common interview scenarios | [phase5-advanced/08-interview-scenarios/lab.md](phase5-advanced/08-interview-scenarios/lab.md) |

---

## How to use these labs

1. Complete [00-setup.md](00-setup.md) once
2. Work through labs in phase order — later labs assume earlier knowledge
3. Each `lab.md` ends with **Interview cues** — practice answering those out loud
4. After finishing a phase, go back to the lesson plan HTML and check off the topics

## Quick reference

```bash
# Check cluster is healthy
kubectl get nodes && kubectl get pods -A | grep -v Running

# Teardown everything when done
kind delete cluster --name k8s-lab
```

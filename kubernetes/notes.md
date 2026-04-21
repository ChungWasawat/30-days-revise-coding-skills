# Interview Checkpoint
These are real questions from DE/DevOps interviews. After today you should be able to answer all of them:
- Q: What is the difference between a Pod and a Deployment?

A Pod is a single instance of a container — if it dies, it's gone. A Deployment wraps a Pod and tells Kubernetes: "I always want N copies of this running." K8s continuously reconciles reality with that desired state, restarting pods automatically if they crash.

- Q: Why can't you store data inside a pod?

Pods are ephemeral — they can be deleted, restarted, or rescheduled to a different node at any time. When a pod is replaced, its filesystem is wiped. For persistent data you use a PersistentVolume (attached storage that exists independently of the pod's lifecycle).

- Q: What is a Service and why do pods need one?

Pods get a random internal IP address that changes every time the pod is recreated. A Service provides a stable DNS hostname and IP that always routes to the current healthy pods matching a label selector. Without Services, you'd have to update every config file every time a pod restarted.

- Q: What's the difference between resource requests and limits?

requests is the minimum guaranteed allocation — K8s uses this to schedule pods onto nodes that have enough capacity. limits is the hard ceiling — if a container exceeds its memory limit, it gets OOMKilled (Out Of Memory). Always set both so pipelines don't starve or crash each other.

- Q: Why can't you just use replicas: 3 on a Postgres Deployment with a PVC?

Because the PVC is ReadWriteOnce — only one node can mount it read-write at a time. With 3 replicas, two pods would fail with FailedMount. Even if they could mount simultaneously, they'd corrupt each other's data. For multi-replica stateful services, you need a StatefulSet with volumeClaimTemplates so each pod gets its own PVC, plus replication handled at the application layer (Postgres streaming replication, for example).

- Q: What's the difference between a PV and a PVC?

A PersistentVolume is the actual storage resource — a piece of disk that exists in the cluster. A PersistentVolumeClaim is a request for storage: "I need 2Gi, RWO." The claim is namespaced (lives in a namespace like default); the volume is cluster-scoped. K8s binds claims to matching volumes, so the pod never has to know about specific disks.

- Q: Why use strategy: Recreate on a database Deployment?

The default RollingUpdate starts a new pod before shutting down the old one — both try to mount the same RWO volume simultaneously, causing the new pod to stuck in ContainerCreating. Recreate shuts down the old pod first, then starts the new one. Brief downtime during rollouts, but the only strategy that works with RWO storage. This limitation is one reason StatefulSets exist — their rolling update is ordered pod-by-pod with proper volume handoff.

- Q: What's a headless Service and when do you need one?

A headless Service has clusterIP: None. Instead of load-balancing to pods, it returns the IPs of all matching pods via DNS. StatefulSets need a headless Service to give each pod its own DNS name (postgres-0.postgres-headless). You'd use this when clients need to address specific replicas — like writing to the primary of a replicated database or implementing client-side sharding.

- Q: What happens to data if you delete a StatefulSet?

The StatefulSet is deleted, pods are terminated, but PVCs from volumeClaimTemplates are NOT automatically deleted. The data survives. Recreating the StatefulSet with the same name reattaches to the existing PVCs. This is intentional — it prevents accidental data loss. To fully remove data, you must delete the PVCs explicitly.


## notes
- configmap and secret have similar purpose but secret is more confidential 
- pod: working service, deployment: larger scale management for pod like network; replica, job: one-time execution job, cronjob: scheduling job
- service and pod connect via service-spec.selector, deployment-spec.template.metadata.labels
- port-forward to connect local device with kube cluster
- use cronjob to extract data from database volume to another data storage (like pg_dump)
- "persistentVolumeReclaimPolicy":"Delete"-default= deleting PVC will delete underlying disk too, "persistentVolumeReclaimPolicy":"Retain"-keeps PV and data after PVC is deleted
- ResourceQuota is for all resources but LimitRange is for each pod/container
```
# Limit
CPU exceeds limit    → throttled (slowed down, NOT killed)
Memory exceeds limit → OOMKilled (pod terminated immediately, then restarted)
```
- Liveness and Readiness probes
```
Readiness Probe                    Liveness Probe
───────────────                    ──────────────
"Is it ready for traffic?"         "Is it still alive?"
 
Fails → pod removed from           Fails → pod RESTARTED
         Service endpoints                  (container killed and recreated)
 
Use for: slow startup,             Use for: deadlocks, memory leaks,
         warming up caches,                 frozen processes that won't
         waiting for dependencies           crash on their own
```
```
#exec to run command inside container (exit code 0 = healthy)
readinessProbe:
  exec:
    command: ["pg_isready", "-U", "admin", "-d", "warehouse"]

#httpGet to set http request to container (http 2xx, 3xx = healthy)
readinessProbe:
  httpGet:
    path: /health
    port: 8080

#tcpSocket to check if port opens
readinessProbe:
  tcpSocket:
    port: 5432

#timing parameters
initialDelaySeconds: 15   # wait before FIRST probe (give app time (avg time to start)) -too short: unnecessary restart, -too long: traffic routed to broken pod for a while
periodSeconds: 5          # how often to probe
timeoutSeconds: 3         # how long to wait for response before counting as failure
failureThreshold: 3       # consecutive failures before action taken (restart)
successThreshold: 1       # consecutive successes to recover (readiness only)
```
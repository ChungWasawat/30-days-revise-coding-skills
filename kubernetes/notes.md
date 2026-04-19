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


## notes
- configmap and secret have similar purpose but secret is more confidential 
- pod: working service, deployment: larger scale management for pod like network; replica, job: one-time execution job, cronjob: scheduling job
- service and pod connect via service-spec.selector, deployment-spec.template.metadata.labels
- port-forward to connect local device with kube cluster
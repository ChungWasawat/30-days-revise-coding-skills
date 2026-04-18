# ── LIST RESOURCES
- `kubectl get pods`                  # list pods in current namespace
- `kubectl get pods -A`               # list pods in ALL namespaces
- `kubectl get deployments`
- `kubectl get services`
- `kubectl get jobs`
- `kubectl get cronjobs`
- `kubectl get all`                   # everything in current namespace

# ── WATCH REAL-TIME UPDATES
* `kubectl get pods -w`              # re-prints table whenever state changes

# ── CONFIGMAPS
- `kubectl get configmaps`          # see all configmaps in kube system


# ── INSPECT A RESOURCE
* `kubectl describe pod my-pod`       # full detail: events, conditions, env vars
* `kubectl describe deployment my-deploy`

# ── SEE WHAT IS IN THE CONFIGMAPS
* `kubectl describe configmap pipeline-config`   # see all key-value pairs

# ── LOGS 
* `kubectl logs my-pod`               # print logs
* `kubectl logs my-pod -f`            # follow logs live (like tail -f)
* `kubectl logs my-pod --previous`    # logs from a pod that already crashed
* `kubectl logs job/my-etl-job`       # logs directly from a job (finds its pod)

# ── EXEC INTO A RUNNING POD
* `kubectl exec -it my-pod -- /bin/bash`
* `kubectl exec -it my-pod -- python3`   # drop into python

# ── APPLY / DELETE MANIFESTS
* `kubectl apply -f manifest.yaml`    # create or update resources (can be pod, job, etc) from file
* `kubectl delete -f manifest.yaml`   # delete resources defined in file
* `kubectl delete pod my-pod`         # delete a specific pod

# ── EXPLAIN KUBE COMPONENT/ RESOURCE
* `kubectl explain job`          # shows apiVersion, fields, and docs for Job
* `kubectl explain pod.spec`     # drill into nested fields
* `kubectl explain <kind>`

# ── SECRETS
To create secrets
* `kubectl create secret generic db-credentials --from-literal=DB_USER=admin --from-literal=DB_PASSWORD=supersecret`
* `kubectl create secret generic db-credentials --from-env-file=.env` with env file
* create secret.yaml
```
    data: 
        DB_USER: YWRtaW4=             
        DB_PASSWORD: c3VwZXJzZWNyZXQ=
```
* `kubectl get secret db-credentials -o yaml`       # Verify (values will show as base64)   
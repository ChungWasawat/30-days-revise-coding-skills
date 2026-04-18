#

### how to load values from environment
1. load all values in configMap and secretRef
```
spec:
  containers:
    - name: pipeline
      image: my-pipeline:latest
      envFrom:
        - configMapRef:
            name: pipeline-config    # every key becomes an env var
        - secretRef:
            name: db-credentials     # every key becomes an env var
```
2. load specific values in configMap and secretRef
```
spec:
  containers:
    - name: pipeline
      image: my-pipeline:latest
      envFrom:
        - configMapRef:
            name: pipeline-config     # load all values like LOG_LEVEL, APP_ENV, OUTPUT_DIR, etc.
      env:
        - name: DATABASE_URL          # pull just this one key from the secret
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: DATABASE_URL
```
in `secret.yaml`
```
# manifests/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
data:
  # echo -n "postgresql+psycopg2://admin:supersecret@postgres-service:5432/warehouse" | base64
  DATABASE_URL: cG9zdGdyZXNxbCtwc3ljb3BnMjovL2FkbWluOnN1cGVyc2VjcmV0QHBvc3RncmVzLXNlcnZpY2U6NTQzMi93YXJlaG91c2U=
```

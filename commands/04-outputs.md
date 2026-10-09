# Sorties des commandes

Sorties observées après l’installation initiale, le 9 octobre 2026. Les valeurs `AGE`, les adresses IP et les noms des pods peuvent changer. Aucun secret n’est inclus.

```bash
$ docker build -t gitops-fastapi:1.0.0 ./app
# ...
#10 naming to docker.io/library/gitops-fastapi:1.0.0 done
#10 DONE 1.4s
```

```bash
$ kind create cluster --name gitops-tp
Creating cluster "gitops-tp" ...
 ✓ Ensuring node image (kindest/node:v1.37.0)
 ✓ Preparing nodes
 ✓ Writing configuration
 ✓ Starting control-plane
 ✓ Installing CNI
 ✓ Installing StorageClass
Set kubectl context to "kind-gitops-tp"
```

```bash
$ kind load docker-image gitops-fastapi:1.0.0 --name gitops-tp
Image: "gitops-fastapi:1.0.0" ... not yet present on node "gitops-tp-control-plane", loading...
```

```bash
$ gh repo create Ala-ADN/tp1-gitops-argocd --public --source=. --remote=origin --push
https://github.com/Ala-ADN/tp1-gitops-argocd
* [new branch] HEAD -> main
```

```bash
$ kubectl create namespace argocd
namespace/argocd created
```

```bash
$ kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
customresourcedefinition.apiextensions.k8s.io/applications.argoproj.io serverside-applied
# ... autres ressources Argo CD créées (ServiceAccounts, RBAC, Deployments, Services)
deployment.apps/argocd-server serverside-applied
deployment.apps/argocd-repo-server serverside-applied
statefulset.apps/argocd-application-controller serverside-applied
```

```bash
$ kubectl -n argocd rollout status deployment/argocd-server --timeout=300s
deployment "argocd-server" successfully rolled out
```

```bash
$ kubectl -n argocd rollout status deployment/argocd-repo-server --timeout=300s
deployment "argocd-repo-server" successfully rolled out
```

```bash
$ kubectl apply -f argocd/application.yaml
application.argoproj.io/fastapi-demo created
```

```bash
$ kubectl -n gitops-demo rollout status deployment/fastapi-demo --timeout=300s
deployment "fastapi-demo" successfully rolled out
```

```bash
$ kubectl config current-context
kind-gitops-tp
```

```bash
$ kubectl -n argocd get application fastapi-demo -o jsonpath='{.status.sync.status} {.status.health.status}{"\n"}'
Synced Healthy
```

```bash
$ kubectl -n gitops-demo get deployment,pods,service
NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/fastapi-demo   1/1     1            1           11m

NAME                                READY   STATUS    RESTARTS   AGE
pod/fastapi-demo-86495c9695-4kw86   1/1     Running   0          11m

NAME                   TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/fastapi-demo   ClusterIP   10.96.141.84   <none>        80/TCP    11m
```

```bash
$ kubectl -n gitops-demo exec deployment/fastapi-demo -- python -c 'import urllib.request; print(urllib.request.urlopen("http://127.0.0.1:8000/health").read().decode())'
{"status":"ok"}
```

Les scénarios de démonstration (mise à l’échelle, drift, image invalide et rollback) restent à exécuter en direct ; leurs sorties ne sont pas présentées ici comme déjà vérifiées.

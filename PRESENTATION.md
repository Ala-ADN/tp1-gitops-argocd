# TP : Continuous Deployment avec GitOps et Argo CD

## Liens et objectif

- Dépôt Git public prévu : https://github.com/Ala-ADN/tp1-gitops-argocd
- Application : petite API FastAPI avec `/` et `/health`.
- Infrastructure locale : Kubernetes dans kind, Argo CD installé dans le namespace `argocd`.
- Source de vérité : `k8s/overlays/demo/kustomization.yaml` et les ressources de `k8s/base/`.
- Application Argo CD déclarée dans `argocd/application.yaml`.

Le dépôt contient le code de l'API, son Dockerfile et les manifests Kustomize. L'image `gitops-fastapi:1.0.0` est construite localement et chargée dans kind avant le premier déploiement. Cela évite de créer un compte de registre pour ce TP local. Pour déployer sur un autre cluster, publier l'image dans un registre accessible et changer `newName` dans Kustomize.

## Architecture

```text
GitHub (branche main, manifests Kustomize)
                  │
                  ▼ lecture périodique
             Argo CD Application
                  │
                  ▼ réconciliation
       Kubernetes : Deployment + Service
                  │
                  ▼
             API FastAPI
```

Argo CD lit Git et applique l'état désiré : `automated.enabled`, `selfHeal` et `prune` sont activés. Le dépôt est public afin que le contrôleur puisse le lire sans secret. Les commandes de préparation sont dans [`commands/01-setup.txt`](commands/01-setup.txt). Les manipulations en direct sont dans [`commands/02-demo.txt`](commands/02-demo.txt).

## Démonstration orale

| Scénario | Action | Ce que je montre |
| --- | --- | --- |
| Déploiement continu | Je passe de 1 à 2 répliques dans Kustomize, puis `git push`. | Argo CD détecte le commit et le Deployment passe à 2 pods sans `kubectl apply` de ma part. |
| Drift et self-healing | Je supprime le Deployment avec `kubectl delete`. | L'écart est détecté, puis Argo CD recrée automatiquement le Deployment. L'état OutOfSync peut être très bref. |
| Sync contre Health | Je référence un registre d'image inexistant, puis `git push`. | **Synced** signifie que le cluster correspond à Git. **Degraded** signifie que les pods ne fonctionnent pas ; `kubectl describe` montre l'erreur de tirage d'image. L'état peut d'abord être **Progressing**. |
| Historique et rollback | J'ouvre **History and Rollback** et je choisis la révision stable. | Je coupe temporairement Auto-Sync, lance le rollback, puis annule dans Git le commit défectueux et réactive Auto-Sync. L'état final est Synced + Healthy. |

## Pourquoi couper Auto-Sync avant le bouton Rollback ?

Argo CD bloque le rollback d'historique tant qu'Auto-Sync est activé. Après le rollback dans l'UI, le cluster fonctionne, mais Git contient encore la mauvaise image : l'Application peut donc être OutOfSync. `git revert` remet le dépôt à l'état stable et préserve l'historique des commits. Une fois Auto-Sync réactivé, Git et le cluster coïncident à nouveau.

## Vérifications à présenter

```text
kubectl config current-context
kubectl -n gitops-demo get deployment,pods,service
kubectl -n gitops-demo describe pods -l app=fastapi-demo
git log --oneline -4
```

Dans l'UI, montrer le panneau de l'Application, les statuts **Sync** et **Health**, les ressources et l'onglet **History and Rollback**. Après la présentation, le cluster peut être supprimé avec [`commands/03-cleanup.txt`](commands/03-cleanup.txt).

 <div align="center">
# 🚀 Mini-Projet 2 — Application 3-Tiers Sécurisée et Persistante

### Déploiement et sécurisation avec Kubernetes (k3s)

![Kubernetes](https://img.shields.io/badge/Kubernetes-k3s-326CE5?style=for-the-badge&logo=kubernetes)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?style=for-the-badge&logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql)
![Python](https://img.shields.io/badge/Python-Backend-3776AB?style=for-the-badge&logo=python)
![DevOps](https://img.shields.io/badge/DevOps-Cloud-00A98F?style=for-the-badge)

📄 **Rapport du mini-projet :** [Consulter le rapport PDF](mini_projet2.pdf)


---

## 1. Présentation du projet

Ce mini-projet consiste à développer, conteneuriser et déployer une application web trois niveaux en utilisant Docker et Kubernetes (k3s).

L'application réalisée est **Mes Contacts**, un gestionnaire de contacts permettant d'ajouter, consulter, modifier et supprimer des contacts.

Le projet met en pratique les principales fonctionnalités de Kubernetes concernant le déploiement, la configuration, la gestion des ressources, la persistance des données et la sécurité.

### Objectifs

- Développer et tester une application en local.
- Construire et publier les images Docker.
- Déployer les composants dans un namespace Kubernetes dédié.
- Configurer ResourceQuota et LimitRange.
- Externaliser la configuration avec ConfigMap et Secret.
- Déployer PostgreSQL avec StatefulSet.
- Assurer la persistance des données avec PVC.
- Exposer l'application avec Ingress et Traefik.
- Mettre en place une sauvegarde planifiée avec CronJob.
- Gérer les permissions avec RBAC et ServiceAccounts.
- Renforcer la sécurité avec SecurityContext et NetworkPolicies.

---

## 2. Architecture de l'application

L'application repose sur une architecture trois niveaux :

| Niveau | Composant | Fonction |
|---|---|---|
| Présentation | Frontend / Nginx | Interface web Mes Contacts |
| Application | API REST | Traitement des opérations CRUD |
| Données | PostgreSQL | Stockage des contacts |

### Architecture Kubernetes

```text
                  UTILISATEUR
                       |
                       |
                Ingress - Traefik
                app.k3s.local
                       |
                       |
                 frontend-svc
                       |
                       |
                FRONTEND POD
                    Nginx
                       |
                    /api/
                       |
                       |
                   api-svc
                       |
                       |
                 API DEPLOYMENT
                   2 REPLICAS
                       |
                       |
                  db-service
                  Headless
                       |
                       |
                POSTGRESQL
                 StatefulSet
                    db-0
                       |
                       |
                    PVC
                 Persistent
                   Storage


              BACKUP : CronJob
                       |
                    pg_dump
                       |
                    backup-pvc


              SÉCURITÉ KUBERNETES
                       |
              +--------+--------+
              |        |        |
           Resource  LimitRange  RBAC
            Quota
                       |
                 NetworkPolicies
                       |
                 SecurityContext
```

### Technologies utilisées

- Docker et Docker Compose.
- Docker Hub.
- Kubernetes (k3s).
- PostgreSQL.
- Python pour le backend.
- HTML, CSS et JavaScript pour le frontend.
- Nginx.
- Traefik et Ingress.
- YAML.
- PowerShell.
- VMware Workstation.

---

## 3. Organisation du dépôt

```text
Mini-Projet2-Kubernetes/
│
├── app/
│   ├── backend/
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   └── requirements.txt
│   │
│   └── frontend/
│       ├── Dockerfile
│       ├── default.conf
│       └── index.html
│
├── k8s/
│   ├── 00-namespace/
│   │   └── quota.yaml
│   │
│   ├── 10-config/
│   │   ├── app-config.yaml
│   │   └── secret.example.yaml
│   │
│   ├── 20-db/
│   │   ├── db-service.yaml
│   │   ├── db-statefulset.yaml
│   │   ├── backup-pvc.yaml
│   │   └── db-backup.yaml
│   │
│   ├── 30-app/
│   │   ├── api-deployment.yaml
│   │   ├── api-service.yaml
│   │   ├── frontend-configmap.yaml
│   │   ├── frontend-deployment.yaml
│   │   ├── frontend-service.yaml
│   │   └── ingress.yaml
│   │
│   └── 40-security/
│       ├── serviceaccounts.yaml
│       └── rbac.yaml
│
├── screenshots/
│   ├── 01-docker-compose-build.png
│   ├── 02-application-local-mes-contacts.png
│   ├── 03-docker-image-tagging.png
│   ├── ...
│   └── 43-final-application-validation.png
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 4. Réalisation du projet par phases

### Phase 0 — Développement et test local

Construction des composants avec Docker Compose et vérification du fonctionnement de l'application Mes Contacts.

**Preuves :**

![Build Docker Compose](screenshots/01-docker-compose-build.png.jpg)

![Application locale](screenshots/02-application-local-mes-contacts.png.jpg)

### Phase 1 — Conteneurisation et publication

Création des images Docker, attribution des tags versionnés et publication sur Docker Hub.

Images applicatives :

- `arijbelaid/todo-api:1.0.0`
- `arijbelaid/todo-frontend:1.0.0`

**Preuves :**

![Tagging des images](screenshots/03-docker-image-tagging.png.jpg)

![Publication Docker Hub](screenshots/04-dockerhub-image-push.png.jpg)

### Phase 2 — Namespace, ResourceQuota et LimitRange

Création du namespace `miniproj2`, configuration des quotas et définition des limites de ressources.

**Preuves :**

![ResourceQuota YAML](screenshots/05-resourcequota-yaml.png.jpg)

![Application des quotas](screenshots/06-namespace-quota-application.png.jpg)

![Vérification du quota](screenshots/07-resourcequota-verification.png.jpg)

![Test LimitRange](screenshots/08-limitrange-test.png.jpg)

### Phase 3 — ConfigMap et Secret

Externalisation de la configuration et création des identifiants de connexion à la base de données avec Kubernetes Secret.

Un fichier modèle est utilisé pour Git afin de ne pas publier les véritables identifiants.

**Preuves :**

![ConfigMap](screenshots/09-configmap-yaml.png.jpg)

![Création du Secret](screenshots/10-kubernetes-secret-creation.png.jpg)

![Secret modèle](screenshots/11-secret-example-git.png.jpg)

![Application ConfigMap](screenshots/12-configmap-application.png.jpg)

![Vérification ConfigMap et Secret](screenshots/13-configmap-secret-verification.png.jpg)

### Phase 4 — Base de données avec StatefulSet

Déploiement de PostgreSQL avec un Service Headless et un StatefulSet.

Configuration du volume persistant pour conserver les données de la base.

**Preuves :**

![Service Headless](screenshots/14-database-headless-service.png.jpg)

![StatefulSet](screenshots/15-postgresql-statefulset-yaml.png.jpg)

![Application des manifestes](screenshots/16-database-manifests-application.png.jpg)

![Vérification PostgreSQL](screenshots/17-database-pod-verification.png.jpg)

### Phase 5 — Déploiement API et frontend

Déploiement des composants applicatifs dans Kubernetes et vérification de leur état.

Consultation des logs de l'API pour vérifier les requêtes `/health` et `/ready`.

**Preuves :**

![Déploiement API frontend](screenshots/18-api-frontend-deployment.png.jpg)

![Statut des Pods](screenshots/19-kubernetes-pods-status.png.jpg)

![Logs API](screenshots/20-api-logs-health-ready.png.jpg)

### Phase 6 — Ingress

Configuration de Traefik et création de l'Ingress pour permettre l'accès à l'application à travers le nom d'hôte `app.k3s.local`.

**Preuves :**

![Ingress YAML](screenshots/21-ingress-yaml.png.jpg)

![Application Ingress](screenshots/22-ingress-application.png.jpg)

![Test Ingress](screenshots/23-ingress-curl-test.png.jpg)

![Application accessible](screenshots/24-application-access-ingress.png)

### Phase 7 — Persistance et résilience

Ajout de contacts et vérification de leur présence dans PostgreSQL.

Suppression du Pod `db-0`, puis vérification de sa recréation automatique et de la conservation des données.

Test de la résilience des Pods API.

**Preuves :**

![Contacts avant suppression](screenshots/25-contacts-before-pod-deletion.png.jpg)

![Suppression du Pod](screenshots/26-database-pod-deletion.png.jpg)

![Recréation du Pod](screenshots/27-database-pod-recreation.png.jpg)

![Persistance des données](screenshots/28-data-persistence-verification.png.jpg)

![Résilience API](screenshots/29-api-pod-resilience.png.jpg)

### Phase 8 — Sauvegarde planifiée

Création du volume de sauvegarde et configuration du CronJob pour automatiser les sauvegardes PostgreSQL.

Exécution d'un Job de test et vérification de l'état des Pods ainsi que des données de la base.

**Preuves présentes dans le rapport :**

![Configuration PVC et CronJob](screenshots/30-backup-pvc-cronjob-yaml.png.jpg)

![Application du Job](screenshots/31-backup-job-application.png.jpg)

![Vérification du Job](screenshots/32-backup-job-verification.png.jpg)

![Vérification PostgreSQL](screenshots/33-postgresql-backup-data-check.png.jpg)

### Phase 9 — RBAC et ServiceAccounts

Création des ServiceAccounts et configuration des permissions avec Role et RoleBinding.

Vérification des droits d'accès du compte `dev-viewer` et modification des manifestes applicatifs.

**Preuves :**

![ServiceAccounts](screenshots/34-serviceaccounts-creation.png.jpg)

![Role et RoleBinding](screenshots/35-rbac-role-rolebinding-yaml.png.jpg)

![Application RBAC](screenshots/36-rbac-configuration-application.png.jpg)

![Vérification RBAC](screenshots/37-rbac-permissions-verification.png)

![Modification des Deployments](screenshots/38-serviceaccount-deployments-update.png.jpg)

![Test du jeton](screenshots/39-serviceaccount-token-test.png.jpg)

### Phase 10 — Durcissement et NetworkPolicies

Application des configurations de sécurité et vérification de la désactivation du montage automatique du jeton ServiceAccount.

Test des NetworkPolicies et vérification du SecurityContext avec les paramètres de sécurité des conteneurs.

Validation du fonctionnement final de l'application.

**Preuves :**

![Désactivation du jeton](screenshots/40-serviceaccount-token-disabled.png.jpg)

![Test NetworkPolicy](screenshots/41-networkpolicy-connectivity-test.png.jpg)

![SecurityContext](screenshots/42-securitycontext-verification.png.jpg)

![Validation finale](screenshots/43-final-application-validation.png.jpg)

---

## 7. Conclusion

Ce mini-projet nous a permis de mettre en pratique les concepts essentiels de Kubernetes et des pratiques DevOps à travers le déploiement d'une application trois niveaux.

La réalisation a permis de travailler sur la conteneurisation, l'orchestration, la gestion des ressources, la configuration externalisée, la persistance des données et la sécurisation des communications.

Les différentes phases ont également permis de comprendre les mécanismes de résilience, de contrôle des accès et de protection des applications dans un environnement Kubernetes.

**Mini-Projet 2 — Application 3-Tiers Sécurisée et Persistante**

**Master DevOps & Cloud — ISET Tozeur**

**Année universitaire 2026–2027**


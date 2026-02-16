# Guide Complet & Test du Projet MLOps 🚀

## Vue d'ensemble
Ce document vous guide à travers la plateforme MLOps complète que nous avons construite. Il couvre tout, du développement local au déploiement automatisé CI/CD.

## 1. Boucle de Développement Locale

### Entraînement (Airflow)
1.  **Déclencheur** : DAG `credit_scoring_training` dans Airflow ([http://localhost:8080](http://localhost:8080)).
2.  **Processus** : Ingestion des données -> Validation -> Entraînement XGBoost -> Explications (SHAP) -> Évaluation.
3.  **Versioning** :
    -   Les données sont hachées (MD5) et le hash est loggué dans les paramètres MLflow.
    -   Le modèle est versionné dans les Artefacts MLflow ([http://localhost:5000](http://localhost:5000)).

### Service d'API (FastAPI)
1.  **Rechargement à Chaud (Hot-Reload)** : L'API recharge automatiquement le nouveau modèle dès la fin de l'entraînement (via le point de terminaison `/reload`).
2.  **Prédiction** : `POST /predict` renvoie le score de risque, la classification et les valeurs SHAP.
3.  **Monitoring** : Prometheus collecte les métriques -> Grafana les affiche.

---

## 2. Pipeline CI/CD (GitHub Actions)
Nous avons établi un pipeline robuste pour chaque `git push`.

### Intégration Continue (CI)
-   **Linting** : `ruff` vérifie la qualité du code et les imports inutilisés.
-   **Tests** : `pytest` exécute les tests unitaires dans `tests/` pour vérifier la santé et la logique de l'API.

### Déploiement Continu (CD)
-   **Build** : L'image Docker `scoring-api` est construite.
-   **Push**(Publication) : L'image est poussée sur Docker Hub avec les tags `latest` et le `sha` du commit.
-   **Auto-Déploiement** : Watchtower (en local) détecte la nouvelle image sur Docker Hub et met à jour le conteneur en cours d'exécution automatiquement.

![Succès Docker Hub](https://github.com/Ahikpa/advanced_mlops/actions/workflows/mlops.yml/badge.svg)

---

## 3. Checklist de Vérification

### ✅ Validations Effectuées
-   [x] **DAG Airflow** : S'exécute avec succès et loggue dans MLflow.
-   [x] **API** : Répond correctement aux endpoints `/predict` et `/reload`.
-   [x] **Monitoring** : Les tableaux de bord Grafana affichent l'activité de l'API.
-   [x] **CI/CD** : Les GitHub Actions sont vertes, et Docker Hub contient l'image.

### 🧪 Comment Tester Manuellement
1.  **Lancer un Entraînement** : Activez le DAG dans Airflow et attendez la fin.
2.  **Vérifier MLflow** : Confirmez qu'un nouveau Run existe avec le paramètre `data_hash`.
3.  **Tester l'API** :
    -   Utilisez le Swagger UI : [http://localhost:8000/docs](http://localhost:8000/docs)
    -   Envoyez une requête `POST /predict` avec un JSON de test.
4.  **Vérifier le Rechargement** : Les logs de l'API doivent indiquer "Model reloaded successfully" juste après l'entraînement.

  
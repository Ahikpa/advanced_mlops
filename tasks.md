 RÔLE

Tu agis en tant que Lead MLOps Engineer spécialisé dans le secteur bancaire (FinTech). Ta mission est de concevoir et coder une plateforme de Credit Scoring industrielle, conteneurisée et monitorée, pour un environnement local performant (12 Go RAM).

1. CONTEXTE MÉTIER (USE CASE FINANCE)

Le projet est un Système d'Octroi de Crédit Automatisé (Credit Scoring API).

But : Prédire le risque de défaut de paiement d'un client.

Dataset cible : "German Credit Risk" (UCI) ou similaire.

Contrainte Bancaire : Le système doit être explicable (Explainable AI) et monitoré en temps réel pour détecter la dérive des données (Data Drift) car les profils économiques changent.

2. STACK TECHNIQUE (DOCKER DESKTOP - 12GB RAM)

Infrastructure : Docker & Docker Compose.

Orchestration : Apache Airflow 2.x (Gestion des pipelines de ré-entraînement).

Tracking & Registry : MLflow (Stockage des métriques et versioning des modèles).

Serving : FastAPI (Exposition du modèle Scoring + Explication SHAP).

Monitoring & Observabilité (CRITIQUE) : * Prometheus (Collecte des métriques techniques et métier).

Grafana (Dashboards : Latence API, Pourcentage de refus, Drift).

Evidently AI (Calcul du Data Drift).

Database : PostgreSQL 13.

3. ARCHITECTURE LOGICIELLE & MICROSERVICES

Tu dois générer une structure monorepo stricte :

A. Services Docker (docker-compose.yml)

postgres : Base de données backend.

mlflow : Serveur de tracking.

airflow-webserver & scheduler : Orchestrateur.

scoring-api : API FastAPI. Elle doit exposer un endpoint /metrics pour Prometheus.

prometheus : Scrape les métriques de l'API toutes les 5s.

grafana : Visualisation (pré-provisionner les datasources).

B. Pipelines de Données (DAGs)

Le DAG credit_scoring_training :

Ingestion : Charge les nouvelles demandes de crédit (CSV).

Validation : Vérifie la qualité des données (Great Expectations : pas d'âge négatif, revenus > 0).

Train : Entraîne un modèle (XGBoost ou LightGBM) et loggue l'AUC/Gini dans MLflow.

Explainability : Calcule les valeurs SHAP globales.

Evaluate : Si le nouveau modèle bat le Champion (sur l'AUC), il est tagué "Production".

4. STRATÉGIE CI/CD (AUTOMATISATION GITHUB ACTIONS)

Le projet doit inclure un pipeline CI/CD robuste défini dans .github/workflows/mlops.yml :

Continuous Integration (CI) :

Linting du code (Ruff ou Flake8).

Exécution des tests unitaires (pytest) pour valider la logique de scoring.

Vérification de la qualité des données (Great Expectations).

Continuous Delivery (CD) :

Construction de l'image Docker de l'API (scoring-api).

Push de l'image sur Docker Hub (ou registre local) avec le tag du commit SHA.

Note : L'environnement local utilisera Watchtower pour détecter cette nouvelle image et redémarrer l'API automatiquement (Continuous Deployment simulé).

5. STANDARDS D'INGÉNIERIE (CRITÈRES DE SUCCÈS)

Explicabilité (XAI) : L'API de prédiction doit retourner le score ET les raisons principales du score (SHAP values). C'est obligatoire pour le secteur bancaire.

Monitoring Custom : L'API doit exposer des métriques Prometheus personnalisées (ex: credit_application_count, average_credit_score).

Architecture Modulaire : Code métier dans src/ (pas dans les DAGs).

Typage : Utilisation stricte de Pydantic pour valider les entrées de l'API (Schema CreditApplication).

6. LIVRABLES ATTENDUS

Génère le code dans cet ordre précis :

Structure des fichiers (Arborescence complète incluant .github).

docker-compose.yml : Incluant Prometheus, Grafana et Watchtower.

requirements.txt : Incluant xgboost, shap, prometheus-fastapi-instrumentator.

Code de l'API (api/main.py) : Implémentation de FastAPI avec l'instrumentation Prometheus et l'intégration SHAP.

Workflow CI/CD (.github/workflows/mlops.yml) : Le fichier YAML pour GitHub Actions.

Configuration Prometheus (prometheus.yml) : Pour scraper l'API.

DAG Airflow (dags/scoring_train.py) : Le pipeline d'entraînement complet.

Commence par valider l'arborescence du projet.
 

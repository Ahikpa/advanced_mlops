# Guide de Test du Projet MLOps 🚀

Suivez ces étapes pour comprendre le flux complet du projet, de l'entraînement du modèle jusqu'au monitoring.

---

### Étape 1 : Orchestration et Entraînement (Airflow)
Le flux commence par le déclenchement du pipeline d'entraînement.

1.  Ouvrez **Airflow** : [http://localhost:8080](http://localhost:8080)
    -   *User/Pass : `airflow` / `airflow`*
2.  Activez le DAG `credit_scoring_training` (le bouton "Pause/Unpause" en haut à gauche).
3.  Cliquez sur le bouton **Play** (Trigger DAG) à droite pour lancer l'exécution.
4.  **Ce qui se passe :**
    -   `ingest_data` : Charge le dataset `german_credit_data.csv`.
    -   `validate_data` : Vérifie la qualité des données.
    -   `train_model` : Entraîne un modèle XGBoost et loggue tout dans MLflow.
    -   `explain_model` & `evaluate_model` : Génèrent les explications SHAP et comparent les performances.

---

### Étape 2 : Tracking des Expériences (MLflow)
Une fois le DAG terminé, le modèle est stocké.

1.  Ouvrez **MLflow** : [http://localhost:5000](http://localhost:5000)
2.  Vous verrez une nouvelle expérience nommée `credit_scoring_experiment`.
3.  Cliquez sur le dernier "Run". Vous y trouverez :
    -   Les **Metrics** (comme l'AUC).
    -   Les **Parameters** : Vérifiez la présence du `data_hash` (votre versioning de données).
    -   Le **Modèle** (dans la section Artifacts).

---

      "Purpose": "car"
    }
    ```
4.  Cliquez sur **Execute**.
5.  **Résultat :** Vous recevrez une `prediction` (0 ou 1) et le score de probabilité.

---

### Étape 4 : Monitoring (Prometheus & Grafana)
L'API génère des métriques à chaque appel.

1.  **Vérifier les métriques brutes** : [http://localhost:8000/metrics](http://localhost:8000/metrics)
    -   Cherchez `http_request_duration_seconds_count` pour voir vos appels à l'API.
2.  **Vérifier Prometheus** : [http://localhost:9090/targets](http://localhost:9090/targets)
    -   Vérifiez que la cible `scoring-api` est bien en statut **UP**.
3.  **Visualiser dans Grafana** : [http://localhost:3000](http://localhost:3000)
    -   *User/Pass : `admin` / `admin`*
    -   Allez dans **Dashboards** pour voir les performances de l'API.

---

### Étape 5 : Flux CD (Watchtower)
Watchtower tourne en arrière-plan. Si vous poussez une nouvelle image Docker de l'API sur votre registre, Watchtower la détectera et redémarrera le conteneur automatiquement.

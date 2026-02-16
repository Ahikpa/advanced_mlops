import pandas as pd
import shap
import pickle
import os
import mlflow
import mlflow.xgboost
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from schemas import CreditApplication

app = FastAPI(title="Credit Scoring API", description="API for predicting credit risk with explainability.")

# Initialize Prometheus Instrumentator
Instrumentator().instrument(app).expose(app)

# Configuration
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
EXPERIMENT_NAME = "credit_scoring_experiment"
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
EXPERIMENT_NAME = "credit_scoring_experiment"
# FEATURE_PATH is no longer a static path, it will be downloaded from artifacts

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Global variables for model and explainer
model = None
explainer = None
feature_names = None

def load_latest_model():
    global model, explainer, feature_names
    try:
        # 2. Try to load model from MLflow
        client = mlflow.tracking.MlflowClient()
        experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
        if experiment:
            runs = client.search_runs(
                experiment_ids=[experiment.experiment_id],
                filter_string="status = 'FINISHED'",
                order_by=["attribute.start_time DESC"],
                max_results=1
            )
            if runs:
                run_id = runs[0].info.run_id
                
                # Download feature names artifact
                local_dir = "/tmp"
                mlflow.artifacts.download_artifacts(run_id=run_id, artifact_path="model_features.pkl", dst_path=local_dir)
                feature_path = os.path.join(local_dir, "model_features.pkl")
                
                with open(feature_path, "rb") as f:
                    feature_names = pickle.load(f)
                print(f"Feature names loaded from run {run_id}: {len(feature_names)} features.")

                model_uri = f"runs:/{run_id}/model"
                model = mlflow.xgboost.load_model(model_uri)
                explainer = shap.TreeExplainer(model)
                print(f"Model loaded successfully from MLflow run: {run_id}")
            else:
                print("No successful runs found in experiment.")
        else:
            print(f"Experiment '{EXPERIMENT_NAME}' not found.")
            
    except Exception as e:
        print(f"Error during model loading: {e}")

@app.post("/reload")
def reload_model():
    """Endpoint to manually trigger a model reload from MLflow."""
    load_latest_model()
    if model is not None:
        return {"status": "success", "message": "Model reloaded successfully."}
    else:
        raise HTTPException(status_code=503, detail="Model reload failed. Check logs.")

@app.on_event("startup")
def startup_event():
    load_latest_model()

@app.post("/predict")
def predict(application: CreditApplication):
    global model, explainer, feature_names
    
    if model is None or feature_names is None:
        # Attempt to reload if not loaded
        load_latest_model()
        if model is None or feature_names is None:
            raise HTTPException(status_code=503, detail="Model not loaded. Please wait for the training pipeline to finish.")

    try:
        # 1. Preprocessing & Alignment
        df = pd.DataFrame([application.dict()])
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()
        df = pd.get_dummies(df, columns=cat_cols, dummy_na=True)
        
        # Add missing columns from alignment list
        for col in feature_names:
            if col not in df.columns:
                df[col] = 0
                
        # Reorder and filter to match training exactly
        df = df[feature_names]
        
        # 2. Prediction
        prob = float(model.predict_proba(df)[0, 1])
        
        # 3. Explainability (SHAP)
        shap_vals = explainer.shap_values(df)
        # Handle different SHAP output formats (sometimes list for multi-class)
        if isinstance(shap_vals, list):
            shap_vals = shap_vals[1] # For binary classification, use second class
            
        # Map feature names to SHAP values
        importance = dict(zip(feature_names, [float(v) for v in shap_vals[0]]))
        
        return {
            "risk_score": round(prob, 4),
            "classification": "High Risk" if prob > 0.5 else "Low Risk",
            "shap_values": importance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "features_loaded": feature_names is not None
    }

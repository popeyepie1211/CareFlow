"""
predict.py - Make Predictions with Trained Model
===================================================
What: Loads the saved Random Forest model and predicts test results.
Why:  Demonstrates model inference as part of the pipeline.
How:  Uses Joblib to load the model and predicts on sample data.

Pipeline flow:
  model.joblib -> predict.py -> predictions
"""

import joblib
import pandas as pd


def load_model(filepath="ml/model.joblib"):
    """Load the trained model from disk."""
    try:
        model = joblib.load(filepath)
        print(f"[SUCCESS] Model loaded from '{filepath}'")
        return model
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        return None


def predict(model, input_data):
    """
    Make predictions using the trained model.

    Args:
        model:      Trained RandomForestClassifier
        input_data: DataFrame with feature columns

    Returns:
        Array of predicted class labels
    """
    predictions = model.predict(input_data)
    print(f"[INFO] Generated {len(predictions)} predictions")
    return predictions


# --- Run directly to test ---
if __name__ == "__main__":
    model = load_model()
    if model is not None:
        # Sample patient data for testing
        # Columns: age, gender, medical_condition, admission_type,
        #          insurance_provider, billing_amount, length_of_stay
        # (Values are label-encoded integers for categorical columns)
        sample = pd.DataFrame([
            [65, 0, 2, 1, 3, 35000.00, 14],
            [30, 1, 0, 0, 1, 22000.00, 7],
            [45, 0, 4, 2, 0, 48000.00, 21],
        ], columns=["age", "gender", "medical_condition", "admission_type",
                     "insurance_provider", "billing_amount", "length_of_stay"])

        preds = predict(model, sample)
        print(f"Predictions: {preds}")
        print("(0=Abnormal, 1=Inconclusive, 2=Normal)")

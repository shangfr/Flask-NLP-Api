# -*- coding: utf-8 -*-
"""
Created on Tue May 25 11:18:20 2021

@author: shangfr
"""

import mlflow
import mlflow.sklearn
import pandas as pd
import matplotlib.pyplot as plt
 
from numpy import savetxt
 
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_diabetes
 
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

db = load_diabetes()
X = db.data
y = db.target
X_train, X_test, y_train, y_test = train_test_split(X, y)

mlflow.get_tracking_uri()
mlflow.get_artifact_uri()

# 设定tracking_uri：数据库
mlflow.set_tracking_uri('http://localhost:5000')
mlflow.set_experiment("test_02")

# With autolog() enabled, all model parameters, a model score, and the fitted model are automatically logged.  
with mlflow.start_run():
    
    # Enable autolog()
    # mlflow.sklearn.autolog() requires mlflow 1.11.0 or above.
    mlflow.sklearn.autolog()
    # Set the model parameters. 
    n_estimators = 100
    max_depth = 6
    max_features = 5
    
    # Create and train model.
    rf = RandomForestRegressor(n_estimators = n_estimators, max_depth = max_depth, max_features = max_features)
    rf.fit(X_train, y_train)
    
    # Use the model to make predictions on the test dataset.
    predictions = rf.predict(X_test)
    
    
    
# mlflow ui --backend-store-uri 'sqlite:///ml_test.db'   
# mlflow models serve -m models:/mymodel/1 -p 1234 --no-conda
# mlflow models serve -m mlruns/1/e6752244e3d842aea249d5a91af92dd8/artifacts/model -p 1234  --no-conda
import mlflow.pyfunc

model_name = "mymodel"
model_version = 5

model = mlflow.pyfunc.load_model(
    model_uri=f"models:/{model_name}/{model_version}"
)

model.predict([X_test[0]])    
    
model.predict(123)
    


from mlflow.pyfunc import PythonModel


class MultiModel(PythonModel):

    def predict(self,context, X):
        return [X]


# Create a features.txt artifact file
features = "rooms, zipcode, median_price, school_rating, transport"
with open("features.txt", 'w') as f:
    f.write(features) 
    
dictionary = {"k": "v"}

mlflow.set_tracking_uri('sqlite:///ml_test.db')
mlflow.set_experiment("test_07")    
import os
with mlflow.start_run() as run:
    mlflow.log_param("alpha", 1)
    mlflow.log_param("l1_ratio", 1)
    mlflow.log_metric("rmse", 10)
    mlflow.log_dict(dictionary, "data.json")
    mlflow.log_artifact("features.txt")
    mlflow.log_text("text1", "file1.txt")
    
    mlflow.pyfunc.save_model(
        path=os.path.join(run.info.artifact_uri,'model'),
        python_model= MultiModel(),
        code_path=['multi_model.py'],
        conda_env={
            'channels': ['defaults', 'conda-forge'],
            'dependencies': [
                'mlflow=1.2.0',
                'numpy=1.16.5',
                'python=3.6.9',
                'scikit-learn=0.21.3',
                'cloudpickle==1.2.2'
            ],
            'name': 'mlflow-env'
        }
    )
    

import joblib
joblib.dump(python_model, 'filename.pkl') 
clf = joblib.load('./mlruns/7/99e8bb06c9164a4b9cae1d4d6e63012a/artifacts/model/python_model.pkl') 

clf.predict(context=None,X=1)

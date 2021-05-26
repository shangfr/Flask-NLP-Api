# -*- coding: utf-8 -*-
"""
Created on Tue May 25 17:40:17 2021

@author: shangfr
"""

import os
import mlflow
from mlflow.pyfunc import PythonModel


class MultiModel(PythonModel):
    def load_context(self, context):
        import paddlehub as hub
        self.simnet_model = hub.Module(name="simnet_bow")
        self.context = context

    def predict(self, context, sentence):

        test_text = [[sentence], ['接口上大嫁风尚']]
        results = self.simnet_model.similarity(texts=test_text)

        return results


mlflow.set_tracking_uri('sqlite:///ml_test.db')
mlflow.set_experiment("test_001")
dictionary = {"k": "v"}
with mlflow.start_run() as run:
    mlflow.log_param("alpha", 1)
    mlflow.log_param("l1_ratio", 1)
    mlflow.log_metric("rmse", 10)
    mlflow.log_dict(dictionary, "data.json")
    #mlflow.log_artifact("features.txt")
    mlflow.log_text("text1", "file1.txt")

    mlflow.pyfunc.save_model(
        path=os.path.join(run.info.artifact_uri, 'model'),
        python_model=MultiModel(),
        code_path=['use_mlflow.py'],
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
    
    
import mlflow.pyfunc

model_name = "mymodel"
model_version = 1

model = mlflow.pyfunc.load_model(
    model_uri=f"models:/{model_name}/{model_version}"
)


    
model.predict('今天天气太热了')
model.context()

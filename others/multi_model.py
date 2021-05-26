# -*- coding: utf-8 -*-
"""
Created on Tue May 25 16:33:44 2021

@author: shangfr
"""

import numpy as np
from mlflow.pyfunc import PythonModel
from sklearn.base import clone

class MultiModel(PythonModel):

    def __init__(self, estimator=None, n=10):
        self.n = n
        self.estimator = estimator

    def fit(self, X, y=None):
        self.estimators = []
        for i in range(self.n):
            e = clone(self.estimator)
            e.set_params(random_state=i)
            X_bootstrap = X.sample(frac=1, replace=True, random_state=i)
            y_bootstrap = y.sample(frac=1, replace=True, random_state=i)
            e.fit(X_bootstrap, y_bootstrap)
            self.estimators.append(e)
        return self

    def predict(self, context, X):
        return np.stack([
            np.maximum(0, self.estimators[i].predict(X))
            for i in range(self.n)], axis=1
        )
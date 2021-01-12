import math

import numpy as np

import pandas as pd

from sklearn.feature_selection import VarianceThreshold


class FeatureSelector:
    def __init__(self, df):
        self.df = df

    def select_features(self):
        total_features = len(self.df.columns)
        print("Total Features to proceed with Feature Selection: {}...".format(total_features))

        print("Selecting Important Features using Variance Threshold...")
        current_features = self.variance()
        print("Proceeding with Feature Selection using Dispersion Ratio...")
        current_features = self.dispersion_ratio()

        return current_features

    def variance(self):
        v_threshold = VarianceThreshold(threshold=0)
        v_threshold.fit(self.df)
        importance_by_variance = v_threshold.get_support()
        importance_by_variance_dict = dict(zip(self.df.columns,importance_by_variance))
        important_features = list(importance_by_variance).count(True)
        print("Number of important features: {}\n".format(important_features))

        current_features = []
        for key,value in importance_by_variance_dict.items():
            if value == True:
                current_features.append(key)
        
        return current_features
    
    def dispersion_ratio(self):
        self.df = self.df + 1 #avoid 0 division

        aritmeticMean = np.mean(self.df, axis =0 )
        geometricMean = np.power(np.prod(self.df, axis =0 ),1/self.df.shape[0])
        R = aritmeticMean/geometricMean
        
        current_features = []
        for i in range(len(R)):
            dispersion_value = R[i]
            if dispersion_value >= 0.5:
                current_features.append(self.df.columns[i])
        
        print("Number of important features by dispersion ratio: {}".format(len(current_features)))
        print("Final Features are", ', '.join(current_features)[:-2])

        return current_features
        
    
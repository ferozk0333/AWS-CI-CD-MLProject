#derived columns, encoding, categorical features into numerical ones etc

import sys 
import os   
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer   #used to create pipeline (OHE->StdScaler)
from sklearn.impute import SimpleImputer        #handle missing values
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:      # gives any path/inputs that we may require for transformation components
    preprocessor_obj_file_path = os.path.join('artifacts',"preprocessor.pkl")      #just in case we wish to save a model in a pickle file


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        
    def get_data_transformer_object(self):                # to create pickle file

        '''This function is responsible for data transformation'''

        try:
            num_features = ['writing_score','reading_score']
            cat_features = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]

            #num_pipeline first handles missing values and then scales the values.
            num_pipeline = Pipeline(
                steps= [
                    ("imputer",SimpleImputer(strategy="median")),                         # handling missing values, median because of outliers
                    ("scaler",StandardScaler())
                ]

            )

            cat_pipeline = Pipeline(
                steps= [
                    ("imputer",SimpleImputer(strategy="most_frequent")),                 # handling missing values with mode
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )

            logging.info("Categorical Columns: {}".format(cat_features))
            logging.info("Numerical Columns: {}".format(num_features))

            # let's join the two pipelines together
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,num_features),      #pipeline name, what pipeline it is, column names
                    ("cat_pipeline",cat_pipeline,cat_features)
                ]
            )
           
            return preprocessor


        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            print(train_df)

            logging.info("Train&Test read completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "math_score"
            num_features = ['writing_score','reading_score']
            cat_features = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)   # fit vs fit_transform
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)


            

            train_arr = np.c_[                      #c_ --> concatenation along second axis
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[                      #c_ --> concatenation along second axis
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info("Saved preprocessing object")

            #saving pickle file, definition in utils.py
            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj

            )
            
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )


    
        except Exception as e:
            raise CustomException(e,sys)



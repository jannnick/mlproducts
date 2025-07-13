"""
import sys
import pandas as pd
from src.exceptions import CustomException
from src.utils import load_object
import os

class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self, features):
        try:
            model_path = os.path.join("artifacts/model.pkl")
            preprocessor_path = os.path.join("artifacts/preprocessor.pkl")
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            data_scaled = preprocessor.transform(features)
            predictions = model.predict(data_scaled)
            return predictions
        except Exception as e:
            raise CustomException(e, sys) from e
        
class CustomData:
    def __init__(self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education: str,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int):
        
       # Handle None values with defaults or raise error
        self.gender = gender if gender is not None else "Unknown"
        self.race_ethnicity = race_ethnicity if race_ethnicity is not None else "Unknown"
        self.parental_level_of_education = parental_level_of_education if parental_level_of_education is not None else "Unknown"
        self.lunch = lunch if lunch is not None else "Unknown"
        self.test_preparation_course = test_preparation_course if test_preparation_course is not None else "Unknown"
        self.reading_score = reading_score if reading_score is not None else 0
        self.writing_score = writing_score if writing_score is not None else 0

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)

"""
import sys
import pandas as pd  # Fixed typo: pancdas -> pandas
from src.exceptions import CustomException
from src.utils import load_object
import os

class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self, features):
        try:
            model_path = os.path.join("artifacts", "model.pkl")  # Fixed path construction
            preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")  # Fixed path construction
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            
            # Debug: Print the categories known by the preprocessor
            print("=== PREPROCESSOR DEBUG INFO ===")
            print(f"Input features shape: {features.shape}")
            print(f"Input features:\n{features}")
            
            # Check preprocessor transformers and their categories
            for name, transformer, columns in preprocessor.transformers_:
                print(f"\nTransformer: {name}")
                print(f"Columns: {columns}")
                if hasattr(transformer, 'categories_'):
                    for i, categories in enumerate(transformer.categories_):
                        col_name = columns[i] if i < len(columns) else f'column_{i}'
                        print(f"  {col_name}: {categories}")
                elif hasattr(transformer, 'steps'):
                    # If it's a pipeline, check each step
                    for step_name, step_transformer in transformer.steps:
                        if hasattr(step_transformer, 'categories_'):
                            print(f"  Step '{step_name}' categories:")
                            for i, categories in enumerate(step_transformer.categories_):
                                col_name = columns[i] if i < len(columns) else f'column_{i}'
                                print(f"    {col_name}: {categories}")
            
            print("=== END DEBUG INFO ===\n")
            
            data_scaled = preprocessor.transform(features)
            predictions = model.predict(data_scaled)
            return predictions
        except Exception as e:
            raise CustomException(e, sys) from e

class CustomData:
    def __init__(self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education: str,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int):
        
        # Define valid categories based on typical student performance datasets
        valid_categories = {
            'gender': ['male', 'female'],
            'race_ethnicity': ['group A', 'group B', 'group C', 'group D', 'group E'],
            'parental_level_of_education': [
                'some high school', 
                'high school', 
                'some college', 
                'associate\'s degree', 
                'bachelor\'s degree', 
                'master\'s degree'
            ],
            'lunch': ['standard', 'free/reduced'],
            'test_preparation_course': ['none', 'completed']
        }
        
        # Validate and assign with proper defaults (not 'Unknown')
        self.gender = gender if gender in valid_categories['gender'] else 'female'
        self.race_ethnicity = race_ethnicity if race_ethnicity in valid_categories['race_ethnicity'] else 'group C'
        self.parental_level_of_education = parental_level_of_education if parental_level_of_education in valid_categories['parental_level_of_education'] else 'some college'
        self.lunch = lunch if lunch in valid_categories['lunch'] else 'standard'
        self.test_preparation_course = test_preparation_course if test_preparation_course in valid_categories['test_preparation_course'] else 'none'
        
        # Handle numeric values
        self.reading_score = reading_score if reading_score is not None else 50
        self.writing_score = writing_score if writing_score is not None else 50
        
        # Debug print to see what values are being used
        print(f"CustomData initialized with:")
        print(f"  gender: {self.gender}")
        print(f"  race_ethnicity: {self.race_ethnicity}")
        print(f"  parental_level_of_education: {self.parental_level_of_education}")
        print(f"  lunch: {self.lunch}")
        print(f"  test_preparation_course: {self.test_preparation_course}")
        print(f"  reading_score: {self.reading_score}")
        print(f"  writing_score: {self.writing_score}")

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            df = pd.DataFrame(custom_data_input_dict)
            
            # Additional validation - ensure no None or null values
            if df.isnull().any().any():
                raise ValueError("DataFrame contains null values")
                
            print(f"Generated DataFrame:\n{df}")
            print(f"DataFrame dtypes:\n{df.dtypes}")
            
            return df

        except Exception as e:
            raise CustomException(e, sys)

# Additional utility function to inspect your preprocessor
def inspect_preprocessor(preprocessor_path="artifacts/preprocessor.pkl"):
    """
    Utility function to inspect what categories your preprocessor expects.
    
    """
    try:
        preprocessor = load_object(file_path=preprocessor_path)
        
        print("=== PREPROCESSOR INSPECTION ===")
        
        for name, transformer, columns in preprocessor.transformers_:
            print(f"\nTransformer: {name}")
            print(f"Columns: {columns}")
            
            if hasattr(transformer, 'categories_'):
                print("Categories:")
                for i, categories in enumerate(transformer.categories_):
                    col_name = columns[i] if i < len(columns) else f'column_{i}'
                    print(f"  {col_name}: {list(categories)}")
            
            elif hasattr(transformer, 'steps'):
                print("Pipeline steps:")
                for step_name, step_transformer in transformer.steps:
                    print(f"  Step: {step_name}")
                    if hasattr(step_transformer, 'categories_'):
                        print("    Categories:")
                        for i, categories in enumerate(step_transformer.categories_):
                            col_name = columns[i] if i < len(columns) else f'column_{i}'
                            print(f"      {col_name}: {list(categories)}")
        
        print("\n=== END INSPECTION ===")
        
    except Exception as e:
        print(f"Error inspecting preprocessor: {e}")

# inspect_preprocessor()
# End-to-End Student Performance Prediction Project (with some explanations on the connections between modules)

This project is a complete end-to-end machine learning application designed to predict a student's math score based on various demographic and academic attributes. It is built with a modular and scalable coding framework, featuring a full pipeline for data ingestion, preprocessing, model training, and deployment via a Flask web application.

-----

## **Project Structure** 

```
MLPRODUCTS/
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── predict_pipeline.py
│   │   └── train_pipeline.py
│   ├── __init__.py
│   ├── exceptions.py
│   ├── logger.py
│   └── utils.py
├── templates/
│   ├── home.html
│   └── index.html
├── .gcloudignore
├── .gitignore
├── app.yaml
├── main.py
├── requirements.txt
└── setup.py
```

-----

## **File Descriptions** 

### **Core Application Files**

  * **`main.py`**: The entry point for the Flask web application. It defines the application's routes, including the home page (`/`) and the prediction endpoint (`/predictdata`). This script handles both GET requests (to display the data entry form) and POST requests (to process the user's input and return a prediction).

  * **`setup.py`**: The setup script for the project. It uses `setuptools` to manage the project's packaging and dependencies. The `find_packages()` function automatically discovers all packages within the `src` directory, and the `get_requirements()` function reads the `requirements.txt` file to install all necessary libraries.

  * **`requirements.txt`**: A list of all the Python libraries required for the project to run successfully. These dependencies are installed automatically when setting up the project.

  * **`app.yaml`**: A configuration file for deploying the application on Google App Engine. It specifies the Python runtime environment.

-----

### **Source Code (`src`)**

#### **Components (`src/components`)**

These modules represent the core stages of the machine learning pipeline.

  * **`data_ingestion.py`**:

      * **`DataIngestionConfig`**: A data class that defines the file paths for the raw, training, and testing data, which are stored in the `artifacts` directory.
      * **`DataIngestion`**: This class handles reading the initial dataset (from `notebook/data/stud.csv`), splitting it into training and testing sets using `train_test_split`, and saving them as CSV files. The `initiate_data_ingestion` method orchestrates this process and returns the file paths for the training and testing data.

  * **`data_transformation.py`**:

      * **`DataTransformationConfig`**: A data class that specifies the path for saving the data preprocessor object (`preprocessor.pkl`).
      * **`DataTransformation`**: This class is responsible for all data preprocessing.
          * `get_data_transformer_object()`: Creates a `ColumnTransformer` pipeline to apply different transformations to numerical and categorical features. The numerical pipeline handles missing values and scaling, while the categorical pipeline manages missing values and one-hot encoding.
          * `initiate_data_transformation()`: Applies the preprocessing pipeline to the training and testing data and saves the fitted preprocessor object for future use.

  * **`model_trainer.py`**:

      * **`ModelTrainerConfig`**: A data class that defines the file path for saving the trained model (`model.pkl`).
      * **`ModelTrainer`**: This class manages the training and evaluation of multiple machine learning models.
          * `initiate_model_trainer()`: Trains a variety of regression models, evaluates their performance using `GridSearchCV` for hyperparameter tuning, identifies the best model based on the R² score, and saves it as a pickle file.

#### **Pipelines (`src/pipeline`)**

  * **`train_pipeline.py`**: This script (represented by the `if __name__ == "__main__":` block in `data_ingestion.py` in your provided code) orchestrates the entire training process by calling the component modules in sequence:

    1.  `DataIngestion.initiate_data_ingestion()`
    2.  `DataTransformation.initiate_data_transformation()`
    3.  `ModelTrainer.initiate_model_trainer()`

  * **`predict_pipeline.py`**: This module is designed for making predictions on new data.

      * **`PredictPipeline`**: The `predict()` method loads the saved preprocessor and model objects to transform new input data and generate a prediction.
      * **`CustomData`**: This class structures the input from the web form into a Pandas DataFrame that is compatible with the model's prediction method.

#### **Utilities (`src`)**

  * **`exceptions.py`**: Defines a custom exception class, `CustomException`, which provides detailed error messages, including the file name and line number where the exception occurred.

  * **`logger.py`**: Sets up a logging system to record important information, warnings, and errors during the project's execution, which is crucial for debugging and monitoring.

  * **`utils.py`**: Contains helper functions used across the project.

      * **`save_object()`** and **`load_object()`**: Functions to save and load Python objects (like the model and preprocessor) to and from files.
      * **`evaluate_models()`**: A function that iterates through a dictionary of models, performs hyperparameter tuning, and evaluates them to find the best-performing one.

#### **Web Templates (`templates`)**

  * **`index.html`**: The main landing page of the web application.
  * **`home.html`**: The HTML template for the user input form. It includes fields for all the features required for prediction and displays the predicted math score that is passed back from the `main.py` application.

-----

## **Workflow and Connections** 

### **Training Workflow**

1.  The training process is initiated, which calls `data_ingestion.py` to read the raw data and create `train.csv` and `test.csv`.
2.  These CSV files are then passed to `data_transformation.py`, which preprocesses the data and saves a `preprocessor.pkl` object.
3.  The transformed data is fed into `model_trainer.py`, which trains and evaluates multiple models to find the best one and saves it as `model.pkl`.

### **Prediction Workflow**

1.  A user submits their data through the form in `home.html`.
2.  The `/predictdata` route in `main.py` receives the data.
3.  The `CustomData` class in `predict_pipeline.py` structures the input into a DataFrame.
4.  The `PredictPipeline` class loads the saved `preprocessor.pkl` and `model.pkl` to make a prediction on the new data.
5.  The result is returned to `main.py` and displayed on the `home.html` page.

-----

## **How to Run the Project** 

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd MLPRODUCTS
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the training pipeline (to train the model):**

    ```bash
    python src/components/data_ingestion.py
    ```

5.  **Run the Flask application:**

    ```bash
    python main.py
    ```

6.  **Open your web browser and navigate to:**
    `http://127.0.0.1:5000`

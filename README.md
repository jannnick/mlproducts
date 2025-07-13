# End-to-End Student Performance Prediction Project

This is a complete machine learning application that predicts a student's math score based on various academic and demographic factors. The project is built with a modular structure, following best practices for creating scalable and maintainable ML systems. It includes a full pipeline for data handling and model training, and a **Flask** web interface for real-time predictions.

-----

## **Project Structure** 

The project is organized logically to separate concerns, making it easy to navigate and understand.

```
MLPRODUCTS/
├── src/                  # Contains the core application logic and ML pipeline.
├── templates/            # HTML files for the web front-end.
├── main.py               # The entry point that runs the Flask web server.
├── requirements.txt      # A list of all required Python libraries.
└── setup.py              # Script for packaging the project and its dependencies.
```

-----

## **File Descriptions** 

Each file has a specific role in either the machine learning pipeline or the web application.

### **Core Application Files**

  * **`main.py`**: The main script that launches the **Flask** web application. It defines the API endpoints (routes) that handle user requests, process input, and return predictions.
  * **`requirements.txt`**: This file lists all the project's **dependencies** (e.g., `pandas`, `scikit-learn`, `Flask`). The libraries listed here are installed to run the project.
  * **`setup.py`**: This is the project's **setup script**. It's used for packaging the `src` directory as a Python package and automatically installing the dependencies from `requirements.txt`.
  * **`app.yaml`**: A configuration file used for deploying the application to cloud platforms like **Google App Engine**.

### **Source Code (`src`)**

This directory is the heart of the project.

  * **`components/`**: This folder contains the individual stages of the ML pipeline.

      * `data_ingestion.py`: Reads the raw dataset, performs the crucial **train-test split**, and saves the resulting `train.csv` and `test.csv` files into the `artifacts` directory.
      * `data_transformation.py`: Handles all data preprocessing. It creates a **preprocessor** object (a `ColumnTransformer`) to apply different cleaning steps to numerical and categorical columns. This preprocessor is then saved as a pickle file (`preprocessor.pkl`).
      * `model_trainer.py`: Responsible for training and evaluating multiple machine learning models. It uses **GridSearchCV** for hyperparameter tuning, selects the best-performing model based on its **R² score**, and saves the final trained model as `model.pkl`.

  * **`pipeline/`**: This folder contains scripts that orchestrate the execution of the pipeline.

      * `train_pipeline.py`: Executes the complete training sequence by calling the components in order: ingestion, transformation, and then model training.
      * `predict_pipeline.py`: Contains the logic for making predictions on new data. It loads the saved `preprocessor.pkl` and `model.pkl` to transform the input and generate a prediction.

  * **`utils.py`**: A collection of **utility functions** used across the project, such as functions to save and load objects (like our model) and the model evaluation logic.

  * **`logger.py` & `exceptions.py`**: These modules provide essential functionality for **logging** the application's progress and handling **custom exceptions** for more informative error messages.

### **Web Templates (`templates`)**

  * **`home.html` & `index.html`**: These are the **HTML templates** that form the user interface. They contain the input form for users to enter student data and the area where the prediction is displayed.

-----

## **Workflow Explained** 

The project operates in two distinct workflows: training the model and using it for predictions.

### **Training Workflow**

The training pipeline is a sequential process that prepares the model for use:

1.  **Ingestion**: The `data_ingestion` module reads the raw data and creates the `train.csv` and `test.csv` datasets.
2.  **Transformation**: The `data_transformation` module takes these datasets, learns the best way to clean and prepare the data, and saves this logic in `preprocessor.pkl`.
3.  **Training**: Finally, the `model_trainer` takes the prepared data, finds the best predictive model, and saves it as `model.pkl`.

These saved files (`preprocessor.pkl` and `model.pkl`) are called **artifacts**, and they are the key outputs of the training workflow.

### **Prediction Workflow**

When a user requests a prediction from the web app:

1.  The user submits data through the form in `home.html`.
2.  The Flask app in `main.py` receives this data.
3.  The `predict_pipeline` loads the saved `preprocessor.pkl` to prepare the new data in the exact same way the training data was prepared.
4.  It then loads `model.pkl` and feeds the prepared data into it to get a prediction.
5.  The result is sent back to the user and displayed on the web page.

-----

## **How to Run the Project** 

To get the project running locally, follow these steps in your terminal:

1.  **Clone the repository**:

    ```bash
    git clone <your-repository-url>
    cd MLPRODUCTS
    ```

2.  **Create a virtual environment** (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install all dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the training pipeline** to generate the model artifacts:

    ```bash
    python src/components/data_ingestion.py
    ```

5.  **Start the Flask application**:

    ```bash
    python main.py
    ```

6.  **Open your browser** and navigate to `http://127.0.0.1:5000` to use the application.

Final AI/ML Capstone Project-Zepto Data & AI Platform

Student Name:Seemakurthi Alekhya

Course:IIT Patna-Certificate Program in Artificial Intelligence and MachineLearning.

Project Overview
-------------------------------------------
This project demonstrates an end-to-end Artificial Intelligence and MachineLearning workflow through three connected modules.The repository contains a complete data engineering pipeline, an analytics and machinelearning pipeline, and a Retrieval-Augmented Generation(RAG)support assistant.


Repository Structure
-------------------------------------------
final-ai-ml-capstone-project/
README.md
requirements.txt
data_pipeline/
analytics/
support_assistant/

-------------------------------------------

Module 1-Data Pipeline
Objective

Build a complete data engineering pipeline using the BooksToScrape website.

Tasks Completed

.Scraped book data using Requests and BeautifulSoup.
.Collected more than 60 books across multiple categories.
.Cleaned price,rating,and availability columns.
.Converted GBP price to INR using a fixed conversion rate.
.Create SQLite database with normalized tables.
.Executed SQL queries using SELECT, WHERE, ORDER BY, LIMIT, DISTINCT, BETWEEN/IN, and JOIN.
.Compared SQL JOIN output with Pandas merge output.

Output Files

.raw_books.csv
.cleaned_books.csv
.books.db

-------------------------------------------
Module 2-Analytics Pipeline
Objective

Perform Exploratory Data Analysis and build MachineLearning Models using the Titanic dataset.

Dataset
Loaded using:

sns.load_dataset("titanic")

Saved as
titanic.csv

Exploratory Data Analysis

.Dataset profiling.
Missing value analysis.
.Missing value handling.
.Histogram and Box Plot for Age and Fare.
.IQR-based outlier detection.
.Correlation heatmap.
.Survival analysis by gender and passenger class.
.Four multivariate visualizations with interpretation.
.Feature engineering using family_size and is_alone.

MachineLearning Pipeline

.Stratified Train-Test Split.
.ColumnTransformer preprocessing.
.StandardScaler.
.OneHotEncoder
.Logistic Regression.
.Decision Tree.
.Random Forest.
.Confusion Matrix.
.Accuracy.
.Precision.
.Recall.
.F1 Score.
ROC Curve and AUC.
.SMOTE.
.GridSearchCV.
.Linear Regression side task.
.Saved best model using Joblib.

Output Files

.titanic.csv
.titanic_cleaned.csv
.titanic_feature_engineered.csv
.best_pipeline.joblib

-------------------------------------------

Module 3 - Zepto Support Assistant

Objective

Build a Retrieval-Augmented Generation(RAG) assistant using Zepto policy documents.

Technologies Used

.Sentence Transformers
.ChromaDB
.LangGraph
.FastAPI
.Pydantic
.Docker

RAG Workflow

1.Load policy documents.
2.Generate embeddings.
3.Store embeddings in ChromaDB.
4.Retrieve top matching documents.
5.Generate grounded responses.
6.Return JSON response through FastAPI

API Endpoint

POST/ask

Sample Features

.Delivery policy lookup.
.Return policy lookup.
.Membership policy lookup.
.General question routing.

-------------------------------------------

Installation

Install all dependencies using one consolidated requirements file.

pip install -r requirements.txt

-------------------------------------------

How to Run

Module 1

python data_pipeline/scrape_books.py

python data_pipeline/clean_books.py

python data_pipeline/create_database.py

python data_pipeline/sql_queries.py


Module 2

Run notebooks inside VS Code.

analytics/01_data_story.ipynb

analytics/02_ml_pipeline.ipynb

Module 3

cd support_assistant

python rag_pipeline.py

uvicorn main --reload

-------------------------------------------

Design Decisions

Module 1

.Used normalized SQLite schema with primary and foreign keys.
.Used fixed GBP to INR conversion rate (1 GBP = 105.50INR)

Module 2

.Used median and mode imputation.
.Used ColumnTransformer and Pipeline to prevent data leakage.
.Used SMOTE only on training data.

Module 3
.Used local embeddings with all-MiniLM-L6-v2.
.Used ChromaDB as vector database.
.Used LangGraph for routing.
.Used MOCK_LLM for offline deterministic responses.

-------------------------------------------

##Project Structure
-'data_pipeline'-Data scraping,cleaning,SQLite database, and SQL queries.
-'analytics'-Titanic dataset analysis, visualization, and machinelearning.
-'support_assistant'-RAG-based Zepto policy support assistant using ChromaDB, LangGraph, and FastAPI.

-------------------------------------------

##Installation

Install the project dependencies using:
'''bash
pip install -r requirements.txt

Author

Seemakurthi Alekhya




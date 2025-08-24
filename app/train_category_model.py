import os
from dotenv import load_dotenv
import joblib
import nltk
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from data_base.models.form_of_payment_model import FormOfPayment
from data_base.models.monthly_expense_model import MonthlyExpense
from data_base.models.expense_category_model import ExpenseCategory
from nltk.corpus import stopwords
load_dotenv()

DATABASE_URI = os.getenv("DB_CONNECTION_STRING")

# Download stopwords
nltk.download('stopwords')
stopwords_pt = stopwords.words('portuguese')

# Set up the database connection
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
db = Session()

# Find categories
db_categorys = (db.query(
                        MonthlyExpense.description, 
                        MonthlyExpense.expense_category_id)
                    .join(ExpenseCategory)
                    .group_by(
                        MonthlyExpense.description, 
                        MonthlyExpense.expense_category_id)
                    .filter(MonthlyExpense.expense_category_id != 24)
                    .all())

# db_categorys = (db.query(
#     monthly_expense_model.MonthlyExpense.description,
#     monthly_expense_model.MonthlyExpense.expense_category_id
# ).filter(monthly_expense_model.MonthlyExpense.expense_category_id != 24).all())

df = pd.DataFrame(db_categorys, columns=["description", "category_id"])

# Train the model
vectorizer = TfidfVectorizer(lowercase=True, stop_words=stopwords_pt)
X = vectorizer.fit_transform(df['description'])
y = df['category_id']
clf = MultinomialNB()
clf.fit(X, y)


os.makedirs('model', exist_ok=True)

# Save the model and vectorizer
joblib.dump(vectorizer, 'model/vectorizer.pkl')
joblib.dump(clf, 'model/category_clf.pkl')

print("Model and vectorizer saved successfully!")
import os
from dotenv import load_dotenv
import joblib
import nltk
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from data_base.models.form_of_payment_model import FormOfPayment
from data_base.models.monthly_expense_model import MonthlyExpense
from data_base.models.expense_category_model import ExpenseCategory
from nltk.corpus import stopwords
load_dotenv()

DATABASE_URI = os.getenv("DB_CONNECTION_STRING")
env = os.getenv("ENVIRONMENT")

# Download stopwords
nltk.download('stopwords')
stopwords_pt = stopwords.words('portuguese')

# Set up the database connection
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
db = Session()

print("Loading training data from database...")
# Find categories - REMOVED GROUP BY to preserve sample frequency
db_categorys = (db.query(
                        MonthlyExpense.description, 
                        MonthlyExpense.expense_category_id)
                    .join(ExpenseCategory)
                    .filter(MonthlyExpense.expense_category_id != 24)
                    .all())

# db_categorys = (db.query(
#     monthly_expense_model.MonthlyExpense.description,
#     monthly_expense_model.MonthlyExpense.expense_category_id
# ).filter(monthly_expense_model.MonthlyExpense.expense_category_id != 24).all())

df = pd.DataFrame(db_categorys, columns=["description", "category_id"])

print(f"Total training samples: {len(df)}")
print(f"\nCategory distribution:")
print(df['category_id'].value_counts().sort_index())

# Remove categories with only 1 sample (can't be used in stratified split)
category_counts = df['category_id'].value_counts()
single_sample_categories = category_counts[category_counts == 1]
if len(single_sample_categories) > 0:
    print(f"\n⚠️  Removing categories with only 1 sample (cannot be used in train/test split):")
    for cat_id in single_sample_categories.index:
        print(f"   Category {cat_id}")
    df = df[~df['category_id'].isin(single_sample_categories.index)]
    print(f"   Remaining samples: {len(df)}\n")

# Validate minimum samples per category
min_samples_per_category = 5
category_counts = df['category_id'].value_counts()
undersized_categories = category_counts[category_counts < min_samples_per_category]
if len(undersized_categories) > 0:
    print(f"\n⚠️  WARNING: The following categories have fewer than {min_samples_per_category} samples:")
    for cat_id, count in undersized_categories.items():
        print(f"   Category {cat_id}: {count} samples")
    print("   These categories may have poor prediction accuracy.\n")

if len(df) < 20:
    print("\n❌ ERROR: Insufficient training data. Need at least 20 samples.")
    exit(1)

# Train the model with improved features
print("\nTraining model with improved TF-IDF features (ngrams)...")
# Using ngram_range=(1,2) to capture phrases like "restaurante japonês"
vectorizer = TfidfVectorizer(
    lowercase=True, 
    stop_words=stopwords_pt,
    ngram_range=(1, 2),  # Include both unigrams and bigrams
    max_features=1000    # Increased from default to capture more patterns
)
X = vectorizer.fit_transform(df['description'])
y = df['category_id']

# Split data for validation
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# Train with balanced class weights
clf = MultinomialNB(class_prior=None)  # Will use balanced priors from training data
clf.fit(X_train, y_train)

# Evaluate the model
print("\n" + "="*60)
print("MODEL EVALUATION METRICS")
print("="*60)

y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✓ Overall Accuracy: {accuracy:.2%}")

print("\nClassification Report:")
print("-" * 60)
print(classification_report(y_test, y_pred, zero_division=0))

print("\nConfusion Matrix:")
print("-" * 60)
print(confusion_matrix(y_test, y_pred))

# Save the model and vectorizer
os.makedirs('model', exist_ok=True)

if env == "development":
    joblib.dump(vectorizer, 'model/vectorizer.pkl')
    joblib.dump(clf, 'model/category_clf.pkl')
    # Save metrics for reference
    metrics = {
        'accuracy': accuracy,
        'total_samples': len(df),
        'train_samples': X_train.shape[0],
        'test_samples': X_test.shape[0]
    }
    joblib.dump(metrics, 'model/metrics.pkl')
else:
    # Save the model and vectorizer
    joblib.dump(vectorizer, '/app/model/vectorizer.pkl')
    joblib.dump(clf, '/app/model/category_clf.pkl')
    metrics = {
        'accuracy': accuracy,
        'total_samples': len(df),
        'train_samples': X_train.shape[0],
        'test_samples': X_test.shape[0]
    }
    joblib.dump(metrics, '/app/model/metrics.pkl')

print("\n" + "="*60)
print("✓ Model, vectorizer, and metrics saved successfully!")
print("="*60)
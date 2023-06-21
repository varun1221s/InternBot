import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources if not already downloaded
nltk.download('stopwords')
nltk.download('wordnet')

# Function to clean the text
def clean_text(text):
    # Convert to lowercase
    text = str(text).lower()
    # Remove HTML tags
    text = re.sub('<.*?>', '', text)
    # Remove non-alphabetic characters
    text = re.sub('[^a-zA-Z]', ' ', text)
    # Tokenize the text
    tokens = text.split()
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    # Join the tokens back into a single string
    cleaned_text = ' '.join(tokens)
    return cleaned_text

# Read the CSV file
data = pd.read_csv('formatted_data.csv')

# Clean the 'Question Title' column
data['cleaned_title'] = data['Question Title'].apply(clean_text)

# Save the cleaned data to a new CSV file
data.to_csv('cleaned_data.csv', index=False)

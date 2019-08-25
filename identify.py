# import required packages
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# import training dataset into pandas dataframe using the read_table method
"""
dataset is tab separated.
we will be using '\t' as the value for 'sep' argument which specify this format.
rename the column by specifying a list ['label', 'content'] to the 'names' argument of read_table().
"""
df = pd.read_table("doccollection/DocCollection", sep='\t', header=None, 
                   names=['label', 'content'])

# Data Preprocessing
# map labels yes to 1 and no to 0 for training dataset
df['label'] = df.label.map({'no':0, 'yes':1})

# prepare training data
x_train = df['content']
y_train = df['label']

# applying Bag of Words processing to our dataset using count vectorizer 
count_vector = CountVectorizer()
training_data = count_vector.fit_transform(x_train)

# apply Naive Bayes algorithm
# fit training data to Multinomial Naive Bayes classifier in sckit-learn
naive_bayes = MultinomialNB()
naive_bayes.fit(training_data, y_train)
# print("Data preprocessing done")

# import testing dataset into pandas dataframe using the read_table method
df_test = pd.read_table("doccollection/TestCollection", sep='\t', header=None, 
                   names=['label', 'content'])

# map labels yes to 1 and no to 0 for test dataset
df_test['label'] = df_test.label.map({'no':0, 'yes':1})

# prepare testing data
x_test = df_test['content']
y_test = df_test['label']

# applying Bag of Words processing to our testing dataset using count vectorizer
testing_data = count_vector.transform(x_test)

# make predictions on testing dataset using predict method
predictions = naive_bayes.predict(testing_data)

# check accuracy
# print('Accuracy score: ', format(accuracy_score(y_test, predictions)))

# function to make prediction on input document's text
def make_predictions():
    # load text from predict file
    df_predict = pd.read_table("predict/predict", sep='\t', header=None, 
                   names=['label', 'content'])
    # map labels yes to 1 and no to 0 for test dataset
    df_predict['label'] = df_predict.label.map({'no':0, 'yes':1})
    x_predict = df_predict['content']
    # apply bag of words
    prediction_data = count_vector.transform(x_predict)
    # return predicted label
    result =  naive_bayes.predict(prediction_data)
    return result[0]

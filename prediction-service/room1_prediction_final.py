from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import io
from sklearn.multioutput import MultiOutputClassifier
# import neattext.functions as nfx
from sklearn.neighbors import KNeighborsClassifier
# below package is madatory
# pip install neattext

s = io.StringIO()

data_input_path = '/Users/srikar/Desktop/workspace/graduate_project/prediction-service/room1_final.csv'

with open(data_input_path) as file:
    for line in file:
        s.write(str(line).replace(", ,", ","))
s.seek(0)

df = pd.read_csv(s)
# print(data.head())
# print(data.tail())
# print(data.columns)
# print(data.shape)
# print(data.describe())
df.head()
df['Result'].value_counts()
sns.countplot(x='Result', data=df)
df['empty_status'].value_counts()
Xfeatures = df['empty_status']
ylabels = df[['Result', 'Alert']]
x_train, x_test, y_train, y_test = train_test_split(
    Xfeatures, ylabels, test_size=0.3, random_state=7)
pipe_lr = Pipeline(steps=[('cv', CountVectorizer()),
                          ('lr_multi', MultiOutputClassifier(LogisticRegression()))])

pipe_lr.fit(x_train, y_train)
Pipeline(steps=[('cv', CountVectorizer()),
                ('lr_multi',
                 MultiOutputClassifier(estimator=LogisticRegression()))])
Pipeline(steps=[('cv', CountVectorizer()),
                ('lr_multi',
                 MultiOutputClassifier(estimator=LogisticRegression()))])
Pipeline(steps=[('cv', CountVectorizer()),
                ('lr_multi',
                 MultiOutputClassifier(estimator=LogisticRegression()))])
pipe_lr.score(x_test, y_test)
print(x_test.iloc[0])
print("Actual Prediction:", y_test.iloc[0])
ex1 = x_test.iloc[0]
print(ex1)
pipe_lr.predict([ex1])
print(pipe_lr.classes_)
pipe_lr.predict_proba([ex1])

pipe_knn = Pipeline(steps=[('cv', CountVectorizer()),
                    ('knn', KNeighborsClassifier(n_neighbors=4))])
pipe_knn.fit(x_train, y_train)
pipe_knn.predict([ex1])

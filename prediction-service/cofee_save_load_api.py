import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import io
import sklearn
from sklearn.multioutput import MultiOutputClassifier
import neattext.functions as nfx
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
#below package is madatory
#pip install neattext
def cofee_details(status):
    s = io.StringIO()
    with open('E:\\lokesh_india\\smart_home\\final\\cofee_details.csv') as file:
        for line in file:
            s.write(str(line).replace(", ,", ","))
    s.seek(0)
    df = pd.read_csv(s)
    #print(df.head())
    # print(data.tail())
    # print(data.columns)
    # print(data.shape)
    # print(data.describe())
    #print(df.head())
    #print(df['Result'].value_counts())
    sns.countplot(x='Result',data=df)
    #print(df['outside_temp'].value_counts())
    Xfeatures = df['date_time']
    ylabels = df[['Result','movement']]
    x_train,x_test,y_train,y_test = train_test_split(Xfeatures,ylabels,test_size=0.3,random_state=7)

    # sc = sklearn.preprocessing.StandardScaler()
    # x_train = sc.fit_transform(x_train)
    # x_train = sc.fit_transform(x_test)
    pipe_lr = Pipeline(steps=[('cv',CountVectorizer()),
                            ('lr_multi',MultiOutputClassifier(LogisticRegression()))])
    pipe_lr.fit(x_train,y_train)
    Pipeline(steps=[('cv', CountVectorizer()),
                    ('lr_multi',
                    MultiOutputClassifier(estimator=LogisticRegression()))])
    Pipeline(steps=[('cv', CountVectorizer()),
                    ('lr_multi',
                    MultiOutputClassifier(estimator=LogisticRegression()))])
    Pipeline(steps=[('cv', CountVectorizer()),
                    ('lr_multi',
                    MultiOutputClassifier(estimator=LogisticRegression()))])
    pipe_lr.score(x_test,y_test)
    # print(x_test.iloc[0])
    # print("Actual Prediction:",y_test.iloc[0])
    ex1 = status
    print(ex1)
    pipe_lr.predict([ex1])
    #print(pipe_lr.classes_)
    pipe_lr.predict_proba([ex1])
    pipe_knn = Pipeline(steps=[('cv',CountVectorizer()),('knn',KNeighborsClassifier(n_neighbors=4))])
    pipe_knn.fit(x_train,y_train)
    filename = 'E:\\lokesh_india\\smart_home\\final\\cofee_details.pkl'
    pickle.dump(pipe_lr,open(filename,'wb'))
    result = pipe_knn.predict([ex1])
    loaded_model = pickle.load(open(filename, 'rb'))
    score = loaded_model.score(x_test,y_test)
    predict = loaded_model.predict(x_test)    
    #print(predict)
    #print('-----------------------------')
    #predict = loaded_model.predict(y_test)    
    #print(predict)
    #print('-----------------------------')
    return result

result = cofee_details('2000:7:21 7:56:46')
print(result)

result1 = cofee_details('2000:7:21 9:56:46')
print(result1)

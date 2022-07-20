import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import io
from sklearn.multioutput import MultiOutputClassifier
import neattext.functions as nfx
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle


data_input_path = '/Users/srikar/Desktop/workspace/graduate_project/prediction-service/room1_final.csv'
trained_model_dump = '/Users/srikar/Desktop/workspace/graduate_project/prediction-service/trained_model_room1.pkl'


def room_1_predict(param):
    s = io.StringIO()
    with open(data_input_path) as file:
        for line in file:
            s.write(str(line).replace(", ,", ","))
    s.seek(0)
    df = pd.read_csv(s)
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
    # print(x_test.iloc[0])
    #print("Actual Prediction:",y_test.iloc[0])
    ex1 = param
    #print(ex1+" input")
    pipe_lr.predict([ex1])
    # print(pipe_lr.classes_)
    pipe_lr.predict_proba([ex1])
    pipe_knn = Pipeline(
        steps=[('cv', CountVectorizer()), ('knn', KNeighborsClassifier(n_neighbors=4))])
    pipe_knn.fit(x_train, y_train)

    pickle.dump(pipe_lr, open(trained_model_dump, 'wb'))
    print('model saved')
    # result = pipe_knn.predict([ex1])
    # score = loaded_model.score(x_test, y_test)


def predict_light(movement_status, timestamp):
    loaded_model = pickle.load(open(trained_model_dump, 'rb'))
    predict = loaded_model.predict([movement_status])

    return predict
    # print('-----------------------------')
    # predict = loaded_model.predict(y_test)
    # print(predict)
    # print('-----------------------------')
    # print(loaded_model)
    # return result


# room_1_predict('no')

# print('-----------------------------')
# result = predict_light('yes')
# print(result)
# result2 = predict_light('no')
# print(result2)
# result3 = predict_light('no')
# print(result3)
# result4 = predict_light('yes')
# print(result4)
# # result1 = room_1_predict('yes')
# # print(result1 + " is the result")

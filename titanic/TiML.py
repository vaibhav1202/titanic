
# coding: utf-8

# In[1]:


import pandas as pd
from xgboost import XGBClassifier
import pickle
import os
import numpy as np
from bokeh.layouts import column

def preprocessing(df):
    def get_title(name):
        if '.' in name:
            return name.split(',')[1].split('.')[0].strip()
        else:
            return 'Unknown'
    def title_map(title):
        if title in ['Mr']:
            return 1
        elif title in ['Master']:
            return 30
        elif title in ['Ms','Mlle','Miss']:
            return 40
        elif title in ['Mme','Mrs']:
            return 50
        else:
            return 2
        
    df.Sex = df.Sex.map({"male":0, "female":5})
    df['title'] = df['Name'].apply(get_title).apply(title_map)   
    mfare = df["Fare"].median()
    df["Fare"].fillna(mfare, inplace=True)
    df.loc[ df['Fare'] <= 7.91, 'Fare'] = 0
    df.loc[(df['Fare'] > 7.91) & (df['Fare'] <= 14.454), 'Fare'] = 10
    df.loc[(df['Fare'] > 14.454) & (df['Fare'] <= 31), 'Fare'] = 20
    df.loc[ df['Fare'] > 31, 'Fare'] = 30
    df.drop(["Ticket", "Cabin", "Name", "PassengerId"],axis="columns" ,inplace=True)
    df["Age"][df["title"]==1].fillna(32, inplace=True)
    df["Age"][df["title"]==2].fillna(45, inplace=True)
    df["Age"][df["title"]==3].fillna(4, inplace=True) 
    df["Age"][df["title"]==4].fillna(21, inplace=True)
    df["Age"][df["title"]==5].fillna(35, inplace=True)
    mage = df.Age.mean()
    df.Age = df.Age.fillna(mage)
    df["Age"] = pd.cut(df["Age"], bins=[-1,10, 16, 100], labels=[100,10,1])
    df["Pclass"].replace([1,2,3], [3,2,1], inplace=True)
    df["SibSp"].fillna(0, inplace=True)
    df["fam"] = df["SibSp"] + df["Parch"] + 1
    df["fam"] = pd.cut(df["fam"], bins=[0,2,5,7,100], labels=[0, 10, 3, 2])
    df.drop(["SibSp", "Parch"],axis="columns" ,inplace=True)
    df['Age'] = df['Age'].astype(int)
    df['fam'] = df['fam'].astype(int)
    df['Pclass'] = df['Pclass'].astype(int)
    df = pd.get_dummies(df)
    return df


# In[2]:


def training(df):
    df = preprocessing(df)
    #train with all data
    y = df["Survived"]
    X = df.drop(["Survived"], axis='columns')
    
    dummyRow = pd.DataFrame(np.zeros(len(X.columns)).reshape(1, len(X.columns)), columns=X.columns)    
    dummyRow.to_csv("dummyRow.csv", index=False)
    model = XGBClassifier(n_estimators=10, max_depth=4,
     min_child_weight=9, objective= 'binary:logistic', scale_pos_weight=0.9)
    model.fit(X, y)
    pkl_filename = "pickle_model.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model, file)


# In[3]:


def pred(ob):
    print(1)
    d1 = ob.to_dict()
    df = pd.DataFrame(d1, index=[0])
    print("**"*50)
    print(df.head())
    df = preprocessing(df)    
    print("--"*50)
    print(df.head())
    dummyrow_filename = "./dummyRow.csv"
    dummyrow_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), dummyrow_filename)    
    print(2)
    df2 = pd.read_csv(dummyrow_filename)    
    for c1 in df.columns:
        df2[c1] = df[c1]        
    print("=="*50)
    print(df2.head())        
    pkl_filename = "./pickle_model.pkl"
    pkl_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), pkl_filename)
    with open(pkl_filename, 'rb') as file:
        model = pickle.load(file)
    pred = model.predict(df2)
    return pred


# In[4]:

if __name__ == "__main__":
    df = pd.read_csv("train.csv")
    training(df)


# In[5]:


#     sc = StandardScaler()
#     sc.fit(X)
#     pkl_filename2 = "pickle_scaler.pkl"
#     with open(pkl_filename2, 'wb') as file:
#         pickle.dump(sc, file)


#     pkl_filename2 = "./pickle_scaler.pkl"
#     pkl_filename2 = os.path.join(os.path.abspath(os.path.dirname(__file__)), pkl_filename2)
#     with open(pkl_filename2, 'rb') as file:
#         sc = pickle.load(file)


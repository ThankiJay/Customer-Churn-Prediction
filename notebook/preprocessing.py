import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def preprocess(df, option):

    #Defining the map function
    def binary_map(feature):
        return feature.map({'Yes':1, 'No':0, 'Male':1 ,'Female':0})


    # Encode binary categorical features
    binary_list = ['gender',
                   'SeniorCitizen', 
                   'Partner',
                   'Dependents',
                   'PhoneService',
                   'MultipleLines',
                   'IntrntSrvc_DSL',
                   'IntrntSrvc_FiberOptic',
                   'IntrntSrvc_No',
                   'OnlineSecurity',
                   'OnlineBackup',
                   'DeviceProtection',
                   'TechSupport',
                   'StreamingTV',
                   'StreamingMovies',
                   'Contract_Monthly',
                   'Contract_OneYear',
                   'Contract_TwoYear',
                   'PaperlessBilling',
                   'PayMthd_BankTransfer',
                   'PayMthd_CreditCard',
                   'PayMthd_ElectronicCheck',
                   'PayMthd_MailedCheck']
    df[binary_list] = df[binary_list].apply(binary_map)

    #feature scaling
    sc = MinMaxScaler()
    df['tenure'] = sc.fit_transform(df[['tenure']])
    df['MonthlyCharges'] = sc.fit_transform(df[['MonthlyCharges']])
    df['TotalCharges'] = sc.fit_transform(df[['TotalCharges']])
    return df
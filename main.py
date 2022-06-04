# -*- coding: utf-8 -*-
"""Project_Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Xww6TyQzL-pM5WXtNrHZIAHXIvHv9Q7h

## Proyecto Final Inteligencia Artificial - Satisfacción de los pasajeros de una Aerolinea

Desarrollado por: Juanita Marulanda Argüello y Yorman Adrian Vera Rozo

Se tiene como objetivo la predicción de qué tan satisfechos (satisfecho o no satisfecho) 
se encuentran los usuarios con una aerolínea. El dataset se encuentra en 
https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction.
Los datos de entrenamiento tiene una cantidad de 103904 muestras, con las siguientes características: 
- "Gender"
- "Customer Type"
- "Age","Class"
- "Inflight wifi service"
- "Ease of Online booking"
- "Gate location","Food and drink"
- "Online boarding","Seat comfort"
- "Inflight entertainment"
- "On-board service","Leg room service"
- "Baggage handling","Checkin service"
- "Inflight service"
-Y como etiquetas tiene: 
- "satisfaction"

Librerías utilizadas
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import decomposition
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA, KernelPCA
from sklearn.model_selection import train_test_split
from matplotlib.colors import ListedColormap
from sklearn import svm
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve,roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

"""Limpieza y preprocesamiento de los datos"""

data = pd.read_csv("train.csv", sep=",") # Importar los datos
test = pd.read_csv("test.csv", sep=",") # Importar los datos

print("Los datos vacios en train son: \n")
print(data.isnull().sum()) #Se mira cuales columnas les falta datos

print("Los datos vacios en test son: \n")
print(test.isnull().sum()) #Se mira cuales columnas les falta datos

# Se eliminan las columnas que no se utilizaran
data = data.drop(['id', 'Type of Travel', 'Flight Distance', 'Departure/Arrival time convenient', 'Departure Delay in Minutes','Arrival Delay in Minutes'], axis=1)
print("Las dimensiones del conjunto de datos son:",data.shape)

#Eliminar las filas con valores nulos o completarlos con la media de los existentes

data = data[data['Gender'].notna()]
data = data[data['Customer Type'].notna()]
data = data[data['Age'].notna()]
data = data[data['Class'].notna()]
data = data[data['Inflight wifi service'].notna()]
data = data[data['Ease of Online booking'].notna()]
data = data[data['Gate location'].notna()]
data = data[data['Food and drink'].notna()]
data = data[data['Online boarding'].notna()]
data = data[data['Seat comfort'].notna()]
data = data[data['Inflight entertainment'].notna()]
data = data[data['On-board service'].notna()]
data = data[data['Leg room service'].notna()]
data = data[data['Baggage handling'].notna()]
data = data[data['Checkin service'].notna()]
data = data[data['Inflight service'].notna()]
data = data[data['satisfaction'].notna()]

print("Las nuevas dimensiones del conjunto de datos son:",data.shape)

data.loc[data['Gender'] == 'Male', 'Gender'] = '1'
data.loc[data['Gender'] == 'Female', 'Gender'] = '0'

data.loc[data['Customer Type'] == 'Loyal Customer', 'Customer Type'] = '1'
data.loc[data['Customer Type'] == 'disloyal Customer', 'Customer Type'] = '0'

data.loc[data['Class'] == 'Business', 'Class'] = '2'
data.loc[data['Class'] == 'Eco Plus', 'Class'] = '1'
data.loc[data['Class'] == 'Eco', 'Class'] = '0'

data.loc[data['satisfaction'] == 'satisfied', 'satisfaction'] = '1'
data.loc[data['satisfaction'] == 'neutral or dissatisfied', 'satisfaction'] = '0'

"""Crear csv con datos limpios."""

clean_data = pd.DataFrame(data, columns = ['Gender','Customer Type','Age','Class','Inflight wifi service','Ease of Online booking','Gate location','Food and drink','Online boarding','Seat comfort','Inflight entertainment','On-board service','Leg room service','Baggage handling','Checkin service','Inflight service','satisfaction'])
#print("Datos limpios ", clean_data)

clean_data.to_csv('clean_data.csv')

Xo = pd.DataFrame(clean_data, columns = ['Gender','Customer Type','Age','Class','Inflight wifi service','Ease of Online booking','Gate location','Food and drink','Online boarding','Seat comfort','Inflight entertainment','On-board service','Leg room service','Baggage handling','Checkin service','Inflight service'])
Y  = pd.DataFrame(clean_data, columns = ['satisfaction'])

"""Seleccion de los datos de train y test, Normalización y PCA"""

#--------------------Seleccionar datos train y test para el modelo (80% y 20%)-----------------------------------

X_train, X_test, Y_train, Y_test = train_test_split(Xo, Y, test_size=0.2, train_size=0.8, random_state=0)

#--------------------Funcion Nomrmalizacion(X)---------------------------------------------------

def normMinMax(Xo):
    #scaler = StandardScaler()
    #scaler.fit(Xo)
    scaler = MinMaxScaler()
    scaler.fit(Xo)
    #print(Xo)
    X = scaler.transform(Xo)
    #print(X,X.shape)
    return X


#--------------------Funcion PCA (X, Numero de componentes)-----------------------------------
def PCAfunction(X, comps):
    pca = decomposition.PCA(n_components=comps,whiten=True,svd_solver='auto')
    pca.fit(X)
    X = pca.transform(X)
    print("Pesos de PCA:",pca.explained_variance_ratio_,'\n')
    sumpca = sum(pca.explained_variance_ratio_)
    print("Se puede hacer reduccion dimensional, quedaria con ",comps,"y la suma de las componentes que quedan es:", sumpca,"\n")
    return X

"""Usando grid search se buscan los hiperparámetros para 3 métodos: Regresión Logística, SVM y Neuronal Networks"""

Xn = normMinMax(X_train)
X_train =PCAfunction(Xn,15)


Xtn = normMinMax(X_test)
X_test =PCAfunction(Xtn,15)
'''
Se buscan los hiperparámetros por medio de GridSearch con crossvalidation. 
Se entrenan los diferentes métodos con los hiperparámetros encontrados y se obtiene 
accuracy y roc_auc con el conjunto de datos de test, que corresponde al 10% del dataset.

Referencia de la función GridSearch
https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html


'''

#-------------------- Regresión Logística---------------------------------

#https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html?highlight=logistic#

LR = LogisticRegression(C=10)
LR.fit(X_train,Y_train.values.ravel())

Y_pred_LR = LR.predict(X_test)
Acc_LR = LR.score(X_test,Y_test.values.ravel())
Y_test_scores_LR = LR.decision_function(X_test)


MCC_LR = matthews_corrcoef(Y_test, Y_pred_LR)
print("\n","matthews_corrcoef para LR: ", MCC_LR,"\n")


print("Accuracy LR Test: ",Acc_LR)

Auc_LR = roc_auc_score(Y_test.values.ravel(),Y_pred_LR)
print("roc_auc LR Test: ",Auc_LR)

print("\n Matriz de confusion para Regresion Logistica")
cm_LR=confusion_matrix(Y_test.values.ravel(),Y_pred_LR)
sns.heatmap(cm_LR,annot=True,fmt='d')
plt.show()


MCC = matthews_corrcoef(Y_test, Y_pred_LR)
print("\n","matthews_corrcoef: ", MCC,"\n")
ACC = accuracy_score(Y_test, Y_pred_LR)
print("Accuracy: ", ACC,"\n")

#-------------------- Support Vector Machine -------------------------------
#https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html

MSV = svm.SVC(kernel="sigmoid", C=10, gamma='scale')
MSV.fit(X_train,Y_train.values.ravel())

ACC = MSV.score(X_train, Y_train.values.ravel())


Y_test_predicted_SVM = (MSV.predict(X_test))
Y_test_scores = MSV.decision_function(X_test)


MCC_SVM = matthews_corrcoef(Y_test, Y_test_predicted_SVM)
print("\n","matthews_corrcoef para SVM: ", MCC_SVM,"\n")



Y_pred_SVM = MSV.predict(X_test)
Acc_SVM = MSV.score(X_test,Y_test.values.ravel())
print("Accuracy SVM Test: ",Acc_SVM)

Auc_SVM = roc_auc_score(Y_test.values.ravel(),Y_pred_SVM)
print("roc_auc SVM Test: ",Auc_SVM)

print("\n Matriz de confusion para Support vector Machine")
cm_SVM=confusion_matrix(Y_test.values.ravel(),Y_pred_SVM)
sns.heatmap(cm_SVM,annot=True,fmt='d')
plt.show()

#------------------------------Redes Neuronales--------------------------
#https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html#sklearn.neural_network.MLPClassifier

ANN = MLPClassifier(hidden_layer_sizes=(100,100), activation='relu', solver='adam', alpha=10, batch_size='auto', learning_rate='adaptive', max_iter=5000)
ANN.fit(X_train,Y_train.values.ravel())


Y_test_predicted_ANN = (ANN.predict(X_test))
Y_pred_ANN = ANN.predict(X_test)

MCC_ANN = matthews_corrcoef(Y_test, Y_test_predicted_ANN)
print("\n","matthews_corrcoef para ANN: ", MCC_ANN,"\n")


Acc_ANN = accuracy_score(Y_test.values.ravel(),Y_test_predicted_ANN)
print("Accuracy ANN Test: ",Acc_ANN)

Auc_ANN = roc_auc_score(Y_test,Y_pred_ANN)
print("roc_auc ANN Test: ",Auc_ANN)


print("\n Matriz de confusion para Redes Neuronales")
cm_ANN=confusion_matrix(Y_test.values.ravel(),Y_pred_ANN)
sns.heatmap(cm_ANN,annot=True,fmt='d')
plt.show()

"""Usando el archivo de validación 'test.csv' se obtiene el accuracy y la roc auc para cada uno de los tres métodos implementados."""

#------------------Con el Conjunto de Validación TEST.csv----------------------------------------------------------


def limpiardatos(test):
    # Se eliminan las columnas que no se utilizaran
    test = test.drop(["id", "Type of Travel", "Flight Distance", "Departure/Arrival time convenient", "Departure Delay in Minutes","Arrival Delay in Minutes"], axis=1)
    print("\n Las dimensiones del conjunto de datos son:",test.shape)
    
    #Eliminar las filas con valores nulos o completarlos con la media de los existentes
    
    test = test[test["Gender"].notna()]
    test = test[test["Customer Type"].notna()]
    test = test[test["Age"].notna()]
    test = test[test["Class"].notna()]
    test = test[test["Inflight wifi service"].notna()]
    test = test[test["Ease of Online booking"].notna()]
    test = test[test["Gate location"].notna()]
    test = test[test["Food and drink"].notna()]
    test = test[test["Online boarding"].notna()]
    test = test[test["Seat comfort"].notna()]
    test = test[test["Inflight entertainment"].notna()]
    test = test[test["On-board service"].notna()]
    test = test[test["Leg room service"].notna()]
    test = test[test["Baggage handling"].notna()]
    test = test[test["Checkin service"].notna()]
    test = test[test["Inflight service"].notna()]
    test = test[test["satisfaction"].notna()]
    
    print("Las nuevas dimensiones del conjunto de datos son:",test.shape)
    
    test.loc[test["Gender"] == "Male", "Gender"] = "1"
    test.loc[test["Gender"] == "Female", "Gender"] = "0"
    
    test.loc[test["Customer Type"] == "Loyal Customer", "Customer Type"] = "1"
    test.loc[test["Customer Type"] == "disloyal Customer", "Customer Type"] = "0"
    
    test.loc[test["Class"] == "Business", "Class"] = "2"
    test.loc[test["Class"] == "Eco Plus", "Class"] = "1"
    test.loc[test["Class"] == "Eco", "Class"] = "0"
    
    test.loc[test["satisfaction"] == "satisfied", "satisfaction"] = "1"
    test.loc[test["satisfaction"] == "neutral or dissatisfied", "satisfaction"] = "0"
    
    
    X_val = pd.DataFrame(test, columns = ["Gender","Customer Type","Age","Class","Inflight wifi service","Ease of Online booking","Gate location","Food and drink","Online boarding","Seat comfort","Inflight entertainment","On-board service","Leg room service","Baggage handling","Checkin service","Inflight service"])
    Y_val  = pd.DataFrame(test, columns = ["satisfaction"])
    
    return X_val,Y_val
        

    
X_val,Y_val = limpiardatos(test)

X_val = normMinMax(X_val)
X_val =PCAfunction(X_val,15)

#Regresion Logisitica

Y_val_pred_LR = (LR.predict(X_val))
ValAcc_LR = LR.score(X_val,Y_val.values.ravel())
print("Accuracy LR Validation: ",ValAcc_LR)

ValAuc_LR = roc_auc_score(Y_val.values.ravel(),Y_val_pred_LR)
print("roc_auc LR Validation: ",ValAuc_LR)

MCC = matthews_corrcoef(Y_val, Y_val_pred_LR)
print("\n","matthews_corrcoef Regresion Logisitica: ", MCC,"\n")

#Support vector Machine

Y_val_pred_SVM = (MSV.predict(X_val))
ValAcc_SVM = MSV.score(X_val,Y_val.values.ravel())
print("Accuracy SVM Validation: ",ValAcc_SVM)

ValAuc_SVM = roc_auc_score(Y_val.values.ravel(),Y_val_pred_SVM)
print("roc_auc SVM Validation: ",ValAuc_SVM)

MCC = matthews_corrcoef(Y_val, Y_val_pred_SVM)
print("\n","matthews_corrcoef SVM: ", MCC,"\n")
 
#Redes Neuronales

Y_val_pred_ANN = (ANN.predict(X_val))
ValAcc_ANN = ANN.score(X_val,Y_val.values.ravel())
print("Accuracy ANN Validation: ",ValAcc_ANN)

ValAuc_ANN = roc_auc_score(Y_val.values.ravel(),Y_val_pred_ANN)
print("roc_auc ANN Validation: ",ValAuc_ANN)

MCC = matthews_corrcoef(Y_val, Y_val_pred_ANN)
print("\n","matthews_corrcoef ANN: ", MCC,"\n")

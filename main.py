
import pandas as pd
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
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve,roc_auc_score


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

Xo = pd.DataFrame(data, columns = ['Gender','Customer Type','Age','Class','Inflight wifi service','Ease of Online booking','Gate location','Food and drink','Online boarding','Seat comfort','Inflight entertainment','On-board service','Leg room service','Baggage handling','Checkin service','Inflight service'])
Y  = pd.DataFrame(data, columns = ['satisfaction']) 
test.isnull().sum() #Se mira cuales columnas les falta datos


#--------------------NORMALIZACIÓN---------------------------------------------------


def normMinMax(Xo):
    #scaler = StandardScaler()
    #scaler.fit(Xo)
    scaler = MinMaxScaler()
    scaler.fit(Xo)
    print(Xo)
    X = scaler.transform(Xo)
    print(X,X.shape)
    return X


#--------------------PCA (X, Numero de componentes)-----------------------------------
def PCA(X, comps):
    pca = decomposition.PCA(n_components=comps,whiten=True,svd_solver='auto')
    pca.fit(X)
    X = pca.transform(X)
    print("Pesos de PCA:",pca.explained_variance_ratio_)
    sumpca = sum(pca.explained_variance_ratio_)
    print("Se puede hacer reduccion dimensional, quedaria con ",comps,"y la suma de las componentes que quedan es:", sumpca,"\n")


#--------------------REGRESION LOGISITCA----------------------------------------------
X_norm = normMinMax(Xo)
X_pca = PCA(X_norm,16)






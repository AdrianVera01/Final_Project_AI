
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import decomposition
#from sklearn import datasets
#from sklearn.preprocessing import StandardScaler
#from sklearn.preprocessing import MinMaxScaler
#from sklearn.decomposition import PCA, KernelPCA
#from sklearn.model_selection import train_test_split
#from matplotlib.colors import ListedColormap
#from sklearn import svm
#from sklearn.linear_model import LogisticRegression
#from sklearn.metrics import matthews_corrcoef
#from sklearn.metrics import accuracy_score
#from sklearn.metrics import roc_curve,roc_auc_score



data = pd.read_csv("train.csv", sep=",") # Importar los datos
# Se eliminan las columnas que no se utilizaran
data = data.drop(['id', 'Type of Travel', 'Departure/Arrival time convenient', 'Departure Delay in Minutes','Arrival Delay in Minutes'], axis=1)
#print(data)
print("Las dimensiones del conjunto de datos son:",data.shape)

#Eliminar las filas con valores nulos o completarlos con la media de los existentes

data = data[data['Gender'].notna()]
data = data[data['Customer Type'].notna()]
data = data[data['Age'].notna()]
data = data[data['Class'].notna()]
data = data[data['Flight Distance'].notna()]
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


print("Hello World")

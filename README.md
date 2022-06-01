## Proyecto Final Inteligencia Artificial - Satisfacción de los pasajeros de una Aerolinea

Desarrollado por: Juanita Marulanda Argüello y Yorman Adrian Vera Rozo

Se tiene como objetivo la predicción de qué tan satisfechos (satisfecho o no satisfecho) se encuentran los usuarios con una aerolínea. El dataset se encuentra en https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction. Los datos de entrenamiento tiene una cantidad de 103904 muestras. Con las siguientes características: "Gender","Customer Type","Age","Class","Inflight wifi service","Ease of Online booking","Gate location","Food and drink","Online boarding","Seat comfort","Inflight entertainment","On-board service","Leg room service","Baggage handling","Checkin service","Inflight service". Y como etiquetas tiene: "satisfaction".

Se realizó preprocesamiento de los datos, normalización y PCA. Se propuso usar Regresión Logística, Máquinas de Soporte Vectorial y Redes Neuronales. Por medio de GridSearch se iteró para encontrar los mejores parámetros para cada uno de los métodos. El método que tenga mejor Coeficiente de correlación de Mathews es el seleccionado para la solución del problema.

Resultados Obtenidos por cada Método:

![image](https://user-images.githubusercontent.com/79531784/171408542-8891cd1d-c263-48f4-bb6a-1c2618907820.png)


Conclusiones:

- Como el dataset tiene mas de 100000 datos, el GridSearch de las máquina de soporte vectorial puede tardar alrededor de 6 horas. Esto se debe a que también se tiene 3 hiperparámetros con distintos valores a iterar.
- 
 


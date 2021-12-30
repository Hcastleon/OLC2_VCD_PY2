import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io,base64
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
#matplotlib inline

def analisis(pais,independiente,dependiente,contenido,encabezado):
    data_graph = []
    #obtengo la data :)
    df =  pd.DataFrame(contenido,columns=[encabezado,independiente,dependiente])
    #obtengo las rows que quiero (filtro por pais)
    datita = df.loc[df[encabezado] == pais]
    datita[independiente] = datita[independiente].astype('category').cat.codes
    datita[dependiente] = pd.to_numeric(datita[dependiente])
    posx = datita.columns.get_loc(independiente)
    posy= datita.columns.get_loc(dependiente)
    x = datita.iloc[:,posx].values.reshape(-1,1)
    y = datita.iloc[:,posy].values

    poly_reg=PolynomialFeatures(degree=4)
    X_poly=poly_reg.fit_transform(x)
    poly_reg.fit(X_poly,y)
    lin_reg2=LinearRegression()
    lin_reg2.fit(X_poly,y)

    #Visualising the pollynomial regression model results
    fig = plt.figure()
    plt.scatter(x,y,color='#FF5959')
    plt.plot(x,lin_reg2.predict(poly_reg.fit_transform(x)),color='#676FA3')
    plt.title('Polynomial Regression')
    plt.xlabel('Fechas')
    plt.ylabel('Casos nuevos')

    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b64)
    #Visualising the outlayers

    red_circle = dict(markerfacecolor='#FF5959', marker='o', markeredgecolor='white')
    fig2, axs = plt.subplots(1, 2, figsize=(12,5))
    for i, ax in enumerate(axs.flat):
        i = i+1
        ax.boxplot(datita.iloc[:,i], flierprops=red_circle)
        ax.set_title(datita.columns[i], fontsize=10)
        ax.tick_params(axis='y', labelsize=10)
    plt.tight_layout()

    flike = io.BytesIO()
    fig2.savefig(flike)
    b642 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b642)

    fig3=plt.figure(figsize=(16, 6))
    heatmap=plt.heatmap(datita.corr(),vmin=-1, vmax=1, annot=True)
    heatmap.set_title('Correlation and Heatmap', fontdict={'fontsize':10}, pad=10)

    flike = io.BytesIO()
    fig3.savefig(flike)
    b643 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b643)

    return data_graph


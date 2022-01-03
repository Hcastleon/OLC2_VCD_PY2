import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io,base64
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error

def analisis_cantidad(pais,independiente,dependiente,contenido,encabezado):
    data_graph = []
    regiones = []
    rergion_totales =[]
    #obtengo la data :)
    df =  pd.DataFrame(contenido,columns=[encabezado,independiente,dependiente])
    df = df.replace('',np.nan, regex=True)
    df = df.dropna()
    #obtengo las rows que quiero (filtro por pais)
    datita = df.loc[df[encabezado] == pais]
    for j in datita[independiente].values:
        if not(j in regiones):
            regiones.append(j)

    for i in regiones:
        datita2 = datita.loc[datita[independiente] == i]
        total = datita2[dependiente].sum()
        rergion_totales.append(total)

    cm = sns.color_palette("flare",len(regiones))
    fig = plt.figure()
    plt.bar(regiones,rergion_totales,width = 0.4,color=cm)
    plt.title('Deaths for Regions')
    plt.xlabel('Regions')
    plt.ylabel('Total Deaths')

    for i, v in enumerate(rergion_totales):
        plt.text(i + .25,v + 3, str(v), color='#676FA3', fontweight='bold')

    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.tight_layout()

    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b64)

    return {'graficas':data_graph,'inde':independiente,'depe':dependiente,'filtrado':pais}

def analisis_cantidad(pais,independiente,dependiente,contenido,encabezado):
    data_graph = []
    muertes = 0
    casos =0
    #obtengo la data :)
    df =  pd.DataFrame(contenido,columns=[encabezado,independiente,dependiente])
    df = df.replace('',np.nan, regex=True)
    df = df.dropna()
    #obtengo las rows que quiero (filtro por pais)
    datita = df.loc[df[encabezado] == pais]
    muertes= pd.to_numeric(datita[independiente]).sum()
    casos = pd.to_numeric(datita[dependiente]).sum()

    total = casos - muertes
    cm = sns.color_palette("flare",2)
    fig = plt.figure()
    librerias = [independiente,dependiente]
    valores = [muertes,total]
    explode_vals = [0.15,0]
    plt.pie(x=valores, labels=librerias, colors = cm, autopct='%1.2f%%', shadow=True,
    explode = explode_vals)
    plt.title('Percentage of deaths compared to total cases in a country, region or continent')

    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b64)

    return {'graficas':data_graph,'inde':independiente,'depe':dependiente,'filtrado':pais}
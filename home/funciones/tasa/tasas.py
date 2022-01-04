import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io,base64
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
#matplotlib inline

def analisis_tasas(continente,independiente,dependiente,dependiente2,contenido,encabezado):
    data_graph = []
    #obtengo la data :)
    df =  pd.DataFrame(contenido,columns=[encabezado,independiente,dependiente,dependiente2])
    df = df.replace('',np.nan, regex=True)
    df = df.dropna()

    #obtengo las rows que quiero (filtro por pais)
    datita = df.loc[df[encabezado] == continente]

    fechas = pd.DatetimeIndex(datita[independiente])
    datita[independiente] = datita[independiente].astype('category').cat.codes
    datita[dependiente] = pd.to_numeric(datita[dependiente])
    datita[dependiente2] = pd.to_numeric(datita[dependiente2])
    posx = datita.columns.get_loc(independiente)
    posy= datita.columns.get_loc(dependiente)
    posy2= datita.columns.get_loc(dependiente2)
    x = datita.iloc[:,posx].values.reshape(-1,1)
    y = datita.iloc[:,posy].values
    y2 = datita.iloc[:,posy2].values

    fig = plt.figure()
    poly_reg=PolynomialFeatures(degree=4)
    X_poly=poly_reg.fit_transform(x)
    poly_reg.fit(X_poly,y)
    lin_reg2=LinearRegression()
    lin_reg2.fit(X_poly,y)
    plt.plot(fechas,lin_reg2.predict(poly_reg.fit_transform(x)),color='#FF5959', label = 'Cases')

    poly_reg2=PolynomialFeatures(degree=4)
    X_poly2=poly_reg2.fit_transform(x)
    poly_reg2.fit(X_poly2,y2)
    lin_reg2_1=LinearRegression()
    lin_reg2_1.fit(X_poly2,y2)

    #Visualising the pollynomial regression model results
    plt.plot(fechas, lin_reg2_1.predict(poly_reg2.fit_transform(x)), 'o-r', label = 'Deaths',color='#676FA3')
    plt.title('Polynomial Regression')
    plt.xlabel('Time')
    plt.ylabel('Cases and deaths')
    plt.legend(frameon=False, loc='upper left', ncol=2)
    plt.xticks(rotation=45)
    plt.tight_layout()

    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b64)
    #Visualising the outlayers

    errors = []
    errors2 = []

    for i in range(26):
        errors.append([i] + grados(i, x, y))
        errors2.append([i] + grados(i, x, y2))

    df2 = pd.DataFrame(errors, columns = ['degree','data'])
    df3 = pd.DataFrame(errors2, columns = ['degree','data'])

    fig4 = plt.figure()
    plt.plot(df2['degree'], df2['data'], 'o-r', label = 'Cases',color='#676FA3')
    plt.plot(df3['degree'], df3['data'], 'o-r', label = 'Deaths',color='#FF5959')
    plt.xlabel('Degree')
    plt.ylabel('Data')
    plt.title('Data for different degrees of Polynomial Regression')
    plt.legend(frameon=False, loc='upper left', ncol=2)

    flike = io.BytesIO()
    fig4.savefig(flike)
    b644 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b644)

    best_grade=np.argmin(errors, axis=0)[1]
    best_grade2=np.argmin(errors2, axis=0)[1]

    fig5 = plt.figure()
    poly_reg=PolynomialFeatures(degree=best_grade)
    X_poly=poly_reg.fit_transform(x)
    poly_reg.fit(X_poly,y)
    lin_reg2=LinearRegression()
    lin_reg2.fit(X_poly,y)
    plt.plot(fechas,lin_reg2.predict(poly_reg.fit_transform(x)),color='#FF5959', label = 'Cases')

    poly_reg2=PolynomialFeatures(degree=best_grade2)
    X_poly2=poly_reg2.fit_transform(x)
    poly_reg2.fit(X_poly2,y2)
    lin_reg2_1=LinearRegression()
    lin_reg2_1.fit(X_poly2,y2)

    plt.plot(fechas, lin_reg2_1.predict(poly_reg2.fit_transform(x)), 'o-r', label = 'Deaths',color='#676FA3')
    plt.title('Polynomial Regression')
    plt.xlabel('Time')
    plt.ylabel('Cases and deaths')
    plt.legend(frameon=False, loc='upper left', ncol=2)
    plt.xticks(rotation=45)
    plt.tight_layout()

    flike = io.BytesIO()
    fig5.savefig(flike)
    b645 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b645)

    return {'graficas':data_graph,'grado':best_grade,'grado2':best_grade2,'inde':independiente,'depe':dependiente,'depe2':dependiente2}

def analisis_tasas_locas(continente,independiente,dependiente,dependiente2,contenido,encabezado):
    data_graph = []
    #obtengo la data :)
    df =  pd.DataFrame(contenido,columns=[encabezado,independiente,dependiente,dependiente2])
    df = df.replace('',np.nan, regex=True)
    df = df.dropna()

    #obtengo las rows que quiero (filtro por pais)
    datita = df.loc[df[encabezado] == continente]

    fechas = pd.DatetimeIndex(datita[independiente])
    tasa_totalitos = pd.to_numeric(datita[dependiente]) - pd.to_numeric(datita[dependiente2])


    cm = sns.color_palette("flare",len(tasa_totalitos))
    fig = plt.figure()
    plt.bar(fechas,tasa_totalitos,width = 0.4,color=cm)
    plt.title('Rate of new cases for new deaths ')
    plt.xlabel('Date')
    plt.ylabel('Rate')

    for i, v in enumerate(tasa_totalitos):
        plt.text(i + .25,v + 3, str(v), color='#676FA3', fontweight='bold')

    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.tight_layout()

    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b64)

    return {'graficas':data_graph,'inde':independiente,'depe':dependiente,'depe2':dependiente2}

def tasa_muerte(pais,muertes,poplacion,contenido,encabezado):
    data_graph = []
    #obtengo la data :)
    df =  pd.DataFrame(contenido,columns=[encabezado,muertes,poplacion])
    df = df.replace('',np.nan, regex=True)
    df = df.dropna()
    df[encabezado] = df[encabezado].str.strip()
    #obtengo las rows que quiero (filtro por pais)
    datita = df.loc[df[encabezado] == pais]

    total_muertes = pd.to_numeric(datita[muertes]).sum()
    last_element = pd.to_numeric(datita[poplacion].iloc[-1])
    data_labels =['tasa de muertes','otros']
    data_total = [total_muertes/last_element,1-(total_muertes/last_element)]
    cm = sns.color_palette("Set2",2)
    fig = plt.figure()
    explode_vals = [0.15,0]
    plt.pie(x=data_total, labels=data_labels, colors = cm, autopct='%1.2f%%', shadow=True,
    explode = explode_vals)
    plt.title('Percentage of cases group by sex in a country')
    my_circle=plt.Circle( (0,0), 0.7, color='white')
    p=plt.gcf()
    p.gca().add_artist(my_circle)

    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b64)

    return {'graficas':data_graph,'inde':muertes,'depe':poplacion,'filtrado':pais}


def grados(degrees, x_test, y_test):
    features = PolynomialFeatures(degree=degrees)
    x_test_transformed = features.fit_transform(x_test)
    model = LinearRegression()
    model.fit(x_test_transformed,y_test)
    test_pred = model.predict(x_test_transformed)
    rmse_poly = mean_squared_error(y_test, test_pred, squared = False)

    return [rmse_poly]
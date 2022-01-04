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
    df =  pd.DataFrame(contenido,columns=[encabezado,independiente,dependiente])
    df = df.replace('',np.nan, regex=True)
    df = df.dropna()

    df2 =  pd.DataFrame(contenido,columns=[encabezado,independiente,dependiente2])
    df2 = df2.replace('',np.nan, regex=True)
    df2 = df2.dropna()

    #obtengo las rows que quiero (filtro por pais)
    datita = df.loc[df[encabezado] == continente]
    datita2 = df2.loc[df2[encabezado] == continente]

    #Elimno duplicados
    datita = datita.drop_duplicates(subset=[independiente])
    datita2 = datita2.drop_duplicates(subset=[independiente])

    datita[independiente] = datita[independiente].astype('category').cat.codes
    datita[dependiente] = pd.to_numeric(datita[dependiente])
    posx = datita.columns.get_loc(independiente)
    posy= datita.columns.get_loc(dependiente)
    x = datita.iloc[:,posx].values.reshape(-1,1)
    y = datita.iloc[:,posy].values

    datita2[independiente] = datita[independiente].astype('category').cat.codes
    datita2[dependiente2] = pd.to_numeric(datita2[dependiente2])
    posx_1 = datita2.columns.get_loc(independiente)
    posy_1 = datita2.columns.get_loc(dependiente2)
    x_2 = datita2.iloc[:,posx_1].values.reshape(-1,1)
    y_2 = datita2.iloc[:,posy_1].values

    poly_reg=PolynomialFeatures(degree=4)
    X_poly=poly_reg.fit_transform(x)
    poly_reg.fit(X_poly,y)
    lin_reg2=LinearRegression()
    lin_reg2.fit(X_poly,y)

    poly_reg2=PolynomialFeatures(degree=4)
    X_poly2=poly_reg2.fit_transform(x_2)
    poly_reg2.fit(X_poly2,y_2)
    lin_reg2_1=LinearRegression()
    lin_reg2_1.fit(X_poly2,y_2)

    #Visualising the pollynomial regression model results
    fig = plt.figure()
    plt.plot(x,lin_reg2.predict(poly_reg.fit_transform(x)),color='#FF5959', label = 'Cases')
    plt.plot(x_2, lin_reg2_1.predict(poly_reg2.fit_transform(x_2)), 'o-r', label = 'Deaths',color='#676FA3')
    plt.title('Polynomial Regression')
    plt.xlabel('Time')
    plt.ylabel('Cases')
    plt.legend(frameon=False, loc='upper left', ncol=2)

    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b64)
    #Visualising the outlayers

    errors = []
    errors2 = []

    for i in range(26):
        errors.append([i] + grados(i, x, y))
        errors2.append([i] + grados(i, x_2, y_2))

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

    poly_reg=PolynomialFeatures(degree=best_grade)
    X_poly=poly_reg.fit_transform(x)
    poly_reg.fit(X_poly,y)
    lin_reg2=LinearRegression()
    lin_reg2.fit(X_poly,y)

    poly_reg2=PolynomialFeatures(degree=best_grade2)
    X_poly2=poly_reg2.fit_transform(x_2)
    poly_reg2.fit(X_poly2,y_2)
    lin_reg2_1=LinearRegression()
    lin_reg2_1.fit(X_poly2,y_2)

    #Visualising the pollynomial regression model results
    fig5 = plt.figure()
    plt.plot(x,lin_reg2.predict(poly_reg.fit_transform(x)),color='#FF5959', label = 'Cases')
    plt.plot(x_2, lin_reg2_1.predict(poly_reg2.fit_transform(x_2)), 'o-r', label = 'Deaths',color='#676FA3')
    plt.title('Polynomial Regression')
    plt.xlabel('Time')
    plt.ylabel('Cases')
    plt.legend(frameon=False, loc='upper left', ncol=2)

    flike = io.BytesIO()
    fig5.savefig(flike)
    b645 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b645)

    return {'graficas':data_graph,'grado':best_grade,'grado2':best_grade2,'inde':independiente,'depe':dependiente,'depe2':dependiente2}

def analisis_tasas_locas(continente,independiente,dependiente,dependiente2,dependiente3,contenido,encabezado):
    data_graph = []
    #obtengo la data :)
    df =  pd.DataFrame(contenido,columns=[encabezado,independiente,dependiente])
    df = df.replace('',np.nan, regex=True)
    df = df.dropna()

    df2 =  pd.DataFrame(contenido,columns=[encabezado,independiente,dependiente2])
    df2 = df2.replace('',np.nan, regex=True)
    df2 = df2.dropna()

    df3 =  pd.DataFrame(contenido,columns=[encabezado,independiente,dependiente3])
    df3 = df3.replace('',np.nan, regex=True)
    df3 = df3.dropna()

    #obtengo las rows que quiero (filtro por pais)
    datita = df.loc[df[encabezado] == continente]
    datita2 = df2.loc[df2[encabezado] == continente]
    datita3 = df3.loc[df3[encabezado] == continente]

    #Elimno duplicados
    datita = datita.drop_duplicates(subset=[independiente])
    datita2 = datita2.drop_duplicates(subset=[independiente])
    datita3 = datita3.drop_duplicates(subset=[independiente])

    datita[independiente] = datita[independiente].astype('category').cat.codes
    datita[dependiente] = pd.to_numeric(datita[dependiente])
    posx = datita.columns.get_loc(independiente)
    posy= datita.columns.get_loc(dependiente)
    x = datita.iloc[:,posx].values.reshape(-1,1)
    y = datita.iloc[:,posy].values

    datita2[independiente] = datita2[independiente].astype('category').cat.codes
    datita2[dependiente2] = pd.to_numeric(datita2[dependiente2])
    posx_1 = datita2.columns.get_loc(independiente)
    posy_1 = datita2.columns.get_loc(dependiente2)
    x_2 = datita2.iloc[:,posx_1].values.reshape(-1,1)
    y_2 = datita2.iloc[:,posy_1].values

    datita3[independiente] = datita3[independiente].astype('category').cat.codes
    datita3[dependiente3] = pd.to_numeric(datita3[dependiente3])
    posx_2 = datita3.columns.get_loc(independiente)
    posy_2 = datita3.columns.get_loc(dependiente3)
    x_3 = datita3.iloc[:,posx_2].values.reshape(-1,1)
    y_3 = datita3.iloc[:,posy_2].values

    poly_reg=PolynomialFeatures(degree=4)
    X_poly=poly_reg.fit_transform(x)
    poly_reg.fit(X_poly,y)
    lin_reg2=LinearRegression()
    lin_reg2.fit(X_poly,y)

    poly_reg2=PolynomialFeatures(degree=4)
    X_poly2=poly_reg2.fit_transform(x_2)
    poly_reg2.fit(X_poly2,y_2)
    lin_reg2_1=LinearRegression()
    lin_reg2_1.fit(X_poly2,y_2)

    poly_reg3=PolynomialFeatures(degree=4)
    X_poly3=poly_reg3.fit_transform(x_3)
    poly_reg3.fit(X_poly3,y_3)
    lin_reg2_2=LinearRegression()
    lin_reg2_2.fit(X_poly3,y_3)

    #Visualising the pollynomial regression model results
    fig = plt.figure()
    plt.plot(x,lin_reg2.predict(poly_reg.fit_transform(x)),color='#FF5959', label = 'Total_Cases')
    plt.plot(x_2, lin_reg2_1.predict(poly_reg2.fit_transform(x_2)), 'o-r', label = 'Cases',color='#f39c12')
    plt.plot(x_3, lin_reg2_2.predict(poly_reg3.fit_transform(x_3)), 'o-r', label = 'Deaths',color='#676FA3')
    plt.title('Polynomial Regression')
    plt.xlabel('Time')
    plt.ylabel('Cases')
    plt.legend(frameon=False, loc='upper left', ncol=2)

    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b64)
    #Visualising the outlayers

    errors = []
    errors2 = []
    errors3 = []

    for i in range(26):
        errors.append([i] + grados(i, x, y))
        errors2.append([i] + grados(i, x_2, y_2))
        errors3.append([i] + grados(i, x_3, y_3))

    df2 = pd.DataFrame(errors, columns = ['degree','data'])
    df3 = pd.DataFrame(errors2, columns = ['degree','data'])
    df4 = pd.DataFrame(errors3, columns = ['degree','data'])

    fig4 = plt.figure()
    plt.plot(df2['degree'], df2['data'], 'o-r', label = 'Total_Cases',color='#676FA3')
    plt.plot(df3['degree'], df3['data'], 'o-r', label = 'Cases',color='#f39c12')
    plt.plot(df4['degree'], df4['data'], 'o-r', label = 'Deaths',color='#FF5959')
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
    best_grade3=np.argmin(errors3, axis=0)[1]

    poly_reg=PolynomialFeatures(degree=best_grade)
    X_poly=poly_reg.fit_transform(x)
    poly_reg.fit(X_poly,y)
    lin_reg2=LinearRegression()
    lin_reg2.fit(X_poly,y)

    poly_reg2=PolynomialFeatures(degree=best_grade2)
    X_poly2=poly_reg2.fit_transform(x_2)
    poly_reg2.fit(X_poly2,y_2)
    lin_reg2_1=LinearRegression()
    lin_reg2_1.fit(X_poly2,y_2)

    poly_reg3=PolynomialFeatures(degree=best_grade3)
    X_poly3=poly_reg3.fit_transform(x_3)
    poly_reg3.fit(X_poly3,y_3)
    lin_reg2_2=LinearRegression()
    lin_reg2_2.fit(X_poly3,y_3)

    #Visualising the pollynomial regression model results
    fig5 = plt.figure()
    plt.plot(x,lin_reg2.predict(poly_reg.fit_transform(x)),color='#FF5959', label = 'Total_Cases')
    plt.plot(x_2, lin_reg2_1.predict(poly_reg2.fit_transform(x_2)), 'o-r', label = 'Cases',color='#f39c12')
    plt.plot(x_3, lin_reg2_2.predict(poly_reg3.fit_transform(x_3)), 'o-r', label = 'Deaths',color='#676FA3')
    plt.title('Polynomial Regression')
    plt.xlabel('Time')
    plt.ylabel('Cases')
    plt.legend(frameon=False, loc='upper left', ncol=2)

    flike = io.BytesIO()
    fig5.savefig(flike)
    b645 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b645)

    return {'graficas':data_graph,'grado':best_grade,'grado2':best_grade2,'grado3':best_grade3,'inde':independiente,'depe':dependiente,'depe2':dependiente2,'depe3':dependiente3}

# def regresar_tasa(pais,independiente,dependiente,contenido,encabezado):
#     df =  pd.DataFrame(contenido,columns=[encabezado,independiente,dependiente])
#     df = df.replace('',np.nan, regex=True)
#     df = df.dropna()
#     #obtengo las rows que quiero (filtro por pais)
#     datita = df.loc[df[encabezado] == pais]
#     if len(datita.values) == 0:
#         return 0

#     datita[independiente] = datita[independiente].astype('category').cat.codes
#     datita[dependiente] = pd.to_numeric(datita[dependiente])
#     tasa = ((max(datita[dependiente]) - min(datita[dependiente]))/ min(datita[dependiente]))*100
#     return tasa


def grados(degrees, x_test, y_test):
    features = PolynomialFeatures(degree=degrees)
    x_test_transformed = features.fit_transform(x_test)
    model = LinearRegression()
    model.fit(x_test_transformed,y_test)
    test_pred = model.predict(x_test_transformed)
    rmse_poly = mean_squared_error(y_test, test_pred, squared = False)

    return [rmse_poly]

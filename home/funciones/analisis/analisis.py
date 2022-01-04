import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io,base64
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
import itertools
#matplotlib inline

def analisis_a(pais,pais2,independiente,dependiente,contenido,encabezado):
    data_graph = []
    data_list = []
    lista_variables = [pais,pais2]
    #obtengo la data :)
    df =  pd.DataFrame(contenido,columns=[encabezado,independiente,dependiente])
    df = df.replace('',np.nan, regex=True)
    df = df.dropna()
    #obtengo las rows que quiero (filtro por pais)
    for i in lista_variables:
        datita = df.loc[df[encabezado] == i]
        data_list.append(datita)

    cm = sns.color_palette("viridis",len(lista_variables)).as_hex()
    fig_together = plt.figure()
    for (i,j,k) in zip(data_list,lista_variables,cm):
        fechas = pd.DatetimeIndex(i[independiente])
        i[independiente] = i[independiente].astype('category').cat.codes
        i[dependiente] = pd.to_numeric(i[dependiente])
        posx = i.columns.get_loc(independiente)
        posy= i.columns.get_loc(dependiente)
        x = i.iloc[:,posx].values.reshape(-1,1)
        y = i.iloc[:,posy].values

        poly_reg=PolynomialFeatures(degree=4)
        X_poly=poly_reg.fit_transform(x)
        poly_reg.fit(X_poly,y)
        lin_reg2=LinearRegression()
        lin_reg2.fit(X_poly,y)
        #together :)
        plt.plot(fechas,lin_reg2.predict(poly_reg.fit_transform(x)),color=k, label=j)


    plt.xlabel('Time')
    plt.ylabel('Cases')
    plt.legend(frameon=False, loc='upper left', ncol=2)
    plt.title('Polynomial Regression for the n countrys')
    plt.xticks(rotation=45)
    plt.tight_layout()

    flike = io.BytesIO()
    fig_together.savefig(flike)
    b64_together = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b64_together)

    best_grade = []

    cm = sns.color_palette("rocket_r",len(lista_variables)).as_hex()
    fig4 = plt.figure()
    for (i,j,k) in zip(data_list,lista_variables,cm):
        i[independiente] = i[independiente].astype('category').cat.codes
        i[dependiente] = pd.to_numeric(i[dependiente])
        posx = i.columns.get_loc(independiente)
        posy= i.columns.get_loc(dependiente)
        x = i.iloc[:,posx].values.reshape(-1,1)
        y = i.iloc[:,posy].values

        errors = []
        for l in range(26):
            errors.append([l] + grados(l, x, y))

        best_grade.append(np.argmin(errors, axis=0)[1])
        df2 = pd.DataFrame(errors, columns = ['degree','data'])

        plt.plot(df2['degree'], df2['data'], 'o-r', label = j,color=k)

    plt.xlabel('Degree')
    plt.ylabel('Data')
    plt.legend(frameon=False, loc='upper left', ncol=2)
    plt.title('Data for different degrees of Polynomial Regression')

    flike = io.BytesIO()
    fig4.savefig(flike)
    b644 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b644)

    cm = sns.color_palette("viridis",len(lista_variables)).as_hex()
    fig5 = plt.figure()
    for (i,j,k,l) in zip(data_list,lista_variables, best_grade,cm):
        fechas = pd.DatetimeIndex(i[independiente])
        i[independiente] = i[independiente].astype('category').cat.codes
        i[dependiente] = pd.to_numeric(i[dependiente])
        posx = i.columns.get_loc(independiente)
        posy= i.columns.get_loc(dependiente)
        x = i.iloc[:,posx].values.reshape(-1,1)
        y = i.iloc[:,posy].values

        poly_reg=PolynomialFeatures(degree=k)
        X_poly=poly_reg.fit_transform(x)
        poly_reg.fit(X_poly,y)
        lin_reg2=LinearRegression()
        lin_reg2.fit(X_poly,y)
        #together :)
        plt.plot(fechas,lin_reg2.predict(poly_reg.fit_transform(x)),color=l, label=j)

    #Visualising the pollynomial regression model results with the best degree
    plt.xlabel('Time')
    plt.ylabel('Cases')
    plt.legend(frameon=False, loc='upper left', ncol=2)
    plt.title(f'Polynomial Regression for the n countrys with the best degree')
    plt.xticks(rotation=45)
    plt.tight_layout()

    flike = io.BytesIO()
    fig5.savefig(flike)
    b645 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b645)

    return {'graficas':data_graph,'grado':best_grade,'inde':independiente,'depe':dependiente, 'pais':lista_variables}

def analisis_a_varios(lista_variables,independiente,dependiente,contenido,encabezado):
    data_graph = []
    data_list = []
    #obtengo la data :)
    df =  pd.DataFrame(contenido,columns=[encabezado,independiente,dependiente])
    df = df.replace('',np.nan, regex=True)
    df = df.dropna()
    #obtengo las rows que quiero (filtro por pais)
    for i in lista_variables:
        datita = df.loc[df[encabezado] == i]
        data_list.append(datita)

    cm = sns.color_palette("viridis",len(lista_variables)).as_hex()
    fig_together = plt.figure()
    for (i,j,k) in zip(data_list,lista_variables,cm):
        fechas = pd.DatetimeIndex(i[independiente])
        i[independiente] = i[independiente].astype('category').cat.codes
        i[dependiente] = pd.to_numeric(i[dependiente])
        posx = i.columns.get_loc(independiente)
        posy= i.columns.get_loc(dependiente)
        x = i.iloc[:,posx].values.reshape(-1,1)
        y = i.iloc[:,posy].values

        poly_reg=PolynomialFeatures(degree=4)
        X_poly=poly_reg.fit_transform(x)
        poly_reg.fit(X_poly,y)
        lin_reg2=LinearRegression()
        lin_reg2.fit(X_poly,y)
        #together :)
        plt.plot(fechas,lin_reg2.predict(poly_reg.fit_transform(x)),color=k, label=j)


    plt.xlabel('Time')
    plt.ylabel('Cases')
    plt.legend(frameon=False, loc='upper left', ncol=2)
    plt.title('Polynomial Regression for the n countrys')
    plt.xticks(rotation=45)
    plt.tight_layout()

    flike = io.BytesIO()
    fig_together.savefig(flike)
    b64_together = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b64_together)

    best_grade = []

    cm = sns.color_palette("rocket_r",len(lista_variables)).as_hex()
    fig4 = plt.figure()
    for (i,j,k) in zip(data_list,lista_variables,cm):
        i[independiente] = i[independiente].astype('category').cat.codes
        i[dependiente] = pd.to_numeric(i[dependiente])
        posx = i.columns.get_loc(independiente)
        posy= i.columns.get_loc(dependiente)
        x = i.iloc[:,posx].values.reshape(-1,1)
        y = i.iloc[:,posy].values

        errors = []
        for l in range(26):
            errors.append([l] + grados(l, x, y))

        best_grade.append(np.argmin(errors, axis=0)[1])
        df2 = pd.DataFrame(errors, columns = ['degree','data'])

        plt.plot(df2['degree'], df2['data'], 'o-r', label = j,color=k)

    plt.xlabel('Degree')
    plt.ylabel('Data')
    plt.legend(frameon=False, loc='upper left', ncol=2)
    plt.title('Data for different degrees of Polynomial Regression')

    flike = io.BytesIO()
    fig4.savefig(flike)
    b644 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b644)

    cm = sns.color_palette("viridis",len(lista_variables)).as_hex()
    fig5 = plt.figure()
    for (i,j,k,l) in zip(data_list,lista_variables, best_grade,cm):
        fechas = pd.DatetimeIndex(i[independiente])
        i[independiente] = i[independiente].astype('category').cat.codes
        i[dependiente] = pd.to_numeric(i[dependiente])
        posx = i.columns.get_loc(independiente)
        posy= i.columns.get_loc(dependiente)
        x = i.iloc[:,posx].values.reshape(-1,1)
        y = i.iloc[:,posy].values

        poly_reg=PolynomialFeatures(degree=k)
        X_poly=poly_reg.fit_transform(x)
        poly_reg.fit(X_poly,y)
        lin_reg2=LinearRegression()
        lin_reg2.fit(X_poly,y)
        #together :)
        plt.plot(fechas,lin_reg2.predict(poly_reg.fit_transform(x)),color=l, label=j)

    #Visualising the pollynomial regression model results with the best degree
    plt.xlabel('Time')
    plt.ylabel('Cases')
    plt.legend(frameon=False, loc='upper left', ncol=2)
    plt.title(f'Polynomial Regression for the n countrys with the best degree')
    plt.xticks(rotation=45)
    plt.tight_layout()

    flike = io.BytesIO()
    fig5.savefig(flike)
    b645 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b645)

    return {'graficas':data_graph,'grado':best_grade,'inde':independiente,'depe':dependiente, 'pais':lista_variables}




def grados(degrees, x_test, y_test):
    features = PolynomialFeatures(degree=degrees)
    x_test_transformed = features.fit_transform(x_test)
    model = LinearRegression()
    model.fit(x_test_transformed,y_test)
    test_pred = model.predict(x_test_transformed)
    rmse_poly = mean_squared_error(y_test, test_pred, squared = False)

    return [rmse_poly]
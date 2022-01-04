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
    #obtengo la data :)
    df =  pd.DataFrame(contenido,columns=[encabezado,independiente,dependiente])
    df = df.replace('',np.nan, regex=True)
    df = df.dropna()
    #obtengo las rows que quiero (filtro por pais)
    datita = df.loc[df[encabezado] == pais]
    datita2 = df.loc[df[encabezado] == pais2]

    tablita =datita.describe()
    fig0,ax = plt.subplots(1,1)
    cm = sns.color_palette("flare",15)
    cm2 = sns.color_palette("flare",5)
    pd.plotting.table(ax,tablita, rowColours=cm, colLabels=tablita.columns, colColours=cm2, loc='center')
    ax.axis('off')

    flike = io.BytesIO()
    fig0.savefig(flike)
    b640 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b640)

    tablita2 =datita2.describe()
    fig0_1,ax = plt.subplots(1,1)
    cm = sns.color_palette("flare",15)
    cm2 = sns.color_palette("flare",5)
    pd.plotting.table(ax,tablita2, rowColours=cm, colLabels=tablita2.columns, colColours=cm2, loc='center')
    ax.axis('off')

    flike = io.BytesIO()
    fig0_1.savefig(flike)
    b640_1 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b640_1)

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
    plt.xlabel('Time')
    plt.ylabel('Cases')

    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b64)

    datita2[independiente] = datita2[independiente].astype('category').cat.codes
    datita2[dependiente] = pd.to_numeric(datita2[dependiente])
    posx_0 = datita2.columns.get_loc(independiente)
    posy_0= datita2.columns.get_loc(dependiente)
    x_0 = datita2.iloc[:,posx_0].values.reshape(-1,1)
    y_0 = datita2.iloc[:,posy_0].values

    poly_reg2=PolynomialFeatures(degree=4)
    X_poly2=poly_reg2.fit_transform(x_0)
    poly_reg2.fit(X_poly2,y_0)
    lin_reg2_0=LinearRegression()
    lin_reg2_0.fit(X_poly2,y_0)

    #Visualising the pollynomial regression model results
    fig_1 = plt.figure()
    plt.scatter(x_0,y,color='#FF5959')
    plt.plot(x_0,lin_reg2_0.predict(poly_reg2.fit_transform(x_0)),color='#676FA3')
    plt.title('Polynomial Regression')
    plt.xlabel('Time')
    plt.ylabel('Cases')

    flike = io.BytesIO()
    fig_1.savefig(flike)
    b64_1 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b64_1)
    #together :)
    fig_together = plt.figure()
    plt.plot(x,lin_reg2.predict(poly_reg.fit_transform(x)),color='#73c6b6', label=pais)
    plt.plot(x_0,lin_reg2_0.predict(poly_reg2.fit_transform(x_0)),color='#676FA3', label=pais2)
    plt.xlabel('Time')
    plt.ylabel('Cases')
    plt.legend(frameon=False, loc='upper left', ncol=2)
    plt.title('Polynomial Regression for the two countrys')

    flike = io.BytesIO()
    fig_together.savefig(flike)
    b64_together = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b64_together)
    #Visualising the outlayers
    red_circle = dict(markerfacecolor='#FF5959', marker='o', markeredgecolor='white')
    fig2, axs = plt.subplots(1, 2, figsize=(12,5))
    for i, ax in enumerate(axs.flat):
        i = i +1
        ax.boxplot(datita.iloc[:,i], flierprops=red_circle)
        ax.set_title(datita.columns[i], fontsize=10)
        ax.tick_params(axis='y', labelsize=10)
    plt.tight_layout()

    flike = io.BytesIO()
    fig2.savefig(flike)
    b642 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b642)

    red_circle = dict(markerfacecolor='#FF5959', marker='o', markeredgecolor='white')
    fig2_1, axs = plt.subplots(1, 2, figsize=(12,5))
    for i, ax in enumerate(axs.flat):
        i = i +1
        ax.boxplot(datita2.iloc[:,i], flierprops=red_circle)
        ax.set_title(datita2.columns[i], fontsize=10)
        ax.tick_params(axis='y', labelsize=10)
    plt.tight_layout()

    flike = io.BytesIO()
    fig2_1.savefig(flike)
    b642_1 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b642_1)

    fig3=plt.figure(figsize=(16, 6))
    heatmap=sns.heatmap(datita.corr(),vmin=-1, vmax=1, annot=True)
    heatmap.set_title('Correlation and Heatmap', fontdict={'fontsize':10}, pad=10)

    flike = io.BytesIO()
    fig3.savefig(flike)
    b643 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b643)

    fig3_1=plt.figure(figsize=(16, 6))
    heatmap=sns.heatmap(datita2.corr(),vmin=-1, vmax=1, annot=True)
    heatmap.set_title('Correlation and Heatmap', fontdict={'fontsize':10}, pad=10)
    
    flike = io.BytesIO()
    fig3_1.savefig(flike)
    b643_1 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b643_1)

    errors = []
    errors2 = []

    for i in range(26):
        errors.append([i] + grados(i, x, y))
        errors2.append([i] + grados(i, x_0, y_0))


    df2 = pd.DataFrame(errors, columns = ['degree','data'])
    df3 = pd.DataFrame(errors2, columns = ['degree','data'])

    fig4 = plt.figure()
    plt.plot(df2['degree'], df2['data'], 'o-r', label = pais,color='#676FA3')
    plt.plot(df3['degree'], df3['data'], 'o-r', color='#73c6b6', label=pais2)
    plt.xlabel('Degree')
    plt.ylabel('Data')
    plt.legend(frameon=False, loc='upper left', ncol=2)
    plt.title('Data for different degrees of Polynomial Regression')

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
    X_poly2=poly_reg2.fit_transform(x_0)
    poly_reg2.fit(X_poly2,y_0)
    lin_reg2_0=LinearRegression()
    lin_reg2_0.fit(X_poly2,y_0)

    #Visualising the pollynomial regression model results with the best degree
    fig5 = plt.figure()
    plt.plot(x,lin_reg2.predict(poly_reg.fit_transform(x)),color='#73c6b6', label=pais)
    plt.plot(x_0,lin_reg2_0.predict(poly_reg2.fit_transform(x_0)),color='#676FA3', label=pais2)
    plt.xlabel('Time')
    plt.ylabel('Cases')
    plt.legend(frameon=False, loc='upper left', ncol=2)
    plt.title(f'Polynomial Regression for the two countrys with the best degree: {best_grade} and {best_grade2}')

    flike = io.BytesIO()
    fig5.savefig(flike)
    b645 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b645)

    return {'graficas':data_graph,'grado':best_grade,'grado2':best_grade2,'inde':independiente,'depe':dependiente,'filtrado':pais,'filtrado2':pais2}

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
        plt.plot(x,lin_reg2.predict(poly_reg.fit_transform(x)),color=k, label=j)


    plt.xlabel('Time')
    plt.ylabel('Cases')
    plt.legend(frameon=False, loc='upper left', ncol=2)
    plt.title('Polynomial Regression for the n countrys')

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
        plt.plot(x,lin_reg2.predict(poly_reg.fit_transform(x)),color=l, label=j)

    #Visualising the pollynomial regression model results with the best degree
    plt.xlabel('Time')
    plt.ylabel('Cases')
    plt.legend(frameon=False, loc='upper left', ncol=2)
    plt.title(f'Polynomial Regression for the n countrys with the best degree')

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
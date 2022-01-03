import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io,base64
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
#matplotlib inline

def analisis_p(pais,independiente,dependiente,prediccion,contenido,encabezado):
    data_graph = []
    #obtengo la data :)
    df =  pd.DataFrame(contenido,columns=[encabezado,independiente,dependiente])
    df = df.replace('',np.nan, regex=True)
    df = df.dropna()
    #obtengo las rows que quiero (filtro por pais)
    datita = df.loc[df[encabezado] == pais]

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

    datita[independiente] = datita[independiente].astype('category').cat.codes
    datita[dependiente] = pd.to_numeric(datita[dependiente])
    posx = datita.columns.get_loc(independiente)
    posy= datita.columns.get_loc(dependiente)
    x = datita.iloc[:,posx].values.reshape(-1,1)
    y = datita.iloc[:,posy].values

    temporal = np.arange(0,len(x)+ int(prediccion))
    x_1 = temporal.reshape((-1, 1))

    poly_reg=PolynomialFeatures(degree=4)
    X_poly=poly_reg.fit_transform(x)
    poly_reg.fit(X_poly,y)
    lin_reg2=LinearRegression()
    lin_reg2.fit(X_poly,y)

    resultado = lin_reg2.predict(poly_reg.fit_transform([x[-1]+int(prediccion)]))

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

    #Visualising the pollynomial regression model results
    fig1 = plt.figure()
    plt.plot(x_1,lin_reg2.predict(poly_reg.fit_transform(x_1)),color='#676FA3')
    plt.title('Polynomial Regression with Prediccion')
    plt.xlabel('Time')
    plt.ylabel('Cases')

    flike = io.BytesIO()
    fig1.savefig(flike)
    b641 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b641)
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
    heatmap=sns.heatmap(datita.corr(),vmin=-1, vmax=1, annot=True)
    heatmap.set_title('Correlation and Heatmap', fontdict={'fontsize':10}, pad=10)


    flike = io.BytesIO()
    fig3.savefig(flike)
    b643 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b643)

    errors = []

    for i in range(26):
        errors.append([i] + grados(i, x, y))

    df2 = pd.DataFrame(errors, columns = ['degree','data'])

    fig4 = plt.figure()
    plt.plot(df2['degree'], df2['data'], 'o-r', label = 'Data',color='#676FA3')
    plt.xlabel('Degree')
    plt.ylabel('Data')
    plt.title('Data for different degrees of Polynomial Regression')

    flike = io.BytesIO()
    fig4.savefig(flike)
    b644 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b644)

    best_grade=np.argmin(errors, axis=0)[1]

    poly_reg=PolynomialFeatures(degree=best_grade)
    X_poly=poly_reg.fit_transform(x)
    poly_reg.fit(X_poly,y)
    lin_reg2=LinearRegression()
    lin_reg2.fit(X_poly,y)

    #Visualising the pollynomial regression model results with the best degree
    fig5 = plt.figure()
    plt.plot(x_1,lin_reg2.predict(poly_reg.fit_transform(x_1)),color='#FF5959')
    plt.title(f'Polynomial Regression Prediccion with the best degree: {best_grade}')
    plt.xlabel('Time')
    plt.ylabel('Cases')

    flike = io.BytesIO()
    fig5.savefig(flike)
    b645 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b645)

    return {'graficas':data_graph,'grado':best_grade,'inde':independiente,'depe':dependiente,'filtrado':pais,'resultado':resultado}

def analisis2_p(pais,depa,independiente,dependiente,prediccion,contenido,encabezado,encabezado2):
    data_graph = []
    #obtengo la data :)
    df =  pd.DataFrame(contenido,columns=[encabezado,encabezado2,independiente,dependiente])
    df = df.dropna()
    #obtengo las rows que quiero (filtro por pais)
    datita = df.loc[df[encabezado] == pais]
    datita = datita.loc[datita[encabezado2] == depa]

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

    datita[independiente] = datita[independiente].astype('category').cat.codes
    datita[dependiente] = pd.to_numeric(datita[dependiente])
    posx = datita.columns.get_loc(independiente)
    posy= datita.columns.get_loc(dependiente)
    x = datita.iloc[:,posx].values.reshape(-1,1)
    y = datita.iloc[:,posy].values

    temporal = np.arange(0,len(x)+ int(prediccion))
    x_1 = temporal.reshape((-1, 1))

    poly_reg=PolynomialFeatures(degree=4)
    X_poly=poly_reg.fit_transform(x)
    poly_reg.fit(X_poly,y)
    lin_reg2=LinearRegression()
    lin_reg2.fit(X_poly,y)

    resultado = lin_reg2.predict(poly_reg.fit_transform([x[-1]+int(prediccion)]))

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

    #Visualising the pollynomial regression model results
    fig1 = plt.figure()
    plt.plot(x_1,lin_reg2.predict(poly_reg.fit_transform(x_1)),color='#676FA3')
    plt.title('Polynomial Regression with Prediccion')
    plt.xlabel('Time')
    plt.ylabel('Cases')

    flike = io.BytesIO()
    fig1.savefig(flike)
    b641 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b641)
    #Visualising the outlayers

    red_circle = dict(markerfacecolor='#FF5959', marker='o', markeredgecolor='white')
    fig2, axs = plt.subplots(1, 2, figsize=(12,5))
    for i, ax in enumerate(axs.flat):
        i = i +2
        if i > 1:
            ax.boxplot(datita.iloc[:,i], flierprops=red_circle)
            ax.set_title(datita.columns[i], fontsize=10)
            ax.tick_params(axis='y', labelsize=10)
    plt.tight_layout()

    flike = io.BytesIO()
    fig2.savefig(flike)
    b642 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b642)

    fig3=plt.figure(figsize=(16, 6))
    heatmap=sns.heatmap(datita.corr(),vmin=-1, vmax=1, annot=True)
    heatmap.set_title('Correlation and Heatmap', fontdict={'fontsize':10}, pad=10)


    flike = io.BytesIO()
    fig3.savefig(flike)
    b643 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b643)

    errors = []

    for i in range(26):
        errors.append([i] + grados(i, x, y))

    df2 = pd.DataFrame(errors, columns = ['degree','data'])

    fig4 = plt.figure()
    plt.plot(df2['degree'], df2['data'], 'o-r', label = 'Data',color='#676FA3')
    plt.xlabel('Degree')
    plt.ylabel('Data')
    plt.title('Data for different degrees of Polynomial Regression')

    flike = io.BytesIO()
    fig4.savefig(flike)
    b644 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b644)

    best_grade=np.argmin(errors, axis=0)[1]

    poly_reg=PolynomialFeatures(degree=best_grade)
    X_poly=poly_reg.fit_transform(x)
    poly_reg.fit(X_poly,y)
    lin_reg2=LinearRegression()
    lin_reg2.fit(X_poly,y)

    #Visualising the pollynomial regression model results with the best degree
    fig5 = plt.figure()
    plt.plot(x_1,lin_reg2.predict(poly_reg.fit_transform(x_1)),color='#FF5959')
    plt.title(f'Polynomial Regression Prediccion with the best degree: {best_grade}')
    plt.xlabel('Time')
    plt.ylabel('Cases')

    flike = io.BytesIO()
    fig5.savefig(flike)
    b645 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b645)

    return {'graficas':data_graph,'grado':best_grade,'inde':independiente,'depe':dependiente,'filtrado':pais,'filtrado2':depa,'resultado':resultado}

def analisis_year_p(pais,independiente,dependiente,contenido,encabezado):
    data_graph = []
    #obtengo la data :)
    df =  pd.DataFrame(contenido,columns=[encabezado,independiente,dependiente])
    df = df.replace('',np.nan, regex=True)
    df = df.dropna()
    #obtengo las rows que quiero (filtro por pais)
    datita = df.loc[df[encabezado] == pais]
    years = pd.DatetimeIndex(datita[independiente]).year

    min_year = pd.DatetimeIndex(datita[independiente]).is_year_end
    prediccion = [i for i, val in enumerate(min_year) if val and years[i] == min(years)]

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

    resultado = lin_reg2.predict(poly_reg.fit_transform([prediccion]))

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

    #Visualising the pollynomial regression model results
    fig1 = plt.figure()
    plt.plot(x,lin_reg2.predict(poly_reg.fit_transform(x)),color='#676FA3')
    plt.title('Polynomial Regression with Prediccion')
    plt.xlabel('Time')
    plt.ylabel('Cases')

    flike = io.BytesIO()
    fig1.savefig(flike)
    b641 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b641)
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
    heatmap=sns.heatmap(datita.corr(),vmin=-1, vmax=1, annot=True)
    heatmap.set_title('Correlation and Heatmap', fontdict={'fontsize':10}, pad=10)


    flike = io.BytesIO()
    fig3.savefig(flike)
    b643 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b643)

    errors = []

    for i in range(26):
        errors.append([i] + grados(i, x, y))

    df2 = pd.DataFrame(errors, columns = ['degree','data'])

    fig4 = plt.figure()
    plt.plot(df2['degree'], df2['data'], 'o-r', label = 'Data',color='#676FA3')
    plt.xlabel('Degree')
    plt.ylabel('Data')
    plt.title('Data for different degrees of Polynomial Regression')

    flike = io.BytesIO()
    fig4.savefig(flike)
    b644 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b644)

    best_grade=np.argmin(errors, axis=0)[1]

    poly_reg=PolynomialFeatures(degree=best_grade)
    X_poly=poly_reg.fit_transform(x)
    poly_reg.fit(X_poly,y)
    lin_reg2=LinearRegression()
    lin_reg2.fit(X_poly,y)

    #Visualising the pollynomial regression model results with the best degree
    fig5 = plt.figure()
    plt.plot(x,lin_reg2.predict(poly_reg.fit_transform(x)),color='#FF5959')
    plt.title(f'Polynomial Regression Prediccion with the best degree: {best_grade}')
    plt.xlabel('Time')
    plt.ylabel('Cases')

    flike = io.BytesIO()
    fig5.savefig(flike)
    b645 = base64.b64encode(flike.getvalue()).decode()
    data_graph.append(b645)

    return {'graficas':data_graph,'grado':best_grade,'inde':independiente,'depe':dependiente,'filtrado':pais,'resultado':resultado}

def grados(degrees, x_test, y_test):
    features = PolynomialFeatures(degree=degrees)
    x_test_transformed = features.fit_transform(x_test)
    model = LinearRegression()
    model.fit(x_test_transformed,y_test)
    test_pred = model.predict(x_test_transformed)
    rmse_poly = mean_squared_error(y_test, test_pred, squared = False)

    return [rmse_poly]
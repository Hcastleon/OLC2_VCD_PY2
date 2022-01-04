# Organizacion de computadoras y lenguajes 2
<h1 align="center">
  <br>
  <a></a>
  <br>
  Coronavirus Data Analysis With Machine Learning
  <br>
</h1>

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)
[![GitHub issues](https://img.shields.io/github/issues/Naereen/StrapDown.js.svg)](https://github.com/Hcastleon/OLC2_VCD_PY1/issues)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
![Python](https://img.shields.io/pypi/pyversions/py)
![Django](https://img.shields.io/pypi/djversions/djangorestframework)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)

## Tabla de Contenido
1. [Requisitos](#requisitos)
3. [Librerias](#detalle)
4. [Flujo del programa](#flujo)
5. [Codigo](#codigito)
6. [Autor](#name)

### Requisitos <a name="requisitos"></a>
| Componente | Mínimo                                                                | Recomendado                                                    |
| ---------- | --------------------------------------------------------------------- | -------------------------------------------------------------- |
| Procesador | Procesador de x64 bits de doble núcleo de 1,9 gigahercios (GHz) | Procesador de 64 bits de doble núcleo de 3,3 gigahercios (GHz) |
| Memoria    | 8 GB de RAM                                                           | 16 GB de RAM o más                                              |
| Disco Duro | 6 GB de espacio disponible en el disco duro                           | 6 GB de espacio disponible en el disco duro                    |
| Pantalla   | 1024 x 768                                                            | 1024 x 768                                                     |

### Librerias <a name="detalle"></a>
 *  pandas               1.3.5
 *  numpy                1.21.5
 *  seaborn              0.11.2
 *  matplotlib           3.5.1
 *  scikit-learn         1.0.2
 *  reportlab            3.6.5

### Flujo <a name="flujo"></a>
![imagen1](/image/flujo.png)
![imagen2](https://miro.medium.com/max/700/1*mcVw24ZtqLpo8_-K1kroIQ.png)

### Codigo <a name="codigito"></a>
#### Manejo de extensiones csv,xls|xlsx,json
> se utilizaron las librerias nativas csv, json y la libreria pandas para poder hacer lectura de los archivos de entrada

~~~
csv_reader = csv.DictReader(csvreader)
aux = pd.read_excel(archivo)
diccionario = json.load(archivo)
~~~

#### Manejo de data
>Pandas es una biblioteca de código abierto que se basa en la biblioteca NumPy. Es un paquete de Python que ofrece varias estructuras de datos y operaciones para manipular datos numéricos y series de tiempo. Con la cual se realizo el analisis de datos.

>La mayoria de los analisis se realiza con un modelo de regresion polinomial, ayudandonos de la herramienta scikit-learn.

> Estos clasificadores son atractivos porque tienen soluciones de forma cerrada que se pueden calcular fácilmente, son intrínsecamente multiclase, han demostrado funcionar bien en la práctica y no tienen hiperparámetros para ajustar.

>La regresión polinomial es un algoritmo bien conocido. Es un caso especial de regresión lineal, por el hecho de que creamos algunas características polinomiales antes de crear una regresión lineal.

>Con scikit learn, es posible crear uno en una canalización combinando estos dos pasos (Polynomialfeatures y LinearRegression).

> como por ejemplo:

~~~
X, y = df[["x_1", "x_2"]], df["y"]
poly = PolynomialFeatures(degree=2, include_bias=False)
poly_features = poly.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(poly_features, y, test_size=0.3, random_state=42)
~~~

> para ver los resultados graficos de las regresiones polinomiales se utiliza la libreria matlibplot y se generan mediante:
~~~
plt.figure(figsize=(10, 6))
plt.title("polynomial regression)", size=16)
plt.scatter(x, y)
plt.plot(x, y_predicted, c="red")
plt.show()
~~~

#### Generacion de reportes
>Lo primero que hacemos es importar el módulo reportlab.pdfgen.canvas, luego creamos una instancia de la clase canvas.Canvas pasándole como argumento el nombre o la ruta del archivo que queremos generar, y por último invocamos el método Canvas.save() que guarda efectivamente los cambios en el documento.

>Si bien nuestro objeto c representa al archivo íntegro sobre el que estamos trabajando, un canvas debe ser pensado simplemente como una hoja en blanco en la que debemos escribir, dibujar o lo que fuere. Estas operaciones de escritura o dibujo ocurrirán siempre entre la creación del documento y el método que guarda los cambios.

> Por ejemplo:

~~~
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
w, h = A4
c = canvas.Canvas("hola-mundo.pdf", pagesize=A4)
c.drawString(50, h - 50, "¡Hola, mundo!")
c.showPage()
c.save()
~~~

> reportlab tiene una infinidad de librerias con las cuales se puede utilizar dar un diseño especifico al pdf a crear

> como por ejemplo:
~~~
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Titulos',
            fontName='Times-Roman', fontSize=20,alignment=TA_CENTER))
styles.add(ParagraphStyle(name='Cuerpo',
            fontName='Times-Roman', fontSize=10, alignment=TA_JUSTIFY, leading=14))
styles.add(ParagraphStyle(name='Subtitulo',
            fontName='Times-Roman', fontSize=10, bulletAnchor ='start', bulletFontName ='I', bulletFontSize = 10, bulletIndent = 10, leading=14, spaceAfter=20 ))
styles.add(ParagraphStyle(name='Equations',
            fontName='Times-Roman', fontSize=12, alignment=TA_CENTER, leading=14, spaceAfter=15, spaceBefore=15))
~~~

### Autor <a name="name"></a>
| Nombre | Carné |
| ------ | ------ |
| Heidy Carolina Castellanos de León | 201612282 |
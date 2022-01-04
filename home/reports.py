import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, PageBreak, PageTemplate, NextPageTemplate, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus.flowables import Spacer
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

def reporte_tendencia1(titulo,nombre,graficas, datos):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    doc = BaseDocTemplate(buffer, showBoundary=0, pagesizes=A4)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Titulos',
               fontName='Times-Roman', fontSize=20,alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Cuerpo',
               fontName='Times-Roman', fontSize=10, alignment=TA_JUSTIFY, leading=14))
    styles.add(ParagraphStyle(name='Subtitulo',
               fontName='Times-Roman', fontSize=10, bulletAnchor ='start', bulletFontName ='I', bulletFontSize = 10, bulletIndent = 10, leading=14, spaceAfter=20 ))
    styles.add(ParagraphStyle(name='Equations',
               fontName='Times-Roman', fontSize=12, alignment=TA_CENTER, leading=14, spaceAfter=15, spaceBefore=15))

    frame0 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width, doc.height, id='encabezado')

    frame1_1 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col1')

    frame2_1 = Frame(doc.leftMargin+doc.width/2+4, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col2')

    story = []
    story.append(NextPageTemplate('cabeza'))
    story.append(Paragraph(titulo, styles['Titulos']))
    story.append(Spacer(0,20))
    story.append(Paragraph("""Universidad de San Carlos de Guatemala, Facultad de Ingenieria, Escuela de Ciencias y Sistemas, Organizacion computacional y lenguajes 2""", styles['Subtitulo']))


    story.append(NextPageTemplate('cuerpo'))
    story.append(PageBreak())
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Regresion Polinomial", styles['Subtitulo']))
    story.append(Paragraph(""" El análisis de regresión engloba a un conjunto de métodos estadísticos que usamos cuando tanto la variable de respuesta como las variables predictivas son contínuas y queremos predecir valores de la primera en función de valores observados de las segundas. En esencia, el análisis de regresión consiste en ajustar un modelo a los datos, estimando coeficientes a partir de las observaciones, con el fin de predecir valores de la variable de respuesa a partir de una (regresión simple) o más variables (regresión múltiple) predictivas o explicativas. """, styles['Cuerpo']))
    story.append(
        Paragraph("Con el uso de una regresion polinomial se usa una variable de respuesta cuantitativa a partir de una variable predictora cuantitativa, donde la relacion se modela como una funcion polinomial de orden n", styles['Cuerpo']))
    story.append(
        Paragraph("Usamos los modelos para estimar el valor promedio de la variable de respuesta en función de parámetros estimados de los datos. De manera general, podemos predecir valores de la variable de respuesta usando esta fórmula:", styles['Cuerpo']))
    story.append(Paragraph(
        """Equation : estima<sub>i</sub> = (modelo) +  error<sub>i</sub>""", styles['Equations']))
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Analisis de la data", styles['Subtitulo']))
    story.append(
        Paragraph("Para el modelo actual se realizo el analisis descriptivo, con el cual podremos llegar a un compromiso óptimo entre realismo del modelo, grado de ajuste del modelo a los datos, y mínima varianza de la estima.", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[0], width=200, height=150))
    story.append(
        Paragraph(f"Con los parametros de entrada tenemos como variable independiente: {datos['inde']} y como variable dependiente: {datos['depe']}", styles['Cuerpo']))
    story.append(
        Paragraph("Con los que hace el analsis de progresion polinomial de grado 4", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[1], width=200, height=150))
    story.append(
        Paragraph("Un outlier es una observación anormal y extrema en una muestra estadística o serie temporal de datos que puede afectar potencialmente a la estimación de los parámetros del mismo. Por lo que hay que estar pendientes de ellos y analizar su comportamiento, para la muestra de nuestro datos se encuentran: ", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[2], width=200, height=150))
    story.append(
        Paragraph("El cálculo de la correlación entre dos variables es independiente del orden o asignación de cada variable a X e Y, mide únicamente la relación entre ambas sin considerar dependencias. Como en el caso de nuestros datos: ", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[3], width=200, height=150))
    story.append(
        Paragraph("""Lo que hemos visto hasta ahora es sólo la “mitad de la historia”. Además de los parámetros a y b, necesitamos calcular la incertidumbre asociada a cada una de estas estimas. Es decir, necesitamos calcular el error estándar de cada parámetro de nuestro modelo de regresión. El error cuadrado desviacion media  (RMSE
) de la distribución de muestreo de nustra data. El cual nos indica cuánta variación existe entre muestras.""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[4], width=200, height=150))
    story.append(
        Paragraph(f"""Con el estudio previo del RMSE ya se puede ver el mejor grado que se acopla a la muestra de nuestros datos por lo que podemos dar un analisis mas preciso, que nos da como resultado un grado {datos['grado']} y una regresion:""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[5], width=200, height=150))
    story.append(PageBreak())

    doc.addPageTemplates([
        PageTemplate(id='cabeza', frames=[
            frame0]),
        PageTemplate(id='cuerpo', frames=[
            frame1_1, frame2_1]),
    ])

    doc.build(story)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=nombre)

def reporte_prediccion1(titulo,nombre,graficas, datos):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    doc = BaseDocTemplate(buffer, showBoundary=0, pagesizes=A4)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Titulos',
               fontName='Times-Roman', fontSize=20,alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Cuerpo',
               fontName='Times-Roman', fontSize=10, alignment=TA_JUSTIFY, leading=14))
    styles.add(ParagraphStyle(name='Subtitulo',
               fontName='Times-Roman', fontSize=10, bulletAnchor ='start', bulletFontName ='I', bulletFontSize = 10, bulletIndent = 10, leading=14, spaceAfter=20 ))
    styles.add(ParagraphStyle(name='Equations',
               fontName='Times-Roman', fontSize=12, alignment=TA_CENTER, leading=14, spaceAfter=15, spaceBefore=15))

    frame0 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width, doc.height, id='encabezado')

    frame1_1 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col1')

    frame2_1 = Frame(doc.leftMargin+doc.width/2+4, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col2')

    story = []
    story.append(NextPageTemplate('cabeza'))
    story.append(Paragraph(titulo, styles['Titulos']))
    story.append(Spacer(0,20))
    story.append(Paragraph("""Universidad de San Carlos de Guatemala, Facultad de Ingenieria, Escuela de Ciencias y Sistemas, Organizacion computacional y lenguajes 2""", styles['Subtitulo']))


    story.append(NextPageTemplate('cuerpo'))
    story.append(PageBreak())
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Regresion Polinomial", styles['Subtitulo']))
    story.append(Paragraph(""" El análisis de regresión engloba a un conjunto de métodos estadísticos que usamos cuando tanto la variable de respuesta como las variables predictivas son contínuas y queremos predecir valores de la primera en función de valores observados de las segundas. En esencia, el análisis de regresión consiste en ajustar un modelo a los datos, estimando coeficientes a partir de las observaciones, con el fin de predecir valores de la variable de respuesa a partir de una (regresión simple) o más variables (regresión múltiple) predictivas o explicativas. """, styles['Cuerpo']))
    story.append(
        Paragraph("Con el uso de una regresion polinomial se usa una variable de respuesta cuantitativa a partir de una variable predictora cuantitativa, donde la relacion se modela como una funcion polinomial de orden n", styles['Cuerpo']))
    story.append(
        Paragraph("Usamos los modelos para estimar el valor promedio de la variable de respuesta en función de parámetros estimados de los datos. De manera general, podemos predecir valores de la variable de respuesta usando esta fórmula:", styles['Cuerpo']))
    story.append(Paragraph(
        """Equation : estima<sub>i</sub> = (modelo) +  error<sub>i</sub>""", styles['Equations']))
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Analisis de la data", styles['Subtitulo']))
    story.append(
        Paragraph("Para el modelo actual se realizo el analisis descriptivo, con el cual podremos llegar a un compromiso óptimo entre realismo del modelo, grado de ajuste del modelo a los datos, y mínima varianza de la estima.", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[0], width=200, height=150))
    story.append(
        Paragraph(f"Con los parametros de entrada tenemos como variable independiente: {datos['inde']} y como variable dependiente: {datos['depe']}", styles['Cuerpo']))
    story.append(
        Paragraph("Con los que hace el analsis de progresion polinomial de grado 4", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[1], width=200, height=150))
    story.append(
        Paragraph(f"Ya con el modelo entrenado se procede a realizar la prediccion que nos da un resultado de {datos['resultado']}.", styles['Cuerpo']))
    story.append(
        Paragraph("Con los que hace el analsis de prediccion de una progresion polinomial de grado 4", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[2], width=200, height=150))
    story.append(
        Paragraph("Un outlier es una observación anormal y extrema en una muestra estadística o serie temporal de datos que puede afectar potencialmente a la estimación de los parámetros del mismo. Por lo que hay que estar pendientes de ellos y analizar su comportamiento, para la muestra de nuestro datos se encuentran: ", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[3], width=200, height=150))
    story.append(
        Paragraph("El cálculo de la correlación entre dos variables es independiente del orden o asignación de cada variable a X e Y, mide únicamente la relación entre ambas sin considerar dependencias. Como en el caso de nuestros datos: ", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[4], width=200, height=150))
    story.append(
        Paragraph("""Lo que hemos visto hasta ahora es sólo la “mitad de la historia”. Además de los parámetros a y b, necesitamos calcular la incertidumbre asociada a cada una de estas estimas. Es decir, necesitamos calcular el error estándar de cada parámetro de nuestro modelo de regresión. El error cuadrado desviacion media  (RMSE
) de la distribución de muestreo de nustra data. El cual nos indica cuánta variación existe entre muestras.""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[5], width=200, height=150))
    story.append(
        Paragraph(f"""Con el estudio previo del RMSE ya se puede ver el mejor grado que se acopla a la muestra de nuestros datos por lo que podemos dar un analisis mas preciso, que nos da como resultado un grado {datos['grado']} y una prediccion de regresion:""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[6], width=200, height=150))
    story.append(PageBreak())

    doc.addPageTemplates([
        PageTemplate(id='cabeza', frames=[
            frame0]),
        PageTemplate(id='cuerpo', frames=[
            frame1_1, frame2_1]),
    ])

def reporte_prediccion2(titulo,nombre,graficas,graficas2, datos,datos2):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    doc = BaseDocTemplate(buffer, showBoundary=0, pagesizes=A4)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Titulos',
               fontName='Times-Roman', fontSize=20,alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Cuerpo',
               fontName='Times-Roman', fontSize=10, alignment=TA_JUSTIFY, leading=14))
    styles.add(ParagraphStyle(name='Subtitulo',
               fontName='Times-Roman', fontSize=10, bulletAnchor ='start', bulletFontName ='I', bulletFontSize = 10, bulletIndent = 10, leading=14, spaceAfter=20 ))
    styles.add(ParagraphStyle(name='Equations',
               fontName='Times-Roman', fontSize=12, alignment=TA_CENTER, leading=14, spaceAfter=15, spaceBefore=15))

    frame0 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width, doc.height, id='encabezado')

    frame1_1 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col1')

    frame2_1 = Frame(doc.leftMargin+doc.width/2+4, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col2')

    story = []
    story.append(NextPageTemplate('cabeza'))
    story.append(Paragraph(titulo, styles['Titulos']))
    story.append(Spacer(0,20))
    story.append(Paragraph("""Universidad de San Carlos de Guatemala, Facultad de Ingenieria, Escuela de Ciencias y Sistemas, Organizacion computacional y lenguajes 2""", styles['Subtitulo']))


    story.append(NextPageTemplate('cuerpo'))
    story.append(PageBreak())
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Regresion Polinomial", styles['Subtitulo']))
    story.append(Paragraph(""" El análisis de regresión engloba a un conjunto de métodos estadísticos que usamos cuando tanto la variable de respuesta como las variables predictivas son contínuas y queremos predecir valores de la primera en función de valores observados de las segundas. En esencia, el análisis de regresión consiste en ajustar un modelo a los datos, estimando coeficientes a partir de las observaciones, con el fin de predecir valores de la variable de respuesa a partir de una (regresión simple) o más variables (regresión múltiple) predictivas o explicativas. """, styles['Cuerpo']))
    story.append(
        Paragraph("Con el uso de una regresion polinomial se usa una variable de respuesta cuantitativa a partir de una variable predictora cuantitativa, donde la relacion se modela como una funcion polinomial de orden n", styles['Cuerpo']))
    story.append(
        Paragraph("Usamos los modelos para estimar el valor promedio de la variable de respuesta en función de parámetros estimados de los datos. De manera general, podemos predecir valores de la variable de respuesta usando esta fórmula:", styles['Cuerpo']))
    story.append(Paragraph(
        """Equation : estima<sub>i</sub> = (modelo) +  error<sub>i</sub>""", styles['Equations']))
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Analisis de la data", styles['Subtitulo']))
    story.append(
        Paragraph("El analisis de esta prediccion se lleva acabo una por medio de los casos y otra por medio de las muertes por lo que contamos con el siguiente resultado:", styles['Cuerpo']))    
    story.append(
        Paragraph(f"Para el modelo actual se realizo el analisis descriptivo de la data compuesta por {datos['depe']}, con el cual podremos llegar a un compromiso óptimo entre realismo del modelo, grado de ajuste del modelo a los datos, y mínima varianza de la estima.", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[0], width=200, height=150))
    story.append(
        Paragraph(f"Para el modelo actual se realizo el analisis descriptivo de la data compuesta por {datos2['depe']}, con el cual podremos llegar a un compromiso óptimo entre realismo del modelo, grado de ajuste del modelo a los datos, y mínima varianza de la estima.", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas2[0], width=200, height=150))
    story.append(
        Paragraph(f"Con los parametros de entrada para el analisis de los casos tenemos como variable independiente: {datos['inde']} y como variable dependiente: {datos['depe']}", styles['Cuerpo']))
    story.append(
        Paragraph("Con los que hace el analsis de progresion polinomial de grado 4", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[1], width=200, height=150))
    story.append(
        Paragraph(f"Con los parametros de entrada para el analisis de las muertes tenemos como variable independiente: {datos2['inde']} y como variable dependiente: {datos2['depe']}", styles['Cuerpo']))
    story.append(
        Paragraph("Con los que hace el analsis de progresion polinomial de grado 4", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas2[1], width=200, height=150))
    story.append(
        Paragraph(f"Ya con el modelo entrenado se procede a realizar la prediccion que nos da un resultado de {datos['resultado']} para los casos.", styles['Cuerpo']))
    story.append(
        Paragraph("Con los que hace el analsis de prediccion de una progresion polinomial de grado 4", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[2], width=200, height=150))
    story.append(
        Paragraph(f"Y para las muertes nos da un resultado de {datos2['resultado']} para los casos.", styles['Cuerpo']))
    story.append(
        Paragraph("Con los que hace el analsis de prediccion de una progresion polinomial de grado 4", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas2[2], width=200, height=150))
    story.append(
        Paragraph("Un outlier es una observación anormal y extrema en una muestra estadística o serie temporal de datos que puede afectar potencialmente a la estimación de los parámetros del mismo. Por lo que hay que estar pendientes de ellos y analizar su comportamiento, para la muestra de nuestro datos se encuentran: ", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[3], width=200, height=150))
    story.append(Image("data:image/png;base64," +
                    graficas2[3], width=200, height=150))
    story.append(
        Paragraph("El cálculo de la correlación entre dos variables es independiente del orden o asignación de cada variable a X e Y, mide únicamente la relación entre ambas sin considerar dependencias. Como en el caso de nuestros datos: ", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[4], width=200, height=150))
    story.append(Image("data:image/png;base64," +
                    graficas2[4], width=200, height=150))
    story.append(
        Paragraph("""Lo que hemos visto hasta ahora es sólo la “mitad de la historia”. Además de los parámetros a y b, necesitamos calcular la incertidumbre asociada a cada una de estas estimas. Es decir, necesitamos calcular el error estándar de cada parámetro de nuestro modelo de regresión. El error cuadrado desviacion media  (RMSE
) de la distribución de muestreo de nustra data. El cual nos indica cuánta variación existe entre muestras.""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[5], width=200, height=150))
    story.append(Image("data:image/png;base64," +
                    graficas2[5], width=200, height=150))
    story.append(
        Paragraph(f"""Con el estudio previo del RMSE ya se puede ver el mejor grado que se acopla a la muestra de nuestros datos por lo que podemos dar un analisis mas preciso, que nos da como resultado un grado {datos['grado']} y una prediccion de regresion:""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[6], width=200, height=150))
    story.append(
        Paragraph(f"""Y como resultado de muertes tenemos un grado {datos2['grado']} y una prediccion de regresion:""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas2[6], width=200, height=150))
    story.append(PageBreak())

    doc.addPageTemplates([
        PageTemplate(id='cabeza', frames=[
            frame0]),
        PageTemplate(id='cuerpo', frames=[
            frame1_1, frame2_1]),
    ])

    doc.build(story)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=nombre)


def reporte_analisis1(titulo,nombre,graficas, datos):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    doc = BaseDocTemplate(buffer, showBoundary=0, pagesizes=A4)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Titulos',
               fontName='Times-Roman', fontSize=20,alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Cuerpo',
               fontName='Times-Roman', fontSize=10, alignment=TA_JUSTIFY, leading=14))
    styles.add(ParagraphStyle(name='Subtitulo',
               fontName='Times-Roman', fontSize=10, bulletAnchor ='start', bulletFontName ='I', bulletFontSize = 10, bulletIndent = 10, leading=14, spaceAfter=20 ))
    styles.add(ParagraphStyle(name='Equations',
               fontName='Times-Roman', fontSize=12, alignment=TA_CENTER, leading=14, spaceAfter=15, spaceBefore=15))

    frame0 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width, doc.height, id='encabezado')

    frame1_1 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col1')

    frame2_1 = Frame(doc.leftMargin+doc.width/2+4, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col2')

    story = []
    story.append(NextPageTemplate('cabeza'))
    story.append(Paragraph(titulo, styles['Titulos']))
    story.append(Spacer(0,20))
    story.append(Paragraph("""Universidad de San Carlos de Guatemala, Facultad de Ingenieria, Escuela de Ciencias y Sistemas, Organizacion computacional y lenguajes 2""", styles['Subtitulo']))


    story.append(NextPageTemplate('cuerpo'))
    story.append(PageBreak())
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Regresion Polinomial", styles['Subtitulo']))
    story.append(Paragraph(""" El análisis de regresión engloba a un conjunto de métodos estadísticos que usamos cuando tanto la variable de respuesta como las variables predictivas son contínuas y queremos predecir valores de la primera en función de valores observados de las segundas. En esencia, el análisis de regresión consiste en ajustar un modelo a los datos, estimando coeficientes a partir de las observaciones, con el fin de predecir valores de la variable de respuesa a partir de una (regresión simple) o más variables (regresión múltiple) predictivas o explicativas. """, styles['Cuerpo']))
    story.append(
        Paragraph("Con el uso de una regresion polinomial se usa una variable de respuesta cuantitativa a partir de una variable predictora cuantitativa, donde la relacion se modela como una funcion polinomial de orden n", styles['Cuerpo']))
    story.append(
        Paragraph("Usamos los modelos para estimar el valor promedio de la variable de respuesta en función de parámetros estimados de los datos. De manera general, podemos predecir valores de la variable de respuesta usando esta fórmula:", styles['Cuerpo']))
    story.append(Paragraph(
        """Equation : estima<sub>i</sub> = (modelo) +  error<sub>i</sub>""", styles['Equations']))
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Analisis de la data", styles['Subtitulo']))
    story.append(
        Paragraph(f"El analisis predictivo se lleva acabo una por medio de la comparacion de dos paises {datos['filtrado']} y {datos['filtrado2']}", styles['Cuerpo']))    
    story.append(
        Paragraph(f"Para el modelo actual se realizo el analisis descriptivo de la data compuesta por {datos['depe']}, con el cual podremos llegar a un compromiso óptimo entre realismo del modelo, grado de ajuste del modelo a los datos, y mínima varianza de la estima.", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[0], width=200, height=150))
    story.append(Image("data:image/png;base64," +
                    graficas[1], width=200, height=150))
    story.append(
        Paragraph(f"Con los parametros de entrada para el analisis de los casos tenemos como variable independiente: {datos['inde']} y como variable dependiente: {datos['depe']}", styles['Cuerpo']))
    story.append(
        Paragraph("Con los que hace el analsis de progresion polinomial de grado 4", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[2], width=200, height=150))
    story.append(Image("data:image/png;base64," +
                    graficas[3], width=200, height=150))
    story.append(
        Paragraph("Para comparar las datas", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[4], width=200, height=150))
    story.append(
        Paragraph("Un outlier es una observación anormal y extrema en una muestra estadística o serie temporal de datos que puede afectar potencialmente a la estimación de los parámetros del mismo. Por lo que hay que estar pendientes de ellos y analizar su comportamiento, para la muestra de nuestro datos se encuentran: ", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[5], width=200, height=150))
    story.append(Image("data:image/png;base64," +
                    graficas[6], width=200, height=150))
    story.append(
        Paragraph("El cálculo de la correlación entre dos variables es independiente del orden o asignación de cada variable a X e Y, mide únicamente la relación entre ambas sin considerar dependencias. Como en el caso de nuestros datos: ", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[7], width=200, height=150))
    story.append(Image("data:image/png;base64," +
                    graficas[8], width=200, height=150))
    story.append(
        Paragraph("""Lo que hemos visto hasta ahora es sólo la “mitad de la historia”. Además de los parámetros a y b, necesitamos calcular la incertidumbre asociada a cada una de estas estimas. Es decir, necesitamos calcular el error estándar de cada parámetro de nuestro modelo de regresión. El error cuadrado desviacion media  (RMSE
) de la distribución de muestreo de nustra data. El cual nos indica cuánta variación existe entre muestras.""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[9], width=200, height=150))
    story.append(
        Paragraph(f"""Y como resultado de muertes tenemos un grado {datos['grado']} y {datos['grado2']}, teniendo asi una regresion:""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[10], width=200, height=150))
    story.append(PageBreak())

    doc.addPageTemplates([
        PageTemplate(id='cabeza', frames=[
            frame0]),
        PageTemplate(id='cuerpo', frames=[
            frame1_1, frame2_1]),
    ])

    doc.build(story)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=nombre)

def reporte_analisis2(titulo,nombre,graficas, datos):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    doc = BaseDocTemplate(buffer, showBoundary=0, pagesizes=A4)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Titulos',
               fontName='Times-Roman', fontSize=20,alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Cuerpo',
               fontName='Times-Roman', fontSize=10, alignment=TA_JUSTIFY, leading=14))
    styles.add(ParagraphStyle(name='Subtitulo',
               fontName='Times-Roman', fontSize=10, bulletAnchor ='start', bulletFontName ='I', bulletFontSize = 10, bulletIndent = 10, leading=14, spaceAfter=20 ))
    styles.add(ParagraphStyle(name='Equations',
               fontName='Times-Roman', fontSize=12, alignment=TA_CENTER, leading=14, spaceAfter=15, spaceBefore=15))

    frame0 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width, doc.height, id='encabezado')

    frame1_1 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col1')

    frame2_1 = Frame(doc.leftMargin+doc.width/2+4, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col2')

    story = []
    story.append(NextPageTemplate('cabeza'))
    story.append(Paragraph(titulo, styles['Titulos']))
    story.append(Spacer(0,20))
    story.append(Paragraph("""Universidad de San Carlos de Guatemala, Facultad de Ingenieria, Escuela de Ciencias y Sistemas, Organizacion computacional y lenguajes 2""", styles['Subtitulo']))


    story.append(NextPageTemplate('cuerpo'))
    story.append(PageBreak())
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Regresion Polinomial", styles['Subtitulo']))
    story.append(Paragraph(""" El análisis de regresión engloba a un conjunto de métodos estadísticos que usamos cuando tanto la variable de respuesta como las variables predictivas son contínuas y queremos predecir valores de la primera en función de valores observados de las segundas. En esencia, el análisis de regresión consiste en ajustar un modelo a los datos, estimando coeficientes a partir de las observaciones, con el fin de predecir valores de la variable de respuesa a partir de una (regresión simple) o más variables (regresión múltiple) predictivas o explicativas. """, styles['Cuerpo']))
    story.append(
        Paragraph("Con el uso de una regresion polinomial se usa una variable de respuesta cuantitativa a partir de una variable predictora cuantitativa, donde la relacion se modela como una funcion polinomial de orden n", styles['Cuerpo']))
    story.append(
        Paragraph("Usamos los modelos para estimar el valor promedio de la variable de respuesta en función de parámetros estimados de los datos. De manera general, podemos predecir valores de la variable de respuesta usando esta fórmula:", styles['Cuerpo']))
    story.append(Paragraph(
        """Equation : estima<sub>i</sub> = (modelo) +  error<sub>i</sub>""", styles['Equations']))
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Analisis de la data", styles['Subtitulo']))
    story.append(
        Paragraph(f"El analisis predictivo se lleva acabo una por medio de la comparacion entre {datos['pais']}.", styles['Cuerpo']))    
    story.append(
        Paragraph(f"Con los parametros de entrada para el analisis de los casos tenemos como variable independiente: {datos['inde']} y como variable dependiente: {datos['depe']}", styles['Cuerpo']))
    story.append(
        Paragraph("Con los que hace el analsis de progresion polinomial de grado 4", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[0], width=200, height=150))
    story.append(
        Paragraph("""Lo que hemos visto hasta ahora es sólo la “mitad de la historia”. Además de los parámetros a y b, necesitamos calcular la incertidumbre asociada a cada una de estas estimas. Es decir, necesitamos calcular el error estándar de cada parámetro de nuestro modelo de regresión. El error cuadrado desviacion media  (RMSE
) de la distribución de muestreo de nustra data. El cual nos indica cuánta variación existe entre muestras.""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[1], width=200, height=150))
    story.append(
        Paragraph(f"""Y como resultado tenemos grados de {datos['grado']}, teniendo asi una regresion:""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[2], width=200, height=150))
    story.append(PageBreak())

    doc.addPageTemplates([
        PageTemplate(id='cabeza', frames=[
            frame0]),
        PageTemplate(id='cuerpo', frames=[
            frame1_1, frame2_1]),
    ])

    doc.build(story)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=nombre)

def reporte_comparacion(titulo,nombre,graficas,graficas2, datos,datos2):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    doc = BaseDocTemplate(buffer, showBoundary=0, pagesizes=A4)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Titulos',
               fontName='Times-Roman', fontSize=20,alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Cuerpo',
               fontName='Times-Roman', fontSize=10, alignment=TA_JUSTIFY, leading=14))
    styles.add(ParagraphStyle(name='Subtitulo',
               fontName='Times-Roman', fontSize=10, bulletAnchor ='start', bulletFontName ='I', bulletFontSize = 10, bulletIndent = 10, leading=14, spaceAfter=20 ))
    styles.add(ParagraphStyle(name='Equations',
               fontName='Times-Roman', fontSize=12, alignment=TA_CENTER, leading=14, spaceAfter=15, spaceBefore=15))

    frame0 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width, doc.height, id='encabezado')

    frame1_1 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col1')

    frame2_1 = Frame(doc.leftMargin+doc.width/2+4, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col2')

    story = []
    story.append(NextPageTemplate('cabeza'))
    story.append(Paragraph(titulo, styles['Titulos']))
    story.append(Spacer(0,20))
    story.append(Paragraph("""Universidad de San Carlos de Guatemala, Facultad de Ingenieria, Escuela de Ciencias y Sistemas, Organizacion computacional y lenguajes 2""", styles['Subtitulo']))


    story.append(NextPageTemplate('cuerpo'))
    story.append(PageBreak())
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Regresion Polinomial", styles['Subtitulo']))
    story.append(Paragraph(""" El análisis de regresión engloba a un conjunto de métodos estadísticos que usamos cuando tanto la variable de respuesta como las variables predictivas son contínuas y queremos predecir valores de la primera en función de valores observados de las segundas. En esencia, el análisis de regresión consiste en ajustar un modelo a los datos, estimando coeficientes a partir de las observaciones, con el fin de predecir valores de la variable de respuesa a partir de una (regresión simple) o más variables (regresión múltiple) predictivas o explicativas. """, styles['Cuerpo']))
    story.append(
        Paragraph("Con el uso de una regresion polinomial se usa una variable de respuesta cuantitativa a partir de una variable predictora cuantitativa, donde la relacion se modela como una funcion polinomial de orden n", styles['Cuerpo']))
    story.append(
        Paragraph("Usamos los modelos para estimar el valor promedio de la variable de respuesta en función de parámetros estimados de los datos. De manera general, podemos predecir valores de la variable de respuesta usando esta fórmula:", styles['Cuerpo']))
    story.append(Paragraph(
        """Equation : estima<sub>i</sub> = (modelo) +  error<sub>i</sub>""", styles['Equations']))
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Analisis de la data", styles['Subtitulo']))
    story.append(
        Paragraph("El analisis de esta prediccion se lleva acabo una por medio de los casos y otra por medio de las muertes por lo que contamos con el siguiente resultado:", styles['Cuerpo']))    
    story.append(
        Paragraph(f"Para el modelo actual se realizo el analisis descriptivo de la data compuesta por {datos['depe']}, con el cual podremos llegar a un compromiso óptimo entre realismo del modelo, grado de ajuste del modelo a los datos, y mínima varianza de la estima.", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[0], width=200, height=150))
    story.append(
        Paragraph(f"Para el modelo actual se realizo el analisis descriptivo de la data compuesta por {datos2['depe']}, con el cual podremos llegar a un compromiso óptimo entre realismo del modelo, grado de ajuste del modelo a los datos, y mínima varianza de la estima.", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas2[0], width=200, height=150))
    story.append(
        Paragraph(f"Con los parametros de entrada para el analisis de los casos tenemos como variable independiente: {datos['inde']} y como variable dependiente: {datos['depe']}", styles['Cuerpo']))
    story.append(
        Paragraph("Con los que hace el analsis de progresion polinomial de grado 4", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[1], width=200, height=150))
    story.append(
        Paragraph(f"Con los parametros de entrada para el analisis de las muertes tenemos como variable independiente: {datos2['inde']} y como variable dependiente: {datos2['depe']}", styles['Cuerpo']))
    story.append(
        Paragraph("Con los que hace el analsis de progresion polinomial de grado 4", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas2[1], width=200, height=150))
    story.append(
        Paragraph("Un outlier es una observación anormal y extrema en una muestra estadística o serie temporal de datos que puede afectar potencialmente a la estimación de los parámetros del mismo. Por lo que hay que estar pendientes de ellos y analizar su comportamiento, para la muestra de nuestro datos se encuentran: ", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[2], width=200, height=150))
    story.append(Image("data:image/png;base64," +
                    graficas2[2], width=200, height=150))
    story.append(
        Paragraph("El cálculo de la correlación entre dos variables es independiente del orden o asignación de cada variable a X e Y, mide únicamente la relación entre ambas sin considerar dependencias. Como en el caso de nuestros datos: ", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[3], width=200, height=150))
    story.append(Image("data:image/png;base64," +
                    graficas2[3], width=200, height=150))
    story.append(
        Paragraph("""Lo que hemos visto hasta ahora es sólo la “mitad de la historia”. Además de los parámetros a y b, necesitamos calcular la incertidumbre asociada a cada una de estas estimas. Es decir, necesitamos calcular el error estándar de cada parámetro de nuestro modelo de regresión. El error cuadrado desviacion media  (RMSE
) de la distribución de muestreo de nustra data. El cual nos indica cuánta variación existe entre muestras.""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[4], width=200, height=150))
    story.append(Image("data:image/png;base64," +
                    graficas2[4], width=200, height=150))
    story.append(
        Paragraph(f"""Con el estudio previo del RMSE ya se puede ver el mejor grado que se acopla a la muestra de nuestros datos por lo que podemos dar un analisis mas preciso, que nos da como resultado un grado {datos['grado']} y una prediccion de regresion:""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[5], width=200, height=150))
    story.append(
        Paragraph(f"""Y como resultado de pruebas tenemos un grado {datos2['grado']} y una prediccion de regresion:""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas2[5], width=200, height=150))
    story.append(PageBreak())

    doc.addPageTemplates([
        PageTemplate(id='cabeza', frames=[
            frame0]),
        PageTemplate(id='cuerpo', frames=[
            frame1_1, frame2_1]),
    ])

    doc.build(story)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=nombre)

def reporte_muertes1(titulo,nombre,graficas, datos):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    doc = BaseDocTemplate(buffer, showBoundary=0, pagesizes=A4)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Titulos',
               fontName='Times-Roman', fontSize=20,alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Cuerpo',
               fontName='Times-Roman', fontSize=10, alignment=TA_JUSTIFY, leading=14))
    styles.add(ParagraphStyle(name='Subtitulo',
               fontName='Times-Roman', fontSize=10, bulletAnchor ='start', bulletFontName ='I', bulletFontSize = 10, bulletIndent = 10, leading=14, spaceAfter=20 ))
    styles.add(ParagraphStyle(name='Equations',
               fontName='Times-Roman', fontSize=12, alignment=TA_CENTER, leading=14, spaceAfter=15, spaceBefore=15))

    frame0 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width, doc.height, id='encabezado')

    frame1_1 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col1')

    frame2_1 = Frame(doc.leftMargin+doc.width/2+4, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col2')

    story = []
    story.append(NextPageTemplate('cabeza'))
    story.append(Paragraph(titulo, styles['Titulos']))
    story.append(Spacer(0,20))
    story.append(Paragraph("""Universidad de San Carlos de Guatemala, Facultad de Ingenieria, Escuela de Ciencias y Sistemas, Organizacion computacional y lenguajes 2""", styles['Subtitulo']))


    story.append(NextPageTemplate('cuerpo'))
    story.append(PageBreak())
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Analisis de la data", styles['Subtitulo']))
    story.append(
        Paragraph(f"El analisis predictivo se lleva acabo una por medio de la comparacion entre {datos['filtrado']}.", styles['Cuerpo']))
    story.append(
        Paragraph(f"Con los parametros de entrada para el analisis de los casos tenemos como variable independiente: {datos['inde']} y como variable dependiente: {datos['depe']}", styles['Cuerpo']))
    story.append(
        Paragraph("Con los que hace el analsis de datos:", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[0], width=200, height=150))
    story.append(
        Paragraph("""Muestra los datos usando varias barras de la misma anchura, cada una de las cuales representa una categoría concreta. La altura de cada barra es proporcional a una agregación específica.""", styles['Cuerpo']))
    story.append(
        Paragraph(""" La principal característica del diagrama de barras es que se forman escaleras con las barras. Cuando vemos escaleras en un gráfico indica que estamos delante una variable discreta.""", styles['Cuerpo']))
    story.append(PageBreak())

    doc.addPageTemplates([
        PageTemplate(id='cabeza', frames=[
            frame0]),
        PageTemplate(id='cuerpo', frames=[
            frame1_1, frame2_1]),
    ])

    doc.build(story)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=nombre)

def reporte_muertes2(titulo,nombre,graficas, datos):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    doc = BaseDocTemplate(buffer, showBoundary=0, pagesizes=A4)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Titulos',
               fontName='Times-Roman', fontSize=20,alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Cuerpo',
               fontName='Times-Roman', fontSize=10, alignment=TA_JUSTIFY, leading=14))
    styles.add(ParagraphStyle(name='Subtitulo',
               fontName='Times-Roman', fontSize=10, bulletAnchor ='start', bulletFontName ='I', bulletFontSize = 10, bulletIndent = 10, leading=14, spaceAfter=20 ))
    styles.add(ParagraphStyle(name='Equations',
               fontName='Times-Roman', fontSize=12, alignment=TA_CENTER, leading=14, spaceAfter=15, spaceBefore=15))

    frame0 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width, doc.height, id='encabezado')

    frame1_1 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col1')

    frame2_1 = Frame(doc.leftMargin+doc.width/2+4, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col2')

    story = []
    story.append(NextPageTemplate('cabeza'))
    story.append(Paragraph(titulo, styles['Titulos']))
    story.append(Spacer(0,20))
    story.append(Paragraph("""Universidad de San Carlos de Guatemala, Facultad de Ingenieria, Escuela de Ciencias y Sistemas, Organizacion computacional y lenguajes 2""", styles['Subtitulo']))


    story.append(NextPageTemplate('cuerpo'))
    story.append(PageBreak())
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Analisis de la data", styles['Subtitulo']))
    story.append(
        Paragraph(f"El analisis predictivo se lleva acabo una por medio de la comparacion entre {datos['filtrado']}.", styles['Cuerpo']))
    story.append(
        Paragraph(f"Con los parametros de entrada para el analisis de los casos tenemos como variable independiente: {datos['inde']} y como variable dependiente: {datos['depe']}", styles['Cuerpo']))
    story.append(
        Paragraph("Con los que hace el analsis de datos:", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[0], width=200, height=150))
    story.append(
        Paragraph("""Cada valor del carácter estudiado corresponde a un sector. Las medidas de los ángulos de los sectores son proporcionales a los números representados (o a las frecuencias asociadas).""", styles['Cuerpo']))
    story.append(PageBreak())

    doc.addPageTemplates([
        PageTemplate(id='cabeza', frames=[
            frame0]),
        PageTemplate(id='cuerpo', frames=[
            frame1_1, frame2_1]),
    ])

    doc.build(story)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=nombre)

def reporte_tasas1(titulo,nombre,graficas, datos):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    doc = BaseDocTemplate(buffer, showBoundary=0, pagesizes=A4)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Titulos',
               fontName='Times-Roman', fontSize=20,alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Cuerpo',
               fontName='Times-Roman', fontSize=10, alignment=TA_JUSTIFY, leading=14))
    styles.add(ParagraphStyle(name='Subtitulo',
               fontName='Times-Roman', fontSize=10, bulletAnchor ='start', bulletFontName ='I', bulletFontSize = 10, bulletIndent = 10, leading=14, spaceAfter=20 ))
    styles.add(ParagraphStyle(name='Equations',
               fontName='Times-Roman', fontSize=12, alignment=TA_CENTER, leading=14, spaceAfter=15, spaceBefore=15))

    frame0 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width, doc.height, id='encabezado')

    frame1_1 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col1')

    frame2_1 = Frame(doc.leftMargin+doc.width/2+4, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col2')

    story = []
    story.append(NextPageTemplate('cabeza'))
    story.append(Paragraph(titulo, styles['Titulos']))
    story.append(Spacer(0,20))
    story.append(Paragraph("""Universidad de San Carlos de Guatemala, Facultad de Ingenieria, Escuela de Ciencias y Sistemas, Organizacion computacional y lenguajes 2""", styles['Subtitulo']))


    story.append(NextPageTemplate('cuerpo'))
    story.append(PageBreak())
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Regresion Polinomial", styles['Subtitulo']))
    story.append(Paragraph(""" El análisis de regresión engloba a un conjunto de métodos estadísticos que usamos cuando tanto la variable de respuesta como las variables predictivas son contínuas y queremos predecir valores de la primera en función de valores observados de las segundas. En esencia, el análisis de regresión consiste en ajustar un modelo a los datos, estimando coeficientes a partir de las observaciones, con el fin de predecir valores de la variable de respuesa a partir de una (regresión simple) o más variables (regresión múltiple) predictivas o explicativas. """, styles['Cuerpo']))
    story.append(
        Paragraph("Con el uso de una regresion polinomial se usa una variable de respuesta cuantitativa a partir de una variable predictora cuantitativa, donde la relacion se modela como una funcion polinomial de orden n", styles['Cuerpo']))
    story.append(
        Paragraph("Usamos los modelos para estimar el valor promedio de la variable de respuesta en función de parámetros estimados de los datos. De manera general, podemos predecir valores de la variable de respuesta usando esta fórmula:", styles['Cuerpo']))
    story.append(Paragraph(
        """Equation : estima<sub>i</sub> = (modelo) +  error<sub>i</sub>""", styles['Equations']))
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Analisis de la data", styles['Subtitulo']))
    story.append(
        Paragraph(f"Aquí estamos observando cual es el comportamiento entre variables.", styles['Cuerpo']))    
    story.append(
        Paragraph(f"Con los parametros de entrada para el analisis tenemos como variable independiente: {datos['inde']} y como variable dependiente: {datos['depe']} y {datos['depe2']}", styles['Cuerpo']))
    story.append(
        Paragraph("Con los que hace el analsis de progresion polinomial de grado 4", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[0], width=200, height=150))
    story.append(
        Paragraph("""Lo que hemos visto hasta ahora es sólo la “mitad de la historia”. Además de los parámetros a y b, necesitamos calcular la incertidumbre asociada a cada una de estas estimas. Es decir, necesitamos calcular el error estándar de cada parámetro de nuestro modelo de regresión. El error cuadrado desviacion media  (RMSE
) de la distribución de muestreo de nustra data. El cual nos indica cuánta variación existe entre muestras.""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[1], width=200, height=150))
    story.append(
        Paragraph(f"""Y como resultado tenemos grados de {datos['grado']} y {datos['grado2']}, teniendo asi una regresion:""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[2], width=200, height=150))
    story.append(PageBreak())

    doc.addPageTemplates([
        PageTemplate(id='cabeza', frames=[
            frame0]),
        PageTemplate(id='cuerpo', frames=[
            frame1_1, frame2_1]),
    ])

    doc.build(story)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=nombre)

def reporte_tasas2(titulo,nombre,graficas, datos):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    doc = BaseDocTemplate(buffer, showBoundary=0, pagesizes=A4)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Titulos',
               fontName='Times-Roman', fontSize=20,alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Cuerpo',
               fontName='Times-Roman', fontSize=10, alignment=TA_JUSTIFY, leading=14))
    styles.add(ParagraphStyle(name='Subtitulo',
               fontName='Times-Roman', fontSize=10, bulletAnchor ='start', bulletFontName ='I', bulletFontSize = 10, bulletIndent = 10, leading=14, spaceAfter=20 ))
    styles.add(ParagraphStyle(name='Equations',
               fontName='Times-Roman', fontSize=12, alignment=TA_CENTER, leading=14, spaceAfter=15, spaceBefore=15))

    frame0 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width, doc.height, id='encabezado')

    frame1_1 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col1')

    frame2_1 = Frame(doc.leftMargin+doc.width/2+4, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col2')

    story = []
    story.append(NextPageTemplate('cabeza'))
    story.append(Paragraph(titulo, styles['Titulos']))
    story.append(Spacer(0,20))
    story.append(Paragraph("""Universidad de San Carlos de Guatemala, Facultad de Ingenieria, Escuela de Ciencias y Sistemas, Organizacion computacional y lenguajes 2""", styles['Subtitulo']))


    story.append(NextPageTemplate('cuerpo'))
    story.append(PageBreak())
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Regresion Polinomial", styles['Subtitulo']))
    story.append(Paragraph(""" El análisis de regresión engloba a un conjunto de métodos estadísticos que usamos cuando tanto la variable de respuesta como las variables predictivas son contínuas y queremos predecir valores de la primera en función de valores observados de las segundas. En esencia, el análisis de regresión consiste en ajustar un modelo a los datos, estimando coeficientes a partir de las observaciones, con el fin de predecir valores de la variable de respuesa a partir de una (regresión simple) o más variables (regresión múltiple) predictivas o explicativas. """, styles['Cuerpo']))
    story.append(
        Paragraph("Con el uso de una regresion polinomial se usa una variable de respuesta cuantitativa a partir de una variable predictora cuantitativa, donde la relacion se modela como una funcion polinomial de orden n", styles['Cuerpo']))
    story.append(
        Paragraph("Usamos los modelos para estimar el valor promedio de la variable de respuesta en función de parámetros estimados de los datos. De manera general, podemos predecir valores de la variable de respuesta usando esta fórmula:", styles['Cuerpo']))
    story.append(Paragraph(
        """Equation : estima<sub>i</sub> = (modelo) +  error<sub>i</sub>""", styles['Equations']))
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Analisis de la data", styles['Subtitulo']))
    story.append(
        Paragraph(f"Aquí estamos observando cual es el comportamiento entre variables.", styles['Cuerpo']))
    story.append(
        Paragraph(f"Con los parametros de entrada para el analisis tenemos como variable independiente: {datos['inde']} y como variable dependiente: {datos['depe']}, {datos['depe2']} y {datos['depe3']}", styles['Cuerpo']))
    story.append(
        Paragraph("Con los que hace el analsis de progresion polinomial de grado 4", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[0], width=200, height=150))
    story.append(
        Paragraph("""Lo que hemos visto hasta ahora es sólo la “mitad de la historia”. Además de los parámetros a y b, necesitamos calcular la incertidumbre asociada a cada una de estas estimas. Es decir, necesitamos calcular el error estándar de cada parámetro de nuestro modelo de regresión. El error cuadrado desviacion media  (RMSE
) de la distribución de muestreo de nustra data. El cual nos indica cuánta variación existe entre muestras.""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[1], width=200, height=150))
    story.append(
        Paragraph(f"""Y como resultado tenemos grados de {datos['grado']}, {datos['grado2']} y {datos['grado3']}, teniendo asi una regresion:""", styles['Cuerpo']))
    story.append(Image("data:image/png;base64," +
                    graficas[2], width=200, height=150))
    story.append(PageBreak())

    doc.addPageTemplates([
        PageTemplate(id='cabeza', frames=[
            frame0]),
        PageTemplate(id='cuerpo', frames=[
            frame1_1, frame2_1]),
    ])

    doc.build(story)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=nombre)


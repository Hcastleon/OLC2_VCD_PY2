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
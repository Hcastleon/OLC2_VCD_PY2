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

def reporte_tendencia1(nombre,graficas, datos):
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
               fontName='Times-Roman', fontSize=14, alignment=TA_CENTER, leading=14, spaceAfter=15, spaceBefore=15))

    frame0 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width, doc.height, id='encabezado')

    # frame1 = Frame(doc.leftMargin, doc.bottomMargin-300,
    #                doc.width/2-4, doc.height-300, id='col1')

    # frame2 = Frame(doc.leftMargin+doc.width/2+4, doc.bottomMargin-300,
    #                doc.width/2-4, doc.height-300, id='col2')

    frame1_1 = Frame(doc.leftMargin, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col1')

    frame2_1 = Frame(doc.leftMargin+doc.width/2+4, doc.bottomMargin,
                   doc.width/2-4, doc.height, id='col2')

    story = []
    story.append(NextPageTemplate('cabeza'))
    story.append(Paragraph("Tendencia de la infección por Covid-19 en un País", styles['Titulos']))
    story.append(Spacer(0,20))
    story.append(Paragraph("""Universidad de San Carlos de Guatemala, Facultad de Ingenieria, Escuela de Ciencias y Sistemas, Organizacion computacional y lenguajes 2""", styles['Subtitulo']))


    story.append(NextPageTemplate('cuerpo'))
    story.append(PageBreak())
    story.append(
        Paragraph("<SEQ ID = 'spam' />. Modelo de regresión lineal simple", styles['Subtitulo']))
    story.append(Paragraph(""" Los modelos de regresión lineal son ampliamente usados en la ingeniería ya que sirven para analizar el
    comportamiento de las variables de entrada (o regresora) y salida (o respuesta) estableciendo predicciones y
    estimaciones [8]. En este trabajo la variable regresora corresponde a la distorsión armónica individual de corriente y
    la variable de respuesta corresponde a la distorsión armónica individual de tensión.
    La ecuación (3), muestra la representación de un modelo de regresión lineal simple, donde Y es la respuesta, X es la
    variable regresora, 0 y 1 son los parámetros del modelo o coeficientes de regresión y es el error del modelo""", styles['Cuerpo']))
    story.append(
        Paragraph("El coeficiente de determinación R2 se expresa como un porcentaje que indica la variación de los valores de la variable independiente que se puede explicar con la ecuación de regresión", styles['Cuerpo']))
    story.append(Paragraph(
        """Equation : Y = <greek>b</greek><sub>0</sub> + <greek>B</greek><sub>1</sub> X <greek>e</greek>""", styles['Equations']))
    story.append(Paragraph(
        """Equation (&alpha;): <greek>B</greek><sub>0</sub>+ <super><greek>ip</greek></super>  = -1""", styles['Equations']))
    story.append(Image("data:image/png;base64," +
                    graficas[0], width=200, height=150))
    story.append(Image("data:image/png;base64," +
                    graficas[1], width=200, height=150))
    story.append(Image("data:image/png;base64," +
                    graficas[2], width=200, height=150))
    story.append(Image("data:image/png;base64," +
                    graficas[3], width=200, height=150))
    story.append(Image("data:image/png;base64," +
                    graficas[4], width=200, height=150))
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
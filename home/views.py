from django.shortcuts import render
from django.contrib import messages

import pathlib
import logging
import csv
import json

import pandas as pd
from home.funciones.predicciones.prediccion1 import analisis2_p, analisis_p, analisis_year_p

from home.funciones.tendencias.Tendencia1 import analisis, analisis2
from home.reports import reporte_tendencia1

archivo = None
encabezados = []
diccionario = []
temporal = None
temporal2 = None
grafica = None
grafica2 = None
# Create your views here.
def home(request):
    return render(request,'index.html')
#servicess
def opencsv(request):
    return render(request,'opencsv.html')
def archivo(request):
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        global archivo, encabezados,diccionario
        diccionario = []
        archivo = request.FILES['formFile']
        nombrecito = archivo.name
        if pathlib.Path(nombrecito).suffix == '.csv':
            csvreader = archivo.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(csvreader)
            for row in csv_reader:
                for clave in list(row.keys()):
                    if clave is None:
                        del row[clave]
                diccionario.append(row)
            encabezados = diccionario[0].keys()
        elif pathlib.Path(nombrecito).suffix == '.xls' or pathlib.Path(nombrecito).suffix == '.xlsx':
            aux = pd.read_excel(archivo)
            diccionario = aux.to_dict('records')
            encabezados = diccionario[0].keys()
        elif pathlib.Path(nombrecito).suffix == '.json':
            diccionario = json.load(archivo)
            encabezados = diccionario[0].keys()
        else:
            messages.error(request, f"Cannot parse data with {pathlib.Path(nombrecito).suffix} file type")
            return render(request,'opencsv.html')
    messages.success(request, "The file was uploaded successfully")
    return render(request,'archivos.html',{'titulo':nombrecito, 'cabecera': encabezados, 'contenido' : diccionario})
#funciones
def funcion_1(request):
    seleccionados = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect','')
        tenind = request.POST.get('ten_independiente','')
        tenden = request.POST.get('ten_dependiente','')
        if pais_select != '' :
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Tendencia_infeccion.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if pais != '' and tenden != '' and tenind!='' and temporal != None:
                grafica =analisis(pais,tenind,tenden,diccionario,temporal)
            return render(request,'funciones/Tendencia_infeccion.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado']})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('Tendencia de la infección por Covid-19 en un País','TICovid19_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Tendencia_infeccion.html',{'cabecera':encabezados,'graph':''})

def funcion_2(request):
    seleccionados = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect','')
        tenind = request.POST.get('ten_independiente','')
        tenden = request.POST.get('ten_dependiente','')
        if pais_select != '' :
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Tendencia_infeccion_dia.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if pais != '' and tenden != '' and tenind!='' and temporal != None:
                grafica =analisis(pais,tenind,tenden,diccionario,temporal)
            return render(request,'funciones/Tendencia_infeccion_dia.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado']})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('Tendencia del número de infectados por día de un País','TIDia_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Tendencia_infeccion_dia.html',{'cabecera':encabezados,'graph':''})

def funcion_3(request):
    seleccionados = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect','')
        tenind = request.POST.get('ten_independiente','')
        tenden = request.POST.get('ten_dependiente','')
        if pais_select != '' :
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Tendencia_vacunacion.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if pais != '' and tenden != '' and tenind!='' and temporal != None:
                grafica =analisis(pais,tenind,tenden,diccionario,temporal)
            return render(request,'funciones/Tendencia_vacunacion.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado']})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('Tendencia de la vacunación de en un País','TV_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Tendencia_vacunacion.html',{'cabecera':encabezados,'graph':''})

def funcion_4(request):
    seleccionados = []
    seleccionados2 = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect1','')
        depa_select = request.POST.get('camposelect2','')
        pais = request.POST.get('paisselect','')
        depa = request.POST.get('depaselect','')
        tenind = request.POST.get('ten_independiente','')
        tenden = request.POST.get('ten_dependiente','')
        if pais_select != '' and depa_select != '' :
            global temporal, temporal2
            temporal = pais_select
            temporal2 = depa_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            for i in diccionario:
                for j in i:
                    if j == depa_select:
                        if not(i[j] in seleccionados2):
                            seleccionados2.append(i[j])
            return render(request,'funciones/Tendencia_casos.html',{'cabecera':encabezados, 'pais': seleccionados, 'depa': seleccionados2,'graph':''})
        else:
            if depa != '' and pais != '' and tenden != '' and tenind!='' and temporal != None:
                grafica =analisis2(pais,depa,tenind,tenden,diccionario,temporal,temporal2)
            return render(request,'funciones/Tendencia_casos.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado']})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('Tendencia de casos confirmados de Coronavirus en un departamento de un País','TCDepa_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Tendencia_casos.html',{'cabecera':encabezados,'graph':''})

def funcion_5(request):
    seleccionados = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect','')
        tenind = request.POST.get('ten_independiente','')
        tenden = request.POST.get('ten_dependiente','')
        regresion = request.POST.get('dato_regresion','')
        if pais_select != '':
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Prediccion_infectados.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if  pais != '' and tenden != '' and tenind!='' and temporal != None and regresion!='':
                grafica =analisis_p(pais,tenind,tenden,regresion,diccionario,temporal)
            return render(request,'funciones/Prediccion_infectados.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado'],'result':grafica['resultado']})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('TICovid19_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Prediccion_infectados.html',{'cabecera':encabezados,'graph':''})

def funcion_6(request):
    seleccionados = []
    seleccionados2 = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect1','')
        depa_select = request.POST.get('camposelect2','')
        pais = request.POST.get('paisselect','')
        depa = request.POST.get('depaselect','')
        tenind = request.POST.get('ten_independiente','')
        tenden = request.POST.get('ten_dependiente','')
        regresion = request.POST.get('dato_regresion','')
        if pais_select != '' and depa_select != '' :
            global temporal, temporal2
            temporal = pais_select
            temporal2 = depa_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            for i in diccionario:
                for j in i:
                    if j == depa_select:
                        if not(i[j] in seleccionados2):
                            seleccionados2.append(i[j])
            return render(request,'funciones/Prediccion_muertes_depa.html',{'cabecera':encabezados, 'pais': seleccionados, 'depa': seleccionados2,'graph':''})
        else:
            if depa != '' and pais != '' and tenden != '' and tenind!='' and temporal != None and regresion!='':
                grafica =analisis2_p(pais,depa,tenind,tenden,regresion,diccionario,temporal,temporal2)
            return render(request,'funciones/Prediccion_muertes_depa.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado'],'result':grafica['resultado']})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('TICovid19_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Prediccion_muertes_depa.html',{'cabecera':encabezados,'graph':''})

def funcion_7(request):
    seleccionados = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect','')
        tenind = request.POST.get('ten_independiente','')
        tenden = request.POST.get('ten_dependiente','')
        regresion = request.POST.get('dato_regresion','')
        if pais_select != '':
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Prediccion_muerte_pais.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if  pais != '' and tenden != '' and tenind!='' and temporal != None and regresion!='':
                grafica =analisis_p(pais,tenind,tenden,regresion,diccionario,temporal)
            return render(request,'funciones/Prediccion_muerte_pais.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado'],'result':grafica['resultado']})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('TICovid19_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Prediccion_muerte_pais.html',{'cabecera':encabezados,'graph':''})

def funcion_8(request):
    seleccionados = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect','')
        tenind = request.POST.get('ten_independiente','')
        tenden = request.POST.get('ten_dependiente','')
        regresion = request.POST.get('dato_regresion','')
        if pais_select != '':
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Prediccion_infectados_year.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if  pais != '' and tenden != '' and tenind!='' and temporal != None and regresion!='':
                grafica =analisis_p(pais,tenind,tenden,regresion,diccionario,temporal)
            return render(request,'funciones/Prediccion_infectados_year.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado'],'result':grafica['resultado']})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('TICovid19_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Prediccion_infectados_year.html',{'cabecera':encabezados,'graph':''})

def funcion_9(request):
    seleccionados = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect','')
        tenind = request.POST.get('ten_independiente','')
        tenden = request.POST.get('ten_dependiente','')
        regresion = request.POST.get('dato_regresion','')
        if pais_select != '':
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Prediccion_por_dia.html',{'cabecera':encabezados, 'data': seleccionados,'graph':''})
        else:
            if  pais != '' and tenden != '' and tenind!='' and temporal != None and regresion!='':
                grafica =analisis_p(pais,tenind,tenden,regresion,diccionario,temporal)
            return render(request,'funciones/Prediccion_por_dia.html',{'cabecera':encabezados, 'data': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado'],'result':grafica['resultado']})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('TICovid19_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Prediccion_por_dia.html',{'cabecera':encabezados,'graph':''})


def funcion_10(request):
    seleccionados = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect','')
        tenind = request.POST.get('ten_independiente','')
        tenden = request.POST.get('ten_dependiente','')
        if pais_select != '':
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Prediccion_year_dia.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if  pais != '' and tenden != '' and tenind!='' and temporal != None:
                grafica =analisis_year_p(pais,tenind,tenden,diccionario,temporal)
            return render(request,'funciones/Prediccion_year_dia.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado'],'result':grafica['resultado']})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('TICovid19_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Prediccion_year_dia.html',{'cabecera':encabezados,'graph':''})

def funcion_11(request):
    seleccionados = []
    global grafica,grafica2
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('dataselect','')
        tenind = request.POST.get('ten_independiente','')
        tenden = request.POST.get('ten_dependiente','')
        tenden2 = request.POST.get('ten_dependiente2','')
        regresion = request.POST.get('dato_regresion','0')
        if pais_select != '':
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Prediccion_casos_muertes.html',{'cabecera':encabezados, 'data': seleccionados,'graph':''})
        else:
            if  pais !='' and tenden != '' and tenind!='' and tenden2!='' and regresion!='':
                grafica =analisis_p(pais,tenind,tenden,regresion,diccionario,temporal)
                grafica2 =analisis_p(pais,tenind,tenden2,regresion,diccionario,temporal)
            return render(request,'funciones/Prediccion_casos_muertes.html',{'cabecera':encabezados,'graph':grafica['graficas'],'graph2':grafica2['graficas'],'indep':tenind,'dep':tenden,'dep2':tenden2,'grado':grafica['grado'],'grado2':grafica2['grado'],'result':grafica['resultado'],'result2':grafica2['resultado']})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('TICovid19_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Prediccion_casos_muertes.html',{'cabecera':encabezados,'graph':''})

def funcion_12(request):
    seleccionados = []
    global grafica,grafica2
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect1','')
        pais2 = request.POST.get('paisselect2','')
        tenind = request.POST.get('ten_independiente','')
        tenden = request.POST.get('ten_dependiente','')
        if pais_select != '':
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Comp_vacuna.html',{'cabecera':encabezados, 'data': seleccionados,'graph':''})
        else:
            if  pais !='' and tenden != '' and tenind!='' and pais2!='':
                grafica =analisis_p(pais,tenind,tenden,diccionario,temporal)
                grafica2 =analisis_p(pais,tenind,diccionario,temporal)
            return render(request,'funciones/Comp_vacuna.html',{'cabecera':encabezados,'graph':grafica['graficas'],'graph2':grafica2['graficas'],'indep':tenind,'dep':tenden,'dep2':tenden2,'grado':grafica['grado'],'grado2':grafica2['grado'],'result':grafica['resultado'],'result2':grafica2['resultado']})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('TICovid19_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Comp_vacuna.html',{'cabecera':encabezados,'graph':''})
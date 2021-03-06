from django.shortcuts import render
from django.contrib import messages

import pathlib
import logging
import csv
import json

import pandas as pd
from home.funciones.analisis.analisis import analisis_a, analisis_a_varios
from home.funciones.muertes.muertes import analisis_cantidad, analisis_cantidad_casos, analisis_cantidad_muertes, analisis_cantidad_regiones, analisis_clasificacion, analisis_factores
from home.funciones.predicciones.prediccion1 import analisis2_p, analisis_p, analisis_year_p
from home.funciones.tasa.tasas import analisis_tasas, analisis_tasas_locas, tasa_muerte

from home.funciones.tendencias.Tendencia1 import analisis, analisis2
from home.reports import reporte_analisis1, reporte_analisis2, reporte_comparacion, reporte_muertes1, reporte_muertes2, reporte_prediccion1, reporte_prediccion2, reporte_tasas1, reporte_tasas2, reporte_tendencia1

archivo = None
encabezados = []
diccionario = []
temporal = None
temporal2 = None
grafica = None
grafica2 = None
temp_variables =[]
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
        try:
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
                return render(request,'archivos.html',{'titulo':nombrecito, 'cabecera': encabezados, 'contenido' : diccionario})
            elif pathlib.Path(nombrecito).suffix == '.xls' or pathlib.Path(nombrecito).suffix == '.xlsx':
                aux = pd.read_excel(archivo)
                diccionario = aux.to_dict('records')
                encabezados = diccionario[0].keys()
                return render(request,'archivos.html',{'titulo':nombrecito, 'cabecera': encabezados, 'contenido' : diccionario})
            elif pathlib.Path(nombrecito).suffix == '.json':
                diccionario = json.load(archivo)
                encabezados = diccionario[0].keys()
                return render(request,'archivos.html',{'titulo':nombrecito, 'cabecera': encabezados, 'contenido' : diccionario})
            else:
                messages.error(request, f"Cannot parse data with {pathlib.Path(nombrecito).suffix} file type")
                return render(request,'opencsv.html')
        except Exception as inst:
            messages.error(request, f"{inst} need enter a file")
        return render(request,'opencsv.html')

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
                try:
                    grafica =analisis(pais,tenind,tenden,diccionario,temporal)
                    return render(request,'funciones/Tendencia_infeccion.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado']})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Tendencia_infeccion.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('Tendencia de la infecci??n por Covid-19 en un Pa??s','TICovid19_Pais.pdf',grafica['graficas'],grafica)
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
                try:
                    grafica =analisis(pais,tenind,tenden,diccionario,temporal)
                    return render(request,'funciones/Tendencia_infeccion_dia.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado']})
                except Exception as inst:
                        messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Tendencia_infeccion_dia.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('Tendencia del n??mero de infectados por d??a de un Pa??s','TIDia_Pais.pdf',grafica['graficas'],grafica)
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
                try:
                    grafica =analisis(pais,tenind,tenden,diccionario,temporal)
                    return render(request,'funciones/Tendencia_vacunacion.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado']})
                except Exception as inst:
                        messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Tendencia_vacunacion.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('Tendencia de la vacunaci??n de en un Pa??s','TV_Pais.pdf',grafica['graficas'],grafica)
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
            if depa != '' and pais != '' and tenden != '' and tenind!='' and temporal != None and temporal2!=None:
                try:
                    grafica =analisis2(pais,depa,tenind,tenden,diccionario,temporal,temporal2)
                    return render(request,'funciones/Tendencia_casos.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado']})
                except Exception as inst:
                        messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Tendencia_casos.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('Tendencia de casos confirmados de Coronavirus en un departamento de un Pa??s','TCDepa_Pais.pdf',grafica['graficas'],grafica)
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
                try:
                    grafica =analisis_p(pais,tenind,tenden,regresion,diccionario,temporal)
                    return render(request,'funciones/Prediccion_infectados.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado'],'result':grafica['resultado']})
                except Exception as inst:
                        messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Prediccion_infectados.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_prediccion1('Predicci??n de Infectados en un Pa??s','PreInf_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Prediccion_infectados.html',{'cabecera':encabezados,'graph':''})

def funcion_6(request):
    seleccionados = []
    seleccionados2 = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        depa_select = request.POST.get('camposelect2','')
        depa = request.POST.get('depaselect','')
        tenind = request.POST.get('ten_independiente','')
        tenden = request.POST.get('ten_dependiente','')
        regresion = request.POST.get('dato_regresion','')
        if  depa_select != '' :
            global temporal, temporal2
            temporal2 = depa_select
            for i in diccionario:
                for j in i:
                    if j == depa_select:
                        if not(i[j] in seleccionados2):
                            seleccionados2.append(i[j])
            return render(request,'funciones/Prediccion_muertes_depa.html',{'cabecera':encabezados, 'depa': seleccionados2,'graph':''})
        else:
            if depa != '' and tenden != '' and tenind!='' and regresion!='' and temporal2 != None:
                try:
                    grafica =analisis_p(depa,tenind,tenden,regresion,diccionario,temporal2)
                    return render(request,'funciones/Prediccion_muertes_depa.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado'],'result':grafica['resultado']})
                except Exception as inst:
                        messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Prediccion_muertes_depa.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_prediccion1('Predicci??n de mortalidad por COVID en un Departamento','PreMort_Dep.pdf',grafica['graficas'],grafica)
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
                try:
                    grafica =analisis_p(pais,tenind,tenden,regresion,diccionario,temporal)
                    return render(request,'funciones/Prediccion_muerte_pais.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado'],'result':grafica['resultado']})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Prediccion_muerte_pais.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_prediccion1('Predicci??n de mortalidad por COVID en un Pa??s','PreMort_Pais.pdf',grafica['graficas'],grafica)
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
                try:
                    grafica =analisis_p(pais,tenind,tenden,regresion,diccionario,temporal)
                    return render(request,'funciones/Prediccion_infectados_year.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado'],'result':grafica['resultado']})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Prediccion_infectados_year.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_prediccion1('Predicci??n de casos de un pa??s para un a??o','PreCasos_Pais.pdf',grafica['graficas'],grafica)
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
                try:
                    grafica =analisis_p(pais,tenind,tenden,regresion,diccionario,temporal)
                    return render(request,'funciones/Prediccion_por_dia.html',{'cabecera':encabezados, 'data': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado'],'result':grafica['resultado']})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Prediccion_por_dia.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_prediccion1('Predicci??n de casos confirmados por d??a','PreCasos_dia.pdf',grafica['graficas'],grafica)
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
                try:
                    grafica =analisis_year_p(pais,tenind,tenden,diccionario,temporal)
                    return render(request,'funciones/Prediccion_year_dia.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado'],'result':grafica['resultado']})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Prediccion_year_dia.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_prediccion1('Predicci??n de muertes en el ??ltimo d??a del primer a??o de infecciones en un pa??s','PreMurtYear_Pais.pdf',grafica['graficas'],grafica)
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
            if  pais !='' and tenden != '' and tenind!='' and tenden2!='' and regresion!='' and temporal != None:
                try:
                    grafica =analisis_p(pais,tenind,tenden,regresion,diccionario,temporal)
                    grafica2 =analisis_p(pais,tenind,tenden2,regresion,diccionario,temporal)
                    return render(request,'funciones/Prediccion_casos_muertes.html',{'cabecera':encabezados,'graph':grafica['graficas'],'graph2':grafica2['graficas'],'indep':tenind,'dep':tenden,'dep2':tenden2,'grado':grafica['grado'],'grado2':grafica2['grado'],'result':grafica['resultado'],'result2':grafica2['resultado']})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Prediccion_casos_muertes.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_prediccion2('Predicciones de casos y muertes en todo el mundo - Neural Network MLPRegressor','PCM_Mundial.pdf',grafica['graficas'],grafica2['graficas'],grafica,grafica2)
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
            if  pais !='' and tenden != '' and tenind!='' and pais2!='' and temporal!=None:
                try:
                    grafica =analisis_a(pais,pais2,tenind,tenden,diccionario,temporal)
                    return render(request,'funciones/Comp_vacuna.html',{'cabecera':encabezados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado']})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Comp_vacuna.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_analisis2('??nalisis Comparativo de Vacunaci??n entre 2 paises','AnVac_2Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Comp_vacuna.html',{'cabecera':encabezados,'graph':''})


def funcion_13(request):
    seleccionados = []
    global grafica,temp_variables
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
            return render(request,'funciones/Comp_varios.html',{'cabecera':encabezados, 'data': seleccionados,'graph':'','compare':temp_variables})
        elif pais != '':
            temp_variables.append(pais)
            return render(request,'funciones/Comp_varios.html',{'cabecera':encabezados, 'data': seleccionados,'compare':temp_variables,'graph':''})
        else:
            if  len(temp_variables) > 1 and tenden != '' and tenind!='' and temporal!=None:
                try:
                    grafica =analisis_a_varios(temp_variables,tenind,tenden,diccionario,temporal)
                    temp_variables =[]
                    return render(request,'funciones/Comp_varios.html',{'cabecera':encabezados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado']})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Comp_varios.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_analisis2('??nalisis Comparativo entres 2 o m??s paises o continentes','AnComp_n.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Comp_varios.html',{'cabecera':encabezados,'graph':''})

def funcion_14(request):
    seleccionados = []
    global grafica,grafica2
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect1','')
        tenind = request.POST.get('ten_independiente','')
        tenden = request.POST.get('ten_dependiente','')
        tenden2 = request.POST.get('ten_dependiente2','')
        if pais_select != '':
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Comp_vac_nu.html',{'cabecera':encabezados, 'data': seleccionados,'graph':''})
        else:
            if  pais !='' and tenden != '' and tenind!='' and tenden2!='' and temporal!=None:
                try:
                    grafica =analisis(pais,tenind,tenden,diccionario,temporal)
                    grafica2 =analisis(pais,tenind,tenden2,diccionario,temporal)
                    return render(request,'funciones/Comp_vac_nu.html',{'cabecera':encabezados,'graph':grafica['graficas'],'graph2':grafica2['graficas'],'indep':tenind,'dep':tenden,'dep2':tenden2,'grado':grafica['grado'],'grado2':grafica['grado']})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Comp_vac_nu.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_comparacion('Comparaci??n entre el n??mero de casos detectados y el n??mero de pruebas de un pa??s','Compa_Pais.pdf',grafica['graficas'],grafica2['graficas'],grafica,grafica2)
        else:
            return render(request,'funciones/Comp_vac_nu.html',{'cabecera':encabezados,'graph':''})

def funcion_15(request):
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
            return render(request,'funciones/Analisis_muertes.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if  pais !='' and tenden != '' and tenind!='' and temporal!=None:
                try:
                    grafica =analisis(pais,tenind,tenden,diccionario,temporal)
                    return render(request,'funciones/Analisis_muertes.html',{'cabecera':encabezados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado']})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Analisis_muertes.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('An??lisis del n??mero de muertes por coronavirus en un Pa??s','AnaNMurt_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Analisis_muertes.html',{'cabecera':encabezados,'graph':''})

def funcion_16(request):
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
            return render(request,'funciones/indice.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if  pais !='' and tenden != '' and tenind!='' and temporal!=None:
                try:
                    grafica =analisis(pais,tenind,tenden,diccionario,temporal)
                    return render(request,'funciones/indice.html',{'cabecera':encabezados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'grado':grafica['grado']})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/indice.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tendencia1('Indice de Progresi??n de la pandemia','Indice_PP.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/indice.html',{'cabecera':encabezados,'graph':''})

def funcion_17(request):
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
            return render(request,'funciones/Tasa_muertes.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if  pais !='' and tenden != '' and tenind!='' and temporal!=None:
                try:
                    #dato_tasa = regresar_tasa(pais,tenind,tenden,diccionario,temporal)
                    grafica =tasa_muerte(pais,tenind,tenden,diccionario,temporal)
                    return render(request,'funciones/Tasa_muertes.html',{'cabecera':encabezados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Tasa_muertes.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_muertes2('Tasa de mortalidad por coronavirus (COVID-19) en un pa??s','TasaMort_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Tasa_muertes.html',{'cabecera':encabezados,'graph':''})

def funcion_18(request):
    seleccionados = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect','')
        tenind = request.POST.get('colum_regiones','')
        tenden = request.POST.get('var_muertes','')
        if pais_select != '':
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Muertes_regiones.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if  pais !='' and tenden != '' and tenind!='' and temporal!=None:
                try:
                    grafica =analisis_cantidad(pais,tenind,tenden,diccionario,temporal)
                    return render(request,'funciones/Muertes_regiones.html',{'cabecera':encabezados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Muertes_regiones.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_muertes1('Muertes seg??n regiones de un pa??s - Covid 19','MuertR_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Muertes_regiones.html',{'cabecera':encabezados,'graph':''})

def funcion_19(request):
    seleccionados = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect','')
        tenind = request.POST.get('colum_deaths','')
        tenden = request.POST.get('var_casos','')
        if pais_select != '':
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Porcentaje_muertes.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if  pais !='' and tenden != '' and tenind!='' and temporal!=None:
                try:
                    grafica =analisis_cantidad_regiones(pais,tenind,tenden,diccionario,temporal)
                    return render(request,'funciones/Porcentaje_muertes.html',{'cabecera':encabezados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Porcentaje_muertes.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_muertes2('Porcentaje de muertes frente al total de casos en un pa??s, regi??n o continente','PorMuert_lugar.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Porcentaje_muertes.html',{'cabecera':encabezados,'graph':''})

def funcion_20(request):
    seleccionados = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect','')
        tenind = request.POST.get('ten_independiente','')
        tenden = request.POST.get('ten_dependiente','')
        tenden2 = request.POST.get('ten_dependiente2','')
        if pais_select != '':
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Tasa_activos_muertes.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if  pais !='' and tenden != '' and tenind!='' and tenden2!='' and temporal!=None:
                try:
                    grafica =analisis_tasas(pais,tenind,tenden,tenden2,diccionario,temporal)
                    return render(request,'funciones/Tasa_activos_muertes.html',{'cabecera':encabezados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'dep2':tenden2,'grado':grafica['grado'],'grado2':grafica['grado2']})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Tasa_activos_muertes.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_tasas1('Tasa de comportamiento de casos activos en relaci??n al n??mero de muertes en un continente','Tasa_continente.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Tasa_activos_muertes.html',{'cabecera':encabezados,'graph':''})

def funcion_21(request):
    seleccionados = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect','')
        tenind = request.POST.get('ten_independiente','')
        tenden = request.POST.get('ten_dependiente','')
        tenden2 = request.POST.get('ten_dependiente2','')
        if pais_select != '':
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Tasa_loca.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if  pais !='' and tenden != '' and tenind!='' and tenden2!=''  and temporal!=None:
                try:
                    grafica =analisis_tasas_locas(pais,tenind,tenden,tenden2,diccionario,temporal)
                    return render(request,'funciones/Tasa_loca.html',{'cabecera':encabezados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden,'dep2':tenden2})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Tasa_loca.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_muertes1('Tasa de crecimiento de casos de COVID-19 en relaci??n con nuevos casos diarios y tasa de muerte por COVID-19','Tasas_locas.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Tasa_loca.html',{'cabecera':encabezados,'graph':''})


def funcion_22(request):
    seleccionados = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect','')
        tenind = request.POST.get('colum_deaths','')
        tenden = request.POST.get('var_edad','')
        if pais_select != '':
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Muertes_edad.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if  pais !='' and tenden != '' and tenind!='' and temporal!=None:
                try:
                    grafica =analisis_cantidad_muertes(pais,tenind,tenden,diccionario,temporal)
                    return render(request,'funciones/Muertes_edad.html',{'cabecera':encabezados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Muertes_edad.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_muertes1('Muertes promedio por casos confirmados y edad de covid 19 en un Pa??s','MuertesEdad_Pais.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Muertes_edad.html',{'cabecera':encabezados,'graph':''})

def funcion_23(request):
    seleccionados = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect','')
        tenind = request.POST.get('colum_cases','')
        tenden = request.POST.get('var_sexo','')
        if pais_select != '':
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Porcentaje_casos_sexo.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if  pais !='' and tenden != '' and tenind!='' and temporal!=None:
                try:
                    grafica =analisis_cantidad_casos(pais,tenind,tenden,diccionario,temporal)
                    return render(request,'funciones/Porcentaje_casos_sexo.html',{'cabecera':encabezados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Porcentaje_casos_sexo.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_muertes2('Porcentaje de hombres infectados por covid-19 en un Pa??s desde el primer caso activo','Porcentaje_infectados.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Porcentaje_casos_sexo.html',{'cabecera':encabezados,'graph':''})

def funcion_24(request):
    seleccionados = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect','')
        tenind = request.POST.get('colum_factores','')
        tenden = request.POST.get('colum_muertes','')
        if pais_select != '':
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Factores.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if  pais !='' and tenden != '' and tenind!='' and temporal!=None:
                try:
                    grafica =analisis_factores(pais,tenind,tenden,diccionario,temporal)
                    return render(request,'funciones/Factores.html',{'cabecera':encabezados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Factores.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_muertes1('Factores de muerte por COVID-19 en un pa??s','Factores.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Factores.html',{'cabecera':encabezados,'graph':''})

def funcion_25(request):
    seleccionados = []
    global grafica
    if request.method == 'POST':
        logger = logging.getLogger('degub')
        logger.info(request.POST)
        pais_select = request.POST.get('camposelect','')
        pais = request.POST.get('paisselect','')
        tenind = request.POST.get('colum_factores','')
        tenden = request.POST.get('colum_muertes','')
        if pais_select != '':
            global temporal
            temporal = pais_select
            for i in diccionario:
                for j in i:
                    if j == pais_select:
                        if not(i[j] in seleccionados):
                            seleccionados.append(i[j])
            return render(request,'funciones/Clasificacion.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':''})
        else:
            if  pais !='' and tenden != '' and tenind!='' and temporal!=None:
                try:
                    grafica =analisis_clasificacion(pais,tenind,tenden,diccionario,temporal)
                    return render(request,'funciones/Clasificacion.html',{'cabecera':encabezados,'graph':grafica['graficas'],'indep':tenind,'dep':tenden})
                except Exception as inst:
                    messages.error(request, f"somthing went wrong: {inst}")
            else:
                messages.warning(request, f"All fields need to be filled")
            return render(request,'funciones/Clasificacion.html',{'cabecera':encabezados,'graph':''})
    elif request.method == 'GET':
        logger = logging.getLogger('degub')
        logger.info(request.GET)
        if grafica != None and request.GET.get('nombrepdf') == 'nombrepdf':
            return reporte_muertes1('Comportamiento y clasificaci??n de personas infectadas por COVID-19 por municipio en un Pa??s','Comportamiento.pdf',grafica['graficas'],grafica)
        else:
            return render(request,'funciones/Clasificacion.html',{'cabecera':encabezados,'graph':''})
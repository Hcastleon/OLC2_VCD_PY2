from django.shortcuts import render
from django.contrib import messages

import pathlib
import logging
import csv

from home.funciones.tendencias.Tendencia1 import analisis

archivo = None
encabezados = []
diccionario = []
temporal = None

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
            print('es un excel')
        elif pathlib.Path(nombrecito).suffix == '.json':
            print('es un json')
        else:
            print('no se acepta ese tipo de data')
            messages.error(request, f"Cannot parse data with {pathlib.Path(nombrecito).suffix} file type")
            return render(request,'opencsv.html')
    messages.success(request, "The file was uploaded successfully")
    return render(request,'archivos.html',{'titulo':nombrecito, 'cabecera': encabezados, 'contenido' : diccionario})
#funciones
def funcion_1(request):
    seleccionados = []
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
            return render(request,'funciones/Tendencia_infeccion.html',{'cabecera':encabezados, 'pais': seleccionados,'graph':grafica})
    else:
        return render(request,'funciones/Tendencia_infeccion.html',{'cabecera':encabezados,'graph':''})
###############################################################################
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import re
import numpy as np
import time

###############################################################################
#BeautifulSoup

urls = []

pages = [49,97,145,193,241,289,337,385,433,481,529,577,625,673,721,769,817,865,913,961,1009,1057,1105,1153,1201,1249,1297,1345,1393,1441,1489,1537,1585,1633,1681,1729,1777,1825,1873,1921,1969]

            # QUITAR EL APPEND EN LA SEGUNDA LISTA DE PÁGINAS #

# pages = [49,97,145,193] # 1
# pages = [241,289,337,385,433] # 2
# pages = [481,529,577,625,673] # 3
# pages = [721,769,817,865,913] # 4
# pages = [961,1009,1057,1105,1153] # 5
# pages = [1201,1249,1297,1345,1393] # 6
# pages = [1441,1489,1537,1585,1633] # 7
# pages = [1681,1729,1777,1825,1873] # 8
# pages = [1921,1969] # 9

# for i in pages:
#     url = "https://inmuebles.metroscubicos.com/departamentos/venta/distrito-federal/alvaro-obregon/_Desde_" + str(i) + "_PriceRange_0-5500000"
#     urls.append(url)
# urls.append("https://inmuebles.metroscubicos.com/departamentos/venta/distrito-federal/alvaro-obregon/_PriceRange_0-5500000")

for i in pages:
    url = "https://inmuebles.metroscubicos.com/casas/venta/distrito-federal/venustiano-carranza/_Desde_" + str(i)
    urls.append(url)
urls.append("https://inmuebles.metroscubicos.com/casas/venta/distrito-federal/venustiano-carranza/")

reqs = []
for link in urls:
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    reqs.append(req)

page_soups = []

for r in reqs:
    read_link = urlopen(r).read()
    page_soup = soup(read_link, 'lxml')
    page_soups.append(page_soup)
    time.sleep(15)

###############################################################################
#Obtener lista de listas de precios
rentas = []
for ps in range(len(page_soups)):
    precios = page_soups[ps].find_all("div",{"class":"item__price "})
    rentas.append(precios)

#Limpieza de rentas
rentas_limpias = []
for rm in rentas:
    for u in range(len(rm)):
        precio = rm[u].text
        rentas_limpias.append(precio)

###############################################################################
#Obtener lista de listas de direcciones
descripciones = []
for ds in range(len(page_soups)):
    descrip = page_soups[ds].find_all("div",{"class":"item__title"})
    descripciones.append(descrip)

#Limpieza de descripciones
descripcion_limpia = []
for dl in descripciones:
    for dl_ in range(len(dl)):
        descrip_ = dl[dl_].text
        descripcion_limpia.append(descrip_)

###############################################################################
#Obtener lista de listas de habitaciones
habitaciones = []
for hb in range(len(page_soups)):
    habis = page_soups[hb].find_all("div",{"class":"item__attrs"})
    habitaciones.append(habis)


#Limpieza de habitaciones
habitaciones_limpias = []
for nh in habitaciones:
    for h in range(len(nh)):
        hab = nh[h].text
        habitaciones_limpias.append(hab)

###############################################################################
#Convertir lista a DF
direcciones = pd.DataFrame({'Dirección': descripcion_limpia})
renta = pd.DataFrame({'Renta_mensual': rentas_limpias})
rooms = pd.DataFrame({'Metros_cuadrados': habitaciones_limpias})

#Columna para hacer Merge
renta['index1'] = renta.index
direcciones['index1'] = direcciones.index
rooms['index1'] = rooms.index

################################################################################
#Creación de DF de NaNs y Números
lista = []
u = np.nan
for i in direcciones['Dirección']:
    try:
        x = int(re.search(r'\d+', i).group())
        lista.append(x)
    except AttributeError:
        lista.append(u)

numbers = pd.DataFrame({'numbers':lista})

numbers['index1'] = numbers.index

###############################################################################
# M&A
join = pd.merge(renta, direcciones, how='left', on = ['index1'])
join_ = pd.merge(join, numbers, how='left', on = ['index1'])
join_2 = pd.merge(join_, rooms, how='left', on = ['index1'])
del join_2['index1']
join_2.dropna(inplace=True)
del join_2['numbers']

################################################################################
#Exportación
join_2.to_csv('ruta a archivo de colonias final', index = False)

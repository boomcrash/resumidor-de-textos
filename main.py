import urllib.request  
import re
import nltk
import urllib.request
import urllib.request
from inscriptis import get_text

url="https://en.wikipedia.org/wiki/Machine_learning"
url_to_html=urllib.request.urlopen(url).read().decode('utf-8')
html_to_text=get_text(url_to_html)
articulo=html_to_text.replace("[ edit ]","")
#limpieza del texto
articulo=re.sub(r'\[[0-9]*\]',' ',articulo)
#print(articulo)
articulo=re.sub(r'\s+',' ',articulo)
articulo_limpio=re.sub('[^a-zA-Z]',' ',articulo)
articulo_limpio=re.sub(r'\s+',' ',articulo_limpio)

#procesamiento de textos
#print(articulo_limpio)
from nltk import word_tokenize,sent_tokenize

lista_oraciones=nltk.sent_tokenize(articulo)
stopwords=nltk.corpus.stopwords.words("english")
palabras_frecuentes={}
for palabra in nltk.word_tokenize(articulo_limpio):
    if palabra not in stopwords:
        if palabra not in palabras_frecuentes.keys():
            palabras_frecuentes[palabra]=1
        else:
            palabras_frecuentes[palabra]+=1

frecuencia_alta=max(palabras_frecuentes.values())
for palabra in palabras_frecuentes.keys():
    palabras_frecuentes[palabra]=(palabras_frecuentes[palabra]/frecuencia_alta)


puntajes_oraciones={}
for valor in lista_oraciones:
    for palabra in nltk.word_tokenize(valor.lower()):
        if palabra in palabras_frecuentes.keys():
            if len(valor.split(" ")) <30:
                if valor not in puntajes_oraciones.keys():
                    puntajes_oraciones[valor]=palabras_frecuentes[palabra]
                else:
                    puntajes_oraciones[valor]+=palabras_frecuentes[palabra]


import heapq
oraciones_finales=heapq.nlargest(7,puntajes_oraciones,key=puntajes_oraciones.get)

resumen = ' '.join(oraciones_finales)
print("\n")
#print(resumen)

from googletrans import Translator
translator = Translator(service_urls=['translate.googleapis.com'])
traduccion= translator.translate(resumen, dest='es')
print(traduccion.text)
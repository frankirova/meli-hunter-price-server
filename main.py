from fastapi import FastAPI,APIRouter, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import requests

# router = APIRouter()
api = FastAPI()
# Configuración CORS
origins = [
    "https://meli-hunter-price-client.vercel.app/",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:8000",
]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@api.get('/products')
def getProducts():

    url = 'https://api.mercadolibre.com/sites/MLA/search'

    # Parámetros de búsqueda para celulares
    params = {
        'category': 'MLA1055',  # Categoría de celulares en Mercado Libre
        # 'q': 'celular',  # Término de búsqueda
        'limit': 10  # Cantidad de resultados a obtener
    }

    # Realizar la solicitud GET a la API de Mercado Libre
    response = requests.get(url, params=params)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        data = response.json()  # Convertir la respuesta a formato JSON
        results = data.get('results', [])  # Obtener la lista de resultados de la búsqueda
        # Recorrer los resultados e imprimir información relevante
        parsed_data=[]
        for result in results:
            prod = {'id':result['id'], 'title': result['title'], 'price': result['price'], 'img': result['thumbnail']}
            parsed_data.append(prod)
        return parsed_data
    else:
        print('La solicitud no fue exitosa. Código de estado:', response.status_code)

@api.get('/findProducts')
async def findProducts(q: str):
    url = "https://api.mercadolibre.com/sites/MLA/search"
    params = {"q": q}

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    products = data.get("results", [])
    updatedData=[]
    for result in products:
        prod = {'id':result['id'], 'title': result['title'], 'price': result['price'], 'img': result['thumbnail']}
        updatedData.append(prod)
    return updatedData


@api.get('/readOptionsBuy')
async def readOptionsBuy(item_id:str):
    url = "https://api.mercadolibre.com/items/MLA1286887580/shipping_options"
    # params = {"item_id": item_id}


    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    products = data.get("results", [])
    optionsBuy=[]
    for result in products:
        prod = {'id':result['id'], 'title': result['title'], 'price': result['price'], 'img': result['thumbnail']}
        optionsBuy.append(prod)
    return optionsBuy

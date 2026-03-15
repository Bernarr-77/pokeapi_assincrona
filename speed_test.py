import asyncio
import httpx
import time
import requests

async def buscar_pokemon(nome, cliente):
    url = f"https://pokeapi.co/api/v2/pokemon/{nome}"
    resposta = await cliente.get(url)
    dados_brutos = resposta.json()
    pokemon_limpo = {
        "name": dados_brutos["name"],
        "image_url": dados_brutos["sprites"]["front_default"],
        "types": [item["type"]["name"] for item in dados_brutos["types"]],
        "ability": [item["ability"]["name"] for item in dados_brutos["abilities"]],
        "stats": {item["stat"]["name"]: item["base_stat"] for item in dados_brutos["stats"]}
    }
    return pokemon_limpo

async def main():
    async with httpx.AsyncClient() as client:
        inicio = time.time()
        
        lista_pokemon = ["lucario","gengar","pikachu","mewtwo","primarina","xerneas"]
        organiza_pokemon = [buscar_pokemon(nome.lower(), client) for nome in lista_pokemon]
        resultado = await asyncio.gather(*organiza_pokemon)
        fim = time.time()
        print(f"Tempo gasto: {fim - inicio:.5f} segundos\n {resultado}")

asyncio.run(main())



def buscar_pokemon_sincrona(nome):
    url = f"https://pokeapi.co/api/v2/pokemon/{nome}"
    resposta = requests.get(url)
    dados_brutos = resposta.json()
    pokemon_limpo = {
        "name": dados_brutos["name"],
        "image_url": dados_brutos["sprites"]["front_default"],
        "types": [item["type"]["name"] for item in dados_brutos["types"]],
        "ability": [item["ability"]["name"] for item in dados_brutos["abilities"]],
        "stats": {item["stat"]["name"]: item["base_stat"] for item in dados_brutos["stats"]}
    }
    return pokemon_limpo

def sincrono():
    inicio = time.time()
    lista_pokemon = ["lucario","gengar","pikachu","mewtwo","primarina","xerneas"]
    resultado_lista = []
    for pokemon in lista_pokemon:
        resultado = buscar_pokemon_sincrona(pokemon)
        resultado_lista.append(resultado)

    fim = time.time()
    print(f"Tempo gasto: {fim - inicio:.5f} segundos\n {resultado_lista}")
sincrono()


    

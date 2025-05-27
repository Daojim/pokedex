from flask import Flask
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to Jimmy's Pokedex project!"

@app.route("/pokemon/<pokemonName>")
def getPokemon(pokemonName):
    #1. Let user manually type url for now.
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemonName.lower()}"

    #2. Send GET request to the PokeAPI
    response = requests.get(url)

    #3. Handle the case where the Pokemon doesn't exist
    if response.status_code != 200:
        return f"<h1>Error: </h1> Pokemon {pokemonName}' not found"
    
    #4. Parse the JSON data
    data = response.json()

    #5. Extract a few pieces of info
    name = data['name'].title()
    poke_id = data['id']
    sprite = data['sprites']['front_default']
    poke_type = data['types'][0]['type']['name'].title()

    #6. Return a basic HTML response
    return f"""
        <h1>{name}</h1>
        <p>ID: {poke_id}</p>
        <p>Type: {poke_type}</p>
        <img src="{sprite}" alt="{name} sprite">
    """
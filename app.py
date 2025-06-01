from flask import Flask
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to Jimmy's Pokedex project! Type '/pokemon/pikachu' in the URL to see Pikachu!"

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
    frontSprite = data['sprites']['front_default']
    backSprite = data['sprites']['back_default']
    poke_type = data['types'][0]['type']['name'].title()
    height = data['height']
    weight = data['weight']
    latestCry = data['cries']['latest']
    legacyCry = data['cries']['legacy']

    #6. Return a basic HTML response
    return f"""
        <img src="{frontSprite}" alt="{name} sprite"> 
        <img src="{backSprite}" alt="{name} sprite">
        <h1>{name}</h1>
        <p>ID: {poke_id}</p>
        <p>Type: {poke_type}</p>
        <p>Height: {height}</p>
        <p>Weight: {weight}</p>

        <figure>
            <figcaption>Latest audio cry:</figcaption>
            <audio controls>
                <source src="{latestCry}" type="audio/ogg">    
            </audio>
        </figure>

        <figure>
            <figcaption>Legacy audio cry:</figcaption>
            <audio controls>
                Legacy audio cry
                <source src="{legacyCry}" type="audio/ogg">
            </audio>
        </figure>
    """
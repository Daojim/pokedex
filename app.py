from flask import Flask, render_template, request, redirect, url_for
import requests, random

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pokemon')
def redirect_to_pokemon():
    # Read ?name=pikachu from URL
    name = request.args.get('name')  
    if name:
        return redirect(url_for('getPokemon', pokemonName=name))
    return redirect(url_for('index'))


@app.route("/pokemon/<pokemonName>")
def getPokemon(pokemonName):


    #1. Let user manually type url for now.
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemonName.lower()}"
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemonName.lower()}"

    #2. Send GET request to the PokeAPI
    response = requests.get(url)
    species_response = requests.get(species_url)

    #3. Handle the case where the Pokemon doesn't exist
    if response.status_code != 200:
        return f"<h1>Error: </h1> Pokemon {pokemonName}' not found"
    
    #4. Parse the JSON data
    data = response.json()
    species_data = species_response.json()

    #5. Extract a few pieces of info
    name = data['name'].title()
    poke_id = data['id']
    frontSprite = data['sprites']['front_default']
    backSprite = data['sprites']['back_default']
    types = [t['type']['name'].title() for t in data['types']]
    height = data['height']
    weight = data['weight']

    #Initially have no description found
    description = "No description found."

    #If description is found, loop through the data and grab the first English one
    if species_response.status_code == 200:
        species_data = species_response.json()
        for entry in species_data["flavor_text_entries"]:
            if entry["language"]["name"] == "en":
                #Entries have \n and \f characters that will be replaced with spaces.
                description = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
                break
    latestCry = data['cries']['latest']
    legacyCry = data['cries']['legacy']
    
    # For previous and next buttons. Ensures I never go below 1 or above 1010
    prev_id = max(1, poke_id - 1)
    next_id = min(1010, poke_id + 1)


    return render_template(
        "pokemon.html",
        name=name,
        poke_id=poke_id,
        frontSprite=frontSprite,
        backSprite=backSprite,
        types=types,
        height=height,
        weight=weight,
        description=description,
        latestCry=latestCry,
        legacyCry=legacyCry,
        prev_id=prev_id,
        next_id=next_id
    )

@app.route('/random')
def random_pokemon():
    random_id = random.randint(1,1010)
    return redirect(url_for('getPokemon', pokemonName=random_id))
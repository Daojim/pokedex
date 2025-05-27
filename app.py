from flask import Flask
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to Jimmy's Pokedex project!"

@app.route("/pokemon/<pokemonName>")
def getPokemon(name):
    #1.
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    
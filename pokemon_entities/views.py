import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.all()
    for pokemon_entity in pokemon_entities:

        abs_img_url = ''
        if pokemon_entity.pokemon.image:
            rel_img_url = pokemon_entity.pokemon.image.url
            abs_img_url = request.build_absolute_uri(rel_img_url)

        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            abs_img_url,
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url if pokemon.image else None,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    abs_img_url = ''
    if requested_pokemon.image:
        rel_img_url = requested_pokemon.image.url
        abs_img_url = request.build_absolute_uri(rel_img_url)

    pokemon = {
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'img_url': abs_img_url,
        'description': requested_pokemon.description,
    }

    if requested_pokemon.prev_evolution:
        prev_pokemon = requested_pokemon.prev_evolution
        pokemon['previous_evolution'] = {
            'pokemon_id': prev_pokemon.id,
            'img_url': prev_pokemon.image.url,
            'title_ru': prev_pokemon.title,
        }    

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    requested_pokemons_on_map = PokemonEntity.objects.filter(pokemon=requested_pokemon)

    for pokemon_entity in requested_pokemons_on_map:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon['img_url'],
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })

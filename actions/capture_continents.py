import json
import requests

from objects.Country import Country


africa = dict()
oceania = dict()
america = dict()
asia = dict()
europa = dict()

all_world_locations = {'Oceania': oceania, 'Europa': europa, 'América': america, 'Ásia': asia, 'África': africa}

all_regions_of_the_each_continent = dict()
all_countries_of_the_each_region = dict()

try:
    request = requests.get(f"https://servicodados.ibge.gov.br/api/v1/localidades/paises")
    all_countries_from_source_dict = json.loads(request.text)

    for i in all_countries_from_source_dict:
        all_regions_of_the_each_continent[i['sub-regiao']['regiao']['nome']] = set()
        all_countries_of_the_each_region[i['sub-regiao']['nome']] = set()

    for i in all_countries_from_source_dict:
        region = i['sub-regiao']['nome']
        all_regions_of_the_each_continent[i['sub-regiao']['regiao']['nome']].add(region)

        #  ---------------------------------------------------------------------------------------
        code_id = i['id']['ISO-ALPHA-2']
        name = i['nome']
        country = Country(code_id, name)

        country.location['continente'] = i['sub-regiao']['regiao']['nome']
        country.location['regiao'] = i['sub-regiao']['nome']

        if i['regiao-intermediaria'] is None:
            country.location['regiao especifica'] = "---"
        else:
            country.location['regiao especifica'] = i['regiao-intermediaria']['nome']
        #  -----------------------------------------------------------------------------------------

        all_countries_of_the_each_region[i['sub-regiao']['nome']].add(country)

    for i in all_countries_of_the_each_region:
        if i in all_regions_of_the_each_continent['África']:
            africa[i] = all_countries_of_the_each_region[i]

        elif i in all_regions_of_the_each_continent['Ásia']:
            asia[i] = all_countries_of_the_each_region[i]

        elif i in all_regions_of_the_each_continent['América']:
            america[i] = all_countries_of_the_each_region[i]

        elif i in all_regions_of_the_each_continent['Europa']:
            europa[i] = all_countries_of_the_each_region[i]

        elif i in all_regions_of_the_each_continent['Oceania']:
            oceania[i] = all_countries_of_the_each_region[i]

except Exception as ex:
    for i in all_world_locations:
        all_world_locations[i] = {f"xxErrorxx[capture_continents.py]": ex}


def show_continents():
    continents_list = list()
    for item in all_world_locations:
        continents_list.append(item)

    return continents_list


def show_regions_from_selected_continent(continent):
    regions_list = list()
    for item in all_world_locations[continent]:
        regions_list.append(item)

    return regions_list


def show_countries_from_selected_region(cont, region_of_cont):
    countries_list = list()
    try:
        for item in all_world_locations[cont][region_of_cont]:
            countries_list.append(item.name)

    except ConnectionError as connect_error:
        countries_list.append(connect_error)
    finally:
        return countries_list


def show_number_of_countries_by_continent():
    numbers_list = {'Oceania': list(), 'Europa': list(), 'América': list(),
                    'Ásia': list(), 'África': list()}

    for item in all_world_locations:
        for j in all_world_locations[item]:
            cont = len(all_world_locations[item][j])

            if item in numbers_list:
                numbers_list[item].append(cont)

        total = sum(numbers_list[item])
        numbers_list[item] = total

    return numbers_list

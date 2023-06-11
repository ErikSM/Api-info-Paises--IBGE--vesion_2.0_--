import json
import requests

from objects.Country import Country

africa = dict()
oceania = dict()
america = dict()
asia = dict()
europa = dict()

all_world_locations = {'Oceania': oceania, 'Europa': europa, 'América': america,
                       'Ásia': asia, 'África': africa}

all_regions_of_the_each_continent = dict()
all_countries_of_the_each_region = dict()

try:
    request = requests.get(f"https://servicodados.ibge.gov.br/api/v1/localidades/paises")
    all_countries_from_source_dict = json.loads(request.text)

    for item in all_countries_from_source_dict:
        all_regions_of_the_each_continent[item['sub-regiao']['regiao']['nome']] = set()
        all_countries_of_the_each_region[item['sub-regiao']['nome']] = set()

    for item in all_countries_from_source_dict:

        region = item['sub-regiao']['nome']
        all_regions_of_the_each_continent[item['sub-regiao']['regiao']['nome']].add(region)

        #  ---------------------------------------------------------------------------------------
        code_id = item['id']['ISO-ALPHA-2']
        name = item['nome']
        country = Country(code_id, name)

        country.location['continente'] = item['sub-regiao']['regiao']['nome']
        country.location['regiao'] = item['sub-regiao']['nome']

        if item['regiao-intermediaria'] is None:
            country.location['regiao especifica'] = "---"
        else:
            country.location['regiao especifica'] = item['regiao-intermediaria']['nome']
        #  -----------------------------------------------------------------------------------------

        all_countries_of_the_each_region[item['sub-regiao']['nome']].add(country)

    for region_name in all_countries_of_the_each_region:

        if region_name in all_regions_of_the_each_continent['África']:
            africa[region_name] = all_countries_of_the_each_region[region_name]

        elif region_name in all_regions_of_the_each_continent['Ásia']:
            asia[region_name] = all_countries_of_the_each_region[region_name]

        elif region_name in all_regions_of_the_each_continent['América']:
            america[region_name] = all_countries_of_the_each_region[region_name]

        elif region_name in all_regions_of_the_each_continent['Europa']:
            europa[region_name] = all_countries_of_the_each_region[region_name]

        elif region_name in all_regions_of_the_each_continent['Oceania']:
            oceania[region_name] = all_countries_of_the_each_region[region_name]

except Exception as ex:
    for i in all_world_locations:
        all_world_locations[i] = {f"xxErrorxx[capture_continents.py]": ex}


def show_continents():
    continents_list = list()
    for cont in all_world_locations:
        continents_list.append(cont)

    return continents_list


def show_regions_from_selected_continent(continent):
    regions_list = list()
    for reg in all_world_locations[continent]:
        regions_list.append(reg)

    return regions_list


def show_countries_from_selected_region(cont, region_of_cont):
    countries_list = list()
    try:
        for ctry in all_world_locations[cont][region_of_cont]:
            countries_list.append(ctry.name)

    except ConnectionError as connect_error:
        countries_list.append(connect_error)
    finally:
        return countries_list


def show_number_of_countries_by_continent():
    numbers_list = {'Oceania': list(), 'Europa': list(), 'América': list(),
                    'Ásia': list(), 'África': list()}

    for x in all_world_locations:

        for y in all_world_locations[x]:
            cont = len(all_world_locations[x][y])

            if x in numbers_list:
                numbers_list[x].append(cont)

        total = sum(numbers_list[x])
        numbers_list[x] = total

    return numbers_list


show_number_of_countries_by_continent()

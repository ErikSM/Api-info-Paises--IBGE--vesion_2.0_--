import json
import requests

from objects.Country import Country

all_countries_of_the_world_dict_names = dict()
all_countries_of_the_world_dict_acronyms = dict()

try:

    request = requests.get(f"https://servicodados.ibge.gov.br/api/v1/localidades/paises")
    all_world_in_source = json.loads(request.text)

    for item in all_world_in_source:

        code_id = item['id']['ISO-ALPHA-2']
        name = item['nome']
        country = Country(code_id, name)

        country.location['continente'] = item['sub-regiao']['regiao']['nome']
        country.location['regiao'] = item['sub-regiao']['nome']

        if item['regiao-intermediaria'] is None:
            country.location['regiao especifica'] = "---"
        else:
            country.location['regiao especifica'] = item['regiao-intermediaria']['nome']

        all_countries_of_the_world_dict_names[country.name] = country
        all_countries_of_the_world_dict_acronyms[country.code_id] = country

except Exception as ex_1:
    code_id = 'error_ex1'
    name = ex_1
    error_country = Country(code_id, name)

    all_countries_of_the_world_dict_names[f"{ex_1}"] = error_country
    all_countries_of_the_world_dict_acronyms["error_ex1"] = error_country


def capture_information_about_specific_country(pais):
    try:

        specific_request = requests.get(f"https://servicodados.ibge.gov.br/api/v1/paises/{pais}")
        specific_world_in_source = json.loads(specific_request.text)

        id_country = specific_world_in_source[0]['id']['ISO-3166-1-ALPHA-2']
        name_country = specific_world_in_source[0]['nome']['abreviado']

        if specific_world_in_source[0]['localizacao']['regiao-intermediaria'] is None:
            regiao_intermediaria = "---"
        else:
            regiao_intermediaria = specific_world_in_source[0]['localizacao']['regiao-intermediaria']['nome']
        location = {"continente": specific_world_in_source[0]['localizacao']['regiao']['nome'],
                    "regiao": specific_world_in_source[0]['localizacao']['sub-regiao']['nome'],
                    "regiao especifica": regiao_intermediaria}

        area = f"{specific_world_in_source[0]['area']['unidade']['multiplicador']}x " \
               f"{specific_world_in_source[0]['area']['total']} " \
               f"{specific_world_in_source[0]['area']['unidade']['símbolo']}"

        languages = specific_world_in_source[0]['linguas'][0]['nome']
        government = {"capital": specific_world_in_source[0]['governo']['capital']['nome']}
        currency_units = specific_world_in_source[0]['unidades-monetarias'][0]['nome']
        historic = specific_world_in_source[0]['historico']

        information_dict = {"sigla": id_country,
                            "nome": name_country,
                            "localizacao": location,
                            "area": area,
                            "linguas": languages,
                            "governo": government,
                            "unidade-monetaria": currency_units,
                            "historico": historic}

        return information_dict

    except Exception as ex_2:
        error_dict = {"sigla": 'error_ex2',
                      "nome": ex_2,
                      "localizacao": None,
                      "area": None,
                      "linguas": None,
                      "governo": None,
                      "unidade-monetaria": None,
                      "historico": None}

        return error_dict


"""print(all_countries_of_the_world_dict_names)
print(all_countries_of_the_world_dict_acronyms)"""
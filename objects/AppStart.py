from tkinter import *

from actions.capture_continents import all_world_locations, show_regions_from_selected_continent, \
    show_countries_from_selected_region
from actions.capture_countries import all_countries_of_the_world_dict_acronyms, \
    capture_information_about_specific_country
from actions.capture_indicators import show_all_indicators_of_selected_country, \
    show_specific_indicator_of_specific_country, indicator_accessed_dict
from graphics.graphic import lines_graphic_ramp_up
from objects.Country import Country


def start(window=None):
    if window is not None:
        window.destroy()
    AppStart()


class AppStart:

    def __init__(self):

        self.country = None

        self.bg_collor_window = "black"

        self.bg_collor_frame = "#041F21"
        self.bg_collor_subframe = "#041F21"

        self.bg_collor_text = "#031A25"
        self.fg_collor_text = "#AACBDA"
        self.bg_collor_list = "#031A25"
        self.fg_collor_list = "#AACBDA"

        self.bg_collor_labellist = "#041F21"
        self.fg_collor_labellist = "black"
        self.bg_collor_labelbuttom = "#041F21"
        self.fg_collor_labelbuttom = "black"

        self.bg_collor_buttom = "#041F21"
        self.fg_collor_buttom = "black"

        self.window = Tk()
        self.window.title("Busca de Informacoes Basicas de Paises")
        self.window.geometry("+400+100")
        self.window.minsize(height=200, width=200)
        self.window.resizable(False, False)
        self.window.config(bg=self.bg_collor_window)

        # / Menus
        self.menu = Menu(self.window)
        self.window.config(menu=self.menu)

        # // inicio
        self.menu.add_command(label="Tela inicial", command=lambda: start(self.window))

        # // paises
        self.menu_countries = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Paises", menu=self.menu_countries)
        self.menu_countries.add_command(label="Lista de Paises", command=self.open_countries)

        # // continentes
        self.menu_continents = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Continentes", menu=self.menu_continents)
        self.menu_continents.add_command(label="Lista de Continentes", command=self.open_continents)

        self.frame = Frame(self.window, bg=self.bg_collor_frame)
        self.frame.pack()
        self.text = Text(self.window, font="Arial 9 bold", width=100, height=20, bd=20,
                         bg=self.bg_collor_text, fg=self.fg_collor_text)
        self.text.pack()

        self.sub_frame_left = Frame(self.frame, bg=self.bg_collor_subframe, bd=5)
        self.sub_frame_left.pack(side="left")
        self.sub_frame_right = Frame(self.frame, bg=self.bg_collor_subframe, bd=5)
        self.sub_frame_right.pack(side="right")

        self.label_of_list = Label()
        self.label_of_button = Label()
        self.button_action = Button()
        self.all_config_settings("initial", self.search)

        self.list = Listbox(self.sub_frame_right, width=90, height=9, bd=20,
                            bg=self.bg_collor_list, fg=self.fg_collor_text)
        self.list.grid(row=1, column=0)

        self.window.mainloop()

    def open_countries(self):
        self.all_config_settings("countries", self.search)
        self._clear()

        for acronym in all_countries_of_the_world_dict_acronyms:
            if acronym == 'Error_ex1':
                self._error_messege_print(all_countries_of_the_world_dict_acronyms[acronym].name)
            else:
                self.list.insert(END, f"{acronym}:  {all_countries_of_the_world_dict_acronyms[acronym].name}")

                self.text.insert(END, all_countries_of_the_world_dict_acronyms[acronym].show_basic_informaton())

    def open_continents(self):

        self.all_config_settings("continents", self.select_continent)
        self._clear()

        for continent in all_world_locations:
            self.list.insert(END, f"{continent}")

            self.text.insert(END, f"- {continent}\n   Regioes:  {show_regions_from_selected_continent(continent):}\n\n")

    def select_continent(self):
        try:
            continent = self.list.get(ANCHOR)
            all_continent_region = all_world_locations[continent]
        except KeyError:
            self._error_messege_print(KeyError)

        else:
            self.all_config_settings("regions", lambda: self.select_region(continent))
            self._clear()

            for region in all_continent_region:
                self.list.insert(END, f"{region}")

                self.text.insert(END,
                                 f"-{region}:\n  paises: {show_countries_from_selected_region(continent, region)}\n\n")

    def select_region(self, continent):
        try:
            region = self.list.get(ANCHOR)
            all_region_contries = all_world_locations[continent][region]

        except KeyError:
            self._error_messege_print(KeyError)

        else:
            try:
                self.all_config_settings("countries", self.search)
                self._clear()

                for country in all_region_contries:
                    self.list.insert(END, f"{country.code_id}:  {country.name}")

                    self.text.insert(END, f"{country.show_basic_informaton()}")
            except Exception as ex:
                self._error_messege_print(ex, True)

    def search(self):

        name_acronym = self.list.get(ANCHOR)
        self.all_config_settings("search", self.advanced_information_about_country)
        self._clear()

        acronym = name_acronym[0:2]
        name = name_acronym[5:]
        dict_of_information = capture_information_about_specific_country(acronym)

        country = Country(acronym, name, dict_of_information)

        if country.dict_of_attributes['sigla'] == 'Error_ex2':
            self._error_messege_print(country.dict_of_attributes['nome'])
            self.list.insert(END, country.name)
        else:
            for item in country.dict_of_attributes:
                if item == 'historico':
                    self.text.insert(END, f"* {item}:\n\n     {country.dict_of_attributes[item]}")
                else:
                    self.list.insert(END, f"- {item}:  {country.dict_of_attributes[item]}")

        self.country = country

    def advanced_information_about_country(self):

        self.all_config_settings("advanced", self.research_area)
        self._clear()

        self.country.indicators = show_all_indicators_of_selected_country(self.country)

        for research_area in self.country.indicators:
            self.list.insert(END, research_area)

            self.text.insert(END, f"   ** {research_area.title()}:\n")
            for indicator in self.country.indicators[research_area]:
                self.text.insert(END, f"> ( {indicator} )\n")
            self.text.insert(END, f"\n\n")

    def research_area(self):

        research_area = self.list.get(ANCHOR)

        self.all_config_settings("research", self.show_selected_indicator)
        self._clear()

        for indicator in self.country.indicators[research_area]:
            self.list.insert(END, indicator)

        self.text.insert(END, self.country.show_all_informaton_about())

    def show_selected_indicator(self):

        code_of_indicator = self.list.get(ANCHOR)
        code_of_indicator = code_of_indicator[0:5]

        self.all_config_settings("indicator", self.back_to_initial_settings)
        self._clear()

        indicator_selected = show_specific_indicator_of_specific_country(self.country, code_of_indicator)

        indicator_name = indicator_selected['indicador']
        title_to_print = f"        Informacoes existentes sobre indicadores de: ({indicator_name}), " \
                         f"relacionados ao pais: ({self.country.name})\n\n"

        self.text.insert(END, title_to_print)

        self.list.insert(END, self.country.name)
        self.list.insert(END, '\n\n')

        for i in indicator_selected:

            if i == 'xxErrorxx[specific_indicator]':
                self.list.insert(END, i)
                self.text.insert(END, indicator_selected[i])

            elif i == 'series':

                for j in indicator_selected[i][0]['serie']:

                    for date in j:
                        if j[date] is None:
                            pass

                        else:
                            date = date
                            indicator_accessed_dict['date'].append(int(date))

                            information = float(j[date])
                            indicator_accessed_dict['information'].append(information)

                            unit = indicator_selected['unidade']['id']
                            indicator_accessed_dict['unit'].append(unit)

                            multiplier = indicator_selected['unidade']['multiplicador']
                            indicator_accessed_dict['multiplier'].append(multiplier)

                            self.text.insert(END, " -   Periodo de {date}   >>      "
                                                  f"{unit}: {information}      "
                                                  f"multiplicado por: ({multiplier}x) \n")

            else:
                self.list.insert(END, f"{i}:  {indicator_selected[i]}")
                self.list.insert(END, '\n\n')

        print(indicator_accessed_dict)

        lines_graphic_ramp_up(indicator_accessed_dict, f"({self.country.name}): {indicator_name}")

    def back_to_initial_settings(self):
        start(self.window)

    def all_config_settings(self, config_type, button_command):

        self.label_of_list.destroy()

        self.label_of_list = Label(self.sub_frame_right, font="Arial 13 bold",
                                   bg=self.bg_collor_labellist, fg=self.fg_collor_labellist)
        self.label_of_list.grid(row=0, column=0)

        self.label_of_button.destroy()
        self.label_of_button = Label(self.sub_frame_left, font="Arial 10 bold",
                                     bg=self.bg_collor_labelbuttom, fg=self.fg_collor_labelbuttom)
        self.label_of_button.grid(row=0, column=0, columnspan=2)

        self.button_action.destroy()
        self.button_action = Button(self.sub_frame_left, font="Consolas 11 bold", bd=1,
                                    bg=self.bg_collor_buttom, fg=self.fg_collor_buttom)
        self.button_action.grid(row=1, column=1)

        if config_type == "initial":
            self.label_of_list.configure(text="-----------   ----------- :")

            self.label_of_button.configure(text="Lista ao lado:")

            self.button_action.configure(text="Busca", command=button_command)
            self.button_action.config(state=DISABLED)

        elif config_type == "search":
            self.label_of_list.configure(text=f"Infomacoes Basicas:")

            self.label_of_button.configure(text="Saber mais:")

            self.button_action.configure(text=f"<Informacoes>",
                                         command=button_command)

        elif config_type == "advanced":
            self.label_of_list.configure(text=f"Areas de Pesquisa de: ({self.country.name.title()})")

            self.label_of_button.configure(text="Escolha a area:")

            self.button_action.configure(text=f"Pesquisar", command=button_command)

        elif config_type == "research":
            self.label_of_list.configure(text="Indicadores:")

            self.label_of_button.configure(text="Selecione ao lado:")

            self.button_action.configure(text="Selecionar", command=button_command)

        elif config_type == "indicator":
            self.label_of_list.configure(text=f"(fonte: IBGE)")

            self.label_of_button.configure(text="Voltar ao inicio:")

            self.button_action.configure(text="voltar", command=button_command)

        elif config_type == "countries":
            self.label_of_list.configure(text="Paises:")

            self.label_of_button.configure(text="Pais ao lado:")

            self.button_action.configure(text="Busca", command=button_command)

        elif config_type == "continents":
            self.label_of_list.configure(text="Continentes:")

            self.label_of_button.configure(text=f"Continente ao lado:")

            self.button_action.configure(text=f"Selecionar", command=button_command)

        elif config_type == "regions":
            self.label_of_list.configure(text="regioes:")

            self.label_of_button.configure(text=f"Regioes ao lado:")

            self.button_action.configure(text=f"Selecionar", command=button_command)

    def _error_messege_print(self, error_type=None, reset=False):
        self.text.insert(1.0, "-")
        self.text.delete(1.0, END)

        if reset:
            self.button_action.configure(text="voltar", command=self.back_to_initial_settings)

            self.list.insert(1, "-")
            self.list.delete(0, END)
            self.list.insert(END, f'XXX   Acesso Negado  XXX')

        self.text.insert(END, f'xxxxxx__Error__xxxxxx\n\n'
                              f'  (( Possivel problemas  ))\n'
                              f'- Selecione um item antes de avancar caso nao selecionado\n'
                              f'- Verifique se selecionou o item corretamente\n'
                              f'- Problemas com conexao de internet\n\n\n'
                              f'** Desenvolvedor **'
                              f'--- Exception type: {error_type}')

    def _clear(self):
        self.list.insert(1, "-")
        self.list.delete(0, END)

        self.text.insert(1.0, "-")
        self.text.delete(1.0, END)

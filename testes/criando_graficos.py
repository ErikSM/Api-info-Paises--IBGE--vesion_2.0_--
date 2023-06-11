import matplotlib.pyplot as plt


def bars_graphic_ramp_up(dictionary, x_axle_name='x', y_axle_name='y', graphic_name='grafico de barras', y_mask=""):
    plt.figure(figsize=(10, 6), facecolor='grey')
    plt.axes().set_facecolor('grey')
    plt.tick_params(axis='x', labelsize=8)
    plt.tick_params(axis='y', labelsize=8)

    lista_x = list()
    lista_y = list()
    for i in dictionary:
        lista_x.append(i)
        lista_y.append(dictionary[i])

    if len(dictionary) > 3:
        largura_do_grafico = 0.3
    elif len(dictionary) > 5:
        largura_do_grafico = 0.1
    else:
        largura_do_grafico = 0.5
    plt.bar(lista_x, lista_y, align="center", facecolor="black", width=largura_do_grafico)

    plt.title("{}".format(graphic_name), font="Times New Roman", color="black", fontsize=25)
    plt.xlabel("{}".format(x_axle_name), font="Consolas", color="red", fontsize=14)
    plt.ylabel("{} {}".format(y_axle_name, y_mask), font="Consolas", color="red", fontsize=14)

    plt.show()


def lines_graphic_ramp_up(dictionary: dict, graphic_name='grafico de linha'):
    plt.figure(figsize=(8, 4), facecolor='#041F21')
    plt.axes().set_facecolor('#031A25')
    plt.tick_params(axis='x', labelsize=6)
    plt.tick_params(axis='y', labelsize=6)

    y_axle_name = None
    x_axle_name = None
    roster_x = list()
    roster_y = list()

    for i in dictionary:

        if i == 'information':
            roster_y = dictionary[i]
            y_axle_name = f"Unidade:{dictionary['unit'][0]}  -  Mult:(x{dictionary['multiplier'][0]})"

        elif i == 'date':
            roster_x = dictionary[i]
            x_axle_name = 'Datas de pesquisa:'

    plt.plot(roster_x, roster_y, linestyle="-", color="black", marker=".", linewidth=1.0)

    plt.title("{}".format(graphic_name), font="Times New Roman", color="black", fontsize=14)
    plt.xlabel("{}".format(x_axle_name), font="Consolas", color="black", fontsize=9)
    plt.ylabel("{}".format(y_axle_name), font="Consolas", color="black", fontsize=9)

    plt.show()

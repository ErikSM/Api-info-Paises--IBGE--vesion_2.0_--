import matplotlib.pyplot as plt


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
            y_axle_name = f"Unidade em:[ {dictionary['unit'][0]} ]  -  Mult:(x{dictionary['multiplier'][0]})"

        elif i == 'date':
            roster_x = dictionary[i]
            x_axle_name = 'Datas de pesquisa:'

    plt.plot(roster_x, roster_y, linestyle="-", color="red", marker=".", linewidth=1.0)

    plt.title("{}".format(graphic_name), font="Times New Roman", color="black", fontsize=14)
    plt.xlabel("{}".format(x_axle_name), font="Consolas", color="black", fontsize=9)
    plt.ylabel("{}".format(y_axle_name), font="Consolas", color="black", fontsize=9)

    plt.show()

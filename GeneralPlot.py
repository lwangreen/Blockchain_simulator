import matplotlib.pyplot as plt


def set_text_font(legend):
    plt.xticks(fontsize=6, rotation=40)
    plt.yticks(fontsize=6)
    plt.legend(legend, fontsize=8, loc='upper left')


def create_figure(fig_num, plot_title, fig_size=(6, 3), subplotsize=111):
    fig = plt.figure(fig_num, figsize=fig_size)
    ax = plt.subplot(subplotsize)
    plt.title(plot_title)
    return fig, ax


def render_line_chart_plot(x, y):
    plt.plot(x, y)


def render_box_plot(data):
    plt.boxplot(data)



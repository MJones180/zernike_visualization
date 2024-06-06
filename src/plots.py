import matplotlib.pyplot as plt


def scatter_2D(x_grid, y_grid, aberrations):
    ax = plt.subplot(111)
    ax.scatter(x_grid, y_grid, c=aberrations)
    ax.set_aspect(1)
    plt.show()


def scatter_3D(x_grid, y_grid, aberrations):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(x_grid, y_grid, aberrations, vmin=aberrations.min() * 2)
    plt.show()


def get_plots():
    return [('Scatter (2D)', scatter_2D), ('Scatter (3D)', scatter_3D)]

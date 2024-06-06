import matplotlib.pyplot as plt


def scatter_2D(fig, x_grid, y_grid, aberration_field):
    ax = fig.add_subplot(111)
    ax.axis('off')
    ax.set_aspect(1)
    scatter = ax.scatter(x_grid, y_grid, c=aberration_field)
    plt.colorbar(scatter)


def scatter_3D(fig, x_grid, y_grid, aberration_field):
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.plot_surface(x_grid,
                    y_grid,
                    aberration_field,
                    vmin=aberration_field.min() * 2)


def get_plots():
    return [('Scatter (2D)', scatter_2D), ('Scatter (3D)', scatter_3D)]

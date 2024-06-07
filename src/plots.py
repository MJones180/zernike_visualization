import matplotlib.pyplot as plt

# The fig object that all plots will be outputted on, should be global
# so that there is only one
fig = plt.Figure(figsize=(5, 5), dpi=100)


def scatter_2D(x_grid, y_grid, aberration_field, cmap):
    ax = fig.add_subplot(111)
    ax.axis('off')
    ax.set_aspect(1)
    scatter = ax.scatter(x_grid, y_grid, c=aberration_field, cmap=cmap)
    plt.colorbar(scatter)


def scatter_3D(x_grid, y_grid, aberration_field, cmap):
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.plot_surface(x_grid, y_grid, aberration_field, cmap=cmap)


def get_cmap_options():
    return ['jet', 'winter', 'hsv']


def get_plots():
    return {
        'Scatter (2D)': scatter_2D,
        'Scatter (3D)': scatter_3D,
    }

from compute_zernike_terms import compute_zernike_dict_fixed
from display_gui import display_gui
import numpy as np
from plots import get_fig_object, get_plots
from zernike_terms import ZERNIKE_TERM_RANGE

# Number of grid points
GRID_R_POINTS = 100
GRID_THETA_POINTS = 360


def main():
    # Create the polar coordinates
    rho_points = np.linspace(1e-6, 1, GRID_R_POINTS)
    theta_points = np.linspace(0, 2 * np.pi, GRID_THETA_POINTS)
    # The polor coordinates for each location on the grid
    rho_grid, theta_grid = np.meshgrid(rho_points, theta_points)
    # Compute a dictionary of all the Zernike aberrations
    aberrations = compute_zernike_dict_fixed(rho_grid, theta_grid)
    # Create a cartesian representation of the polar grid
    x_grid = rho_grid * np.cos(theta_grid)
    y_grid = rho_grid * np.sin(theta_grid)
    # Current amplitudes for each of the Zernike terms
    zernike_amps = {term: 0 for term in range(*ZERNIKE_TERM_RANGE)}

    def _get_aberration_field():
        # The field representing the sum of all the aberrations
        field = np.zeros_like(x_grid)
        for term, amp in zernike_amps.items():
            if amp != 0:
                field += amp * aberrations[term]
        return field

    # Dict with the available plots as { title: plotting_function, ... }
    plots_listing = get_plots()
    # All plot names, this will be displayed on the GUI
    plot_names = list(plots_listing.keys())
    # Default to the first plotting function
    plotting_func = plots_listing[plot_names[0]]
    # The figure object that all plots will output using
    fig = get_fig_object()

    def _update_plot():
        aberration_field = _get_aberration_field()
        fig.clf()
        plotting_func(fig, x_grid, y_grid, aberration_field)
        fig.canvas.draw()

    def change_plot_type(plot_name):
        nonlocal plotting_func
        plotting_func = plots_listing[plot_name]
        _update_plot()

    def update_zernike_amp(zernike_term, term_val):
        if zernike_term == 'all':
            for term in zernike_amps.keys():
                zernike_amps[term] = 0
            _update_plot()
        elif zernike_amps[zernike_term] != term_val:
            zernike_amps[zernike_term] = term_val
            _update_plot()

    display_gui(fig, update_zernike_amp, change_plot_type, plot_names)


if __name__ == '__main__':
    main()

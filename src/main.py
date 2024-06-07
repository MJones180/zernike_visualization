from compute_zernike_terms import compute_zernike_dict_fixed
from display_gui import display_gui
import numpy as np
from plots import fig, get_cmap_options, get_plots
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
    # The field representing the sum of all the aberrations
    aberration_field = np.zeros_like(x_grid)
    # Dict with the available plots as { title: plotting_function, ... }
    plots_listing = get_plots()
    # All plot names
    plot_names = list(plots_listing.keys())
    # Default to the first plotting function
    plotting_func = plots_listing[plot_names[0]]
    # All colormap names
    cmap_names = get_cmap_options()
    # Default to the first cmap listed
    current_cmap = cmap_names[0]

    def _update_plot():
        # Clear the current figure
        fig.clf()
        # Plot the new data on
        plotting_func(x_grid, y_grid, aberration_field, current_cmap)
        # Update on the GUI
        fig.canvas.draw()

    def change_cmap(cmap_name):
        nonlocal current_cmap
        # Switch to the new cmap
        current_cmap = cmap_name
        _update_plot()

    def change_plot_type(plot_name):
        nonlocal plotting_func
        # Switch to the new plotter
        plotting_func = plots_listing[plot_name]
        _update_plot()

    def update_zernike_amp(zernike_term, term_val=0):
        nonlocal aberration_field
        # Reset all the zernike terms and field
        if zernike_term == 'all_zero':
            aberration_field[:, :] = 0
            for term in zernike_amps.keys():
                zernike_amps[term] = 0
            _update_plot()
        # Since this function gets called for any input change (for instance,
        # adding more zeros), only update if the term's value actually changed
        elif zernike_amps[zernike_term] != term_val:
            # Compute only the difference in how much this term has changed
            term_diff = term_val - zernike_amps[zernike_term]
            # Make the incremental change to the field
            aberration_field += term_diff * aberrations[zernike_term]
            zernike_amps[zernike_term] = term_val
            _update_plot()

    display_gui(
        update_zernike_amp,
        change_cmap,
        cmap_names,
        change_plot_type,
        plot_names,
    )


if __name__ == '__main__':
    main()

from compute_zernike_terms import compute_zernike_dict
from display_gui import display_gui
import numpy as np
from plots import get_plots
from zernike_terms import ZERNIKE_TERM_RANGE

import matplotlib.pyplot as plt

# Number of grid points
GRID_R_POINTS = 100
GRID_THETA_POINTS = 360


def main():
    rho_points = np.linspace(1e-6, 1, GRID_R_POINTS)
    theta_points = np.linspace(0, 2 * np.pi, GRID_THETA_POINTS)
    rho_grid, theta_grid = np.meshgrid(rho_points, theta_points)
    aberrations = compute_zernike_dict(rho_grid, theta_grid)

    plots = get_plots()

    x_grid = rho_grid * np.cos(theta_grid)
    y_grid = rho_grid * np.sin(theta_grid)
    aberration_field = np.zeros_like(x_grid)

    # Plot figure on the GUI
    fig = plt.Figure(figsize=(5, 5), dpi=100)

    zernike_amps = {
        term: 0
        for term in range(ZERNIKE_TERM_RANGE[0], ZERNIKE_TERM_RANGE[1] + 1)
    }

    def _get_aberration_field():
        field = aberration_field.copy()
        for term, amp in zernike_amps.items():
            if amp != 0:
                field += amp * aberrations[term]
        return field

    def _update_plot():
        print('Updating')
        aberration_field = _get_aberration_field()
        fig.clf()
        plot = fig.add_subplot(111)
        plot.scatter(x_grid, y_grid, c=aberration_field)
        fig.canvas.draw()

        # ax = plt.subplot(111)
        # ax.scatter(x_grid, y_grid, c=aberrations)
        # ax.set_aspect(1)
        # plt.show()
        # fig.clf()
        # plot1 = fig.add_subplot(111)
        # y = [(i + term_val)**2 for i in range(101)]
        # # plotting the graph
        # plot1.plot(y)
        # fig.canvas.draw()
        # pass

    def update_zernike_amp(zernike_term, term_val):
        if zernike_term == 'all':
            for term in zernike_amps.keys():
                zernike_amps[term] = 0
            _update_plot()
        elif zernike_amps[zernike_term] != term_val:
            zernike_amps[zernike_term] = term_val
            _update_plot()

    display_gui(fig, update_zernike_amp)


if __name__ == '__main__':
    main()

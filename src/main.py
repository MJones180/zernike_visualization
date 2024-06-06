from compute_zernike_terms import compute_zernike_dict
import numpy as np

# Number of grid points
GRID_R_POINTS = 100
GRID_THETA_POINTS = 360


def main():
    rho_points = np.linspace(1e-6, 1, GRID_R_POINTS)
    theta_points = np.linspace(0, 2 * np.pi, GRID_THETA_POINTS)
    rho_grid, theta_grid = np.meshgrid(rho_points, theta_points)
    aberrations = compute_zernike_dict(rho_grid, theta_grid)


if __name__ == '__main__':
    main()

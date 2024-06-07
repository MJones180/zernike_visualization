import numpy as np
from zernike_terms import ZERNIKE_NOLL_LOOKUP


def compute_zernike_dict_fixed(rho_grid, theta_grid):
    # The `compute_zernike_dict` was not working for spherical aberrations, so
    # below are the equations being computed directly. Equations taken from:
    # webs.optics.arizona.edu/gsmith/Zernike.html
    rho = rho_grid
    theta = theta_grid
    sin = np.sin
    cos = np.cos
    rho2 = rho**2
    rho3 = rho**3
    rho4 = rho**4
    theta2 = theta * 2
    theta3 = theta * 3
    return {
        1: 1,
        2: 2 * rho * cos(theta),
        3: 2 * rho * sin(theta),
        4: 3**0.5 * (2 * rho2 - 1),
        5: 6**0.5 * rho2 * sin(theta2),
        6: 6**0.5 * rho2 * cos(theta2),
        7: 8**0.5 * rho * (3 * rho2 - 2) * sin(theta),
        8: 8**0.5 * rho * (3 * rho2 - 2) * cos(theta),
        9: 8**0.5 * rho3 * sin(theta3),
        10: 8**0.5 * rho3 * cos(theta3),
        11: 5**0.5 * (6 * rho4 - 6 * rho2 + 1),
        12: 10**0.5 * rho2 * (4 * rho2 - 3) * cos(theta2),
        13: 10**0.5 * rho2 * (4 * rho2 - 3) * sin(theta2),
        14: 10**0.5 * rho4 * cos(4 * theta),
        15: 10**0.5 * rho4 * sin(4 * theta),
        16: 12**0.5 * rho * (10 * rho4 - 12 * rho2 + 3) * cos(theta),
        17: 12**0.5 * rho * (10 * rho4 - 12 * rho2 + 3) * sin(theta),
        18: 12**0.5 * rho3 * (5 * rho2 - 4) * cos(theta3),
        19: 12**0.5 * rho3 * (5 * rho2 - 4) * sin(theta3),
        20: 12**0.5 * rho**5 * cos(5 * theta),
        21: 12**0.5 * rho**5 * sin(5 * theta),
        22: 7**0.5 * (20 * rho**6 - 30 * rho4 + 12 * rho2 - 1),
        23: 14**0.5 * rho2 * (15 * rho4 - 20 * rho2 + 6) * sin(theta2),
        24: 14**0.5 * rho2 * (15 * rho4 - 20 * rho2 + 6) * cos(theta2),
    }


# ==============================================================================
# Code below does not work :(
# ==============================================================================

RADIAL_CACHE = {}


def _compute_radial(n, m, rho):
    # Compute the radial component using the q-recursive method outlined by
    # Chee-Way Chong in "A comparative analysis of algorithms for fast
    # computation of Zernike moments" (doi.org/10.1016/S0031-3203(02)00091-2)
    cache_key = (n, m)
    if cache_key in RADIAL_CACHE:
        return RADIAL_CACHE[cache_key]
    m = np.abs(m)
    if n == m:
        result = rho**n
    elif (n - m) <= 2:
        result = n * rho**n - (n - 1) * rho**(n - 2)
    else:
        # Code was not working, so I ended up referring to how HCIPy computed
        # this, and they add 4 do their `m` index, so I am going with that.
        # github.com/ehpor/hcipy/blob/3cdb57f4d5c314dd1589fcd1cc6a669c82b9d39f/hcipy/mode_basis/zernike.py#L131
        m = m + 4
        h3 = -4 * (m - 2) * (m - 3) / ((n + m - 2) * (n - m + 4))
        h2 = h3 * (n + m) * (n - m + 2) / (4 * (m - 1)) + (m - 2)
        h1 = m * (m - 1) / 2 - m * h2 + h3 * (n + m + 2) * (n - m) / 8
        result = (h1 * _compute_radial(n, m, rho) +
                  (h2 + h3 / rho**2) * _compute_radial(n, m - 2, rho))
    RADIAL_CACHE[cache_key] = result
    return result


def _compute_zernike_term(n, m, rho, theta):
    abs_m = np.abs(m)
    radial = _compute_radial(n, abs_m, rho)
    azimuthal_func = np.cos if m > 0 else np.sin
    return radial * azimuthal_func(abs_m * theta)


def compute_zernike_dict(rho_grid, theta_grid):
    return {
        noll_term: _compute_zernike_term(n, m, rho_grid, theta_grid)
        for noll_term, (n, m) in ZERNIKE_NOLL_LOOKUP.items()
    }

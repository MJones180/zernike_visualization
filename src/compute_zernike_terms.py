import numpy as np
from zernike_terms import ZERNIKE_NOLL_LOOKUP

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

import matplotlib.pyplot as plt
import numpy as np

# def noll_to_nm(j):
#     print(j)
# noll_to_nl(8)


def compute_radial_polynomial(n, m, rho):
    print(n - m)
    if n == m:
        return rho**n
    elif (n - m) <= 2:
        return n * rho**n - (n - 1) * rho**(n - 2)
    else:
        # Why the m+4???
        # https://github.com/ehpor/hcipy/blob/3cdb57f4d5c314dd1589fcd1cc6a669c82b9d39f/hcipy/mode_basis/zernike.py#L131
        # https://www.sciencedirect.com/science/article/pii/S0031320302000912
        m = m + 4
        h3 = -4 * (m - 2) * (m - 3) / ((n + m - 2) * (n - m + 4))
        h2 = h3 * (n + m) * (n - m + 2) / (4 * (m - 1)) + (m - 2)
        h1 = m * (m - 1) / 2 - m * h2 + h3 * (n + m + 2) * (n - m) / 8
        return h1 * compute_radial_polynomial(n, m, rho) + (
            h2 + h3 / rho**2) * compute_radial_polynomial(n, m - 2, rho)
        # p = n
        # q = m
        # h3 = -4 * (q - 2) * (q - 3) / ((p + q - 2) * (p - q + 4))
        # h2 = h3 * (p + q) * (p - q + 2) / (4 * (q - 1)) + (q - 2)
        # h1 = q * (q - 1) / 2 - q * h2 + h3 * (p + q + 2) * (p - q) / 8
        # return h1 * compute_radial_polynomial(p, q + 4, rho) + (
        #     h2 + h3 / rho**2) * compute_radial_polynomial(p, q + 2, rho)


R_POINTS = 100
THETA_POINTS = 360
r = np.linspace(0.01, 1, R_POINTS)
theta = np.linspace(0, 2 * np.pi, THETA_POINTS)


def compute_zernike(n, m, rho, theta):
    abs_m = np.abs(m)
    radial = compute_radial_polynomial(n, abs_m, rho)
    azimuthal_func = np.cos if m > 0 else np.sin
    azimuthal = azimuthal_func(abs_m * theta)
    return radial * azimuthal


radius_matrix, theta_matrix = np.meshgrid(r, theta)

# z51 = compute_zernike(5, 1, radius_matrix, theta_matrix)
# z51 = compute_zernike(5, 1, radius_matrix, theta_matrix)
# result = z51 * 1.2 + z11 * 1.5
result = compute_zernike(6, 0, radius_matrix, theta_matrix)

x = radius_matrix * np.cos(theta_matrix)
y = radius_matrix * np.sin(theta_matrix)

ax = plt.subplot(111)
ax.scatter(x, y, c=result)
ax.set_aspect(1)
plt.show()

# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# ax.plot_surface(x, y, result, vmin=result.min() * 2)
# plt.show()

# ax = plt.subplot(111, polar=True)
# ax.plot(theta_matrix, radius_matrix, color='r', ls='none', marker='.')
# plt.show()

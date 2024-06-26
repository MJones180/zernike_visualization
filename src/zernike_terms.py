# ==============================================================================
# Only configured to calculate the first 24 Zernike terms
# ==============================================================================

# Range of Zernike Noll terms, (inclusive, exclusive)
ZERNIKE_TERM_RANGE = (1, 25)

# Names of the Zernike terms in Noll index format
ZERNIKE_TERM_NAMES = {
    1: 'Piston',
    2: 'Tilt X',
    3: 'Tilt Y',
    4: 'Power',
    5: 'Astig 1',
    6: 'Astig 2',
    7: 'Coma 1',
    8: 'Coma 2',
    9: 'Trefoil 1',
    10: 'Trefoil 2',
    11: 'Spherical',
    12: '2nd Astig 1',
    13: '2nd Astrig 2',
    14: 'Tetrafoil 1',
    15: 'Tetrafoil 2',
    16: '2nd Coma 1',
    17: '2nd Coma 2',
    18: '2nd Trefoil 1',
    19: '2nd Trefoil 2',
    20: 'Pentafoil 1',
    21: 'Pentafoil 2',
    22: '2nd Spherical',
    23: '3rd Astig 1',
    24: '3rd Astig 2',
}

# Dictionary of { noll_term: (n [radial index], m [azimuthal index]) }
ZERNIKE_NOLL_LOOKUP = {
    1: (0, 0),
    2: (1, 1),
    3: (1, -1),
    4: (2, 0),
    5: (2, -2),
    6: (2, 2),
    7: (3, -1),
    8: (3, 1),
    9: (3, -3),
    10: (3, 3),
    11: (4, 0),
    12: (4, 2),
    13: (4, -2),
    14: (4, 4),
    15: (4, -4),
    16: (5, 1),
    17: (5, -1),
    18: (5, 3),
    19: (5, -3),
    20: (5, 5),
    21: (5, -5),
    22: (6, 0),
    23: (6, -2),
    24: (6, 2),
}

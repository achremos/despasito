import numpy as np
import logging
import os

if 'NUMBA_DISABLE_JIT' in os.environ:
    disable_jit = os.environ['NUMBA_DISABLE_JIT']
else:
    from .. import disable_jit

if disable_jit:
    os.environ['NUMBA_DISABLE_JIT'] = '1'

from numba import jit

from .constants import ckl_coef

@jit(nopython=True)
def calc_a1s_2d(rho, Cmol2seg, l_kl, zetax, epsilonkl, dkl):
    r""" 
    Return a1s,kl(rho*Cmol2seg,l_kl) in K as defined in eq. 25, used in the calculation of :math:`A_1` the first order term of the perturbation expansion corresponding to the mean-attractive energy.

    Parameters
    ----------
    rho : numpy.ndarray
        Number density of system [molecules/m^3]
    Cmol2seg : float
        Conversion factor from from molecular number density, :math:`\rho`, to segment (i.e. group) number density, :math:`\rho_S`. Shown in eq. 13
    l_kl : numpy.ndarray
        Matrix of mie potential exponents for k,l groups
    zetax : numpy.ndarray
        Matrix of hypothetical packing fraction based on hard sphere diameter for groups (k,l)
    epsilonkl : numpy.ndarray
        Matrix of well depths for groups (k,l)
    dkl : numpy.ndarray
        Matrix of hardsphere diameters for groups (k,l)

    Returns
    -------
    a1s : numpy.ndarray
        Matrix used in the calculation of :math:`A_1` the first order term of the perturbation expansion corresponding to the mean-attractive energy, size is the Ngroups by Ngroups
    """

    logger = logging.getLogger(__name__)
    # Andrew: why is the 4 hard-coded here?

    nbeads = len(dkl)
    zetax_pow = np.zeros((rho.size, 4))
    zetax_pow[:, 0] = zetax
    for i in range(1, 4):
        zetax_pow[:, i] = zetax_pow[:, i - 1] * zetax_pow[:, 0]

    # check if you have more than 1 bead types
    etakl = np.zeros((len(rho), nbeads, nbeads))

    for k in range(nbeads):
        for l in range(nbeads):
            etakl[:, k, l] = np.dot( zetax_pow, np.dot(ckl_coef, np.array( (1.0, 1.0/l_kl[k, l], 1.0/l_kl[k, l]**2, 1.0/l_kl[k, l]**3) )) )

    a1s = (1.0 - (etakl / 2.0)) / ((1.0 - etakl)**3) * -2.0 * np.pi * Cmol2seg * ((epsilonkl * (dkl**3)) / (l_kl - 3.0))
    return (a1s.T * rho).T

@jit(nopython=True)
def calc_a1s_1d(rho, Cmol2seg, l_kl, zetax, epsilonkl, dkl):
    r""" 
    Return a1s,kl(rho*Cmol2seg,l_kl) in K as defined in eq. 25, used in the calculation of :math:`A_1` the first order term of the perturbation expansion corresponding to the mean-attractive energy.

    Parameters
    ----------
    rho : numpy.ndarray
        Number density of system [molecules/m^3]
    Cmol2seg : float
        Conversion factor from from molecular number density, :math:`\rho`, to segment (i.e. group) number density, :math:`\rho_S`. Shown in eq. 13
    l_kl : numpy.ndarray
        Matrix of mie potential exponents for k,l groups
    zetax : numpy.ndarray
        Matrix of hypothetical packing fraction based on hard sphere diameter for groups (k,l)
    epsilonkl : numpy.ndarray
        Matrix of well depths for groups (k,l)
    dkl : numpy.ndarray
        Matrix of hardsphere diameters for groups (k,l)

    Returns
    -------
    a1s : numpy.ndarray
        Matrix used in the calculation of :math:`A_1` the first order term of the perturbation expansion corresponding to the mean-attractive energy, size is the Ngroups by Ngroups
    """

    nbeads = len(dkl)
    zetax_pow = np.zeros((rho.size, 4))
    zetax_pow[:, 0] = zetax
    for i in range(1, 4):
        zetax_pow[:, i] = zetax_pow[:, i - 1] * zetax_pow[:, 0]

    # check if you have more than 1 bead types
    etakl = np.zeros((len(rho), nbeads))

    for k in range(nbeads):
        etakl[:, k] = np.dot( zetax_pow, np.dot(ckl_coef, np.array( (1.0, 1.0/l_kl[k], 1.0/l_kl[k]**2, 1.0/l_kl[k]**3) ) ))

    a1s = (1.0 - (etakl / 2.0)) / (1.0 - etakl)**3 * (- 2.0 * np.pi * Cmol2seg * ((epsilonkl * (dkl**3)) / (l_kl - 3.0) ))

    return (a1s.T * rho).T
import faulthandler
faulthandler.enable()
import os

import tables as tb
import numpy as np
from scipy.linalg import expm

import bright
import mass_stream
import isoname

from metasci.graph import StairStepEnergy

bright_config = bright.bright_config
MassStream = mass_stream.MassStream
FluencePoint = bright.FluencePoint
ReactorParameters = bright.ReactorParameters
ReactorMG = bright.ReactorMG

#libfile = os.getenv("BRIGHT_DATA") + 'lwr_mg.h5'
libfile = os.path.abspath('../DataXS/lwr2/lwr2.h5')
bright.load_track_isos_hdf5(libfile)

bright_config.verbosity = 100

#default_rp = bright.ReactorParameters()
default_rp = bright.lwr_defaults()

default_rp.batches = 3
default_rp.flux = 4*(10**14)

default_rp.fuel_form = {"IHM": 1.0, "O16": 2.0}
default_rp.cladding_form = {"ZR93": 0.5, "ZR95": 0.5}
default_rp.coolant_form = {"H1": 2.0, "O16": 1.0}

default_rp.fuel_density = 10.7
default_rp.cladding_density = 5.87
default_rp.coolant_density = 0.73

default_rp.pnl = 0.98
default_rp.BUt = 50.0
default_rp.use_disadvantage_factor = True
#default_rp.use_disadvantage_factor = False
#default_rp.lattice_type = 'Cylindrical'
default_rp.lattice_type = 'Spherical'
#default_rp.lattice_type = 'Planar'
default_rp.rescale_hydrogen = True

#default_rp.burn_times = np.linspace(0.0, 4200.0, 5)
#default_rp.burn_times = np.linspace(0.0, 100.0, 5)
#default_rp.burn_times = np.linspace(0.0, 5.0, 5)
#default_rp.burn_times = np.linspace(0.0, 2100.0, 5)
default_rp.burn_times = np.linspace(0.0, 365.0, 10)


vers = ''

#rmg = None


def pyphi(rmg, s=0):
    k0 = 1.0
    k1 = 1.0
    phi0 = np.ones(rmg.G, dtype=float)
    phi1 = np.ones(rmg.G, dtype=float)

    print "phi0 = ", phi0
    print
    for i in range(100):
        phi1 = (1.0 / k0) * np.dot(rmg.A_inv_F_tgh[s], phi0)
        k1 = k0 * sum(rmg.nubar_Sigma_f_tg[s] * phi1) / sum(rmg.nubar_Sigma_f_tg[s] * phi0)

        print "k1 = ", k1
        print "phi1 = ", phi1
        print 

        if abs(1.0 - k0/k1) < 0.005 and (abs(1.0 - phi0/phi1) < 0.005).all():
            print i
            break

        k0 = k1
        phi0 = phi1

    k_num = (rmg.V_fuel * rmg.nubar_Sigma_f_fuel_tg[s] * phi0).sum()
    k_den = ((rmg.V_fuel * rmg.Sigma_a_fuel_tg[s] * phi0) + (rmg.V_cool * rmg.Sigma_a_cool_tg[s] * phi0 * rmg.zeta_tg[s])).sum()
    k = k_num / k_den

    return k, phi0


def pyT(rmg, s=1):
    J_order = rmg.J_order
    J_index = rmg.J_index
    J_size = len(J_order)

    phi = rmg.phi_t[s-1]
    phi_g = rmg.phi_tg[s-1]

    dm = rmg.decay_matrix
    fpym = rmg.fission_product_yield_matrix

    sigma_f_itg = rmg.sigma_f_itg
    sigma_gamma_itg = rmg.sigma_gamma_itg
    sigma_2n_itg = rmg.sigma_2n_itg
    sigma_3n_itg = rmg.sigma_3n_itg
    sigma_alpha_itg = rmg.sigma_alpha_itg
    sigma_proton_itg = rmg.sigma_proton_itg
    sigma_gamma_x_itg = rmg.sigma_gamma_x_itg
    sigma_2n_x_itg = rmg.sigma_2n_x_itg

    A = np.zeros((J_size, J_size), dtype=float)

    def lamda_eff(i, ind):
        l = 0.0 
        l += -dm[ind, ind]

        l += sum(phi_g * sigma_f_itg[i][s] * 1E-24)
        l += sum(phi_g * sigma_gamma_itg[i][s] * 1E-24)
        l += sum(phi_g * sigma_2n_itg[i][s] * 1E-24)
        l += sum(phi_g * sigma_3n_itg[i][s] * 1E-24)
        l += sum(phi_g * sigma_alpha_itg[i][s] * 1E-24)
        l += sum(phi_g * sigma_proton_itg[i][s] * 1E-24)
        l += sum(phi_g * sigma_gamma_x_itg[i][s] * 1E-24)
        l += sum(phi_g * sigma_2n_x_itg[i][s] * 1E-24)

        return l


    def b_eff(i, j, ind, jnd):
        b = 0.0
        b += dm[ind, jnd]

        # Get from isos
        j_gamma = ((i/10) + 1) * 10;
        j_2n = j_gamma - 20;
        j_3n = j_2n - 10;
        j_alpha = j_3n - 20010;
        j_proton = j_gamma - 10010;
        j_gamma_x = j_gamma + 1;
        j_2n_x = j_2n + 1;

        # Add the fission source
        b += sum(fpym[ind][jnd] * phi_g * sigma_f_itg[i][s] * 1E-24)

        # Add the capture cross-section
        if j == j_gamma:
            b += sum(phi_g * sigma_gamma_itg[i][s] * 1E-24)

        # Add the (n, 2n) cross-section
        if j == j_2n:
            b += sum(phi_g * sigma_2n_itg[i][s] * 1E-24)

        # Add the (n, 3n) cross-section
        if j == j_3n:
            b += sum(phi_g * sigma_3n_itg[i][s] * 1E-24)

        # Add the (n, alpha) cross-section
        if j == j_alpha:
            b += sum(phi_g * sigma_alpha_itg[i][s] * 1E-24)

        # Add the (n, proton) cross-section
        if j == j_proton:
            b += sum(phi_g * sigma_proton_itg[i][s] * 1E-24)

        # Add the capture (excited) cross-section
        if j == j_gamma_x:
            b += sum(phi_g * sigma_gamma_x_itg[i][s] * 1E-24)

        # Add the (n, 2n *) cross-section
        if j == j_2n_x:
            b += sum(phi_g * sigma_2n_x_itg[i][s] * 1E-24)

        return b


    for i in J_order:
        ind = J_index[i]

        for j in J_order:
            jnd = J_index[j]

            if i == j:
                A[ind, jnd] += -lamda_eff(i, ind)
            else:
                A[ind, jnd] += b_eff(j, i, jnd, ind)

            if np.isnan(A[ind, jnd]):
                A[ind, jnd] = 0.0

        print ind

    print "A:"
    print A
    print
    print "A diag:"
    print A.diagonal()
    print

    dt = (rmg.burn_times[s] - rmg.burn_times[s-1]) * 86400.0

    Adt = A * dt
    exp_Adt = expm(Adt)

    print "e^Adt:"
    print exp_Adt
    print
    print "e^Adt diag:"
    print exp_Adt.diagonal()

    x = np.zeros(len(J_order), dtype=float)
    got_x = np.zeros(len(J_order), dtype=float)
    T_it = rmg.T_it
    for jnd, j in enumerate(J_order):
        x[jnd] = T_it[j][s-1]
        got_x[jnd] = T_it[j][s]
        

    print
    print "Prev x:"
    print x

    new_x = np.dot(exp_Adt, x)
    print
    print "New x:"
    print new_x

    print 
    print "Got x:"
    print got_x

    print 
    print "Diff:"
    print new_x - got_x

    cd = {i: mass for i, mass in zip(rmg.J_order, new_x)}
    ms = mass_stream.MassStream(cd)
    print 
    ms.print_ms()

    return ms

if __name__ == '__main__':

    default_rp.fuel_radius = 0.412
    default_rp.void_radius = 0.4205
    default_rp.clad_radius = 0.475
    default_rp.unit_cell_pitch = 1.33

    default_rp.open_slots = 25
    default_rp.total_slots = 289

    name = 'norm'

    print 'Running figure {0}...'.format(name)

    rmg = ReactorMG(reactor_parameters=default_rp, name='rmg')
    rmg.loadlib(libfile)

    rmg.ms_feed = MassStream({922350: 0.05, 922380: 0.95})
#    rmg.ms_feed = MassStream({922350: 0.03, 922380: 0.97})
#    rmg.ms_feed = MassStream({922350: 0.01, 922380: 0.99})
    rmg.burnup_core()
    rmg.burn_time = 0.0
    rmg.bt_s = 0

    StairStepEnergy(rmg.phi_tg[0][::-1], energy_bins=rmg.E_g[::-1], 
        ylabel='$\\phi$ [relative]', 
        xlabel='Energy [MeV], k = {0:.4}'.format(rmg.k_t[0]), 
        name=name + str(vers))

    st = rmg.Sigma_t_fuel_tg
    sa = rmg.Sigma_a_fuel_tg
    sf = rmg.Sigma_f_fuel_tg
    ss = rmg.Sigma_s_fuel_tgh

#    print pyphi(rmg)
#    x = pyT(rmg)

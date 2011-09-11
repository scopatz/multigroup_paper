import faulthandler
faulthandler.enable()
import os

import tables as tb
import numpy as np

import bright
import mass_stream
import isoname

from metasci.graph import StairStepEnergy

bright_config = bright.bright_config
MassStream = mass_stream.MassStream
FluencePoint = bright.FluencePoint
ReactorParameters = bright.ReactorParameters
ReactorMG = bright.ReactorMG

libfile = os.getenv("BRIGHT_DATA") + 'lwr_mg.h5'
bright.load_track_isos_hdf5(libfile)


#default_rp = bright.ReactorParameters()
default_rp = bright.lwr_defaults()

default_rp.batches = 3
default_rp.flux = 2*(10**14)

default_rp.fuel_form = {"IHM": 1.0, "O16": 2.0}
default_rp.cladding_form = {"ZR93": 0.5, "ZR95": 0.5}
default_rp.coolant_form = {"H1": 2.0, "O16": 1.0}

default_rp.fuel_density = 10.7
default_rp.cladding_density = 5.87
default_rp.coolant_density = 0.73

default_rp.pnl = 0.98
default_rp.BUt = 50.0
default_rp.use_disadvantage_factor = True
#default_rp.lattice_type = 'Cylindrical'
default_rp.lattice_type = 'Spherical'
default_rp.rescale_hydrogen = True

#default_rp.burn_times = np.linspace(0.0, 4200.0, 5)
#default_rp.burn_times = np.linspace(0.0, 100.0, 5)
default_rp.burn_times = np.linspace(0.0, 2100.0, 5)


vers = ''

#rmg = None


def run_rx(rp, name):
    print 'Running figure {0}...'.format(name)

    rmg = ReactorMG(reactor_parameters=rp, name='rmg')
    rmg.loadlib(libfile)

    rmg.ms_feed = MassStream({922350: 0.05, 922380: 0.95})
#   rmg.ms_feed = MassStream({922350: 0.03, 922380: 0.97})
    rmg.burnup_core()
    rmg.burn_time = 0.0
    rmg.bt_s = 0

    StairStepEnergy(rmg.phi_tg[0][::-1], energy_bins=rmg.E_g[::-1], 
        ylabel='$\\phi$ [relative]', 
        xlabel='Energy [MeV], k = {0:.4}'.format(rmg.k_t[0]), 
        name=name + str(vers))

    import pdb; pdb.set_trace()


def run_norm():
    default_rp.fuel_radius = 0.412
    default_rp.void_radius = 0.4205
    default_rp.clad_radius = 0.475
    default_rp.unit_cell_pitch = 1.33

    default_rp.open_slots = 25
    default_rp.total_slots = 289

    run_rx(default_rp, 'norm')


def run_fuel():
    # Only Fuel
    default_rp.fuel_radius = 0.412
    default_rp.void_radius = 0.412
    default_rp.clad_radius = 0.412
    default_rp.unit_cell_pitch = 0.412 * np.sqrt(np.pi)

    default_rp.open_slots = 0
    default_rp.total_slots = 289

    run_rx(default_rp, 'fuel')


def run_cool():
    # Only Cool
    default_rp.fuel_radius = 0.001
    default_rp.void_radius = 0.0
    default_rp.clad_radius = 0.0
    default_rp.unit_cell_pitch = 1.33

    default_rp.open_slots = 0
    default_rp.total_slots = 289

    run_rx(default_rp, 'cool')



if __name__ == '__main__':
    run_norm()
#    run_fuel()
#    run_cool()

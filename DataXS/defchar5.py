#############################
### General specifcations ###
#############################
reactor = "lwr5"
burn_regions = 10                               # Number of burnup annular regions.
burn_time   = 4200								# Number of days to burn the material [days]	
#time_step = 525								# Coarse Time step by which to increment the burn, for MCNP [days]
time_step = 2100								# Coarse Time step by which to increment the burn, for MCNP [days]
email      = "scopatz@gmail.com"		    	# E-mail address to send job information to.

#scheduler = "PBS"
run_serpent_in = 'python'

number_cpus   = 2   # Number of CPUs to run transport code on.
cpus_per_node = 2   # Processors per node

verbosity = 100

# Set isotopes to track
from char.iso_track import load, transmute
core_load_isos      = load           # Initial core loading nuclide list or file
core_transmute_isos = transmute      # Transmutation tracking nuclide list or file


# Load stock template string from char
# Having this allows users to specify other templates
from char.templates.lwr import serpent
xs_gen_template = serpent.xs_gen
burnup_template = serpent.burnup


################################
### Unit Cell Sepcifications ###
################################
fuel_cell_radius = 0.410
void_cell_radius = 0.4185
clad_cell_radius = 0.475
unit_cell_pitch  = 0.65635 * 2.0 
unit_cell_height = 10.0

#fuel_density = [10.7, 10.7*0.9, 10.7*1.1]   # Denisty of Fuel
fuel_density = [10.7*0.95, 10.7*1.05]   # Denisty of Fuel
clad_density = 5.87                         # Cladding Density
cool_density = 0.73                         # Coolant Density

fuel_specific_power = 40.0 / 1000.0   # Power garnered from fuel [MW / kg]


###########################
### MCNPX Specification ###
###########################
# LEU
initial_heavy_metal = {     # Initial heavy metal mass fraction distribution
    922350: 0.04, 
    922380: 0.96, 
    }

#initial_U235 = [0.02, 0.04, 0.06]

initial_heavy_metal = {     # Initial heavy metal mass fraction distribution
    922340: 0.01, 
    922350: 0.04, 
    922380: 0.95, 
    }

#initial_U235 = [0.02, 0.04, 0.06]
initial_U235 = [0.03, 0.05]

#sensitivity_mass_fractions = [1.1, 0.9]

# UOX
fuel_chemical_form = {                 #Dictionary of initial fuel loading. 
    80160: 2.0, 
    "IHM": 1.0, 
    }	


fuel_form_mass_weighted = True  # Flag that determines if the fuel form should be mass weighted (True) or atom weighted (False)

#k_particles   = 5000      #Number of particles to run per kcode cycle
#k_particles   = 1000      #Number of particles to run per kcode cycle
k_particles   = 100      #Number of particles to run per kcode cycle
k_cycles      = 130       #Number of kcode cycles to run
k_cycles_skip = 30        #Number of kcode cycles to run but not tally at the begining.

group_structure = [ 1.00000000e-11,   5.00000000e-09,   1.00000000e-08,
                    1.50000000e-08,   2.00000000e-08,   2.50000000e-08,
                    3.00000000e-08,   3.50000000e-08,   4.20000000e-08,
                    5.00000000e-08,   5.80000000e-08,   6.70000000e-08,
                    8.00000000e-08,   1.00000000e-07,   1.52000000e-07,
                    2.51000000e-07,   4.14000000e-07,   6.83000000e-07,
                    1.12500000e-06,   1.85500000e-06,   3.05900000e-06,
                    5.04300000e-06,   8.31500000e-06,   1.37100000e-05,
                    2.26000000e-05,   3.72700000e-05,   6.14400000e-05,
                    1.01300000e-04,   1.67000000e-04,   2.75400000e-04,
                    4.54000000e-04,   7.48500000e-04,   1.23400000e-03,
                    2.03500000e-03,   2.40400000e-03,   2.84000000e-03,
                    3.35500000e-03,   5.53100000e-03,   9.11900000e-03,
                    1.50300000e-02,   1.98900000e-02,   2.55400000e-02,
                    4.08700000e-02,   6.73800000e-02,   1.11100000e-01,
                    1.83200000e-01,   3.02000000e-01,   3.88700000e-01,
                    4.97900000e-01,   6.39279000e-01,   8.20850000e-01,
                    1.10803000e+00,   1.35335000e+00,   1.73774000e+00,
                    2.23130000e+00,   2.86505000e+00,   3.67879000e+00,
                    4.96585000e+00,   6.06500000e+00,   1.00000000e+01,
                    1.49182000e+01,   1.69046000e+01,   2.00000000e+01,
                    2.50000000e+01]

# Temperature
# Should be a positive multiple of 300 K (ie 300, 600, 900, etc)
temperature = 600


###################################
### Remote Server Specification ###
###################################
remote_url  = "nukestar.me.utexas.edu"						#Remote server address
remote_user = "scopatz"								#Remoter username
remote_dir  = "/home/scopatz/"							#Remote directory to store files.
remote_gateway = 'nukestar01'


#############################
### Serpent Specification ###
#############################

serpent_xsdata = "/usr/share/serpent/xsdata/endf7.xsdata"               # Specifiy which XS library of serpent's to use.
#serpent_xsdata = "/usr/share/serpent/xsdata/jeff311.xsdata"               # Specifiy which XS library of serpent's to use.

# The following two are only needed for burnup runs
serpent_decay_lib = "/usr/share/serpent/xsdata/sss_endfb7.dec"          # Specifiy which decay library of serpent's to use.
serpent_fission_yield_lib = "/usr/share/serpent/xsdata/sss_endfb7.nfy"  # Specifiy which decay library of serpent's to use.
#serpent_decay_lib = "/usr/share/serpent/xsdata/sss_jeff311.dec"          # Specifiy which decay library of serpent's to use.
#serpent_fission_yield_lib = "/usr/share/serpent/xsdata/sss_jeff311.nfy"  # Specifiy which decay library of serpent's to use.

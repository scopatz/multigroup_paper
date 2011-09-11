#############################
### General specifcations ###
#############################
reactor = "fr1"
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
fuel_cell_radius = 0.3115
void_cell_radius = 0.3115
clad_cell_radius = 0.3115
unit_cell_pitch  = 0.8162637 
unit_cell_height = 10.0

#fuel_density = [10.7, 10.7*0.9, 10.7*1.1]   # Denisty of Fuel
fuel_density = [18.0*0.95, 18.0*1.05]   # Denisty of Fuel
clad_density = 0.927                         # Cladding Density
cool_density = 0.927                         # Coolant Density

fuel_specific_power = 40.0 / 1000.0   # Power garnered from fuel [MW / kg]


###########################
### MCNPX Specification ###
###########################
initial_heavy_metal = {     # Initial heavy metal mass fraction distribution
    922340: 2.097600E-07, 
    922350: 1.399700E-03, 
    922360: 6.438000E-06,
    922380: 7.041000E-01,
    932370: 1.391600E-02,
    942380: 6.759000E-03,
    942390: 1.407000E-01,
    942400: 6.640000E-02,
    942410: 3.134100E-02,
    942420: 1.939100E-02, 
    952410: 9.944000E-03,
    952421: 1.884700E-05,
    952430: 4.408000E-03,
    962420: 2.947900E-07,
    962430: 1.507600E-05,
    962440: 1.545200E-03,
    962450: 1.229400E-04, 
    962460: 1.550600E-05,
    }


# Metal
fuel_chemical_form = {                 #Dictionary of initial fuel loading. 
    "IHM": 1.0, 
    }


fuel_form_mass_weighted = True  # Flag that determines if the fuel form should be mass weighted (True) or atom weighted (False)

cool_chemical_form = clad_chemical_form = {
    110230: 1.0,
    }

k_particles   = 5000      #Number of particles to run per kcode cycle
#k_particles   = 1000      #Number of particles to run per kcode cycle
#k_particles   = 100      #Number of particles to run per kcode cycle
k_cycles      = 130       #Number of kcode cycles to run
k_cycles_skip = 30        #Number of kcode cycles to run but not tally at the begining.

group_structure = [1.0e-09, 1.0e-08, 1.0e-07, 1.0e-06, 1.0e-05, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0]


lattice_xy = 15

lattice = ("2 2 2 2 2 2 2 2 2 2 2 2 2 2 2\n"
           "2 2 2 2 2 2 2 1 2 2 2 2 2 2 2\n"
           "2 2 2 2 2 2 1 1 1 2 2 2 2 2 2\n"
           "2 2 2 2 2 1 1 1 1 1 2 2 2 2 2\n"
           "2 2 2 2 1 1 1 1 1 1 1 2 2 2 2\n"
           "2 2 2 1 1 1 1 1 1 1 1 1 2 2 2\n"
           "2 2 1 1 1 1 1 1 1 1 1 1 1 2 2\n"
           "2 1 1 1 1 1 1 1 1 1 1 1 1 1 2\n"
           "2 1 1 1 1 1 1 1 1 1 1 1 1 1 2\n"
           "2 1 1 1 1 1 1 1 1 1 1 1 1 1 2\n"
           "2 1 1 1 1 1 1 1 1 1 1 1 1 1 2\n"
           "2 1 1 1 1 1 1 1 1 1 1 1 1 1 2\n"
           "2 1 1 1 1 1 1 1 1 1 1 1 1 1 2\n"
           "2 1 1 1 1 1 1 1 1 1 1 1 1 1 2\n"
           "2 2 1 1 1 1 1 1 1 1 1 1 1 2 2\n"
           "2 2 2 1 1 1 1 1 1 1 1 1 2 2 2\n"
           "2 2 2 2 1 1 1 1 1 1 1 2 2 2 2\n"
           "2 2 2 2 2 1 1 1 1 1 2 2 2 2 2\n"
           "2 2 2 2 2 2 1 1 1 2 2 2 2 2 2\n"
           "2 2 2 2 2 2 2 1 2 2 2 2 2 2 2\n"
           "2 2 2 2 2 2 2 2 2 2 2 2 2 2 2\n")

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

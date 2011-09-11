#############################
### General specifcations ###
#############################
reactor = "lwr"
burn_regions = 1                                # Number of burnup annular regions.
burn_time   = 4200								# Number of days to burn the material [days]	
time_step = 525								# Coarse Time step by which to increment the burn, for MCNP [days]
email      = "scopatz@gmail.com"		    	# E-mail address to send job information to.

scheduler = "PBS"

number_cpus   = 3   # Number of CPUs to run transport code on.
cpus_per_node = 4   # Processors per node

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

fuel_specific_power = 40.0 / 1000.0   # Power garnered from fuel [W / g]


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

k_particles   = 5000      #Number of particles to run per kcode cycle
k_cycles      = 130       #Number of kcode cycles to run
k_cycles_skip = 30        #Number of kcode cycles to run but not tally at the begining.

group_structure = [1.0e-09, 1.0e-08, 1.0e-07, 1.0e-06, 1.0e-05, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0]

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

RemotePathMPI  = "/usr/local/bin/mpiexec"					#Remote Path to 'mpirun'
RemotePathMCNP = "/usr/share/mcnpxv260/bin/mcnpx260"				#Remote Path to mcnp
RemoteDATAPATH = "/usr/share/mcnpxv260/lib/"					#Remote DATAPATH enviromental variable


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

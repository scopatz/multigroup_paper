#############################
### General specifcations ###
#############################
reactor = "lwr_moretime"
burn_regions = 1                                # Number of burnup annular regions.
burn_time   = 4200								# Number of days to burn the material [days]	
coarse_step = 840								# Coarse Time step by which to increment the burn, for MCNP [days]
fine_step   = 30         						# Shorter time step for ORIGEN runs [days]
#coarse_step = 2100								# Coarse Time step by which to increment the burn, for MCNP [days]
#fine_step   = 150								# Shorter time step for ORIGEN runs [days]
email      = "scopatz@gmail.com"		    	# E-mail address to send job information to.

transport_code = "Serpent"
scheduler = "PBS"

#number_cpus   = 4   # Number of CPUs to run transport code on.
number_cpus   = 3   # Number of CPUs to run transport code on.
cpus_per_node = 4   # Processors per node
#run_parallel = "PBS"

verbosity = 100

# Set isotopes to track
from char.iso_track import load, transmute
core_load_isos      = load           #Initial core loading nuclide list or file
core_transmute_isos = transmute      #Transmutation tracking nuclide list or file
# May also specify a file to load isotopes from
#core_load_isos = "coreloadisos.txt"

#from char.iso_track import uranium
#core_load_isos      = uranium           #Initial core loading nuclide list or file
#core_transmute_isos = uranium      #Transmutation tracking nuclide list or file


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

fuel_density = [10.7, 10.7*0.9, 10.7*1.1]   # Denisty of Fuel
clad_density = 5.87                         # Cladding Density
cool_density = 0.73                         # Coolant Density


###########################
### MCNPX Specification ###
###########################
# LEU
initial_heavy_metal = {     # Initial heavy metal mass fraction distribution
    922350: 0.04, 
    922380: 0.96, 
    }

# UOX
fuel_chemical_form = {                 #Dictionary of initial fuel loading. 
    80160: 2.0, 
    "IHM": 1.0, 
    }	

fuel_specific_power = 40.0 / 1000.0   # Power garnered from fuel [W / g]

fuel_form_mass_weighted = True  # Flag that determines if the fuel form should be mass weighted (True) or atom weighted (False)

#k_particles   = 5000      #Number of particles to run per kcode cycle
k_particles  = 1000      #Number of particles to run per kcode cycle
#k_particles  = 500       #Number of particles to run per kcode cycle
k_cycles      = 130       #Number of kcode cycles to run
k_cycles_skip = 30        #Number of kcode cycles to run but not tally at the begining.

CINDER_DAT = "/usr/share/MCNPX/v260/Data/cinder.dat" 	#path to cinder.dat file, needed for metastables...

#GroupStructure = "1.0e-9 98log 10.0"						#Any Valid MCNP Group structure.  Remember, these are upper energy bounds.
group_structure = [1.0000000000000001e-09, 1e-08, 9.9999999999999995e-08, 9.9999999999999995e-07, 1.0000000000000001e-05,
     0.0001, 0.001, 0.01, 0.10000000000000001, 1.0, 10.0]

# MCNP Tallies to compute.  
#from char.tally_types import mcnp_advanced
#tallies = mcnp_advanced

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

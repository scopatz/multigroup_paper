#############################
### General specifcations ###
#############################
reactor = "lwr6_benchmark"
burn_regions = 10                               # Number of burnup annular regions.
burn_time   = 365.0								# Number of days to burn the material [days]	
#time_step = 525								# Coarse Time step by which to increment the burn, for MCNP [days]
time_step = 40.5555555								# Coarse Time step by which to increment the burn, for MCNP [days]
email      = "scopatz@gmail.com"		    	# E-mail address to send job information to.

#scheduler = "PBS"
run_serpent_in = 'python'

number_cpus   = 2   # Number of CPUs to run transport code on.
cpus_per_node = 2   # Processors per node

verbosity = 100

# Set isotopes to track
from char.iso_track import load, transmute
core_load_isos      = load           # Initial core loading nuclide list or file
#core_transmute_isos = transmute      # Transmutation tracking nuclide list or file
core_transmute_isos = [
 10010,
 10030,
 20040,
 60140,
 80160,
110230,
170360,
280590,
280630,
340790,
360850,
380871,
380890,
380900,
380910,
380930,
380950,
380990,
381030,
390910,
390930,
400930,
400950,
410910,
410931,
410940,
410950,
410951,
420930,
430980,
430990,
441060,
461070,
471081,
481131,
501171,
501191,
501211,
501230,
501250,
501251,
501260,
511240,
511241,
511250,
511260,
521251,
531290,
551340,
551341,
551350,
551360,
551370,
551400,
551410,
551420,
551430,
551440,
551450,
551470,
561330,
561400,
561410,
611460,
611470,
621450,
621480,
621510,
621550,
631490,
631500,
631520,
631540,
631550,
631560,
822060,
822070,
822080,
822100,
832090,
882260,
882280,
892270,
902280,
902290,
902300,
902320,
912310,
922300,
922310,
922320,
922330,
922340,
922350,
922360,
922370,
922380,
922390,
932350,
932360,
932361,
932370,
932380,
932390,
932400,
932401,
932410,
942360,
942370,
942380,
942390,
942400,
942410,
942420,
942430,
942440,
942450,
942460,
952390,
952400,
952410,
952420,
952421,
952430,
952440,
952441,
952450,
952460,
962410,
962420,
962430,
962440,
962450,
962460,
962470,
962480,
962490,
962500,
962510,
972490,
982490,
982500,
982510,
982520,
]

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

#fuel_density = [10.7, 10.7*0.9, 10.7*1.1]  # Denisty of Fuel
fuel_density = 10.7                         # Denisty of Fuel
clad_density = 5.87                         # Cladding Density
cool_density = 0.73                         # Coolant Density

fuel_specific_power = 40.0 / 1000.0   # Power garnered from fuel [MW / kg]


###########################
### MCNPX Specification ###
###########################
# LEU

initial_heavy_metal = {     # Initial heavy metal mass fraction distribution
    922350: 0.045, 
    922380: 0.955, 
    }

# UOX
fuel_chemical_form = {                 #Dictionary of initial fuel loading. 
    80160: 2.0, 
    "IHM": 1.0, 
    }	


fuel_form_mass_weighted = True  # Flag that determines if the fuel form should be mass weighted (True) or atom weighted (False)

k_particles   = 5000      #Number of particles to run per kcode cycle
#k_particles   = 1000      #Number of particles to run per kcode cycle
#k_particles   = 100      #Number of particles to run per kcode cycle
k_cycles      = 130       #Number of kcode cycles to run
k_cycles_skip = 30        #Number of kcode cycles to run but not tally at the begining.

group_structure = [1.0e-09,        1.0e-08,        1.0e-07,        1.0e-06,   
                   1.66810054e-06, 2.78255940e-06, 4.64158883e-06, 7.74263683e-06,   
                   1.29154967e-05, 2.15443469e-05, 3.59381366e-05, 5.99484250e-05,
                   0.0001,         0.00031623,     0.001,          0.00316228, 
                   0.01,           0.1,            1.0,            10.0]

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

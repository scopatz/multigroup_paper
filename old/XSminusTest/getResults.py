KeyExchange = {"1": "(U234 + U235 + U238)",
	"2": "(U238)",
	"3": "(U235)",
	"4": "(U234)",
	"5": "(U235 + U238)",
	"6": "(U234 + U238)",
	"7": "(U234 + U235)",
	}

M = ""
InData = False

E = []
Flux = []
Raw = {}

with open("sphere.o", 'r') as f:
	for line in f:
		ls = line.split()

		if ls == []:
			if InData:
				InData = False
				M = ""
			continue	
		elif (ls[0] == "cell") and (ls[1] == "1"):
			InData = True
		elif InData and (ls[0] == "multiplier"):
			M = ls[-2]
			Raw[M] = []
			continue
		elif InData and (ls[0] == "energy"):
			continue
		elif InData and (M == ""):
			E.append(float(ls[0]))			
			Flux.append(float(ls[1]))			
			continue
		elif InData:
			Raw[M].append(float(ls[1]))
		else:
			continue

TotalFlux = 0.0
for f in Flux:
	TotalFlux = TotalFlux + f

Normalized = {}
for k in Raw.keys():
	Normalized[k] = []
	for n in range(len(Raw[k])):
#		Normalized[k].append( Raw[k][n] * Flux[n] / TotalFlux )
#		Normalized[k].append( Raw[k][n] / TotalFlux )
		if Flux[n] == 0.0:
			Normalized[k].append( 0.0 )
		else:
			Normalized[k].append( Raw[k][n] / Flux[n] )

OneGroupXS = {}
for k in Normalized.keys():
	OneGroupXS[k] = 0.0
	for e in  Normalized[k]:
		OneGroupXS[k] = OneGroupXS[k] + e


print("One Group XS:")
for k in sorted(OneGroupXS.keys()):
	print("\t{0}:{1:{2}}{3}".format(KeyExchange[k], "", len(KeyExchange["1"]) - len(KeyExchange[k]) + 1, OneGroupXS[k]))
print("")

def PrintOneGroupDif(j, k, jper):
	val = OneGroupXS["1"] - jper*OneGroupXS[j]
	valstr = KeyExchange["1"] + " - " + KeyExchange[j] 
	print("{0}: {1}".format(valstr, val))
	print("{0:{1}} {2}".format(KeyExchange[k] + ":", len(valstr)+1, (1.0 - jper)*OneGroupXS[k]))
	print("{0:{1}} {2}".format("Relative Error:", len(valstr)+1, (val - (1.0 - jper)*OneGroupXS[k])/val ))
	print("")

PrintOneGroupDif("7", "2", 0.50)
PrintOneGroupDif("6", "3", 0.75)
PrintOneGroupDif("5", "4", 0.75)

PrintOneGroupDif("2", "7", 0.50)
PrintOneGroupDif("3", "6", 0.25)
PrintOneGroupDif("4", "5", 0.25)

def PrintNormDif(j, k, jper, n):
	val = Normalized["1"][n] - jper*Normalized[j][n]
	valstr = KeyExchange["1"] + " - " + KeyExchange[j] 
	print("\t{0}: {1}".format(valstr, val))
	print("\t{0:{1}} {2}".format(KeyExchange[k] + ":", len(valstr)+1, (1.0 - jper)*Normalized[k][n]))
	print("\t{0:{1}} {2}".format("Relative Error:", len(valstr)+1, (val - (1.0 - jper)*Normalized[k][n])/val ))
	print("")

#for n in [50, 60, 70, 80, 90]:
for n in [60, 70, 80, 90]:
	print("Difference Example for Energy Range [{0}, {1}]".format(E[n], E[n+1]))
	PrintNormDif("7", "2", 0.50, n)
	PrintNormDif("6", "3", 0.75, n)
	PrintNormDif("5", "4", 0.75, n)

	PrintNormDif("2", "7", 0.50, n)
	PrintNormDif("3", "6", 0.25, n)
	PrintNormDif("4", "5", 0.25, n)


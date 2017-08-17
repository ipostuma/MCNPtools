# Preparo l'ambiente per fare il calcolo
from MCNPtools import Gen

# An MCNP output file extracted with readMCTAL.sh
tf141 = "../data/f141_test"

# Read tally data and store info
seg,cos,erg,f141 = Gen.ReadTally(tf141)

# Dfining bins in x (radial distance), cos (angle) and erg (energy)
x = [ 1, 2]
cos=[0, 0.5, 1]
erg =[1]

# Generiamo ora la SDEF
MySDEF = Gen.SDEF(x,cos,erg,f141)
ndis = MySDEF.PrintSDEF("347.4 0 0")

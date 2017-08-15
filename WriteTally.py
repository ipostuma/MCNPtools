from source import MCNPSdefGen as MSG

# example usage of the module
# first you initialize the tally by defining the bins: segment (surface number), angle (cosine) and energy (MeV)
myTally = MSG.TallyGen(cos=[-0.8721762, -0.34552435214, -0.23545612364, -0.12786316235, 0, .12123131, .34234234, .45453453, .65765757, .786753367, .9223163541, 1])
# Once the object is initlialized it can be used to print out the tally needed by MCNP giving:
# surface -> 999
# title -> test
# normFactor -> 1
myTally.PrintTally(999,"test",1)

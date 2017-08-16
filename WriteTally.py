from MCNPtools import Gen

# example usage of the module
# first you initialize the tally by defining the bins: segment (surface number), angle (cosine) and energy (MeV)
cos = [-0.5, 0, 0.5, 1]
myTally = Gen.Tally(cos)
# Once the object is initlialized it can be used to print out the tally needed by MCNP giving:
# surface -> 999
# title -> test
# normFactor -> 1
myTally.PrintTally(999,"test",1)

#!/usr/bin/python -W all
#
# https://github.com/kbat/mc-tools
#

import sys, argparse, string
from os import path, makedirs
from mctools.mcnp.mctal import MCTAL
import numpy as np
#import ROOT
#ROOT.PyConfig.IgnoreCommandLineOptions = True
sys.path.insert(1, '@pythondir@')

def main():
  """
  MCTAL reader.
  Converts \033[1mmctal\033[0m files produced by MCNP(X) into numpy binary.
  """
  parser = argparse.ArgumentParser(description=main.__doc__,
           epilog="Homepage: https://github.com/kbat/mc-tools")
  parser.add_argument('mctal', type=str, help='mctal file name')
  parser.add_argument('dir', type=str, nargs='?', help='directory output', default="")
  parser.add_argument('-v', '--verbose', action='store_true', default=False, dest='verbose', help='explain what is being done')

  arguments = parser.parse_args()

  if not path.isfile(arguments.mctal):
    print( sys.stderr, "mctal2root: File %s does not exist." % arguments.mctal)
    return 1

  m = MCTAL(arguments.mctal,arguments.verbose)

  T = m.Read()

  if m.thereAreNaNs:
    print( sys.stderr, " \033[1;30mOne or more tallies contain NaN values. Conversion will succeed anyway.\033[0m")

  if arguments.dir == "":
    DirToSave = path.dirname(arguments.mctal)+"/mOut"
  else:
    DirToSave = path.dirname(arguments.mctal)+"/"+arguments.dir

  if not path.exists(DirToSave):
    makedirs(DirToSave)

  if arguments.verbose:
    print("\n\033[1;34m[Converting...]\033[0m")

  for tally in T:

    #if arguments.dir == "":
    #    rootFileName = "%s%s" % (arguments.mctal,".txt")
    #else:
    #    rootFileName = arguments.root

    tallyLetter = "f"

    file_ = open(DirToSave+"/"+tallyLetter+str(tally.tallyNumber), 'w')

    if tally.radiograph:
      tallyLetter = tally.getDetectorType(True) # Here the argument set to True enables the short version of the tally type
    if tally.mesh:
      tallyLetter = tally.getDetectorType(True)

    nCells = tally.getNbins("f",False)

    nCora = tally.getNbins("i",False) # Is set to 1 even when mesh tallies are not present

    nCorb = tally.getNbins("j",False) # Is set to 1 even when mesh tallies are not present

    nCorc = tally.getNbins("k",False) # Is set to 1 even when mesh tallies are not present

    nDir = tally.getNbins("d",False)

    usrAxis = tally.getAxis("u")
    nUsr = tally.getNbins("u",False)

    segAxis = tally.getAxis("s")
    nSeg = tally.getNbins("s",True)

    nMul = tally.getNbins("m",False)

    cosAxis = tally.getAxis("c")
    nCos = tally.getNbins("c",False)

    ergAxis = tally.getAxis("e")
    nErg = tally.getNbins("e",False)

    timAxis = tally.getAxis("t")
    nTim = tally.getNbins("t",False)

    if tally.mesh == True:

      bins    = np.array( [nCells,   nDir,   nUsr,   nSeg,   nMul,   nCos,   nErg,   nTim,   nCora,   nCorb,   nCorc], dtype=np.dtype('i4') )

    else:

      bins    = np.array( [nCells,   nDir,   nUsr,   nSeg,   nMul,   nCos,   nErg,   nTim], dtype=np.dtype('i4'))
      binsMin = np.array( [0,        0,      0,      0,      0,      0,      0,      0], dtype=float)
      binsMax = np.array( [1,        1,      1,      1,      1,      1,      1,      1], dtype=float)

    for comment in tally.tallyComment:
        file_.write("#"+comment+"\n")
    file_.write("#seg\tcos\t\tenergy\t\t\t\tres\t\t\t\t\terr\n")
    for f in range(nCells):
      for d in range(nDir):
        for u in range(nUsr):
          for s in range(nSeg):
            seg=s+1
            for m in range(nMul):
              for c in range(nCos):
                cos=1
                if nCos>1:
                    cos=cosAxis[c]
                for e in range(nErg):
                  try:
                      erg=ergAxis[e]
                  except Exception as err:
                      erg=0
                  for t in range(nTim):
                    for k in range(nCorc):
                      for j in range(nCorb):
                        for i in range(nCora):
                          #print "f %i\nd %i\nu %i\ns %i\nm %i\nc %i\ne %i\nt %i\nk %i\nj %i\ni %i\n"%(f,d,u,s,m,c,e,t,k,j,i)#(f,d,u,s,m,c,e,t,k,j,i)
                          #print tally.getValue(f,d,u,s,m,c,e,t,i,j,k,0)
                          res = tally.getValue(f,d,u,s,m,c,e,t,i,j,k,0)
                          err = tally.getValue(f,d,u,s,m,c,e,t,i,j,k,1)
                          file_.write("%i\t\t%02i\t\t%1.4e\t\t\t%1.4e\t\t%1.4e\t%1.4e\n"%(f,seg,cos,erg,res,err*res))
    file_.close()
    if arguments.verbose:
      print(" \033[33mTally %5d saved\033[0m" % (tally.tallyNumber))


  print("\n\033[1;34mOut files saved to:\033[1;32m %s\033[0m\n" % (DirToSave))


if __name__ == "__main__":
    sys.exit(main())

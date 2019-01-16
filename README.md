# MCNPtools
This repo contains python modules and scripts that help managing MCNP simulations and outputs. 

## read MCTAL
To easily plot MCNP data, the script *scripts >  TallyRead.py* reads MCTAL files and generates the directory *mOut* containing a file for each implemented MCNP tally. These files are called by their tally name and contain the results separated in 6 columns:

1.  cell number
2.  segment number
3.  cosine value
4.  energy value
5.  tally output
6.  tally error

These files are easily imported with numpy into a python script and subsequently plotted with matplotlib or other plotting libraries.

## examples
* WriteTally.py -> An example script that uses Gen.Tally module to write a surface current tally
* WriteSDEF.py  -> An example script that uses Gen.SDEF modulte to write an MCNP SDEF source
* readMCTAL.sh  -> Bash script that uses the python module [mc-tools](https://github.com/kbat/mc-tools) to extract tally data into separate files.

## Requirements

* Python versione >= 2.7
* numpy
* matplotlib
* [mc-tools](https://github.com/kbat/mc-tools)

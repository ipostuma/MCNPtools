import numpy as np
import matplotlib.pyplot as plt
import math
import textwrap as tw
import sys

def ArrayPrintForMCNP(initSTR,array,predat=''):
    """ 
    This function helps to format MCNP data binning by keeping 
        each line shorter than 80 characters and by giving an 
        indentation of 5 characters after the first new line.
    """
    mySTR = initSTR
    for d in array:
        mySTR += " {}{}".format(predat,d)
    myText = tw.wrap(mySTR,initial_indent="",width=80,subsequent_indent="     ")
    for line in myText:
        print line

def strictly_increasing(L):
    """ 
    A function to check if a list of values is monotonically 
        increasing of not.
    """
    return all(x<y for x, y in zip(L, L[1:]))

class TallyGen:
    def __init__(self, seg=[1], cos=[1], erg=[10]):
        """ 
        Initialization of the SdefGen module.
            seg -> list of values that represent surface names
            cos -> list of cosine bins, remember that MCNP by 
                   default starts at  cos(theta) = -1
            erg -> list of energy biss, remember that MCNP by 
                   default starts at  0 MeV
        """
        self.seg = seg
        if strictly_increasing(cos):
            self.cos = cos
        else:
            print "Error: cosine bin values are not monotonically increasing"
            sys.exit()
        if strictly_increasing(erg):
            self.erg = erg
        else:
            print "Error: energy bin values are not monotonically increasing"
            sys.exit()
        
    def PrintTally(self,surf,comment,norm):
        """
        A tally is needed to generate a new SDEF in a certain 
            region of space. Therefore this function comes to 
            aid the user by implementing the source just by 
            reading the bin values given in the input:
            segments, cosine and energy bins.
        """
        print "c Neutron current in segment, cosine and energy binning"
        print "fc141 Current tally n/s"
        print "f141:n {}".format(surf)
        ArrayPrintForMCNP("c141",self.cos)
        print "tf141 3j j 1 j j j"
        print "fq141 c e s"
        print "fm141 {}".format(norm)
        ArrayPrintForMCNP("fs141",self.seg,"-")
        ArrayPrintForMCNP("sd141",["1",str(len(self.seg))+"R"],"")
        ArrayPrintForMCNP("sd141",self.erg,"")
     

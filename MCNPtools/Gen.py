import numpy as np
import matplotlib.pyplot as plt
import math
import textwrap as tw
import sys
from os import path, makedirs

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

def ArrayTextForMCNP(initSTR,array,predat=''):
    """ 
    This function helps to format MCNP data binning by keeping 
        each line shorter than 80 characters and by giving an 
        indentation of 5 characters after the first new line.
    """
    mySTR = initSTR
    for d in array:
        mySTR += " {}{}".format(predat,d)
    myText = tw.wrap(mySTR,initial_indent="",width=80,subsequent_indent="     ")
    return myText

def strictly_increasing(L):
    """ 
    A function to check if a list of values is monotonically 
        increasing of not.
    """
    return all(x<y for x, y in zip(L, L[1:]))
    
def ReadTally(myfile):
    """
    The main functions contains several methods to read tally results from an MCNP simulation,
    the function needs a file name as input to work.
    """

    if not path.isfile(myfile):
        print >> sys.stderr, "File %s does not exist." % myfile
        return 1

    # read tally file
    tally = np.loadtxt(myfile)
    # load segments bins
    seg = np.unique(tally[:,1])
    # load cosine bins
    cos = np.unique(tally[:,2])
    # load energy bins
    erg = np.unique(tally[:,3])

    # creation of the matrix containing tally results and errors
    nseg = len(seg)
    ncos = len(cos)
    nerg = len(erg)
    matrix = np.zeros((nseg,ncos,nerg,2))

    # insert data into the matrix
    myI = 0
    for s in range(nseg):
        for c in range(ncos):
            for e in range(nerg):
                matrix[s,c,e]=np.array([tally[myI,4],tally[myI,5]])
                myI+=1
                
    return seg,cos,erg,matrix

class Tally:
    def __init__(self, seg=[1], cos=[1], erg=[10]):
        """ 
        Initialization of the Tally class.
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
        
class SDEF:
    def __init__(self, seg, cos, erg, f141):
        """ 
        Initialization of the SDEF class.
            seg -> list of values that represent radial distance
            cos -> list of cosine bins
            erg -> list of energy bins
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
            
        # Tally f141 was generated with Gen.Tally therefore the result is binned in radial rings, 
        # in angle and energy. As a conseguence we have to compute the radial distribution FSi and 
        # angle distribution for each ring FSiCi.
        self.prob    = f141 
        self.FSi     = np.zeros( len(seg) )
        self.FSiCi   = []
        self.tot     = 0
        for s in range(len(seg)):
            sums = 0
            for c in range(1,len(cos)):
                sumsc = 0
                sumsc = sum(f141[s,c,:,0])
                self.tot += sumsc
                self.FSiCi.append(sumsc)
                sums += sumsc
            self.FSi[s] = sums
    
    def SdefStart(self,nPosDis,nRadDis,nCosDis,nErgDis,Title="Neutron Source generated from f141",vec="1 0 0"):
        print "c  ***********************************************************************"
        print "c  %s"%(Title)
        print "c"
        print "c  Norm Factor {:1.4e}".format(self.tot)
        print "c  ***********************************************************************"
        print "sdef pos=d{0} dir=fpos=d{2} erg=fpos=d{3} rad=fpos=d{1}".format(nPosDis,nRadDis,nCosDis,nErgDis)
        print "     vec {0} axs {0}".format(vec)
            
    def SdefPosPrint(self,pos,ndis=1):
        # create a position array
        myPosArr = [pos for i in range(len(self.FSiCi))]
        # write position si card
        myText  = ArrayTextForMCNP("si{}".format(ndis)+" L ",myPosArr,"  ")
        myText += ArrayTextForMCNP("sp{}".format(ndis)+"   ",self.FSiCi,"")
        return ndis,myText
        
    def SdefRadPrint(self,ndis=1,rep=1):
        x = np.concatenate((np.array([0]),np.array(self.seg)))
        IntDistr = 0 #per ricordarmi il nome delle distribuzioni
        k=ndis+1
        arrayk=[]
        arrayMULTk=[]
        myiter=0
        for i in range(len(x)-1):
            for j in range(rep):
                arrayMULTk.append(k)
            arrayk.append(k)
            IntDistr = k
            k+=1
        myText = ArrayTextForMCNP("ds{}".format(ndis)+" S ",arrayMULTk,"")
        for i in range(len(x)-1):
            myText += ArrayTextForMCNP("si{}".format(arrayk[i])+" H ",[x[i],x[i+1]]," ")
            myText += ArrayTextForMCNP("sp{}".format(arrayk[i])+"   ",[-21, 1]," ")
        return IntDistr, myText
        
    def SdefCosPrint(self,ndis=1,rep=1):
        arrayw=[]
        IntDistr=ndis+1
        for j in range(rep):
            IntDistr=ndis+1
            for i in range(len(self.cos)-1):
                arrayw.append(IntDistr)
                IntDistr+=1
        myText = ArrayTextForMCNP("ds{}".format(ndis)+" S ",arrayw,"")
        for i in range(len(self.cos)-1):
            myText += ArrayTextForMCNP("si{}".format(arrayw[i])+" H ",[self.cos[i],self.cos[i+1]]," ")
            myText += ArrayTextForMCNP("sp{}".format(arrayw[i])+"   ",[0, 1]," ")
            IntDistr=arrayw[i]
        return IntDistr, myText
    
    def SdefErgPrint(self,ndis=1,s=1,c=1):
        arrayq=[ ndis + 1 + i for i in range(s*c) ]
        myText = ArrayTextForMCNP("ds{}".format(ndis)+" S ",arrayq,"")
        myiter = 0
        IntDistr = ndis + 1 
        for i in range(s):
            for j in range(1,c+1):
                myText += ArrayTextForMCNP("si{}".format(arrayq[myiter])+" H  0",self.erg,"")
                myText += ArrayTextForMCNP("sp{}".format(arrayq[myiter])+"    0 ",self.prob[i,j,:,0],"")
                IntDistr = arrayq[myiter]
                myiter += 1
        return IntDistr, myText
        
    def PrintSDEF(self,pos,ndis=1):
        s = len(self.seg)
        c = len(self.cos)-1
        nPosDis,myTextPos = self.SdefPosPrint(pos,ndis)
        nRadDis,myTextRad = self.SdefRadPrint(nPosDis+1,c)
        nCosDis,myTextCos = self.SdefCosPrint(nRadDis+1,s)
        nErgDis,myTextErg = self.SdefErgPrint(nCosDis+1,s,c)
        
        myText = myTextPos + myTextRad + myTextCos + myTextErg
        self.SdefStart(nPosDis,nPosDis+1,nRadDis+1,nCosDis+1)
        for line in myText:
            print line
     

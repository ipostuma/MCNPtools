import numpy as np
import sys, argparse
from os import path, makedirs
import matplotlib.pyplot as plt
import math

def myplot(x, y, yerr, yscale, ylabel, xlabel, savefig, title="", verbose=False, xscale="linear", fmt=",-"):
    """
    This function helps plotting and saving data with error bars
    """
    plt.clf() # clear preceding plots
    plt.title(title)
    plt.errorbar(x,y,yerr=yerr,fmt=fmt)
    plt.yscale(yscale)
    plt.xscale(xscale)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.savefig(savefig)
    if verbose: # only show plot if asked
        plt.show()

def cos2sr(cos):
    """
    this bins converts cos values in sr and generates a normalized numpy array
    knowing the conversion function:
    sr = 2*math.pi*(1-cos)
    """
    cos2 = [ c for c in cos]
    cos2.append(1)
    sterad=[]
    steradnorm=[]
    for i in range(1,len(cos2)):
        steradnorm.append(2*math.pi*(1-(cos2[i-1]))-2*math.pi*(1-cos2[i]))
        sterad.append(2*math.pi*(1-(cos2[i-1]+cos2[i])/2))
    return sterad,steradnorm

def ReadTally(myfile):
    """
    The main functions contains several methods to read and plot tally results from an MCNP simulation,
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
    # generate steradiant bins and normalization array
    sterad,steradnorm = cos2sr(cos)
    # x bin from seg (cm)
    x = []
    for i in range(len(seg)-1):
        if i-1 >= 40 and i-1 < 41:
            x.append(i+10)
        elif i-1 >=41 and i-1 < 42:
            x.append(x[i-1]+25)
        elif i-1 >=42:
            x.append(x[i-1]+25)
        else:
            x.append(i+1)
    x.append(x[len(x)-1]+25)

    # creation of the matrix containing tally results and errors
    nseg = len(seg)
    ncos = len(cos)
    nerg = len(erg)
    matrix = np.zeros((nseg,ncos,nerg,2))

    #print "seg bin\t",nseg
    #print "cos bin\t",ncos
    #print "eng bin\t",nerg

    # insert data into the matrix
    myI = 0
    for s in range(nseg):
        for c in range(ncos):
            for e in range(nerg):
                matrix[s,c,e]=np.array([tally[myI,4],tally[myI,5]])
                myI+=1
                #print "s %i\nc %i\ne %i\n"%(s,c,e)

    # Questa e' la matrie con i dati:
    #   la prima colonna e' il segmento
    #   la seconda colonna e' il coseno
    #   la terza e' l'energia
    #   la quarta e' un array con due valori [y,yerr]

    # Print data from the matrix by recognizing the tally
    FileName = path.basename(myfile)
    FilePath = path.dirname(myfile)
    if FileName == "f1":
       return x,matrix
    if FileName == "f11":
       return x,matrix
    if FileName == "f2":
       return x,matrix
    if FileName == "f12":
       return x,matrix
    if FileName == "f111":
        return cos,matrix
    if FileName == "f112":
        return cos,matrix
    if FileName == "f141":
        return erg,matrix
    if FileName == "f142":
        return erg,matrix
    return x,matrix

def SdefPosPrint(pos,prob,ndis=1):
    print "si%i"%ndis,
    print " L ",
    k=0
    arrayk=[0]
    for i in range(len(prob)):
        k+=1
        if k % 5:
            print " ",pos,
        else:
            print ""
            print "     ",pos,
    print ""
    print "sp%i "%ndis,
    for i in range(len(prob)):
        if i % 6 or i == 0:
            print " ","%1.3e"%prob[i],
        else:
            print ""
            print "     ","%1.3e"%prob[i],
    return ndis

def SdefRadPrint(x,ndis=1,rep=1):
    IntDistr = 0 #per ricordarmi il nome delle distribuzioni
    k=ndis+1
    arrayk=[]
    myiter=0
    print ""
    print "ds%i "%ndis,
    print "S ",
    for i in range(len(x)-1):
        for j in range(rep):
            if (myiter) % 10:
                print " ",k,
            else:
                print ""
                print "     ",k,
            myiter+=1
        arrayk.append(k)
        IntDistr = k
        k+=1
    k=0
    print ""
    myiter=0
    for i in range(len(x)-1):
        print "si%i"%arrayk[myiter]," H ",x[i]," ",x[i+1]
        print "sp%i"%arrayk[myiter]," -21 1"
        myiter+=1
    return IntDistr

def SdefCosPrint(cos,ndis=1,rep=1):
    arrayw=[]
    IntDistr=ndis
    myiter=0
    print "ds%i "%ndis,
    print "S ",
    for j in range(rep):
        IntDistr=ndis+1
        for i in range(len(cos)-1):
            arrayw.append(IntDistr)
            if myiter % 10:
                print " ",IntDistr,
            else:
                print ""
                print "     ",IntDistr,
            myiter+=1
            IntDistr+=1
    myiter = 0
    for i in range(len(cos)-1):
        #for
        print ""
        print "si%i"%arrayw[myiter],
        print " H ",
        print "  ",cos[i]," ",cos[i+1]
        print "sp%i"%arrayw[myiter],
        print " 0 1",
        IntDistr=arrayw[myiter]
        myiter+=1
    print ""
    return IntDistr

def SdefEngPrint(erg,prob,ndis=1,s=1,c=1):
    # energy
    arrayq=[]
    IntDistr=ndis
    print "ds%i "%ndis,
    print " S ",
    for i in range(s):
        for j in range(c):
            IntDistr+=1
            if IntDistr % 6:
                print " ",IntDistr,
            else:
                print ""
                print "     ",IntDistr,
            arrayq.append(IntDistr)
    print ""
    myiter=0
    for i in range(s):
        for j in range(1,c+1):
            #for
            print "si%i"%arrayq[myiter],
            print " H",
            print " 0 ",
            myint=0
            for e in erg:
                myint+=1
                if myint % 5 or myint == 1:
                    print " ","%1.3e"%e,
                else:
                    print ""
                    print "     ","%1.3e"%e,
            print ""
            print "sp%i"%arrayq[myiter],
            print " 0 ",
            for ind in range(len(prob[i,j,:,0])):
                if ind % 5 or ind == 0:
                    print " ","%1.3e"%prob[i,j,ind,0],
                else:
                    print ""
                    print "     ","%1.3e"%prob[i,j,ind,0],
            print ""
            myiter+=1

def SdefStart(Title="Neutron Source generated from f141",NormFactor=0):
    print "c  ***********************************************************************"
    print "c  %s"%(Title)
    print "c"
    print "c  Norm Factor %1.4e"%(NormFactor)
    print "c  ***********************************************************************"
    print "sdef pos=d1 dir=fpos=d39 erg=fpos=d76 rad=fpos=d2"

def SdefPrint(x,erg,cos,f1,f111,f141):
    cos=np.array(cos)
    nc = len(cos)
    ns = len(x)
    x = np.concatenate((np.array([0]),np.array(x)))
    print "c  ***********************************************************************"
    print "c  Neutron Source generated from"
    print "c"
    print "c  Norm Factor %1.4e"%(sum(f1[0:ns,0,0,0]))
    print "c  ***********************************************************************"
    print "sdef sur=d1 dir=fsur=d2 erg=fsur=d3 rad=fsur=d4"
    print "     vec 1 0 0 axs 1 0 0 pos 45.95 0 0"

    # Get rad -1 e +1
    ForwardNeu  = [ f1[i,0,0,0] for i in range(len(x)-1)]
    # adesso ricreiamo la distribuzione
    print "si1",
    print " L ",
    k=0
    arrayk=[0]
    for i in range(len(x)-1):
        k+=1
        if k % 5:
            print " ",1001,
        else:
            print ""
            print "     ",1001,
    print ""
    print "sp1 ",
    for i in range(len(x)-1):
        if i % 2 or i == 0:
            print " ","%1.3e"%ForwardNeu[i],
        else:
            print ""
            print "     ","%1.3e"%ForwardNeu[i],
    # ora vediamo di scrivere bene i rad
    IntDistr = 0 #per ricordarmi il nome delle distribuzioni
    k=5
    arrayk=[]
    print ""
    print "ds4 ",
    print "S ",
    for i in range(len(x)-1):
        if (k) % 10 or (k)==10 or (k)==11:
            print " ",k,
        else:
            print ""
            print "     ",k,
        arrayk.append(k)
        IntDistr = k
        k+=1
    k=0
    print ""
    for i in range(len(x)-1):
        print "si%i"%arrayk[i]," H ",x[i]," ",x[i+1]
        print "sp%i"%arrayk[i]," -21 1"

    # print distribuzione coseno
#    cos = [cos[i] for i in range(1,len(cos))]
#    cos.append(1)
#    cosNorm = []
#    imeno1=-1
#    for i in range(len(cos)):
#        cosNorm.append(cos[i]-imeno1)
#        imeno1=cos[i]
    arrayw=[]
    print "ds2 ",
    print "S ",
    for i in range(len(x)-1):
        IntDistr+=1
        if IntDistr % 6:
            print " ",IntDistr,
        else:
            print ""
            print "     ",IntDistr,
        arrayw.append(IntDistr)
    for i in range(len(x)-1):
        #for
        print ""
        print "si%i"%arrayw[i],
        print " H ",
        print " -1 ",
        for ind in range(len(cos)):
            if ind % 5:
                print " ",cos[ind],
            else:
                print ""
                print "     ",cos[ind],
        print ""
        print "sp%i"%arrayw[i],
        print " 0 ",
        for ind in range(len(cos)):
            if ind % 4:
                print " ","%1.3e"%(f111[i,ind,0,0]),
            else:
                print ""
                print "     ","%1.3e"%(f111[i,ind,0,0]),
        IntDistr=arrayw[i]
    print ""

    # energy
    arrayq=[]
    print "ds3 ",
    print " S ",
    for i in range(len(x)-1):
        IntDistr+=1
        if IntDistr % 6:
            print " ",IntDistr,
        else:
            print ""
            print "     ",IntDistr,
        arrayq.append(IntDistr)
    print ""
    for i in range(len(x)-1):
        #for
        print "si%i"%arrayq[i],
        print " H",
        print " 0 ",
        myint=0
        for e in erg:
            myint+=1
            if myint % 5 or myint == 1:
                print " ","%1.3e"%e,
            else:
                print ""
                print "     ","%1.3e"%e,
        print ""
        print "sp%i"%arrayq[i],
        print " 0 ",
        for ind in range(len(f141[i,1,:,0])):
            mysum=0
            for mysumIT in range(nc):
                mysum+=f141[i,mysumIT,ind,0]
            if ind % 5 or ind == 0:
                print " ","%1.3e"%mysum,
            else:
                print ""
                print "     ","%1.3e"%mysum,
        print ""
    print "c ccccccccccccccccccccccccccccccccccc"
    print "c            sdef end                "
    print "c ccccccccccccccccccccccccccccccccccc"

def Plot141(x,Y,mydir="img/",nick=""):
    nk = len(Y[0,:,0,0])
    ne = len(x)
    ns = len(Y)
    for j in range(ns):
        my_dpi = 300
        plt.figure(figsize=(2400/my_dpi, 1800/my_dpi), dpi=my_dpi)
        y1 = np.zeros(ne)
        for k in range(nk):
            y1 += Y[j,k,:,0]
        plt.xlabel('energy spectrum (MeV)')
        plt.ylabel('neutron current per unit area (ns$^{-1}$ cm$^{-2}$)')
        plt.title("sur %i"%(j))
        plt.plot(x,y1, label="sorgente Vera")
        plt.yscale("log")
        plt.xscale("log")
        plt.legend()
        plt.savefig(mydir+"f141_sur%i_"%(j)+nick+".png",dpi=my_dpi)
        plt.close()

def Plot111(x,Y,mydir="img/",nick=""):
    for j in range(len(Y)):
        my_dpi = 300
        plt.figure(figsize=(2400/my_dpi, 1800/my_dpi), dpi=my_dpi)
        y1 = Y[j,:]
        plt.xlabel('Angular Distribution (cosine)')
        plt.ylabel('neutron current per unit area (ns$^{-1}$ cm$^{-2}$)')
        plt.title("seg %i" %j)
        plt.plot(x,y1, label="sorgenteVera")
        plt.yscale("log")
        plt.legend()
        plt.savefig(mydir+"f111_seg%i_"%(j)+nick+".png",dpi=my_dpi)
        plt.close()

def Plot11(x,Y,mydir="img/",nick=""):
    for j in range(2):
        my_dpi = 300
        plt.figure(figsize=(2400/my_dpi, 1800/my_dpi), dpi=my_dpi)
        y1= Y[:,j,0,0]
        plt.xlabel('radial distance (cm)')
        plt.ylabel('neutron current (ns$^{-1}$)')
        plt.title('dir %i' %j)
        plt.plot(x,y1)
        plt.yscale("log")
        plt.savefig(mydir+"f11_dir%i_"%(j)+nick+".png",dpi=my_dpi)
        #plt.show()
        plt.close()

def Plot1(x,Y,mydir="img/",nick=""):
    my_dpi = 300
    plt.figure(figsize=(2400/my_dpi, 1800/my_dpi), dpi=my_dpi)
    plt.xlabel('radial distance (cm)')
    plt.ylabel('neutron current per unit area (ns$^{-1}$ ${cm}^{-2}$)')
    plt.title(' ')
    plt.plot(x,Y)
    plt.yscale("log")
    plt.savefig(mydir+"f1_"+nick+".png",dpi=my_dpi)
    #plt.show()
    plt.close()

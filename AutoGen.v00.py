import bs4
import numpy as np
import subprocess
import sys

#GMSPATH = "/home/hiro02/gamess2018.new/rungms"
#GMSPATH = "/home/usr0/n70210a/GAMESS.third/rungms   "
GMSPATH = "/home/hiroyanakata/gamess2018.third"

def rungmsinp(out):
    outname       = "result/" + out + ".inp"
    command       = "cd result; " + GMSPATH + out + " 00 36 36  "  + " >&  " + out + ".log; cd ../"
    subprocess.call(command,shell=True)
    return

def Getgmsxyz(nat,out):
	XYZ     = np.zeros((nat,3))
	outname = "result/" + out + ".log"
	ip2     = open(outname,"r")
	while True:
		line1 = ip2.readline()
		if not line1: break
		aa    = line1.split()
		if(len(aa) >= 4):
			if(aa[0] == "COORDINATES"  and aa[2] == "ALL" and aa[3] == "ATOMS"):
				line1 = ip2.readline()
				line1 = ip2.readline()
				for iat in range(nat):
					line1      = ip2.readline()
					aa         = line1.split()
					XYZ[iat,0] = float(aa[2])
					XYZ[iat,1] = float(aa[3])
					XYZ[iat,2] = float(aa[4])

	return XYZ
					
				

def dumpcntrl(opfile,runtyp,function,ichg,mult,basisset):
	if(function=="UHF" or function=="UMP2" or function=="UB3LYP"  or function=="UB2PLYP" or function=="UB3LYPD"): 
		scftyp = "UHF" 
	else:
		scftyp = "RHF"
	dfttyp = "none"
	if(function=="UB3LYPD" or function=="UB3LYP" or function=="B3LYP" or function=="B3LYPD"): 
		dfttyp = "B3LYP"
	if(function=="UB2PLYP" or function=="B2PLYP"): 
		dfttyp = "B2PLYP"
		
#
	opfile.write(" $CONTRL\n")
	opfile.write("  RUNTYP=%s\n"%(runtyp))
	opfile.write("  SCFTYP=%s\n"%(scftyp))
	if(function=="UMP2" or function=="MP2"): 
		opfile.write("  MPLEVL=2\n")
	if(dfttyp!= "none"): opfile.write("  DFTTYP=%s\n"%(dfttyp))
	opfile.write("  NPRINT=-5\n")
	opfile.write("  ISPHER=1\n")
	opfile.write("  MAXIT=200\n")
	if(scftyp=="uhf" or scftyp=="UHF"): opfile.write("  mult=%i\n"%(mult))
	opfile.write("  icharg=%i\n"%(ichg))
	if(basisset == "SBKJC"):
	 	opfile.write(" PP=SBKJC\n")
		
	opfile.write(" $END\n")

	if(function=="UB3LYPD" or function=="B3LYPD"):
		dumpdis(opfile)

	return

def dumpscf(opfile,basisset):
	opfile.write(" $SCF\n")
	opfile.write("  DIRSCF=.T.  NPUNCH=2\n")
	opfile.write("  diis=.t.\n")
#	opfile.write("  swdiis=0.0005\n")
	opfile.write("  fdiff=.t.\n")
	opfile.write("  damp=.t.\n")
	opfile.write(" $END\n")
	if(basisset == "SBKJC"):
	 	opfile.write(" $BASIS\n")
 		opfile.write("   GBASIS=SBKJC\n")
 		opfile.write("   NGAUSS=6\n")
 		opfile.write("   ndfunc=1\n")
 		opfile.write(" $END\n")
	else:
	 	opfile.write(" $BASIS\n")
 		opfile.write("   GBASIS=N31\n")
 		opfile.write("   NGAUSS=6\n")
 		opfile.write("   ndfunc=1\n")
 		opfile.write(" $END\n")
 	opfile.write(" $system\n")
 	opfile.write("   mwords=300\n")
 	opfile.write("   memddi=500\n")
 	opfile.write(" $END\n")
#	opfile.write(" $statpt\n")
#	opfile.write("  HSSEND=.t.\n")
#	opfile.write(" $END\n")
	return

def getatmnum(atom):
	atomtab = {
		'H':1.0,
		'C':6.0,
		'O':8.0,
		'N':7.0,
		'Cl':17.0,
		'S':16.0,
		'Cu':29.0,
		'Ni':28.0,
		'Ga':31.0,
		'Ag':47.0,
		'Pd':46.0,
		'F':9.0,
		'Co':27.0,
	}
	val  = 0.0
	val  = atomtab[atom]
	return val
	
def dumpxyz(opfile,natom,ATM,XYZ):
	opfile.write(" $DATA\n")
	opfile.write(" please give comments here\n")
	opfile.write(" C1\n")
	for iatom in range(natom):
		val = getatmnum(ATM[iatom])
		opfile.write(" %3s  %3.1f  %15.11f   %15.11f   %15.11f\n"%(ATM[iatom],val,XYZ[iatom][0],XYZ[iatom][1],XYZ[iatom][2]))
	opfile.write(" $END\n")
	return

def dumpdis(opfile):
	opfile.write(" $DFT\n")
	opfile.write("  idcver=3\n")
	opfile.write("  dc=.t.\n")
	opfile.write(" $END\n")
	return

def makegmsinp(ATM,XYZ,out,runtyp):
	natom = len(ATM)
#
	outname       = "result/" + out + ".inp"
	opfile        = open(outname,"w")
#	runtyp        = "Optimize"
	function      = "B3LYP"
	basisset      = "6-31G*"
	icharge       = 0
	mult          = 1
	
#
	dumpcntrl(opfile, runtyp, function,icharge,mult,basisset)
	dumpscf(opfile,basisset) 
#	print "Need dispersion? (y/n)"
#	line  = raw_input()
#	aa    = line.split()
#	if(aa[0] == "y"): dumpdis(opfile)
	dumpxyz(opfile,natom,ATM,XYZ)
	return 1


args    = sys.argv
ip1     = open(args[1],"r")
listmol = []
while True:
	line1 = ip1.readline()
	if not line1: break
	aa    = line1.split() 
	listmol.append(aa[0])
	command = "wget http://pccdb.org/search_pubchemqc/view_mol/"  + aa[0]
	subprocess.call(command,shell=True)
#
	ATM  = []
	XYZ  = []
#
	html = open(aa[0]).read()
	soup = bs4.BeautifulSoup(html, "html.parser")
	elm  = soup.select('div table')
	for ii in range(len(elm)): 
		text   = str(elm[ii].getText)
		isgeom = text.find("Atomic number")
		if(isgeom > 0):
			word = text.split()
			for ii in range(len(word)):
				if(word[ii] == "C" or word[ii] == "O"  or word[ii] == "H"  or word[ii] == "N"):
#					bb = word[ii].split()
					ATM.append(word[ii])
					XYZ.append(float(word[ii+4]))
					XYZ.append(float(word[ii+6]))
					XYZ.append(float(word[ii+8]))
	XYZ = np.asarray(XYZ)
	XYZ = XYZ.reshape((len(ATM),3))
#   Geometry Optimization
	makegmsinp(ATM,XYZ,aa[0],"Optimize")
	rungmsinp(aa[0])
	nat = len(ATM)
	XYZ = Getgmsxyz(nat,aa[0])
#   Hessian calculation
	makegmsinp(ATM,XYZ,aa[0]+".hess","Hessian")
	rungmsinp(aa[0]+".hess")
#	ip2 = open(aa[0],"r")
#	while True:
#		line2 = ip2.readline()
#		if not line2: break
#		bb = line2.split()
#		if(len(bb)>=3):
#			if(bb[2] == "geometries"):
#
#    for ii in range(len(elm)): 
#        text  = str(elm[ii].getText)
#        aa    = text.split()
#        ispdf = text.find("PDF") + text.find("pdf")
#        if(ispdf > 0):
#            for val in aa:
#                bb = val.split("=")
#                if(bb[0]=="href"): 
#                    cc      = val.split('"')
#                    command = "wget " + cc[1]
#                    opdf.write("%s\n"%(command))
#    #               subprocess.call(command,shell=True)
#    return

		
#

# calculating guesss and Rvalues
# AL 2mm CD
import numpy,glob,os
dMD=0.10725 #d22
dCD=0.138 #d11
d45=0.1138 #d45
# d33=[x*0.01 for x in range(1,11,1)]# guesses
D33=[x for x in numpy.arange(0.1, .8, 0.1)]
ndecimals = 5
d33=numpy.around(D33, ndecimals)
print d33
allD33=[[i,j,k] for i in d33 for j in d33 for k in d33]
print allD33
rx=[dMD/allD33[t][0] for t in range(0,len(allD33))]

ry=[dCD/allD33[t][1] for t in range(0,len(allD33))]

r45=[d45/allD33[t][2] for t in range(0,len(allD33))]
print "%%%%"
print rx,ry,r45
print "%%%%"
R11 = []
R11 = [1 for i in range(len(allD33)-len(R11))]
R22 = [((ry[ind]*(rx[ind]+1))/(rx[ind]*(ry[ind]+1)))**0.5  for ind in range(0,len(allD33))]
R33 = [((ry[ind])*(rx[ind]+1)/(ry[ind]+rx[ind]))**0.5 for ind in range(0,len(allD33))]
R12=R23=R13=[((3*(rx[ind]+1)*ry[ind])/((2*r45[ind]+1)*(rx[ind]+ry[ind])))**0.5 for ind in range(0, len(allD33))]
print R11
print R22
print R33
print R13
# exporting psf file
# converting list to tuplets
r1 = tuple(R11)#(1, 1, 1)
r2 = tuple(R22)#(1, 1, 1)
r3 = tuple(R33)#(1, 1, 1)
r4 = tuple(R12)#(1, 1, 1)
r5 = tuple(R13)#(1, 1, 1)
r6 = tuple(R23)#(1, 1, 1)
inp_name ="AL2mm45orto_Ecdmd"# "45_al2mm" #give required inputfile name ,and make sure its in same directory as PSF file
nameOFoutputFILE='AlEmdCd_p45'
with open(nameOFoutputFILE+'.PSF', 'w') as file:
    file.write("cd=ParStudy(par=('R11','R22','R33','R12','R13','R23'))" + "\n")
    file.write("cd=ParStudy(par=('R11','R22','R33','R12','R13','R23'))" + "\n")
    file.write("cd.define(DISCRETE,par=('R11'),domain=%s" % (r1,) + ")\n")
    file.write("cd.define(DISCRETE,par=('R22'),domain=%s" % (r2,) + ")\n")
    file.write("cd.define(DISCRETE,par=('R33'),domain=%s" % (r3,) + ")\n")
    file.write("cd.define(DISCRETE,par=('R12'),domain=%s" % (r4,) + ")\n")
    file.write("cd.define(DISCRETE,par=('R13'),domain=%s" % (r5,) + ")\n")
    file.write("cd.define(DISCRETE,par=('R23'),domain=%s" % (r6,) + ")\n")

    file.write("cd.sample(INTERVAL,par='R11',interval=1)" + "\n")
    file.write("cd.sample(INTERVAL,par='R22',interval=1)" + "\n")
    file.write("cd.sample(INTERVAL,par='R33',interval=1)" + "\n")
    file.write("cd.sample(INTERVAL,par='R12',interval=1)" + "\n")
    file.write("cd.sample(INTERVAL,par='R13',interval=1)" + "\n")
    file.write("cd.sample(INTERVAL,par='R23',interval=1)" + "\n")
    file.write("cd.combine(TUPLE, name='dSet3')" + "\n")
    file.write("cd.generate(template='%s')" % inp_name + "\n")
    file.write("cd.execute(ALL)" + "\n")
    file.write("cd.output(step=1,file=ODB)" + "\n")
# remove odb and lck files
for file in glob.glob("*.odb"):
    print file
    os.remove(file)
for file in glob.glob("*.lck"):
    print file
    os.remove(file)
#
# run PSF file in abaqus
import subprocess
subprocess.call("abaqus script=%s"%nameOFoutputFILE, shell=True)
# remove  txt
for file in glob.glob("*.txt"):
    print file
    os.remove(file)

print '%%%%%%'
for file in glob.glob("*.txt"):
    print '3453'+file
print '%%%%%%'
# runing v4Code.py ####
import subprocess
subprocess.call("abaqus cae -noGUI v4Code.py", shell=True)
print '****'
subprocess.call("python plo.py", shell=True)  # works if anakonda is installed and works on cmd
print '****'
print '%%%%%%'
subprocess.call("C:\down\install\ankonda\python plo.py", shell=True)  # works if anakonda is installed and works on cmd
print '%%%%%%'

#C:\down\install\ankonda\python
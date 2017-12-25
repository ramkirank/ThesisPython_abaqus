import subprocess,glob

def rep(dMD,dCD,d45,start,stop,step,decimals,MDorCD,inp_name,nameOFoutputFILE):
    D33 = [x for x in numpy.arange(start,stop,step)]
    ndecimals = 5
    d33 = numpy.around(D33, ndecimals)
    print d33
    allD33 = [[i, j, k] for i in d33 for j in d33 for k in d33]
    print allD33
    rx = [dMD / allD33[t][0] for t in range(0, len(allD33))]

    ry = [dCD / allD33[t][1] for t in range(0, len(allD33))]

    r45 = [d45 / allD33[t][2] for t in range(0, len(allD33))]
    ####
    R11 = []
    R11 = [1 for i in range(len(d33) - len(R11))]
    R22 = [((ry[ind] * (rx[ind] + 1)) / (rx[ind] * (ry[ind] + 1))) ** 0.5 for ind in range(0, len(d33))]
    R33 = [((ry[ind]) * (rx[ind] + 1) / (ry[ind] + rx[ind])) ** 0.5 for ind in range(0, len(d33))]
    R12 = R23 = R13 = [((3 * (rx[ind] + 1) * ry[ind]) / ((2 * r45[ind] + 1) * (rx[ind] + ry[ind]))) ** 0.5 for ind in
                       range(0, len(d33))]

    # exporting psf file
    if MDorCD=="MD":
        r1 = tuple(R11)  # (1, 1, 1)     # converting list to tuplets
        r2 = tuple(R22)  # (1, 1, 1)
    else:
        r1 = tuple(R22)  # (1, 1, 1)
        r2 = tuple(R11)  # (1, 1, 1)
    r3 = tuple(R33)  # (1, 1, 1)
    r4 = tuple(R12)  # (1, 1, 1)
    r5 = tuple(R13)  # (1, 1, 1)
    r6 = tuple(R23)  # (1, 1, 1)
    # inp_name = "AL2mmMDorto"  # give required inputfile name ,and make sure its in same directory as PSF file
    # nameOFoutputFILE = 'AL2mmMD'
    with open(nameOFoutputFILE + '.PSF', 'w') as file:
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
    subprocess.call("abaqus script=%s" % nameOFoutputFILE, shell=True)
    # remove  txt
    for file in glob.glob("*.txt"):
        print file
        os.remove(file)

    print '%%%%%%'
    for file in glob.glob("*.txt"):
        print '3453' + file
    print '%%%%%%'
    # runing v4Code.py ####
    import subprocess
    subprocess.call("abaqus cae -noGUI v4Code.py", shell=True)

def read_mindiff():
    with open('oldresult.csv','r') as file:
        mindiff = file.readlines()
    return mindiff

def writeiter(name,n):
    with open("%s"%name+'no_iteration.csv','w') as file:
        file.write('%s'%n)

accepted_diff=1025
start=0.001
stop=0.003
step=.001
decima=5
# 1st iteration
rep(0.010843106574315,0.004933542294580,0.004852135492708,start,stop,step,decima,"MD","AL2mmMDorto",'AL2mmMD')
# starting from 2nd iteration
for ite in range(2,10):
    print ite
    res1 = read_mindiff()
    res=res1[0]
    if float(res) <= accepted_diff:
        writeiter("if_", ite)
        break
    else:
        nstart =stop
        nstop =nstart+.002
        nstep =step
        ndec =5
        rep(0.010843106574315, 0.004933542294580, 0.004852135492708, nstart, nstop, nstep,ndec,"MD","AL2mmMDorto",'AL2mmMD')
        writeiter("els_", ite)
        stop=nstop
        print "next loop"

import subprocess,glob
# remove  txt
for file in glob.glob("*.txt"):
    print file
    os.remove(file)
print '%%%%%%'
for file in glob.glob("*.txt"):
    print '3453' + file
print '%%%%%%'
print 'running plo.py'
subprocess.call("python plo.py", shell=True)  # works if anakonda is installed and works on cmd
print '%%%%%%'


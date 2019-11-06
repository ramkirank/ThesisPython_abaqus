# run this script from abaqus
# calculate difference and output txt files accordingly
from abaqus import *
from abaqusConstants import *
import odbAccess, glob, numpy,os
n=numpy.arange(.1,3,.1)
rou=numpy.around(n,2)
required_displacement =rou#numpy.around(.3,3,0.1)# [dd for dd in range(0,4)] #give required displacements range
names = []
allnames = []
step_name = 'Step-1'
for file in glob.glob("*.odb"):
    allnames.append(file)

number_of_obd = len(allnames)
print number_of_obd
numberOFodbLEFT = number_of_obd

for i in range(0, numberOFodbLEFT):
    nstr = ''.join(allnames[i])
    opened_odb = odbAccess.openOdb(path=allnames[i])  # nstr)
    Step = opened_odb.steps[step_name]  # ['Step-1']
    historyReg = Step.historyRegions['Node ASSEMBLY.''1']
    ReactionForce = historyReg.historyOutputs['RF2'].data
    displacement = historyReg.historyOutputs['U2'].data
    di=[]
    if ReactionForce:
        for x in range(len(ReactionForce)):
           # rf.append(ReactionForce[x][1])
            di.append(displacement[x][1])
        if max(di)>.1:#max(required_displacement)/:
            names.append(allnames[i])
    else:
        print"****"
##
diff = []
total_diff = []
exp_load = [] # exp
exp_load = []
exp_disp = []
time = []
exp_disp = []
time = []

nameOFexp_file = 'al2mm_45EXP.csv'   # import from txt file with ; as delimeter
with open(nameOFexp_file, 'r') as file:
    lines = file.readlines()
    for data in lines:
        row = data.split('	')
        exp_load.append(float(row[0]))
        exp_disp.append(float(row[1]))
print"-note: the function used is interpolate...so if in ODB file displacement is less thain in below list required_displacement  u will get just straight line "

y_exp = numpy.interp(required_displacement, exp_disp, exp_load)

with open('exp_polyfit.csv', 'w') as file:
    for le in range(len(required_displacement)):
        file.write(str(y_exp[le]) + ";" + str(required_displacement[le]) + "\n")
# ODB import....

number_of_obd = len(names)
print number_of_obd
numberOFodbLEFT = number_of_obd

for i in range(0, numberOFodbLEFT):
    nstr = ''.join(names[i])
    opened_odb = odbAccess.openOdb(path=names[i])  # nstr)
    Step = opened_odb.steps[step_name]  # ['Step-1']
    historyReg = Step.historyRegions['Node ASSEMBLY.''1']
    ReactionForce = historyReg.historyOutputs['RF2'].data
    displacement = historyReg.historyOutputs['U2'].data
    rf = []
    di = []
    with open(names[i] + '.txt', 'w') as file:
        for x in range(len(ReactionForce)):
            rf.append(ReactionForce[x][1])
            di.append(displacement[x][1])
            file.write(str(ReactionForce[x][1]) + ";" + str(displacement[x][1]) + "\n")
    inf=numpy.all(numpy.diff(di) > 0)
    print inf
    max_required_displacement = [req for req in required_displacement if req <= max(di)]
    di_new = [x*2**.5 for x in di]
    y = numpy.interp(max_required_displacement, di_new, rf)  # polyfit exp
    with open(str(names[i]) + 'result.csv', 'w') as file:
        for le in range(len(max_required_displacement)):
            file.write(str(y[le]) + ";" + str(max_required_displacement[le]) + "\n")
    diff.append([e1 - e for e, e1 in zip(y_exp, y*2**.5)])  # operator.sub,y_exp,y)
    total_diff.append(sum(map(abs, diff[i])))

print diff

with open('diff.csv', 'w') as file:
    for nu in range(0, len(diff)):
        file.write(str(diff[nu]) + '\n')

with open('sumdiff.csv', 'w') as file:
    for nu in range(0, len(total_diff)):
        print str(total_diff[nu]) + '->' + str(names[nu]) + '\n'
        file.write(str(total_diff[nu]) + '->' + str(names[nu]) + '\n')
    """result """
    minPdiff = min(total_diff)  # if n>0)
    minIndex = total_diff.index(minPdiff)  # min(total_diff)
    file.write('\n')
    file.write('The best ODB is ' + str(names[minIndex]) + '\n')

with open('oldresult.csv','w') as file:
    minPdiff = min(total_diff)  # if n>0)
    file.write('%s'%minPdiff)


# """result """
# minIndex = total_diff.index(min(total_diff))
# print 'The best ODB is ' + str(names[minIndex])

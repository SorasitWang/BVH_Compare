import csv
import numpy as np
import math
# open the file in read mode
_joints = ["Head","RightFoot","LeftFoot","LeftHand","RightHand","RightArm","RightForeArm"]
_joints1 = ["head","rFoot","lFoot","lHand","rHand","rShldr","rForeArm"]
 
# creating dictreader object

 
# candidate joint
def scoring(diff,max):
    #print("diff",diff)
    #diff = 30 ~ max , 11 ~~ max/2
    return max*(2/(1+pow(math.e,-diff/5))-1)
joints = []
joints1 = []
for joint in _joints :
    joints.append("{}.X".format(joint))
    joints.append("{}.Y".format(joint))
    joints.append("{}.Z".format(joint))
for joint in _joints1 :
    joints1.append("{}.X".format(joint))
    joints1.append("{}.Y".format(joint))
    joints1.append("{}.Z".format(joint))
print(joints)
print(joints1)
def compare(a,b):
    # 0 : pos , 1 : sumDis , 2 : relation
    score = [0,0,0]
    for joint,value in a[0].items():
        score[0] += scoring(abs(value["Avg"]-b[0][joint]["Avg"])*10,1)/len(a[0].keys())
    for joint,value in a[1].items():
        w = 1/6
        if joint=="Head":
            w = 1/3
        score[1] += scoring(abs((value["Distance"])-(b[1][joint]["Distance"]))*10,w)/len(a[1].keys())
    for pair,value in a[2].items():
        # head-foot : 0.7 hand-foot 0.3
        w = 0.15
        if pair=="Head-LeftFoot" or pair=="Head-RightFoot":
            w = 0.35
        #elif pair=="RightHand-LeftHand" or pair=="LeftFoot-LeftHand":
        #    w = 0.15
        score[2] += scoring(abs((value["Avg"])-(b[2][pair]["Avg"]))*10,w)
    #weight score : 0.2 0.4 0.4
    print(1-(0.2*score[0]+0.4*score[1]+0.4*score[2]))
    print([1-score[0],1-score[1],1-score[2]])
    return 



def calculate(name):
    #name = "140_04_worldpos"
    filename = open("./bvh-converter-master/bvh_converter/res/{}_worldpos.csv".format(name), 'r')
    file = csv.DictReader(filename)
    pos = dict()
    stat = dict()
    # iterating over each row and append
    # values to empty list
    for joint in joints:
        pos[joint] = [] 
    r = 0
    for row in file:
        #ignore first 2 frames
        r += 1 
        if r <= 2 : continue
        for joint in joints :
            #if row.get(joint) == None:
            #    pos[joint].append(row[joint])
            pos[joint].append(row[joint])
    frames = len(pos["Head.X"])
    for joint in joints :
        pos[joint] = np.array(pos[joint]).astype(np.float)
        #max , min , diff
      

    pair="RightArm-RightForeArm"
    a = pair.split("-")[0]
    b = pair.split("-")[1]
        
    diff = np.sqrt(np.square(pos["{}.X".format(a)]-pos["{}.X".format(b)]) + np.square(pos["{}.Y".format(a)]-pos["{}.Y".format(b)]) \
        + np.square(pos["{}.Z".format(a)]-pos["{}.Z".format(b)]))
    standard = np.average(diff)

    for joint in joints:
        pos[joint] = pos[joint]/standard
        stat[joint] = dict()
        stat[joint]["Max"] = np.max(pos[joint])
        stat[joint]["Min"] = np.min(pos[joint])
        stat[joint]["Avg"] = np.average(pos[joint])
        diff = np.diff(pos[joint])
        stat[joint]["Distance"] = np.sum(np.absolute(diff))
    #sum x y z
    dis = dict()
    totalDis = dict()
    print("Standard",standard)
    standard = 1
    for joint in _joints:
        if "Arm" in joint :continue
        dis[joint] = np.sqrt( np.square(pos["{}.X".format(joint)]/standard) +
            np.square(pos["{}.Y".format(joint)]/standard) + np.square(pos["{}.Z".format(joint)]/standard))
        diff = np.diff(dis[joint])
        totalDis[joint] = dict()
        totalDis[joint]["Max"]  = np.max(dis[joint])
        totalDis[joint]["Min"]  = np.min(dis[joint])
        totalDis[joint]["Avg"]  = np.average(dis[joint])
        totalDis[joint]["Distance"] = np.sum(np.absolute(diff))
        
    # printing lists

    # print(np.argmax(dis["Head"]),np.argmin(dis["Head"]))
    # print(np.argmax(dis["LeftFoot"]),np.argmin(dis["LeftFoot"]))
    # print(dis["Head"])
    # print(dis["LeftFoot"])
    compare = ["Head-LeftFoot","Head-RightFoot","LeftFoot-LeftHand","RightHand-LeftHand"]
    

    rela = dict()
    for pair in compare :
        a = pair.split("-")[0]
        b = pair.split("-")[1]
        
        diff = np.sqrt(np.square((pos["{}.X".format(a)]-pos["{}.X".format(b)])/ standard) +
             np.square((pos["{}.Y".format(a)]-pos["{}.Y".format(b)])/ standard) \
            + np.square((pos["{}.Z".format(a)]-pos["{}.Z".format(b)])/ standard))
        rela[pair] = dict()
        rela[pair]["Max"] = np.max(diff) 
        rela[pair]["Min"] = np.min(diff) 
        rela[pair]["Avg"] = np.average(diff) 
    #print(stat)

    print(name)
    print(standard)
    print("-------------")
    print(stat)
    print("-------------")
    print(totalDis)
    print("-------------")
    print(rela)
    print("-------------")

    return stat,totalDis,rela,frames,standard

files = ["06_15","10_03","Standup","pick_item","UsingComputer"]#,"boxing"]
#files = ["UsingComputer"]
data = dict()
for file in files:
    data[file] = calculate(file)
'''
for i in range(len(files)):
    for j in range(i,len(files)):
            print(files[i],files[j])
            compare(data[files[i]],data[files[j]]) 
'''
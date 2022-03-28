import csv
import numpy as np
import math
# open the file in read mode
_joints = ["Head","RThumb","LThumb","RightFoot","LeftFoot","LeftHand","RightHand"]

 
# creating dictreader object

 
# candidate joint
def scoring(diff,max):
    #print("diff",diff)
    #diff = 30 ~ max , 11 ~~ max/2
    return max*(2/(1+pow(math.e,-diff/5))-1)
joints = []
for joint in _joints :
    joints.append("{}.X".format(joint))
    joints.append("{}.Y".format(joint))
    joints.append("{}.Z".format(joint))
print(joints)

def compare(a,b):
    # 0 : pos , 1 : sumDis , 2 : relation
    score = [0,0,0]
    for joint,value in a[0].items():
        score[0] += scoring(abs(value["Avg"]-b[0][joint]["Avg"]),1)/len(a[0].keys())
    #score[0]=0
    for joint,value in a[1].items():
        score[1] += scoring(abs(value-b[1][joint]),1)/len(a[1].keys())
    for pair,value in a[2].items():
        score[2] += scoring(abs(value["Avg"]-b[2][pair]["Avg"]),1 / len(a[2].keys()))
    print(1-sum(score)/3)
    print(score)
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
    for row in file:
        for joint in joints :
            pos[joint].append(row[joint])
    for joint in joints :
        pos[joint] = np.array(pos[joint]).astype(np.float)
        #max , min , diff
        stat[joint] = dict()
        stat[joint]["Max"] = np.max(pos[joint])
        stat[joint]["Min"] = np.min(pos[joint])
        stat[joint]["Avg"] = np.average(pos[joint])
        diff = np.diff(pos[joint])
        stat[joint]["Distance"] = np.sum(np.absolute(diff))

    #sum x y z
    dis = dict()
    totalDis = dict()
    for joint in _joints:
    
        dis[joint] = np.sqrt( np.square(pos["{}.X".format(joint)]) + np.square(pos["{}.Y".format(joint)]) + np.square(pos["{}.Z".format(joint)]))
        diff = np.diff(dis[joint])
        totalDis[joint] = np.sum(np.absolute(diff))
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
        
        diff = dis[a]-dis[b]
        rela[pair] = dict()
        rela[pair]["Max"] = np.max(diff)
        rela[pair]["Min"] = np.min(diff)
        rela[pair]["Avg"] = np.average(diff)
    #print(stat)
    print(name)
    print("-------------")
    print(totalDis)
    print("-------------")
    print(rela)
    print("-------------")
    return stat,totalDis,rela

files = ["06_15","10_03","140_04","140_02"]
data = dict()
for file in files:
    data[file] = calculate(file)
for i in range(len(files)):
    for j in range(i,len(files)):
            print(files[i],files[j])
            compare(data[files[i]],data[files[j]]) 
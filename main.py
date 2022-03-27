import csv
import numpy as np
# open the file in read mode
filename = open("./bvh-converter-master/bvh_converter/res/140_04_worldpos.csv", 'r')
 
# creating dictreader object
file = csv.DictReader(filename)
 
# candidate joint
_joints = ["Head","RThumb","LThumb","RightFoot","LeftFoot"]
joints = []
for joint in _joints :
    joints.append("{}.X".format(joint))
    joints.append("{}.Y".format(joint))
    joints.append("{}.Z".format(joint))
print(joints)
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
for joint in _joints:
   
    dis[joint] = np.sqrt( np.square(pos["{}.X".format(joint)]) + np.square(pos["{}.Y".format(joint)]) + np.square(pos["{}.Z".format(joint)]))
    #diff = np.diff(dis[joint])
    #dis[joint] = np.sum(np.absolute(diff))
# printing lists

# print(np.argmax(dis["Head"]),np.argmin(dis["Head"]))
# print(np.argmax(dis["LeftFoot"]),np.argmin(dis["LeftFoot"]))
# print(dis["Head"])
# print(dis["LeftFoot"])
compare = ["Head-LeftFoot","Head-RightFoot"]
rela = dict()
for pair in compare :
    a = pair.split("-")[0]
    b = pair.split("-")[1]
    
    diff = dis[a]-dis[b]
    print(a,b,diff)
    rela[pair] = dict()
    rela[pair]["Max"] = np.max(diff)
    rela[pair]["Min"] = np.min(diff)
    rela[pair]["Avg"] = np.average(diff)
print(rela)



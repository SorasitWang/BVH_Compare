import csv
import numpy as np
import math

_joints = ["Head", "RightFoot", "LeftFoot",
           "LeftHand", "RightHand", "RightUpLeg", "RightLeg"]


joints = []

for joint in _joints:
    joints.append("{}.X".format(joint))
    joints.append("{}.Y".format(joint))
    joints.append("{}.Z".format(joint))

#change path
path = "./bvh-converter-master/bvh_converter/res"

def scoring(diff, max):
    #logistic function adapted by some value
    return max*(2/(1+pow(math.e, -diff/5))-1)


def calculate(name):
    global path
    
    filename = open("{}/{}_worldpos.csv".format(path, name), 'r')
    file = csv.DictReader(filename)

    # position of each joint in every frame
    pos = dict()
    # summary
    stat = dict()

    for joint in joints:
        pos[joint] = []
    r = 0
    for row in file:
        # ignore first 2 frames
        r += 1
        if r <= 2:
            continue
        for joint in joints:

            pos[joint].append(row[joint])

    frames = len(pos["Head.X"])
    for joint in joints:
        if name in ["pick_item", "UsingComputer", "boxing"]:
            pos[joint] = np.array(pos[joint]).astype(np.float)
        else:
            pos[joint] = np.array(pos[joint]).astype(np.float)

    a = "RightUpLeg"
    b = "RightLeg"

    diff = np.sqrt(np.square(pos["{}.X".format(a)]-pos["{}.X".format(b)]) + np.square(pos["{}.Y".format(a)]-pos["{}.Y".format(b)])
                   + np.square(pos["{}.Z".format(a)]-pos["{}.Z".format(b)]))
    # length of UpLeg bone
    unit = np.average(diff)
    print(unit)

    for joint in joints:
        # normalized
        pos[joint] = pos[joint]/unit

        stat[joint] = dict()
        stat[joint]["Max"] = np.max(pos[joint])
        stat[joint]["Min"] = np.min(pos[joint])
        stat[joint]["Boxsize"] = np.max(pos[joint]) - np.min(pos[joint])

        diff = np.diff(pos[joint])
        stat[joint]["Distance"] = np.sum(np.absolute(diff))

    totalDis = dict()
    for joint in _joints:
        jx = "{}.X".format(joint)
        jy = "{}.Y".format(joint)
        jz = "{}.Z".format(joint)

        totalDis[joint] = dict()

        # total distances in Y (vertical), XZ (horizontal), XYZ (all) for each joint
        totalDis[joint]["Dist.Y"] = np.sum(np.absolute(np.diff(pos[jy])))
        totalDis[joint]["Dist.XZ"] = np.sum(np.sqrt(
            np.square(np.diff(pos[jx])) +
            np.square(np.diff(pos[jz]))))
        totalDis[joint]["Dist.XYZ"] = np.sum(np.sqrt(
            np.square(np.diff(pos[jx])) +
            np.square(np.diff(pos[jy])) +
            np.square(np.diff(pos[jz])))) 

        # as for speed, divide the value by (frames - 1)

    compare = ["Head-LeftFoot", "Head-RightFoot",
               "LeftFoot-LeftHand", "RightHand-LeftHand"]

    # between joint
    rela = dict()
    for pair in compare:
        a = pair.split("-")[0]
        b = pair.split("-")[1]

        diff = np.sqrt(np.square((pos["{}.X".format(a)]-pos["{}.X".format(b)])) +
                       np.square((pos["{}.Y".format(a)]-pos["{}.Y".format(b)]))
                       + np.square((pos["{}.Z".format(a)]-pos["{}.Z".format(b)])))
        rela[pair] = dict()
        rela[pair]["Max"] = np.max(diff)
        rela[pair]["Min"] = np.min(diff)
        rela[pair]["Avg"] = np.average(diff)

    print("-------------")
    print("-------------")
    print(name)
    print("-------------")
    print(stat)
    print("-------------")
    print(totalDis)
    print("-------------")
    print(rela)

    return stat, totalDis, rela, frames


def compare(a, b):
    score = [0, 0, 0, 0, 0, 0]

    adapt = 1
    score[1] += 1/4*scoring(adapt*abs((a[1]["Head"]
                ["Dist.XZ"])-(b[1]["Head"]["Dist.XZ"])), 1)
    score[1] += 1/4*scoring(adapt*abs((a[1]["Head"]
                ["Dist.Y"])-(b[1]["Head"]["Dist.Y"])), 1)
    for joint in ["LeftHand","RightHand"]:
         score[1] += 1/4*scoring(adapt*abs((a[1][joint]
                ["Dist.XYZ"])-(b[1][joint]["Dist.XYZ"])), 1)
       

    adapt = 10
    score[2] = 1/3*scoring(adapt*abs((a[2]["Head-LeftFoot"]["Avg"])-(b[2]["Head-LeftFoot"]["Avg"])), 1) + \
        1/3*scoring(adapt*abs((a[2]["Head-RightFoot"]["Avg"])-(b[2]["Head-RightFoot"]["Avg"])), 1) + \
        1/6*scoring(adapt*abs((a[2]["LeftFoot-LeftHand"]["Avg"])-(b[2]["LeftFoot-LeftHand"]["Avg"])), 1) + \
        1/6*scoring(adapt*abs((a[2]["RightHand-LeftHand"]
                    ["Avg"])-(b[2]["RightHand-LeftHand"]["Avg"])), 1)

    score[3] = 1/2*scoring(adapt*abs((a[2]["Head-LeftFoot"]
                                            ["Avg"])-(b[2]["Head-LeftFoot"]["Avg"])), 1) +\
        1/2*scoring(adapt*abs((a[2]["Head-RightFoot"]
                                     ["Avg"])-(b[2]["Head-RightFoot"]["Avg"])), 1)

    circle_a = np.sqrt(a[0]["Head.X"]["Boxsize"]**2 +
                       a[0]["Head.Z"]["Boxsize"]**2)

    circle_b = np.sqrt(b[0]["Head.X"]["Boxsize"]**2 +
                       b[0]["Head.Z"]["Boxsize"]**2)
    score[4] = scoring(np.abs(circle_a - circle_b), 1)

    return score , 1-((score[1]+score[2]+score[4])/3)


files = ["06_15", "10_03", "Standup", "pick_item",
         "UsingComputer", "boxing", "magic", "jogging", "01_14"]

data = dict()
for file in files:
    data[file] = calculate(file)

with open(path+"/result.csv", 'w') as f:
    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    writer.writerow([""]+files)

    for i in range(len(files)):
        row = [files[i]]
        print("----------------- Compare score ---------------")
        print(files[i])
        for j in range(len(files)):
            score , avgScore = compare(data[files[i]], data[files[j]])
            row.append(avgScore)
            print("    ", files[j],avgScore, score)
        print("------------")
        writer.writerow(row)
   
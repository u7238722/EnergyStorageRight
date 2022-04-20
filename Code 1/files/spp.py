#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ciliang ma, haiwang luo
"""
import math
import json
import matplotlib.pyplot as plt


def generate_rectangle(f_name):
    ''':cvar
    to generate the basic rectangle to put the panels, but:
    attention: we return the mid-center coordinates of the panels,
    so we need to change the shape of the small rectangle to fit.
    '''

    with open(f_name,"r") as load_f:
        points = json.load(load_f)

    points_list = points["points"]
    # print(points_list)
    min_lon = points_list[0][0]
    max_lon = points_list[0][0]
    min_lat = points_list[0][1]
    max_lat = points_list[0][1]
    for point in points_list:
        if min_lon > point[0]:
            # to narrow down the area of the rectangle
            # think about the triangle to get the maximum situation
            # so the x = sqrt(120^2 + 60^2) = 134.1641
            # remember to 'add' or 'minus', they are different
            min_lon = point[0]
        if max_lon < point[0]:
            max_lon = point[0]
        if min_lat > point[1]:
            min_lat = point[1]
        if max_lat < point[1]:
            max_lat = point[1]

    length = abs((int)((max_lon - min_lon) * 111 * 1000 * math.cos((min_lon + max_lon) * math.pi / 360)))
    height = (int)((max_lat - min_lat) * 111 * 1000)

    # generate lolution
    t1_num_hor = length // 240
    t1_num_ver = height // 120

    t2_num_hor = (length - 240 * t1_num_hor) // 120
    t2_num_ver = (height - 120 * t1_num_ver) // 120

    print(t2_num_hor)

    sol_dict = {}
    sol_arr = []
    
    for i in range(0,t1_num_ver):
        for j in range(0,t1_num_hor):
            point = ["A",min_lon+(120+j*240)/(111*1000), min_lat+(60+i*120)/(111*1000)]
            if isInPolygon(points_list, point):
                sol_arr.append(point)

        if t2_num_hor > 0:
            point = ["B",(60+(t1_num_hor+1)*240)/(111*1000),min_lat+(60+i*120)/(111*1000)]
            if isInPolygon(points_list, point):
                sol_arr.append(point)

    with open("./test-sol.json", "w") as sf:
        json.dump(sol_arr, sf, indent=2)

    return sol_arr


def isInPolygon(points_list, point):
    nCross = 0
    for i in range(0, len(points_list)):
        p1 = points_list[i]
        p2 = points_list[(i + 1) % len(points_list)]
        if p1[1] == p2[1]:
            continue
        if point[2] < min(p1[1], p2[1]):
            continue
        if point[2] > max(p1[1], p2[1]):
            continue
        x = (point[2] - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
        if x > point[1]:
            nCross = nCross + 1

    return nCross % 2 == 1

#asd
def generate_rectangle_from_list(list):
    points_list = []

    print("spp.py List : ", list)
    error_detect = 0

    # this is used to remove the typo value when user open the website with safari browser. 
    for x in range(len(list)):
        list[x] = ['None' if v is None else v for v in list[x]]
        if error_detect == 1 :
            print("Start to debug")
            old_fst = list[x][0]
            old_second = list[x][1]
            # reorder 
            list[x][0] = next_fst_pos
            list[x][1] =  old_fst
            next_fst_pos = old_second
        print("this is test : ", list[x])
        for y in range(len(list[x])):
            print("Detect bug",list[x][y])
            if ("=" in list[x][y]) and (";" in list[x][y]):
                #if ";" in list[x][y]:
                error_detect = 1

                print("****Found A bug **** ", list[x][y])
                new_string = list[x][y].replace(" ","")
                print("new string ",new_string)
                get_typo_index = new_string.index(';')
                print("*** The index is ",get_typo_index)
                next_fst_pos = new_string[-get_typo_index+1:]
                print("its next fst",next_fst_pos)
                current_lst_pos = new_string[0:get_typo_index-1]
                print("its current second numbner ", current_lst_pos)
                # current index y = 1 position
                list[x][y] = current_lst_pos
                print("Update new :", list[x][y])
                print("Check the current", list[x])
            if "=" in list[x][y]:
                list[x][y] = list[x][y].replace('=','')
                print("Remove the last = symbol")

            if ";" in list[x][y] :
                list[x][y] = list[x][y].replace(';','')
    print("Final new list ", list)
    list = list[0:5]
                
        
           
           
                
        


    for point in list:
        points_list.append([float(point[0]), float(point[1])])

    print("spp.py Point List : ", points_list)
    min_lon = points_list[0][0]
    max_lon = points_list[0][0]
    min_lat = points_list[0][1]
    max_lat = points_list[0][1]
    for point in points_list:
        if min_lon > point[0]:
            min_lon = point[0]
        if max_lon < point[0]:
            max_lon = point[0]
        if min_lat > point[1]:
            min_lat = point[1]
        if max_lat < point[1]:
            max_lat = point[1]

    start_pos = [{"logititude": min_lon, "latitude": min_lat}]

    length = abs((int)((max_lon - min_lon) * 111 * 1000 * math.cos((min_lon + max_lon) * math.pi / 360)))
    height = (int)((max_lat - min_lat) * 111 * 1000)

    # generate lolution
    t1_num_hor = length // 240
    t1_num_ver = height // 120

    #t2_num_hor = (length - 240 * t1_num_hor) // 120
    #t2_num_ver = (height - 120 * t1_num_ver) // 120
    t2_num_hor =  length // 120
    t2_num_ver =  height // 120
    print(t2_num_hor)
    print("test")

    sol_dict = {}
    sol_arr = []

    ## edit_point
    order = 0

    for i in range(0, t1_num_ver):
        for j in range(0, t1_num_hor):
            point = ["A", min_lon + (120 + j * 240) / (111 * 1000), min_lat + (60 + i * 120) / (111 * 1000)]
            if isInPolygon(points_list, point):
                sol_arr.append(point)
    
    for k in range(0,t2_num_ver+2):
        for w in range(0, t2_num_hor+2):
            point_test = ["B", min_lon + (60 + w * 120) / (111 * 1000), min_lat + (60 + k * 120) / (111 * 1000)]
            if isInPolygon(points_list, point_test):
                sol_arr.append(point_test)
            
        

        #if t2_num_hor > 0:
            #point = ["B", min_lon + (60 + j * 240) / (111 * 1000), min_lat + (60 + i * 120) / (111 * 1000)]
            
            #point = ["B", (60 + (t1_num_hor + 1) * 240) / (111 * 1000), min_lat + (60 + i * 120) / (111 * 1000)]
            #if isInPolygon(points_list, point):
            #sol_arr.append(point)

    print("spp.py sol_arr : ", sol_arr)

    return sol_arr

# generate_rectangle("test.json")
# print("finished")
# print(math.cos(60*math.pi/180))

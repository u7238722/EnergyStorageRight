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

    #print(t2_num_hor)

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
def generate_rectangle_from_list(list_exp):
    points_list = []

    #print("spp.py List : ", list_exp)
    error_detect = 0

    # this is used to remove the typo value when user open the website with safari browser. 
    for x in range(len(list_exp)):
        list_exp[x] = ['None' if v is None else v for v in list_exp[x]]
        if error_detect == 1 :
            print("Start to debug")
            old_fst = list_exp[x][0]
            old_second = list_exp[x][1]
            # reorder 
            list_exp[x][0] = next_fst_pos
            list_exp[x][1] =  old_fst
            next_fst_pos = old_second
        #print("this is test : ", list_exp[x])
        for y in range(len(list_exp[x])):
            #print("Detect bug",list_exp[x][y])
            if ("=" in list_exp[x][y]) and (";" in list_exp[x][y]):
                #if ";" in list[x][y]:
                error_detect = 1

                #print("****Found A bug **** ", list_exp[x][y])
                new_string = list_exp[x][y].replace(" ","")
                #print("new string ",new_string)
                get_typo_index = new_string.index(';')
                #print("*** The index is ",get_typo_index)
                next_fst_pos = new_string[-get_typo_index+1:]
                #print("its next fst",next_fst_pos)
                current_lst_pos = new_string[0:get_typo_index-1]
                #print("its current second numbner ", current_lst_pos)
                # current index y = 1 position
                list_exp[x][y] = current_lst_pos
                #print("Update new :", list_exp[x][y])
                #print("Check the current", list_exp[x])
            if "=" in list_exp[x][y]:
                list_exp[x][y] = list_exp[x][y].replace('=','')
                #print("Remove the last = symbol")

            if ";" in list_exp[x][y] :
                list_exp[x][y] = list_exp[x][y].replace(';','')
    #print("Final new list ", list_exp)
    list_exp = list_exp[0:4]
                  


    for point in list_exp:
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
    #print(t2_num_hor)
    #print("test")
    #print(t2_num_hor)

    sol_dict = {}
    sol_arr = []

    ## edit_point
    order = 0
    i = 0
    j = 0
    k = 0
    w = 0
    
    for i in range(0, t1_num_ver+2):
        for j in range(0, t1_num_hor+ round(t1_num_hor * 0.5)):
            point = ["A", min_lon + (120 + j * 240) / (111 * 1000), min_lat + (60 + i * 120) / (111 * 1000)]
            if isInPolygon(points_list, point):
                sol_arr.append(point)
    
    for k in range(0,t2_num_ver+2):
        for w in range(0, t2_num_hor + round(t2_num_hor * 0.5)):
            point_test = ["B", min_lon + (60 + w * 120) / (111 * 1000), min_lat + (60 + k * 120) / (111 * 1000)]
            #if isInPolygon(points_list, point_test):
            sol_arr.append(point_test)
        
    # for a in range(0,t2_num_ver+2):
    #     for b in range(0, t2_num_hor+2):
    #         point_new = ["B", max_lon - (60 + b * 120) / (111 * 1000), max_lat - (60 + a * 120) / (111 * 1000)]
    #         if isInPolygon(points_list, point_new):
    #             sol_arr.append(point_new)
         

        #if t2_num_hor > 0:
            #point = ["B", min_lon + (60 + j * 240) / (111 * 1000), min_lat + (60 + i * 120) / (111 * 1000)]
            
            #point = ["B", (60 + (t1_num_hor + 1) * 240) / (111 * 1000), min_lat + (60 + i * 120) / (111 * 1000)]
            #if isInPolygon(points_list, point):
            #sol_arr.append(point)


    #print("spp.py sol_arr : ", sol_arr)
    # filter(partial(is_not, None), sol_arr)
    # sol_arr.sort()
    # sol_arr = list(sol_arr for sol_arr,_ in itertools.groupby(sol_arr))
   
    # print(" new length is :" ,len(sol_arr))
    #sol_arr = sol_arr[0:80]

    return sol_arr

# generate_rectangle("test.json")
# print("finished")
# print(math.cos(60*math.pi/180))

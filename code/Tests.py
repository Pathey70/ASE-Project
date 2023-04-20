import random
import sys

import TestEngine
from Sym import Sym
from Num import Num
from Data import Data
from Utils import *
from Discretization import bins
from collections import defaultdict
import pandas as pd

def eg_sway(the):
    data = Data(the["file"], the)
    best, rest, _ = data.sway()
    print("\nall ", data.stats(2, data.cols.y))
    print("    ", data.stats(2, data.cols.y, 'div'))
    print("\nbest", data.stats(2, best.cols.y))
    print("    ", data.stats(2, best.cols.y, 'div'))
    print("\nrest", data.stats(2, rest.cols.y))
    print("    ", data.stats(2, rest.cols.y, 'div'))
    print("\nall ~= best?", diffs(best.cols.y, data.cols.y, the))
    print("best ~= rest?", diffs(best.cols.y, rest.cols.y, the))

def eg_xpln(the):
    ans = defaultdict(list)
    ans1 = defaultdict(list)
    l = [8, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37]
    for i in l:
        print('*********')
        the['seed'] = i
        data = Data(the['file'], the)
        best, rest = data.sway_pca()
        rule, most = data.xpln(best, rest)
        # print("\n-----------\nexplain=", showRule(rule))
        data1 = data.clone([i for i in selects(rule, data.rows) if i != None])
        x = data.stats(2, best.cols.y)
        print("sway2", x)
        x2 = data1.stats(2, data1.cols.y)
        print("xpln2", x2)
        for k in x:
            ans[k].append(x[k])
        for k in x2:
            ans1[k].append(x2[k])
    print("sway2_list", dict(ans))
    print("xpln2_list", dict(ans1))
    df = pd.DataFrame.from_dict(ans, orient="index")
    df.to_csv("../etc/data_out/coc10000_sway.csv")
    df1 = pd.DataFrame.from_dict(ans1, orient="index")
    df1.to_csv("../etc/data_out/coc10000_xpln.csv")
    for k in ans:
        ans[k] = round(sum(ans[k]) / 20, 2)
    for k in ans1:
        ans1[k] = round(sum(ans1[k]) / 20, 2)
    print("sway2", dict(ans))
    print("xpln2", dict(ans1))

def eg_get_results(the):
    algorithm=""
    data = Data(the["file"], the)
    if len(data.rows)<=10000 :
        algorithm="Agglomerative Clustering"
    else :
        algorithm="PCA Based Clustering"
    ans = defaultdict(int)
    ans1 = defaultdict(int)
    ans2 = defaultdict(int)
    ans3 = defaultdict(int)

    for i in range(20):
        #print('*********')
        the['seed'] = 937162211 - i * 100
        data = Data(the["file"], the)
        data1 = Data(the["file"], the)


        best, rest, _ = data.sway()

        best1,rest1=None,None
        if algorithm == "Agglomerative Clustering":
            best1,rest1 = data1.sway_agglo()
        else :
            best1,rest1 = data1.sway_pca()    

        x = data.stats(2, best.cols.y)
        x1 = data1.stats(2, best1.cols.y)

        for k in x:
            ans[k] = ans[k] + x[k]
        for k in x1:
            ans1[k] = ans1[k] + x1[k]

        try:
            rule,most= data1.xpln(best1,rest1)
        except:
            continue
    
        data2= data1.clone([i for i in selects(rule,data1.rows) if i!=None])
        x2 = data2.stats(2, data2.cols.y)
        for k in x2:
            ans2[k] = ans2[k] + x2[k]
    
        top2, _ = data.betters(len(best.rows))
        data3 = data.clone(top2)
        x3 = data3.stats(2, data3.cols.y)
        for k in x3:
            ans3[k] = ans3[k] + x3[k]

    for k in ans:
        ans[k] = round(ans[k] / 20, 2)
    for k in ans1:
        ans1[k] = round(ans1[k] / 20, 2)
    for k in ans2:
       ans2[k] = round(ans2[k] / 20, 2)
    for k in ans3:
       ans3[k] = round(ans3[k] / 20, 2)

    print()
    print('Mean Results over 20 runs')
    print()
    print("sway1", dict(ans))
    print(algorithm, dict(ans1))
    print("Xpln2", dict(ans2))
    print("Top", dict(ans3))

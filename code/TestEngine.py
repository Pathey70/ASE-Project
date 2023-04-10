# Referenced : https://www.youtube.com/watch?v=aDTCnAfmyZA

import Tests
from inspect import getmembers, isfunction


tests = []

def run(the):
    global tests
    if the['go'] == 'all' or the['go'] == 'nothing':
        tests = [t for t in getmembers(Tests) if isfunction(t[1]) and t[0].startswith("eg_")]
    else:
        for t in getmembers(Tests):
            if isfunction(t[1]) and t[0].startswith("eg_") and t[0].replace("eg_","") == the['go']:
                tests.append(t)
    fails = 0
    file = open('../etc/out.txt', 'w')
    for test in tests:
        t_name, t_func = test
        try:
            t_func(the)
            print(f"✅PASS : {t_name}")
            file.write(f"✅PASS : {t_name}\n")
        except AssertionError:
            print(f"❌FAIL : {t_name}")
            file.write(f"❌FAIL : {t_name}\n")
            fails += 1
    file.close()

    return fails

import Neuro_pneumonia_trained as np
import Neuro_viral_or_bacterial_trained as nvb
import Neuro_covid_trained as nc
import random

import method

flag = 10

pneumo = np.result_num_pneumo
vb = nvb.result_num_vb
covid = nc.result_num_covid

# flag == 10 cork
# flag == 0 no pneumonia
# flag == 1 bacterial pneumonia
# flag == 2 viral pneumonia
# flag == 3 covid pneumonia

def connector_n():
    if (pneumo == 0):
        print("NO pneumonia")
        flag = 0
    elif (pneumo == 1):
        print("YES pneumonia")
    if (vb == 0 and pneumo == 1):
        print("pneumonia bacterial")
        flag = 1
    elif (vb == 1 and pneumo == 1):
        flag = 2
        print("viral pneumonia")
    if (covid == 0):
        print("NO covid pneumonia")
    elif (covid == 1):
        print("YES covid pneumonia")
        flag = 3

    #if covid != 0: flag = 3
    #print(f"\nflag: {flag}")

    method.clear_eval()
    return flag

def connector():
    if (random.randint(0, 1) == 0):
        print("NO pneumonia")
        flag = 0
    else:
        print("YES pneumonia")
        if (random.randint(0, 1) == 0):
            print("pneumonia bacterial")
            flag = 1
        else:
            print("YES viral pneumonia")
            if (random.randint(0, 1) == 0):
                print("NO covid viral pneumonia")
                flag = 2
            else:
                print("YES covid viral pneumonia")
                flag = 3
    print(f"flag: {flag}")
    return flag
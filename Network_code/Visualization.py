#CHANGE THE DIRECTORY OF THE DISASSEMBLED CAD FILES ACCORDING TO WHERE THEY ARE
#IF NOT CHANGED, RUN THIS CODE CONTAINING CAD/DLx IN THE SAME FOLDER
#
#CHANGE THE NUMBER OF PARTS CONTAINING IN THE ASSEMBLY ACCORDING TO THE ORIGINAL ASSEMBLY FILE


import copy
import numpy as np
import time


import os, errno
from random import randint
import pandas as pd
import os
import networkx as nx
from matplotlib.pyplot import *

def get_folders():
    list_folder = next(os.walk('CAD/.'))[1]
    dl_list = [x for x in list_folder if x.startswith('DL')]
    return dl_list

def get_files(dl):
    list_files = next(os.walk(f'CAD/{dl}/.'), (None, None, []))[2]
#    list_files = glob(f'CAD/{dl}/*.stp')
    list_files = [i.replace(dl, '') for i in list_files]
    list_files = [i.replace('.stp', '') for i in list_files]
    list_files = [i.split('_') for i in list_files]
    for ind, b in enumerate(list_files):
        list_files[ind] = [i for i in b if i != '']
    return list_files


def add_netreference_4(list_n, df, size):
    #convert str to int
    for i in list_n:
        i = [int(n) for n in i]
    #compare current to next
    for i in list_n:
        if len(i) == 1:
            df2 = {'from': 'Initial', 'to': i[0]}
            df = df.append(df2, ignore_index = True)
                    
        if len(i) >= 2:
            i = decode_list2(i, size)
            head, tail = i[:-1], i[-1]
            head.sort() #removing .sort() will give the exact sequence
            tail = i
            tail.sort()
            head = ','.join(head)
            tail = ','.join(tail)
            df2 = {'from': str(head), 'to': str(tail)}
            df = df.append(df2, ignore_index = True)
            
#        print(a, ' - ', len_i)
                    
    return df

def add_netreference_dd(list_n, df, size):
    #convert str to int
    for i in list_n:
        i = [int(n) for n in i]
    #compare current to next
    for i in list_n:
        i = decode_list2(i, size)
        head, tail = i[:-1], i[-1]
        head.sort() #removing .sort() will give the exact sequence
        tail = i
        tail.sort()
        head = ','.join(head)
        tail = ','.join(tail)
        df2 = {'from': str(tail), 'to': 'Fully Disassembled'}
        df = df.append(df2, ignore_index = True)
    return df


def decode_list2(lt, n_solid=15):
    fim = []
    tester = [i for i in range(n_solid)]
    for i, e1 in enumerate(lt):
        fim.append(str(tester[int(e1)]))
        tester.remove(tester[int(e1)])
    return fim
    
    
n_solids = 8  #CHANGE THE NUMBER OF THE PARTS IN THE ASSEMBLY HERE

df_netgraph = pd.DataFrame(columns = ['from','to'])
list_dl = get_folders()
len_dl = len(list_dl)-1
for i,dl in enumerate(list_dl):
    print(i)
    files_DisSeq = get_files(dl)
    df_netgraph = add_netreference_4(files_DisSeq, df_netgraph, n_solids)
    if i == len_dl:
        print('is final at ', i)
        df_netgraph = add_netreference_dd(files_DisSeq, df_netgraph, n_solids)
    
df_netgraph = df_netgraph.drop_duplicates(ignore_index=True)
print(df_netgraph)


#PLOT THE NETWORK GRAPH
G = nx.Graph(nx.from_pandas_edgelist(df_netgraph, 'from', 'to'))
color_map = []
for node in G:
    if node == 'Initial':
        color_map.append('yellow')
    if node == 'Fully Disassembled':
        color_map.append('red')
    if node != 'Fully Disassembled' and node !='Initial': 
        color_map.append('grey')  

#G = nx.from_pandas_edgelist(df_netgraph, 'from', 'to')
figure(figsize=(20, 16))
#change line below to change the time of graph
nx.draw_kamada_kawai(G, node_color=color_map, with_labels=True, node_shape="s",bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.2'))


#check connections of network
leaderboard = {}
for x in G.nodes:
 leaderboard[x] = len(G[x])
s = pd.Series(leaderboard, name='connections')
df2 = s.to_frame().sort_values('connections', ascending=False)
print(df2)



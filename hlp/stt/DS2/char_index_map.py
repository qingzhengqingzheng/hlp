# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 16:50:12 2020

@author: 彭康
"""

# Character_index map list


char_map_str = """
<SPACE> 0
a 1
b 2
c 3
d 4
e 5
f 6
g 7
h 8
i 9
j 10
k 11
l 12
m 13
n 14
o 15
p 16
q 17
r 18
s 19
t 20
u 21
v 22
w 23
x 24
y 25
z 26
' 27
. 28
"""

char_map = {}
index_map = {}

for line in char_map_str.strip().split('\n'):
    ch, index = line.split()
    char_map[ch] = int(index)
    index_map[int(index)] = ch

index_map[0] = ' ' #在index_map里边以0:' '为键值对而char_map里边以'<space>':0为键值对.

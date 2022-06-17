## read style filename [each line] x, y, z ...
## save style: mesh.xls [each line] x, y, z, count, curvature
import csv
from io import TextIOWrapper
import math
import numpy as np

filename = 'D:\membrane.lammpstrj'

def check_input(x_num, y_num):
    if(x_num>=2 and y_num>=2):
        return True
    else:
        return False

def read_data(filename, timestep):
    try:
        f = open(filename,'r')
    except:
        print('cannot open file.')
        return []
    keyword_before = 'ITEM: TIMESTEP'
    current = 0
    while(current<timestep):
        try:
            l = f.readline()
        except:
            return []
        if(l.strip()==keyword_before):
            current = int(f.readline().strip())
            if(current == timestep):
                return get_data(f)
                
            continue
        else:
            continue
    print('cannot find timestep %f in %s'%(timestep,filename))

def get_data(f:TextIOWrapper):
    result = []
    f.readline()
    atom_num = int(f.readline().strip())
    for i in range(4):
        f.readline()
    #find lammpstrj xyz
    l_key =' '.split(f.readline().strip())
    x_index = 0
    y_index = 0
    z_index = 0
    for i in range(len(l_key)):
        if(x_index == 0 and l_key[i][0]=='x'):
            x_index = i-2
        if(y_index == 0 and l_key[i][0]=='y'):
            y_index = i-2
        if(z_index == 0 and l_key[i][0]=='z'):
            z_index = i-2
    if(x_index and y_index and z_index):
        print("Read format success.")
    else:
        print("Check form please.")
        return []
        
    for i in range(atom_num):

        temp = ' '.split(f.readline().strip())
        process_temp = [eval(temp[x_index]),eval(temp[y_index]),eval(temp[z_index])]
        result.append(process_temp)
    return result

def avg(position:list, count, new_position):
    new_x = (position[0]*count + new_position[0])/(count+1)
    new_y = (position[1]*count + new_position[1])/(count+1)
    new_z = (position[2]*count + new_position[2])/(count+1)
    return [new_x, new_y, new_z]

def Save2Csv(datalist):
     with open('D:\membrane.csv', 'w') as csvFile:
         writer = csv.writer(csvFile)
         writer.writerow(['Position.X','Position.Y','Position.Z',"Count","Curvature"])
         for item1 in datalist:
             for item2 in item1:
                writer.writerow([item2[0][0],item2[0][1],item2[0][2],item2[1],item2[2]])

    

    

def Mesh(x_low_b, x_high_b, y_low_b, y_high_b, grid_width,filename,timestep):
    
    x_point_num = int((x_high_b - x_low_b)/grid_width) + 1
    y_point_num = int((y_high_b - y_low_b)/grid_width) + 1
    if(not check_input(x_point_num,y_point_num)):
        print("Mesh Input is incorrect, please try again.")
    # initialize a map
    mesh_map = [[[[0,0,0], 0, 0] for j in range(y_point_num-1)] for i in range(x_point_num-1)]
    datalist = read_data(filename,timestep)
    if(len(datalist)==0):
        print("Error code: -1.")
        return
    for item in datalist:
        i_index = int((item[0]-x_low_b)/grid_width)
        j_index = int((item[1]-y_low_b)/grid_width)
        if(0<=i_index<=x_point_num-2 and 0<=j_index<=y_point_num-2):
            mesh_map[i_index][j_index][0] = avg(mesh_map[i_index][j_index][0],mesh_map[i_index][j_index][1],item)
            mesh_map[i_index][j_index][1] += 1
    

    







f= (0,1,3)
print(f*2)

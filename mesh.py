## read style filename [each line] x, y, z ...
## save style: mesh.xls [each line] x, y, z, count, curvature
import csv
import math
import numpy as np

filename = 'D:\membrane.lammpstrj'
savename = 'D:\membrane.csv'

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
            print(current)
            if(current == timestep):
                print("Find Success.")
                return get_data(f)
                
            continue
        else:
            continue
    print('cannot find timestep %f in %s'%(timestep,filename))

def get_data(f):
    result = []
    f.readline()
    atom_num = int(f.readline().strip())
    print("Atom Number is %f"%atom_num)
    for i in range(4):
        f.readline()
    #find lammpstrj xyz
    l_key =f.readline().strip().split()
    print(l_key)
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

        temp = (f.readline().strip()).split()
        process_temp = [eval(temp[x_index]),eval(temp[y_index]),eval(temp[z_index])]
        result.append(process_temp)
    return result

def avg(position:list, count, new_position):
    new_x = (position[0]*count + new_position[0])/(count+1)
    new_y = (position[1]*count + new_position[1])/(count+1)
    new_z = (position[2]*count + new_position[2])/(count+1)
    return [new_x, new_y, new_z]

def calculate_k(a0,a1,a2,a3,a4,x,y):
    u =2*a3*x+a1
    v = 2*a4*y+a2
    E = 1+math.pow(u,2)
    F = u*v
    G = 1+math.pow(v,2)
    L = 2*a3*(1/math.sqrt(1+math.pow(u,2)+math.pow(v,2)))
    N = 2*a4*(1/math.sqrt(1+math.pow(u,2)+math.pow(v,2)))
    H = (E*N+G*L)/(2*(E*G-F*F))
    return H

def fit_curve(datalist):
    Y = []
    X = []
    for item in datalist:
        Y.append(item[2]) 
        X.append([1,item[0],item[1],item[0]*item[0],item[1]*item[1]])
    X = np.array(X)
    Y = np.array(Y)
    theta = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(Y)
    return theta
    



def Save2Csv(datalist,savename):
    with open(savename, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['Position.X','Position.Y','Position.Z',"Count","Curvature"])
        for item1 in datalist:
            for item2 in item1:
                write_form = [item2[0][0],item2[0][1],item2[0][2],item2[1],item2[2]]
                print(write_form)
                writer.writerow(write_form)
    lines = ''
    with open(savename, 'rt') as csvFile:
        for line in csvFile:
            if(line != '\n'):
                lines+=line
    with open(savename, 'w') as csvFile:
        csvFile.write(lines)

def Mesh(x_low_b, x_high_b, y_low_b, y_high_b, grid_width,filename,timestep,savename):
    
    x_point_num = int((x_high_b - x_low_b)/grid_width) + 1
    y_point_num = int((y_high_b - y_low_b)/grid_width) + 1
    if(not check_input(x_point_num,y_point_num)):
        print("Mesh Input is incorrect, please try again.")
    # initialize a map
    mesh_map = [[[[0,0,0], 0, 0] for _ in range(y_point_num-1)] for i in range(x_point_num-1)]
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
    #start to calculate curvature
    for i in range(x_point_num-1):
        for j in range(y_point_num-1):
            curvature_list = []
            l= i-1
            r=i+1
            u = j+1
            d = j-1
            if(i==0):
                l = -1
            if(j==0):
                d = -1
            if(i == x_point_num-2):
                r = 0
            if(j == y_point_num-2):
                u = 0
            for index1 in [l,i,r]:
                for index2 in [d,j,u]:
                    curvature_list.append(mesh_map[index1][index2][0])
            theta = fit_curve(curvature_list)
            curvature = calculate_k(theta[0],theta[1],theta[2],theta[3],theta[4],mesh_map[i][j][0][0],mesh_map[i][j][0][1])
            print(curvature)
            mesh_map[i][j][2] = curvature
                


    Save2Csv(mesh_map,savename)



Mesh(0,80,0,80,1,filename,24000,savename)

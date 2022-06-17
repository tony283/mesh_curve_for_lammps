import mesh

filename = 'D:\membrane.lammpstrj'
savename = 'D:\membrane.csv'
# *************How to utilize this python file************
# 1. Fill in the location of input lammpstrj file as 'filname' and output csv as 'savename'
# 2. Fill in parameters in mesh.Mesh function 
#   [arg1]: The lower boudary xlo of the membrane
#   [arg2]: The higher boudary xhi of the membrane 
#   [arg3]: The lower boudary ylo of the membrane
#   [arg4]: The higher boudary yhi of the membrane
#   [arg5]: The width between mesh points nearby
#   [arg6]: Don't need to change
#   [arg7]: The timestep in lammpstrj file you want to extract
#   [arg8]: Don't need to change
# 3. Run this function
# You need to add mesh.py in the same folder to import mesh



mesh.Mesh(0,80,0,80,1,filename,24000,savename)
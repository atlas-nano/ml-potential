#!/bin/python
#
#This script convert Siesta output to .cfg file for MLIP input
#Info we need are
#Size => Number of atoms in system. Get this from 'NumberOfAtoms'
#Supercell => Information on the cell. 'Get this from outcell: Unit cell vectors (Ang):'
#AtomData:  id type       cartes_x      cartes_y      cartes_z           fx          fy          fz
#outcoor: Atomic coordinates (Ang): contains id type and xyz info
#for the force 'siesta: Atomic forces (eV/Ang):' data is located here.
#For energy we need the KS energy
#PlusStress is the stress tensor xx, yy, zz,yz,xz,xy
#Found from tag 'Stress tensor Voigt'
#This is reported in kbar to convert to eV
# kbar -> eV
# 1 kbar = 0.1 GPa / 160.21766208 (convert to eV/ang^3) * Volume (ang^3)

import numpy as np
import re,os,sys


class cfg():
    def __init__(self, File1=None):
        if File1 is None:
            self.siesta_output = 'OUT'
        else:
            self.siesta_output = File1
        self.volume=[]
        self.energy=[]
        self.stress=[]
        self.cell_vec =[]
        self.xyz = []
        self.force = []
        self.jobstatus = False
        self.checkjob()
        self.readoutput()
        self.writecfg()
    def checkjob(self):
        #Check job status completion.The volume is reported at the end so self.volume need to be adjust
        with open(self.siesta_output, 'r') as file:
            for line in file.readlines():
                if 'Job completed' in line:
                    self.jobstatus = True

    def readoutput(self):
        #i=0
        inp = [line for line in open(self.siesta_output)]
        ############# SIZE ######################
        with open(self.siesta_output, 'r') as file:
            #inp = file.read()
         for line in file.readlines():
          #print(i)   
          if 'NumberOfAtoms' in line:
              self.natom=int(line.split()[1])
              #print(self.natom)
              break
          #i=i+1
        ############# PlusStress ################  
        with open(self.siesta_output,'r') as file:
         for line in file.readlines():
             if 'Cell volume' in line:
                     self.volume.append(line.split()[-1])
                 #print(line)
        #print(self.volume[:-1])
        if self.jobstatus :
          self.volume=np.array(self.volume[:-1],dtype=float)
        else: 
          self.volume=np.array(self.volume,dtype=float)
        #print(self.volume)
        with open(self.siesta_output,'r') as file:
         for line in file.readlines():
             if 'Voigt' in line:
                 self.stress.append(line.split()[-6:])
                 #print(line)
        self.stress=np.array(self.stress,dtype=float)
        #print(self.stress)
        self.stress=self.stress.ravel().reshape((-1,6))
        #print(self.stress)
        #print(self.stress.shape)
        #print(self.volume.size)
        for i in range(len(self.stress)):
            for j in range(6):
             self.stress[i,j]*=0.1/160.21766208*self.volume[i]
        #print(self.stress)

        ############# Supercell #################
        with open(self.siesta_output,'r') as file:
            for index, line in enumerate(file.readlines()):
                if 'Unit cell vectors' in line:
                    #print(len(line))
                    #print(index)
                    #print(np.array(inp[index+1:index+4]))
                    self.cell_vec.append(inp[index+1:index+4])
        self.cell_vec=np.array(self.cell_vec)#,dtype=float)
        #print(self.cell_vec)
    
        ############# Get position and type ################
        #By default coordinates are printed out in fractional coord
        #We need cartesian coord and therefore need to convert the data
        #Check for flag
        flag_frac = False
        with open(self.siesta_output,'r') as file:
            for index, line in enumerate(file.readlines()):
                if 'outcoor: Atomic coordinates' in line:
                    #print(len(line))
                    #print(index)
                    if 'fractional' in line:
                        flag_frac = True
                    coord=np.array(inp[index+1:index+1+self.natom])
                    #print(len(coord))
                    for i in range(len(coord)):
                        #print(coord[i].split()[0:4])
                        self.xyz.append(coord[i].split()[-3])
                        self.xyz.append(coord[i].split()[0])
                        self.xyz.append(coord[i].split()[1])
                        self.xyz.append(coord[i].split()[2])

                    #self.cell_vec.append(inp[index+1:index+4])
        #print(self.xyz)
        self.xyz=np.array(self.xyz,dtype=float)
        self.xyz=self.xyz.ravel().reshape((-1,self.natom,4))
        #print(self.xyz[0][0].shape)
        ############## Get force #######################333
        with open(self.siesta_output,'r') as file:
            for index, line in enumerate(file.readlines()):
                if 'Atomic forces' in line:
                    #print(len(line))
                    #print(index)
                    force=np.array(inp[index+1:index+1+self.natom])
                    #print(len(coord))
                    for i in range(len(force)):
                        #print(coord[i].split()[0:4])
                        self.force.append(force[i].split()[1])
                        self.force.append(force[i].split()[2])
                        self.force.append(force[i].split()[3])

                    #self.cell_vec.append(inp[index+1:index+4])
        #print(self.xyz)
        self.force=np.array(self.force,dtype=float)
        self.force=self.force.ravel().reshape((-1,self.natom,3))
        #print(self.force)

        ################ Get energy ############################
        with open(self.siesta_output,'r') as file:
         for line in file.readlines():
             if 'E_KS(eV) =' in line:
                 self.energy.append(line.split()[-1])
                 #print(line)
        self.energy=np.array(self.energy,dtype=float)
        #print(self.energy)
        self.Niter = int(len(self.energy))
        #print(self.Niter)
        if flag_frac:
            for i in range(self.Niter):
                A1=self.cell_vec[i][0].split()
                #A1 = np.array(self.cell_vec[i][0],dtype=float)
                #print(A1)
                A2=self.cell_vec[i][1].split()
                A3=self.cell_vec[i][2].split()
                Vec = np.vstack([A1,A2,A3]).T
                Vec= np.array(Vec,dtype=float)
                #print(Vec)
                #print(Vec.shape)
                #break
                for j in range(self.natom):
                 self.xyz[i,j,1:4]=np.matmul(Vec,self.xyz[i,j,1:4]).T
    def writecfg(self):
        with open('train.cfg','w') as f:
            for i in range(self.Niter):
             f.write('BEGIN_CFG\n')
             f.write('Size\n')
             f.write(str(self.natom)+'\n')
             f.write('Supercell\n')
             #print(self.cell_vec[i][0])
             f.write(str(self.cell_vec[i][0]))
             f.write(str(self.cell_vec[i][1]))
             f.write(str(self.cell_vec[i][2]))
             f.write('AtomData: id type cartes_x cartes_y cartes_z     fx     fy     fz\n')
             for j in range(self.natom):
                 f.write('%12d %4d %8.4f %8.4f %8.4f %7.4f %7.4f %7.4f \n' % ( j+1,self.xyz[i,j,0]-1,self.xyz[i,j,1],self.xyz[i,j,2],self.xyz[i,j,3],self.force[i,j,0],self.force[i,j,1],self.force[i,j,2]))#,str(self.force[i,j,:])) )
             f.write('Energy\n')
             f.write(str(self.energy[i]))
             f.write('\nPlusStress: xx yy zz yz xz xy\n')
             f.write('     %5.3f %5.3f %5.3f %5.3f %5.3f %5.3f\n' % (self.stress[i,0],self.stress[i,1],self.stress[i,2],self.stress[i,3],self.stress[i,4],self.stress[i,5] ))
             f.write('Feature    EFS_by   siesta\n') 
             f.write('END_CFG\n\n')




#################################################################################
if __name__ == '__main__':
     #inp = lammpstrj('pvdx.msxx.cross.298K.prod.lammps','data.pvdx.msxx.cross')
     if len(sys.argv)  != 2:
         print("Incorrect input")
         sys.exit("USAGE: python SiestaOUT2MLIPCFG.py  OUT")
     File1 = sys.argv[1]
     #File2 = sys.argv[2]
     #print(File1)
     #print(File2)
     inp = cfg(File1)#,File2)

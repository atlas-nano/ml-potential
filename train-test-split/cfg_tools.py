# FUNCTIONS FOR WORKING WITH MLIP CFG FILES
# author: robert ramji
# contact: rramji@ucsd.edu

import numpy as np

# putting the below functions together
def write_xyz_from_cfg(cfg_file, cfg_name):
    cfgs = read_cfgs(cfg_file)
    xyz = [cfg2data(cfg) for cfg in cfgs]
    write_xyz_trajectory(xyz, cfg_name)

# read a mlip cfg file into an array, line by line
def read_cfgs(cfg_file):
    cfg_trj = []
    with open(cfg_file) as f:
        data = f.readlines()

    for i,line in enumerate(data):
        # line = line.strip('\n')
        if "BEGIN_CFG" in line:
            cfg = [line]
            size = int(data[i+2].strip())
        elif "END_CFG" in line:
            cfg.append(line)
            cfg_trj.append(cfg)
        else:
            try:
                cfg.append(line)
            except ValueError as e:
                print("You got a problem son")
    return cfg_trj

# extract data from mlip cfg file
def cfg2data(cfg):
    size = int(cfg[2].strip())
    element_type_dict = {0: "Li", 1: "C"}
    cell = np.zeros((3,3))
    
    if "Supercell" in cfg[3]:
        for i,line in enumerate(cfg[4:7]):
            dat = line.strip().split()
            vec = np.array([float(a) for a in dat])
            cell[i] = vec

    if "AtomData" in cfg[7]:
        atoms = []
        for i in range(8, 8+size):
            atoms.append(cfg[i].strip().split())
        if len(atoms) != size:
            print("error, num atoms doesn't match size")
    else:
        raise Exception("AtomData not found, check cfg format")
        
    if "Energy" in cfg[8 + size]:
        energy = float(cfg[9 + size].strip())

    atom_data = {
        "size": len(atoms),
        "index": [],
        "element": [],
        "xyz": [],
        "forces": [],
        "energy": energy,
        "cell": cell
    }

    for at in atoms:
        atom_data["index"].append(int(at[0]))
        atom_data["element"].append(element_type_dict[int(at[1])])
        atom_data["xyz"].append([float(at[2]),float(at[3]),float(at[4])])
        atom_data["forces"].append([float(at[5]),float(at[6]),float(at[7])])
        
    return atom_data

# write atom data in atom_data_dict format as defined above into an xyz file
def write_xyz_trajectory(atom_data_dict,name):
    with open(f"{name}.xyz", "w") as f:
        for frame in atom_data_dict:
            f.write(f"{frame['size']}\n")
            f.write(f"graphite\n")

            for i in range(frame['size']):
                x = round(frame['xyz'][i][0],4)
                y = round(frame['xyz'][i][1],4)
                z = round(frame['xyz'][i][2],4)
                f.write(f"{frame['element'][i]}\t{x:.4f}\t{y:.4f}\t{z:.4f}\n")

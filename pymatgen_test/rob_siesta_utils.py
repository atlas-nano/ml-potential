from string import Template

def write_siesta_inputs(system_name, basis, k, head_template, tail_template, fdf_path, structures, strains):

    n_atoms = structures[strains[0]].num_sites
    n_species = len(set(structures[strains[0]].atomic_numbers))
    
    for strain in strains:
    
        file = fdf_path + f"{system_name}.{round(strain,2)}_zStrain.fdf"

        with open(head_template) as f:
            t = Template(f.read())
            head = t.substitute({"name": system_name,
                                 "n_atoms": n_atoms,
                                 "n_species": n_species,
                                 "basis": basis})

        with open(file,"w") as f:
            f.write(head)

        with open(file, "a") as f:
            f.write('\n\nLatticeConstant 1.000000 Ang\n')
            f.write('%block LatticeVectors\n')
            for i in structures[strain].lattice.as_dict()['matrix']:
                f.write(f"\t{i[0]:.10f}\t{i[1]:.10f}\t{i[2]:.10f}\n")
            f.write('%endblock LatticeVectors\n\n')
            f.write('AtomicCoordinatesFormat Ang\n')
            f.write('%block AtomicCoordinatesAndAtomicSpecies\n')
            for i in structures[strain].sites:
                coord = i.coords
                f.write(f"\t{coord[0]:.8f}\t{coord[1]:.8f}\t{coord[2]:.8f}\t{species_index_dict[i.species_string]}\n")
            f.write('%endblock AtomicCoordinatesAndAtomicSpecies\n\n')
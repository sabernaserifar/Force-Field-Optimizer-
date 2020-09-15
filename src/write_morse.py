# Write the data.in file for the LAMMPS optimizer
# Assuming the force field is MORSE

def write_in(ffield, data_file):
    ''' Write the in file '''

    dict = ffield.get_ffield()

    ctrl = dict['CONTROL']

    units         = ctrl['units']
    atom_style    = ctrl['atom_style']
    boundary      = ctrl['boundary']
    special_bonds = ctrl['special_bonds']

    g = open('data.in', 'w')

    g.write('# Morse - generated by optimizer\n')
    g.write('units            ' + units + '\n')
    g.write('atom_style       ' + atom_style + '\n')
    g.write('boundary         ' + boundary + '\n') 
    g.write('#dielectric      1\n')                                   # Commented out
    g.write('#special_bonds    lj 0.0 1.0 1.0 coul 1.0 1.0 1.0\n')     # Change later
    g.write('\n')
    g.write('read_data        ' + data_file + '\n')
    g.write('\n')
    g.write('pair_style       hybrid/overlay morse 12.5 coul/cut 12.50\n')  # Change later
    g.write('\n')
    g.write('#bond_style       zero nocoeff\n')
    g.write('#bond_coeff       *\n')
    g.write('#pair_modify    tail yes\n')
    g.write('#kspace_style    none\n')



    #g.write('#bond_style       harmonic\n')
    g.write('#angle_style      harmonic\n')
    g.write('#dihedral_style   dreiding\n')
    g.write('#improper_style   none\n')
    g.write('#kspace_style     none\n')
    g.write('\n')
    g.write('pair_coeff  * *  coul/cut \n')
    g.write('pair_coeff  * *  morse  0 0 0 \n')
    for i in range(len(dict['VDW'])):
        temp = dict['VDW'][i]
        g.write('pair_coeff ' + str(temp[0]) + ' ' + str(temp[1]) + ' morse ' + ' '.join(map(str, temp[2:])) + '\n')
    g.write('\n')

    # O and H charges of water, this section is not general
    flag_charge = 0
    for i in range(len(dict['ELECTRO'])):
        flag_charge = 1
        temp = dict['ELECTRO'][i]
        g.write('set type ' + '2' + ' ' + ' charge ' + ' '.join(map(str, temp[1:])) + '\n')
    if (flag_charge == 1):
        g.write('set type ' + '1' + ' ' + ' charge ' + str(-float(temp[1])/2.0) + '\n')
    



    g.write('pair_modify pair morse mix geometric\n')
    g.write('# CHECK MIXING RULE FOR MORSE\n')
    g.write('\n')
    """
    for i in range(len(dict['BONDS'])):
        temp = dict['BONDS'][i]
        g.write('bond_coeff ' + str(i+1) + ' ' + ' '.join(map(str, temp[2:])) + '\n')
    for i in range(len(dict['ANGLES'])):
        temp = dict['ANGLES'][i]
        g.write('angle_coeff ' + str(i+1) + ' ' + ' '.join(map(str, temp[3:])) + '\n')
    for i in range(len(dict['DIHEDRALS'])):
        temp = dict['DIHEDRALS'][i]
        g.write('dihedral_coeff ' + str(i+1) + ' ' + ' '.join(map(str, temp[4:])) + '\n')
    """ 

    g.write('\n')
    #g.write('fix              pqeq  all pqeq  1 0.0 20.0 1.0e-6\n')
    g.write('thermo_style     custom etotal pe evdwl  \n')

    g.write('compute 2 all property/atom q\n')
    g.write('compute 3 all property/atom type\n')
    g.write('compute 4 all property/atom id\n')
    g.write('variable charge equal q\n')
    g.write('variable typei equal type\n')
    g.write('variable idi equal id\n')
    g.write('variable evdw equal evdwl\n')

    g.write('compute fox all property/atom fx\n')
    g.write('compute foy all property/atom fy\n')
    g.write('compute foz all property/atom fz\n')

    g.write('variable etota equal etotal\n')
    g.write('compute eng all pe\n')

    g.write('run 0\n')
    g.write('\n')

    g.close()


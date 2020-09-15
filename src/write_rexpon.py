# Write the data.in file for the LAMMPS optimizer
# Assuming the force field is RexPoN

def write_in(ffield, data_file):
    ''' Write the in file '''

    dict = ffield.get_ffield()

    ctrl = dict['CONTROL']

    # Retrieve commands
    units      = ctrl['units']
    atom_style = ctrl['atom_style']
    boundary   = ctrl['boundary']

    g = open('data.in', 'w')

    g.write('# RexPoN - generated by optimizer\n')
    g.write('units            ' + units + '\n')
    g.write('atom_style       ' + atom_style + '\n')                                # Change in CONTROL
    g.write('boundary         ' + boundary + '\n')                               # Change in CONTROL

    g.write('special_bonds lj 1.0 1.0 1.0 coul 1.0 1.0 1.0 \n') 
    g.write('\n')
    g.write('read_data        ' + data_file + '\n')
    g.write('timestep         0.1\n')
    g.write('neigh_modify     one 10000 page 100000\n')
    g.write('\n')
    g.write('pair_style       hybrid/overlay coul/pqeqgauss 0.00 12.00 rexpon NULL lgvdw yes coulomb_off yes checkqeq no safezone 2.0 mincap 200\n') 
    g.write('\n')
    g.write('#           i j                  Xi       Ji       Rc       p  Qc       Rs          K2      K4\n')
    atoms = []
    for i in range(len(dict['ATOMS'])):
        atoms.append(dict['ATOMS'][i][0])
    g.write('pair_coeff  * * rexpon ffield.RexPoN ' + ' '.join(atoms) + '\n') 
    g.write('pair_coeff  * * coul/pqeqgauss 0 0 0 0 0 0 0 0\n')
    for i in range(len(dict['ELECTRO'])):
        temp = dict['ELECTRO'][i]
        g.write('pair_coeff ' + str(temp[0]) + ' ' + str(temp[1]) + ' coul/pqeqgauss ' + ' '.join(map(str, temp[2:])) + '\n')
    g.write('\n')
    #g.write('fix              pqeq  all pqeq  1 0.0 20.0 1.0e-6\n')
    g.write('fix  pqeq all pqeq method 2 nevery 1 charge 0.0 tolerance 1.0e-6 damp 1.0\n')

    g.write('\n')
    g.write("""compute          pqeq all pair coul/pqeqgauss
compute          reax all pair rexpon
variable eb             equal c_reax[1]
variable ea             equal c_reax[2]
variable elp    equal c_reax[3]
variable emol   equal c_reax[4]
variable ev             equal c_reax[5]
variable epen   equal c_reax[6]
variable ecoa   equal c_reax[7]
variable ehb    equal c_reax[8]
variable et             equal c_reax[9]
variable eco    equal c_reax[10]
variable ew             equal c_reax[11]
variable ep             equal c_reax[12]
variable efi    equal c_reax[13]
variable eqeq   equal c_reax[14]
variable epqeq  equal c_pqeq
thermo     1
thermo_style custom step pe v_eb v_ew v_ehb v_ev  v_et v_epqeq\n """)

    g.write('compute 2 all property/atom q\n')
    g.write('compute 3 all property/atom type\n')
    g.write('compute 4 all property/atom id\n')
    g.write('variable charge equal q\n')
    g.write('variable typei equal type\n')
    g.write('variable idi equal id\n')
    g.write('compute fox all property/atom fx\n')
    g.write('compute foy all property/atom fy\n')
    g.write('compute foz all property/atom fz\n')

    g.write('variable etota equal etotal\n')
    g.write('compute eng all pe\n')

    g.write('run 2\n')
    g.write('\n')

    g.close()


    f = open('ffield.RexPoN', 'w')

    f.write('Reactive MD-force field\n')

    temp = dict['GENERAL']
    f.write(str(len(temp)) + '\n')
    for i in range(len(temp)):
        temp2 = temp[i]
        f.write(temp2[0] + '\n')

    temp = dict['ATOMS']
    f.write(str(len(temp)) + '\n')
    f.write('line 1\n')
    f.write('line 2\n')
    f.write('line 3\n')
    for i in range(len(temp)):                                # Modify this later to work
        temp2 = temp[i]
        f.write(temp2[0] + ' ')
        for j in range(len(temp2[1:])/8 + 1):
            if len(' '.join(map(str,temp2[j*8+1:(j+1)*8+1]))) > 1:
                f.write(' '.join(map(str,temp2[j*8+1:(j+1)*8+1])) + '\n')
    
    temp = dict['BONDS']
    f.write(str(len(temp)) + '\n')
    f.write('line 1\n')
    for i in range(len(temp)):
        temp2 = temp[i]
        f.write(temp2[0] + ' ' + temp2[1] + ' ')
        for j in range(len(temp2[2:])/8+1):
            if len(' '.join(map(str,temp2[j*8+2:(j+1)*8+2]))) > 1:
                f.write(' '.join(map(str,temp2[j*8+2:(j+1)*8+2])) + '\n')

    temp = dict['VDW']
    f.write(str(len(temp)) + '\n')
    for i in range(len(temp)):
        temp2 = temp[i]
        f.write(' '.join(map(str, temp2)) + '\n')

    temp = dict['ANGLES']
    f.write(str(len(temp)) + '\n')
    for i in range(len(temp)):
        temp2 = temp[i]
        f.write(' '.join(map(str, temp2)) + '\n')

    temp = dict['DIHEDRALS']
    f.write(str(len(temp)) + '\n')
    for i in range(len(temp)):
        temp2 = temp[i]
        f.write(' '.join(map(str, temp2)) + '\n')
   
    temp = dict['HYDROGEN_BOND']
    f.write(str(len(temp)) + '\n')
    for i in range(len(temp)):
        temp2 = temp[i]
        f.write(temp2[0] + ' ' + temp2[1] + ' ' + temp2[2] + ' ')
        for j in range(len(temp2[3:])/8 + 1):
            if len(' '.join(map(str,temp2[j*8+3:(j+1)*8+3]))) > 1:
                f.write(' '.join(map(str,temp2[j*8+3:(j+1)*8+3])) + '\n')

    f.close()







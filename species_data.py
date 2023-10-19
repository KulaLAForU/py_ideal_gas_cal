# The entire data here comes from the
# https://webbook.nist.gov/chemistry/form-ser/ 
# NIST(National Institute of Standards and Technology) chemistry webbook

############################################################################################
# Unit should be g/mol
sps_M_g_mole = {
    'H2': 2.01588,
    'O2': 31.9988,
    'N2': 28.0134,
    'N': 14.0067,
    'O': 15.9994,
    'H': 1.00794,

}
sps_M = {sps: val / 1000 for sps, val in sps_M_g_mole.items()} # change unit to kg/mol

############################################################################################
# By NIST (https://physics.nist.gov/cgi-bin/cuu/Value?r), molar(universal) gas constant :
R = 8.314462618 # J/mol*K
# P*V = n*R*T 
# n = m/M, R_s = R / M_tol
# P = m/(V*M)R*T = rho * R/M * T = rho * R_s *T 


'''
############################################################################################

speed of sound given by the Newton-Laplace equation:

c = sqrt(K_s / rho) 
which K_s is a coefficient of stiffness
rho is density

c in ideal gases:

K = gamma * p
then 
c = sqrt(gamma * (p/rho))
gamma is the adiabatic index also known as the isentropic expansion factor (c_p / c_v)
By Blottner's model and Eucken's relation, 
the specific heat of constant volume for species s  are written as:
c_v_tr_s = 3/2 * (R / M_s)
c_v_rot_s = R / M_s (Diatomic molecular, i.e. N2, NO)
c_v_rot_s = 0 (Single atom,i.e. O, N)
c_v_vib_s = R / M_s (Diatomic molecular, i.e. N2, NO)
c_v_vib_s = 0 (Single atom,i.e. O, N)
which c_p: specific heat capacity at constant pressure
      c_v: specific heat capacity at constant volume


'''


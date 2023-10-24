# py_ideal_gas_cal
Use ideal gas law to calculate PV=nRT, specific heat capacity of constant volume, heat capasity of constant pressure, gamma (the adiabatic index also known as the isentropic expansion factor (c_p / c_v)), Blottner and Eucken viscosity model and speed of sound in the gas.
For gas specific constant calculation, 3 methods can be choose:

1) General
2) Using Boltzmann constant
3) Use Mayer's relation

The entire data here comes from the https://webbook.nist.gov/chemistry/form-ser/ 
NIST(National Institute of Standards and Technology) chemistry webbook

For Reynolds number and Mach number calculation:

I choose 
Blottner and Eucken viscosity model

mu_tol += frac * 0.1 * exp(A_tol * (log10(T) ** 2) + B_tol * log10(T) + C_tol)
A, B and C are given by chemistry package extracted from http://www.update.uu.se/~jolkkonen/pdf/CRC_TD.pdf and http://www.lmnoeng.com/Flow/GasViscosity.php

This code can tell if you are monatomic or diatomic, 
and thus use a different calculation for specific heat capacity,
because the specific heat at constant volume for species s for translational energy c_v_tr_s is a completely different calculation than c_v_rot_s and c_v_vib_s as follow 

For monatonic:
                c_v = 3/2 * (R / M_s)
                c_p = (R + c_v * M_s) / M_s 
For diatomic:
                c_v = 3/2 * (R / M_s) + 2 * (R / M_s)
                c_p = (R + c_v * M_s) / M_s 


# How to use:

Typing the follow in terminal:
python3 ideal_gas_calculator.py

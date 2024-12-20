import os
from numpy import exp, sqrt, log10, log as ln
import species_data
from chemistry.element import Element

R = species_data.R

# def get_molar_mass(sps):
#     if sps in species_data.sps_M:
#         return species_data.sps_M[sps]
#     else:
#         M = float(input(f" There don't have data exist, please enter the molar mass of {sps}: "))
#         return M

def get_molar_mass(sps):
    try:
        element = Element(sps)
        specie_data = element.get_info()['specie']
        M_s_g = specie_data.get('molWeight')
        M_s = M_s_g / 1000
        return M_s
    except ValueError as e:
        print("Value error of molar mass")

def get_BlottnerEucken(sps):
    try:
        element = Element(sps)
        transport_data = element.get_info()['transport']
        blottner_eucken = transport_data.get('BlottnerEucken', {})
        A = blottner_eucken.get('A')
        B = blottner_eucken.get('B')
        C = blottner_eucken.get('C')
        return A, B, C
    except ValueError as e:
        print("Value error of BlottnerEucken")

def get_number_of_mixture_gases():
    while True:
        num = input(f"Please enter the number of gases in the mixture: ")
        if num.isdigit():
            return int(num)
        else:
            print("Invalid input. Please enter a valid number.")


def calculate_mixed_gas_properties():
    while True:
        num_gases = get_number_of_mixture_gases()
        M_tot = 0
        c_v_tol = 0
        c_p_tol = 0
        mu_tol = 0
        T = Temperature()

        for i in range(num_gases):
            sps = input(f'Please enter the chemical formula of gas {i + 1}: ')
            M_s = get_molar_mass(sps)
            frac = float(input(f'Please enter the mole fraction of {sps}: '))
            M_tot += frac * M_s
            M_type = determine_molecule_type(sps)
            if M_type.lower() == 'monatomic':
                c_v = 3/2 * (R / M_s)
                c_p = (R + c_v * M_s) / M_s # R = J/ kg*K, c_v = (J/K)
            elif M_type.lower() == 'diatomic':
                c_v = 3/2 * (R / M_s) +  (R / M_s)
                c_p = (R + c_v * M_s) / M_s 
            else:
                print('Polyatomic or unknown, check the model')
                continue
            # Notice here is just apply the rule of mixture to calculate the specific heat capacity(c_rot + c_vib = c_vib), the vibration part will be added later
            c_v_tol += frac * c_v
            c_p_tol += frac * c_p
            A, B, C = get_BlottnerEucken(sps)
            mu_tol += frac * 0.1 * exp(A * (ln(T) ** 2) + B * ln(T) + C)
            

        M_avg = float(M_tot)
        R_specific = R / M_tot
        gamma = c_p_tol / c_v_tol
        
        return R_specific, gamma, M_avg, mu_tol, T, c_v_tol, c_p_tol

def Temperature():
    T = float(input(f'Please enter the temperature of (K): '))
    return T

def calculate_R_specific_gamma():
    M_avg = None  
    mu_tol = None
    while True:
        method = input('Please choose the method to calculate R_specific (General/Boltzmann/Mayer): ')
        if method.lower() == 'general':
            R_specific, gamma, M_avg, mu_tol, T, c_v_tol, c_p_tol = calculate_mixed_gas_properties()
        elif method.lower() == 'boltzmann':
            M = float(input('Please enter the molar mass of the gas (kg/mol): '))
            k_B = 1.38e-23  # Boltzmann constant
            R_specific = k_B / M
            gamma = None  
            M_avg = M  
            mu_tol = None
            T = Temperature()
        elif method.lower() == 'mayer':
            c_p = float(input('Please enter the specific heat capacity at constant pressure (J/g·K): '))
            c_v = float(input('Please enter the specific heat capacity at constant volume (J/g·K): '))
            R_specific = c_p - c_v
            gamma = c_p / c_v  
            T = Temperature()
            M_avg = None  
            mu_tol = None   
        else:
            print('Invalid method, Please input again')
            continue
        return R_specific, gamma, M_avg, mu_tol, T, c_v_tol, c_p_tol
    
def determine_molecule_type(sps_det):
    element = Element(sps_det)
    specie_data = element.get_info()['specie']
    particle_type = specie_data.get('particleType')
    if particle_type == 1:
        print('Monatomic')
        return 'Monatomic'
    elif particle_type == 2:
        print('Diatomic')
        return 'Diatomic'
    else:
        return 'Polyatomic or Unknown'


def calculate_ideal_gas_properties():
    while True:
        gas_type = input('Please enter the gas type (Mixture/Single): ')
        if gas_type.lower() == 'mixture':
            R_specific, gamma, M_avg, mu_tol, T, c_v_tol, c_p_tol = calculate_R_specific_gamma()
        elif gas_type.lower() == 'single':
            sps = input(f"Please enter the chemical formula of gas(single):")
            T = Temperature()
            M = get_molar_mass(sps)
            R_specific = R / M
        else:
            print('Invalid gas type, try again')
            continue

        given_properties = input('Please enter the given properties of \n R(selected, if hypersonic sphere),\n P or rho or rhoR(if hypersonic sphere), \n Mach or u,\n L(selected, if Flat Plate),\n separated by commas: ').split(',')

        if 'P' in given_properties or 'p' in given_properties:
            P = float(input('Please enter the pressure (Pa): '))
        else:
            P = None

        if 'rho' in given_properties:
            rho = float(input('Please enter the density (moles) (kg/m^3): '))
        else:
            if 'r' in given_properties or 'R' in given_properties:
                r = float(input('Please enter the sphere radius (M): '))

            if 'rhoR' in given_properties or 'rhor' in given_properties:
                rhoR = float(input('Please enter the density times characteristic length (kg/m^2): '))
                rho = rhoR / r
            else:
                rho = None

        if 'Mach' in given_properties:
            mach = float(input('Please enter the Mach number in x direction: '))
        else:
            mach = None

        if 'u' in given_properties: 
            u = float(input('Please enter the velocity in x direction (m/s): '))
        else:   
            u = None

        if 'L' in given_properties or 'l' in given_properties:
            L = float(input('Please enter the characteristic length (m): '))
        else:
            L = None

        if L is None:
            print('Basic gas calculaiton')
            if P is None:
                P = rho * R_specific * T
            if rho is None:
                rho = P / (R_specific * T)

            c = sqrt(gamma * (P/rho))

            if mach is None:
                mach = u / c
            if u is None:
                u = mach * c            

            print(f'\nPressure: {P} Pa,\n Density: {rho} kg/m^3,\n Temperature: {T} K,\n'
                f'R_specific: {R_specific} J/mol*K,\n Gamma: {gamma},\n Speed of sound in present gas: {c} m/s,\n'
                f'Current Mach number: {mach},\n Current speed: {u} m/s,\n Average molecular weight: {M_avg} kg/mol,\n'
                f'Dynamic viscosity: {mu_tol} Pa*s or N*s/m^2,\n c_p: {c_p_tol}J/g·K,\n c_v: {c_v_tol}J/g·K' )
            break
        else:
            print('Flat plate boundary layer calculation')
            if P is None:
                P = rho * R_specific * T
            if rho is None:
                rho = P / (R_specific * T)

            c = sqrt(gamma * (P/rho))
            # c_2 = sqrt(gamma * R_specific * T)
            
            if mach is None:
                mach = u / c
                Re = (rho * u * L) / mu_tol
            if u is None:
                u = mach * c
                Re = (rho * mach * c * L) / mu_tol
            

            print(f'\nPressure: {P} Pa,\n Density: {rho} kg/m^3,\n Temperature: {T} K,\n'
                f'R_specific: {R_specific} J/mol*K,\n Gamma: {gamma},\n Speed of sound in present gas: {c} m/s,\n'
                f'Current Mach number: {mach},\n Current speed: {u} m/s,\n Average molecular weight: {M_avg} kg/mol,\n'
                f'Dynamic viscosity: {mu_tol} Pa*s or N*s/m^2,\n Reynolds number: {Re},\n c_p: {c_p_tol}J/g·K,\n c_v: {c_v_tol}J/g·K' )
            break
    
if __name__ == "__main__":
    calculate_ideal_gas_properties()

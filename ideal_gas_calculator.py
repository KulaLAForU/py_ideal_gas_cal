from numpy import sqrt
import species_data
from chemistry import Element

R = species_data.R

# def get_molar_mass(sps):
#     if sps in species_data.sps_M:
#         return species_data.sps_M[sps]
#     else:
#         M = float(input(f" There don't have data exist, please enter the molar mass of {sps}: "))
#         return M

def get_molar_mass(sps):
    if sps in Element.('sps'):

        return species_data.sps_M[sps]
    else:
        M = float(input(f" There don't have data exist, please enter the molar mass of {sps}: "))
        return M


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
        for i in range(num_gases):
            sps = input(f'Please enter the chemical formula of gas {i + 1}: ')
            M_s = get_molar_mass(sps)
            frac = float(input(f'Please enter the mole fraction of {sps}: '))
            M_tot += frac * M_s
            M_type = determine_molecule_type(sps)
            if M_type.lower() == 'monatomic':
                c_v = 3/2 * (R / M_s)
                c_p = (R + c_v * M_s) / M_s 
            elif M_type.lower() == 'diatomic':
                c_v = 3/2 * (R / M_s) + 2 * (R / M_s)
                c_p = (R + c_v * M_s) / M_s 
            else:
                print('Polyatomic or unknown, check the model')
                continue
            c_v_tol += frac * c_v
            c_p_tol += frac * c_p
        M_avg = float(M_tot)
        R_specific = R / M_tot
        gamma = c_p_tol / c_v_tol
        return R_specific, gamma, M_avg

def calculate_R_specific_gamma():
    M_avg = None  
    while True:
        method = input('Please choose the method to calculate R_specific (General/Boltzmann/Mayer): ')
        if method.lower() == 'general':
            R_specific, gamma, M_avg = calculate_mixed_gas_properties()
        elif method.lower() == 'boltzmann':
            M = float(input('Please enter the molar mass of the gas (kg/mol): '))
            k_B = 1.38e-23  # Boltzmann constant
            R_specific = k_B / M
            gamma = None  
            M_avg = M  
        elif method.lower() == 'mayer':
            c_p = float(input('Please enter the specific heat capacity at constant pressure (J/mol·K): '))
            c_v = float(input('Please enter the specific heat capacity at constant volume (J/mol·K): '))
            R_specific = c_p - c_v
            gamma = c_p / c_v  
            M_avg = None  
        else:
            print('Invalid method, Please input again')
            continue
        return R_specific, gamma, M_avg  
    
def determine_molecule_type(sps_det):
    els = species_data.sps_M 
    count = 0
    for el in els:
        count += sps_det.count(el)
    if count == 1:
        return 'Monatomic'
    elif count == 2:
        return 'Diatomic'
    else:
        return 'Polyatomic or Unknown'


def calculate_ideal_gas_properties():
    while True:
        gas_type = input('Please enter the gas type (Mixture/Single): ')
        if gas_type.lower() == 'mixture':
            R_specific, gamma, M_avg = calculate_R_specific_gamma()
        elif gas_type.lower() == 'single':
            sps = input(f"Please enter the chemical formula of gas(single):")
            M = get_molar_mass(sps)
            R_specific = R / M
        else:
            print('Invalid gas type, try again')
            continue

        given_properties = input('Please enter the given properties (P, rho, T, any two, separated by commas): ').split(',')

        if 'P' in given_properties:
            P = float(input('Please enter the pressure (Pa): '))
        else:
            P = None

        if 'rho' in given_properties:
            rho = float(input('Please enter the density (moles): kg/m^3'))
        else:
            rho = None

        if 'T' in given_properties:
            T = float(input('Please enter the temperature (K): '))
        else:
            T = None

        if P is None:
            P = rho * R_specific * T
        if rho is None:
            rho = P / (R_specific * T)
        if T is None:
            T = P / (R_specific * rho)
        
        
        c = c = sqrt(gamma * (P/rho))
        print(f'Pressure: {P} Pa, Density: {rho} kg/m^3, Temperature: {T} K, R_specific: {R_specific} J/mol*K, Gamma: {gamma}, Speed of sound in present gas: {c} m/s, Average molecular weight: {M_avg} kg/mol')
        break
    
if __name__ == "__main__":
    calculate_ideal_gas_properties()

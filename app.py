
import streamlit as st

# 4NH3 + 3(O2+3.76N2)====13.28N2 + 6H20
# 2H2 +(O2 + 3.76N2)==== 2H2O + 3.76N2

FUELS = {
    "NH3" : {"M":17,"LHV": 18.6 ,"O2":0.75},
    "H2"  : {"M": 2, "LHV":120, "O2":0.5},

}

#======================================================
#input of Energy Share
#======================================================

st.header("Energy share of NH3 and H2")
E_NH3 = st.number_input("NH3 energy share [%]", 0.0, 100.0, 70.0)
E_H2  = st.number_input("H2 energy share [%]",  0.0, 100.0, 30.0)

st.header("volume Flow of fuel")
V_fuel = st.number_input("Fuel flow [Nm³/min]", 0.0, 1.0, 0.05, step=0.001)

st.header("Inlet conditions")
T_NH3 = st.number_input("NH3 inlet temperature [K]", 273.0, 1000.0, 298.0)
T_H2  = st.number_input("H2 inlet temperature [K]",  273.0, 1000.0, 298.0)
V_air = st.number_input("Air flow [Nm³/min]", 0.0, 1.0, 0.3, step=0.01)
T_air = st.number_input("Air inlet temperature [K]", 273.0, 1300.0, 1273.0)

#==================================================================
# output Air Measurement
#==================================================================

st.header("EXHAUST GASES")
X_H2O = st.number_input("Enter the H2O(%V)",0.0,100.0,0.0)
X_O2 = st.number_input("Enter the O2(%V)",0.0,21.0,0.0)

X_NH3 = st.number_input("Enter the NH3(ppm)",0.0,1000.0,0.0)
X_NO = st.number_input("Enter the NO(ppm)",0.0,100000.0,0.0)
X_N2O = st.number_input("Enter the N2O(ppm)",0.0,1000.0,0.0)


if X_H2O == 0 or V_air == 0:
    st.info("Enter exhaust H2O (wet) and air flow to calculate")
    st.stop()

#======================================================================
#Conversion to mole fraction
#======================================================================
x_H2O = X_H2O/100
x_O2 = X_O2/100
x_NH3 = X_NH3/1e6

x_NO = X_NO/1e6
x_N2O = X_N2O/1e6
x_N2 = 1 - (x_H2O + x_O2 + x_NH3 + x_NO + x_N2O)

#===========================================================================
#O atom calcultion
#===========================================================================
# inlet
m_NH3 = E_NH3/(FUELS["NH3"]["LHV"]*FUELS["NH3"]["M"])
m_H2 =  E_H2/(FUELS["H2"]["LHV"]*FUELS["H2"]["M"])
O2_inlet =( m_NH3*0.75 +m_H2*0.5)/ (m_NH3+ m_H2)  #mole O2 for per mole of  fuel
#===========================================================================
#H atom calcultion
#===========================================================================

Y_H_fuel = (3*m_NH3+2*m_H2)*1.008 /(m_NH3*FUELS["NH3"]["M"]+m_H2 *FUELS["H2"]["M"]) # H atom mass/ mass of fuel

Y_H_exhaust = (2*x_H2O+ 3*x_NH3)*1.008/ (x_H2O*18 + x_O2*32 +x_NH3*17 +x_N2*28 +x_NO*30+x_N2O*44) #H atom mass in exhaust/ mass of mixture

#============================================================================
#Mixture fraction
#============================================================================

MF = Y_H_exhaust/Y_H_fuel

Fuel_Air_ratio = MF/(1-MF)

mass_fuel = (m_NH3*FUELS["NH3"]["M"] + m_H2*FUELS["H2"]["M"]) / (m_NH3 + m_H2)


mass_air = 4.76*28.85 *O2_inlet

Fuel_Air_ratio_ideal = mass_fuel/mass_air

phi_output = Fuel_Air_ratio/ Fuel_Air_ratio_ideal

phi_input =  4.76 * O2_inlet * V_fuel / V_air

st.write(f"φ inlet  = {phi_input:.3f}")
st.write(f"φ outlet = {phi_output:.3f}")
#==========================================================================
#error in combustion
#==========================================================================

change= (phi_output-phi_input)/phi_input
error = change*100

if abs(error) <=3:
   st.success(f"Combustion  Ok  error = {error:.1f} %")
elif abs(error) <=5:
   st.warning(f"Deviation is high = {error:.1f}%")
else:
   st.error(F"check System = {error:.1f}%")

ide
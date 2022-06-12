# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 10:30:34 2021

@author: User
"""

''' Tax parametars''
'''
# =============================================================================
# -------------------------------------------------------------------------------
# Parametar name                       Abbreviation      
# -------------------------------------------------------------------------------
# TAX PARAMETARS
# 
# Corporate tax rate (%)	                t
# Capital allowances (%)	
# - intangibles	                       ai
# - industrial buildings	               ab
# - machinery	                           am
# Treatment of inventories	           v
# Personal tax rates (%)	
# - on interest income	               mi
# - on dividend income	               md
# - on capital gains	                   zc
# Imputation tax credit (%)	           c
# Effective real estate tax rate	       e
# Tax on dividend distributions	       td
# 
# ASSUMPTION
# 
# Real interest rate                     r
# Inflation                              inf
# True economic depreciation	
# - intangibles	                         di
# - industrial buildings	             db
# - machinery	                         dm
# Pre-tax rate of return for EATR, %	  pe
# Shares turned over each period          l
# =============================================================================

import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
#import METR_functions as fun



'''Import data '''

df = pd.read_excel('Dataset.xlsx', 'TaxParametars')

df



'''Define functions '''

# Part 1 Calculated elements

def est_nom_int_rate(r, inf):
    '''
    Parameters
    ----------
    r : real interest rate
    inf : inflation
    Returns
    -------
    Estimate nominal interest rate
    '''
    i = (1+r)*(1+inf)-1
    return i

def accruals_e_cap_gain (mi,zc,l,i):
    '''
    Parameters
    ----------
    i : nominal interest rate
    l : shares turned over each period
    r : real interest rate
    inf : inflation
    
    Returns
    -------
   Accruals-equivalent capital gains tax rate

    '''
    z = (l*zc)/(l+(1-mi)*i)
    return z


def share_disc_rate_cit (mi,z,i):
    '''
    Parameters
    ----------
    mi: Personal tax rates (%) on on interest income
    z: Accruals-equivalent capital gains tax rate
    i : nominal interest rate
        
    Returns
    -------
  Shareholder discount rate only for corporate taxes

    '''
    p = (1-mi)/(1-z)*i
    return p


def share_disc_rate_pit (mi,z,i):
    '''
    Parameters
    ----------
    mi: on interest income
    z: Accruals-equivalent capital gains tax rate
    i : nominal interest rate
        
    Returns
    -------
  Shareholder discount rate for corporate taxes and personal taxes

    '''
    p1 = (1-mi)/(1-z)*i
    return p1


def tax_dis_var_cit (td,t,md,z,c):
    '''
    Parameters
    ----------
    
    td: Tax on dividend distributions	
     t: Corporate tax rate (%)
    md: Personal tax rates (%) on dividend income	 
    z: Accruals-equivalent capital gains tax rate
    c: Imputation tax credit (%)

    Returns
    -------
 Tax discrimination variable only corporate taxes

    '''
    y=((1-td)/(1-t))*((1-md)/((1-z)*(1-c)))
    return y

def tax_dis_var_pit (td,t,md,z,c):
    '''
    Parameters
    ----------
    
    td: Tax on dividend distributions	
     t: Corporate tax rate (%)
    md: Personal tax rates (%) on dividend income	 
    z: Accruals-equivalent capital gains tax rate
    c: Imputation tax credit (%)

    Returns
    -------
 Tax discrimination variable only corporate taxes

    '''
    y1=((1-td)/(1-t))*((1-md)/((1-z)*(1-c)))
    return y1

# Part 2 Net present value of capital allowances
def net_pres_val_cit (t,am,p):
    '''
    Parameters
    ----------
     t: Corporate tax rate (%)
     am: Capital allowances (%) for machinery
     p: Shareholder discount rate only for corporate taxes
     
    Returns
    -------
 Net present value of capital allowances,Capital allowance for machinery:only corporate taxes

    '''
    #Am=(t*am)/(am+p)*(1+((1-am)/(1+p))^1+((1-am)/(1+p))^2+((1-am)/(1+p))^3+((1-am)/(1+p))^4+((1-am)/(1+p))^5+((1-am)/(1+p))^6+((1-am)/(1+p))^7)
    Am=t*am/(am+p)
    return Am


def net_pres_val_pit (t,am,p1):
    '''
    Parameters
    ----------
     t: Corporate tax rate (%)
     am: Capital allowances (%) for machinery
     p1: Shareholder discount rate  Corporate taxes and personal taxes
     
    Returns
    -------
 Net present value of capital allowances,Capital allowance for machinery: corporate taxes and personal taxes

    '''
    Am1=t*am/(am+p1)
    return Am1


def cap_all_build_cit (t,ab,p,am):
    '''
    Parameters
    ----------
     t: Corporate tax rate (%)
     ab: Capital allowances (%) industrial buildings
     am: Capital allowances (%) for machinery
     p: Shareholder discount rate  Corporate taxes
     
    Returns
    -------
   Capital allowance for buildings: - only corporate taxes

    '''
    Ca=(t*ab)/(ab+p)*(1+((1-am)/(1+p))**1+((1-am)/(1+p))**2+((1-am)/(1+p))**3+((1-am)/(1+p))**4+((1-am)/(1+p))**5+((1-am)/(1+p))**6+((1-am)/(1+p))**7+((1-am)/(1+p))**8+((1-am)/(1+p))**9+((1-am)/(1+p))**10+((1-am)/(1+p))**11+((1-am)/(1+p))**12+((1-am)/(1+p))**13+((1-am)/(1+p))**14+((1-am)/(1+p))**15+((1-am)/(1+p))**16+((1-am)/(1+p))**17+((1-am)/(1+p))**18+((1-am)/(1+p))**19+((1-am)/(1+p))**20+((1-am)/(1+p))**21+((1-am)/(1+p))**22+((1-am)/(1+p))**23+((1-am)/(1+p))**24+((1-am)/(1+p))**25)
    return Ca


def cap_all_build_pit (t,ab,p1,am):
    '''
    Parameters
    ----------
     t: Corporate tax rate (%)
     ab: Capital allowances (%) industrial buildings
     am: Capital allowances (%) for machinery
     p1: Shareholder discount rate  Corporate taxes
     
    Returns
    -------
   Capital allowance for buildings: - corporate taxes and personal taxes

    '''
    Ca1=(t*ab)/(ab+p1)*(1+((1-am)/(1+p1))**1+((1-am)/(1+p1))**2+((1-am)/(1+p1))**3+((1-am)/(1+p1))**4+((1-am)/(1+p1))**5+((1-am)/(1+p1))**6+((1-am)/(1+p1))**7+((1-am)/(1+p1))**8+((1-am)/(1+p1))**9+((1-am)/(1+p1))**10+((1-am)/(1+p1))**11+((1-am)/(1+p1))**12+((1-am)/(1+p1))**13+((1-am)/(1+p1))**14+((1-am)/(1+p1))**15+((1-am)/(1+p1))**16+((1-am)/(1+p1))**17+((1-am)/(1+p1))**18+((1-am)/(1+p1))**19+((1-am)/(1+p1))**20+((1-am)/(1+p1))**21+((1-am)/(1+p1))**22+((1-am)/(1+p1))**23+((1-am)/(1+p1))**24+((1-am)/(1+p1))**25)
    return Ca1


def cap_all_intan_cit (t,ai,p):
    '''
    Parameters
    ----------
     t: Corporate tax rate (%)
     ai: Capital allowances (%) intangibles
     p: Shareholder discount rate  Corporate taxes
     
    Returns
    -------
   Capital allowance for intangibles: - only corporate taxes

    '''
    
    Cai=(t*ai)/(ai+p)*(1+((1-ai)/(1+p))**1+((1-ai)/(1+p))**2+((1-ai)/(1+p))**3+((1-ai)/(1+p))**4+((1-ai)/(1+p))**5)
    return Cai


def cap_all_intan_cit (t,ai,p):
    '''
    Parameters
    ----------
     t: Corporate tax rate (%)
     ai: Capital allowances (%) intangibles
     p: Shareholder discount rate  Corporate taxes
     
    Returns
    -------
   Capital allowance for intangibles: - only corporate taxes

    '''
    
    Cai=(t*ai)/(ai+p)*(1+((1-ai)/(1+p))**1+((1-ai)/(1+p))**2+((1-ai)/(1+p))**3+((1-ai)/(1+p))**4+((1-ai)/(1+p))**5)
    return Cai

def cap_all_intan_pit (t,ai,p1):
    '''
    Parameters
    ----------
     t: Corporate tax rate (%)
     ai: Capital allowances (%) intangibles
     p1: Shareholder discount rate  Corporate taxes
     
    Returns
    -------
   Capital allowance for intangibles: - only corporate taxes

    '''
    
    Cai1=(t*ai)/(ai+p1)*(1+((1-ai)/(1+p1))**1+((1-ai)/(1+p1))**2+((1-ai)/(1+p1))**3+((1-ai)/(1+p1))**4+((1-ai)/(1+p1))**5)
    return Cai1


def add_cost_rain_ext_fin (i,y,e):
    '''
    Parameters
    ----------
     i: Nominal interest rate
     y: Tax discrimination variable - Only corporate taxes
     e: Effective real estate tax rate
     
    Returns
    -------
  Additional cost of raising external finance - New equity

    '''
    
    Fne=-((i*(1-y)*(1+e))/(1+i))
    return Fne


def add_cost_rain_ext_fin1 (i,y1,e):
    '''
    Parameters
    ----------
     i: Nominal interest rate
     y1: Tax discrimination variable : Corporate taxes and personal taxes
     e: Effective real estate tax rate
     
    Returns
    -------
  Additional cost of raising external finance - New equity

    '''
    
    Fne1=-((i*(1-y1)*(1+0))/(1+i))
    return Fne1


def add_cost_rain_ext_debt (y,e,i,p,t):
    '''
    Parameters
    ----------
      y: Tax discrimination variable - Only corporate taxes
      e: Effective real estate tax rate
      p: Shareholder discount rate  Corporate taxes
      t: Corporate tax rate (%)
      
    Returns
    -------
  Additional cost of raising external finance - Debt

    '''
    Fde=(y*(1+e)*(p-i*(1-t)))/(1+p)
    return Fde



def add_cost_rain_ext_debt1 (y1,e,i,p1,t):
    '''
    Parameters
    ----------
      y: Tax discrimination variable - Only corporate taxes
      e: Effective real estate tax rate
      p: Shareholder discount rate  Corporate taxes
      t: Corporate tax rate (%)
      
    Returns
    -------
  Additional cost of raising external finance - Debt

    '''
    Fde1=(y1*(1+e)*(p1-i*(1-t)))/(1+p1)
    return Fde1


# ESTIMATION OF EATR

def add_EATR_abs_tax (pe,r):
    '''
    Parameters
    ----------
      pe: Pre-tax rate of return for EATR, %
      r: real interest rate
      
    Returns
    -------
  EATR-Economic rent of the project in the absence of tax

    '''
    Rs=(pe-r)/(1+r)
    return  Rs


'''Estimation of parametars'''

    # Nominal interest rate
df['i'] = est_nom_int_rate(df['r'], df['inf'])
print("Estimate nominal interest rate 'i' is", round(df['i']*100, 2), '%')

    #  Accruals-equivalent capital gains tax rate
df['z'] = accruals_e_cap_gain(df['mi'], df['zc'],df['l'], df['i'])
print("Estimate Accruals-equivalent capital gains tax rate 'z' is", round(df['z']*100, 2), '%')


    #   Shareholder discount rate only for corporate taxes
df['p'] = share_disc_rate_cit(df['mi'], df['z'],df['i'])
print("Shareholder discount rate 'p' is", round(df['p']*100, 2), '%')

    #    Shareholder discount rate for personal income taxes
df['p1'] = share_disc_rate_pit(df['mi'], df['z'],df['i'])
print("Shareholder discount rate 'p1' is", round(df['p1']*100, 2), '%')


    #    Tax discrimination variable only for corporite tax <---OVDE IZLAGA 0.81 A VO PRIMEROT 0.9000
df['y'] = tax_dis_var_cit(df['td'], df['t'], df['md'], df['z'], df['c'])
print("Tax discrimination variable'y' is", round(df['y']*100, 2), '%')


    #    Tax discrimination variable only for corporite tax <---OVDE IZLAGA 0.81 A VO PRIMEROT 0.9000
df['y1'] = tax_dis_var_cit(df['td'], df['t'], df['md'], df['z'], df['c'])
print("Tax discrimination variable'y' is", round(df['y1']*100, 2), '%')


'''Net present value of capital allowances'''
# Capital allowance for machinery


    #     Net present value of capital allowances,Capital allowance for machinery:only corporate taxes
df['Am'] = net_pres_val_cit(df['t'], df['am'], df['p'])
print("Net present value of capital allowances'Am' is", round(df['Am']*100, 2), '%')

    #     Net present value of capital allowances,Capital allowance for machinery: corporate taxes and personal taxes
df['Am1'] = net_pres_val_pit(df['t'], df['am'], df['p1'])
print("Capital allowance for buildings'Am1' is", round(df['Am1']*100, 2), '%')


'''Capital allowance for buildings'''

    #     Capital allowance for buildings: Only corporate taxes
df['Ca1'] = cap_all_build_cit(df['t'], df['ab'], df['p1'],df['am'])
print("Capital allowance for buildings'Ca1' is", round(df['Ca1']*100, 2), '%')

    #     Capital allowance for buildings:  corporate taxes and personal taxes
df['Ca'] = cap_all_build_cit(df['t'], df['ab'], df['p'],df['am'])
print("Net present value of capital allowances'Ca' is", round(df['Ca']*100, 2), '%')


#          Capital allowance for intangibles

df['Cai'] = cap_all_intan_cit(df['t'], df['ai'], df['p'])
print("Capital allowance for intangibles'Cai' is", round(df['Cai']*100, 2), '%')


df['Cai1'] = cap_all_intan_cit(df['t'], df['ai'], df['p1'])
print("Capital allowance for intangibles'Cai1' is", round(df['Cai1']*100, 2), '%')

# Additional cost of raising external finance <---Kaj ovoj parametar ima otpstapuvanje poradi parametarot y koj kaj mene iskaca 0.81 a treba da e 0.900

df['Fne'] = add_cost_rain_ext_fin(df['i'], df['y'], df['e'])
print("Additional cost of raising external finance'Fne' is", round(df['Fne']*100, 2), '%')

df['Fne1'] = add_cost_rain_ext_fin(df['i'], df['y1'], df['e'])
print("Additional cost of raising external finance'Fne1' is", round(df['Fne1']*100, 2), '%')

# Additional cost of raising external finance
df['Fde'] = add_cost_rain_ext_debt(df['y'], df['e'], df['i'],df['p'], df['t'])
print("Additional cost of raising external finance'Fde' is", round(df['Fde']*100, 2), '%')

df['Fde1'] = add_cost_rain_ext_debt(df['y1'], df['e'], df['i'],df['p'], df['t'])
print("Additional cost of raising external finance'Fde1' is", round(df['Fde1']*100, 2), '%')

#EATR
df['Rs'] = add_EATR_abs_tax(df['pe'], df['r'])
print("Additional cost of raising external finance'Rs' is", round(df['Rs']*100, 2), '%')


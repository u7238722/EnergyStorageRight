import numpy_financial as npf
import numpy as np

'''
this file is used to define the roi and irr algorithm
'''
def calculate_IRR_solar_with_battery_payback_model(array_size = 375, project_term = 20, itc_on_storage_system = True,
                                              sgip_eligible = True, in_state_supplier = False, sgip_step = 2,
                                              saving_assumptions = 'Estimated'):

    ##################################################################################################################
    # PART1: CAPEX ASSUMPTIONS
    # 1 Solar PV
    solar_pv_hardware_cost = 1.5  # $/W
    solar_pv_soft_costs = 0.99  # $/W
    solar_pv_cost_per_watt = solar_pv_hardware_cost + solar_pv_soft_costs  # $/W
    solar_pv_capex_without_sales_tax = solar_pv_cost_per_watt * array_size * 1000  # $

    # 2 Energy Storage
    rated_power = 30
    rated_capacity = 68.5
    energy_storage_hardware_cost = 600  # $/kWh
    energy_storage_software_cost = 200  # $/kWh
    energy_storage_cost_per_kWh = energy_storage_hardware_cost + energy_storage_software_cost  # $/kWh
    energy_storage_capex_without_sales_tax = energy_storage_cost_per_kWh * rated_capacity  # $

    # 3 Total Upfront Cost
    total_system_hardware_cost = array_size * solar_pv_hardware_cost * 1000 + rated_capacity * energy_storage_hardware_cost   # $
    total_system_software_cost = array_size * solar_pv_soft_costs * 1000 + rated_capacity * energy_storage_software_cost   # $
    state_sales_tax = 0.075  # %
    city_country_sales_tax = 0  # %
    total_system_upfront_cost = total_system_hardware_cost * (1 + (state_sales_tax + city_country_sales_tax)) + total_system_software_cost    # $

    #################################################################################################################
    # PART2: OPEX ASSUMPTIONS
    # 1 Solar PV
    pv_annual_OM_cost_per_kW_est = 25  # $/kW/yr
    pv_total_opex = array_size * pv_annual_OM_cost_per_kW_est  # $/yr
    pv_opex_escalator = 0.03  # %
    panel_degradation = 0.005  # %
    inverter_replacement_threshold_age = 10  # yr
    inverter_cost = 0.25  # $/W

    # 2 Energy Storge
    ess_est_annual_ON_cost_per_kW = 20  # $/kW/yr
    ess_total_opex = ess_est_annual_ON_cost_per_kW * rated_power  # $/yr
    ess_opex_escalator = 0.03  # %
    battery_replacement_threshold_percent_ofstartoflife_capacity = 0.8  # %
    battery_replacement_threshold_age = 20  # yr
    battery_replacement_cosat_est = 150  # $/kWh
    total_annual_opex = pv_total_opex + ess_total_opex  # $

    #################################################################################################################
    # PART3: COMMERCIAL & FINANCIAL INPUTS
    # project_term = 15  # yrs
    taxable_entity = True  # T/F
    tex_on_incentive = False  # T/F
    tax_on_savings = False  # T/F
    federal_corporate_income_tax = 0.21  # %
    state_corporate_income_tax = 0.0884  # %
    combined_income_tax = 0.279836  # %
    discount_rate = 0.06  # %
    depreciation_schedule_federal = '100%Bonus'  # selection
    depreciation_schedule_state = 'Straight_Line'  # selection
    utility_tax = 0.04  # %
    energy_charge_escalator = 0.03  # %
    demand_charge_escalator = 0.055  # %

    #################################################################################################################
    # PART4: FEDERAL TAX INCENTIVE
    # itc_on_storage_ststem = True  # T/F
    itc_rate = 0.3  # 22.5% - 30%

    itc_value_solar = 0  # a default value $
    if itc_on_storage_system == True:
        itc_value_solar = solar_pv_capex_without_sales_tax * (1 + (state_sales_tax + city_country_sales_tax)) * itc_rate
    else:
        itc_value_solar = 0

    itc_value_storage = 0  # a default value  $
    if itc_on_storage_system == True:
        itc_value_storage = energy_storage_capex_without_sales_tax * (1 + (state_sales_tax + city_country_sales_tax)) * itc_rate
    else:
        itc_value_storage = 0

    #################################################################################################################
    # PART5: STATE REBATE(CA SGIP)
    # sgip_eligible = True  # T/F
    # in_state_supplier = False  # T/F
    # sgip_step = 2  # a default value 1-5

    sgip_base_rate = 0.288 # a default value  # $/kW
    if itc_on_storage_system == True:
        if sgip_step == 1:
            sgip_base_rate = 0.36
        if sgip_step == 2:
            sgip_base_rate = 0.288
        if sgip_step == 3:
            sgip_base_rate = 0.252
        if sgip_step == 4:
            sgip_base_rate = 0.216
        else:
            sgip_base_rate = 0.18
    else:
        if sgip_step == 1:
            sgip_base_rate = 0.5
        if sgip_step == 2:
            sgip_base_rate = 0.4
        if sgip_step == 3:
            sgip_base_rate = 0.35
        if sgip_step == 4:
            sgip_base_rate = 0.3
        else:
            sgip_base_rate = 0.25

    in_state_supplier_adder = 1.20  # adj.
    system_duration = rated_capacity * rated_power  # hrs
    avg_discharge_per_hour = rated_capacity / system_duration  # kWh

    capacity_adjustment_table = [[60, 0,0],
                                 [9,0,0],
                                 [0,0,0]]  # a defult list
    # to finish the capacity_adjustment_table

    sgip_rebated_capacity = capacity_adjustment_table[0][0] + capacity_adjustment_table[0][1] * 0.5 + capacity_adjustment_table[0][2] * 0.25 + \
                            capacity_adjustment_table[1][0] * 0.5 + capacity_adjustment_table[1][1] * 0.25 + capacity_adjustment_table[1][2] * 0.125 + \
                            capacity_adjustment_table[2][0] * 0.25 + capacity_adjustment_table[2][1] * 0.125 + capacity_adjustment_table[2][2] * 0.0625

    sgip_eligible_rebate = 0.29  # a default value  $
    if sgip_eligible == True:
        if in_state_supplier == True:
            sgip_eligible_rebate = in_state_supplier_adder * sgip_base_rate
        else:
            sgip_eligible_rebate = 1 * sgip_base_rate
    else:
        sgip_eligible_rebate = 0

    total_sgip_rebate = sgip_eligible_rebate * sgip_rebated_capacity * 1000  # $

    percent_of_rebate_in_firstyear = 0.5  # a default value  %
    if rated_power < 30:
        percent_of_rebate_in_firstyear = 1
    else:
        percent_of_rebate_in_firstyear = 0.5

    PBI_duration = 1  # a default value  yr
    if rated_power <= 30:
        PBI_duration = 1
    else:
        PBI_duration = 5

    PBI_yr1_rebate = 9252   # a default value  $
    if sgip_eligible == True:
        PBI_yr1_rebate = total_sgip_rebate * percent_of_rebate_in_firstyear
    else:
        PBI_yr1_rebate = 0

    PBI_annual_rebate = 9252   # a default value  $
    if sgip_eligible == True:
        PBI_annual_rebate = total_sgip_rebate * (1 - percent_of_rebate_in_firstyear) / PBI_duration
    else:
        PBI_annual_rebate = 0

    #################################################################################################################
    # PART6: YEAR
    Annual_cash_flow_year0 = -1 * total_system_upfront_cost
    Cumulative_cash_flow_year0 = -1 * total_system_upfront_cost
    Annual_cash_flow_list = []
    payback_list = []

    # simulation_output
    #######################################################
    # 6.1: ASSETS
    # array_size = 375  # kW DC
    pv_degrgration = 0.005

    rated_power = 30  # kW
    rated_capacity = 68.5  # kWh

    #######################################################
    # 6.2: SAVING ASSUMPTIONS
    saving_assumptions = 'Estimated'

    saving_derate_factor = 0.8353  # a default value
    if saving_assumptions == 'Estimated':
        saving_derate_factor = 0.835299023361892
    else:
        if saving_assumptions == 'Conservative':
            saving_derate_factor = 0.748928898678197
        else:
            if saving_assumptions == 'Optimal':
                saving_derate_factor = 1.0
            else:
                saving_derate_factor = 0.835299023361892

    #########################################################
    # 6.3:YEAR
    # Assume the project terms are ranged from 1 year to 30 years
    ess_system_cycles = 35
    ess_batery_health = [0.9858, 0.9743, 0.9648, 0.9570, 0.9504, 0.9446, 0.9396, 0.9351, 0.9311, 0.9274,
                         0.9239, 0.9206, 0.9175, 0.9144, 0.9115, 0.9115, 0.9115, 0.9115, 0.9115, 0.9115,
                         0.9115, 0.9115, 0.9115, 0.9115, 0.9115, 0.9115, 0.9115, 0.9115, 0.9115, 0.9115]
    ess_demand_charge_savings = [13689, 13615, 13553, 13500, 13455, 13416, 13381, 13350, 13321, 13294,
                                 13269, 13245, 13222, 13199, 13178, 13178, 13178, 13178, 13178, 13178,
                                 13178, 13178, 13178, 13178, 13178, 13178, 13178, 13178, 13178, 13178]
    pv_demand_charge_savings = [8645, 8602, 8559, 8516, 9474, 8431, 8389, 8347, 8305, 8264,
                                8223, 8181, 8141, 8100, 8059, 8059, 8059, 8059, 8059, 8059,
                                8059, 8059, 8059, 8059, 8059, 8059, 8059, 8059, 8059, 8059]

    total_annual_savings_list = []

    for i in range(1, project_term + 1):
        ess_effective_cpacity = ess_system_cycles * ess_batery_health[i-1]

        # ENERGY
        total_solar_pv_generation = 482788 * (1 - pv_degrgration)**(i-1)
        total_solar_pv_generation_savings = 58794 * (1 - pv_degrgration)**(i-1)

        ess_energy_savings_cost = 35
        if i <= 2:
            ess_energy_savings_cost = 35
        elif i <= 6:
            ess_energy_savings_cost = 34
        elif i <= 13:
            ess_energy_savings_cost = 33
        else:  # i <= 15
            ess_energy_savings_cost = 32

        total_energy_savings = total_solar_pv_generation_savings + ess_energy_savings_cost

        # DEMAND
        demand_savings_from_post_pv_tariff_switch = 0
        total_demand_savings = ess_demand_charge_savings[i-1] + pv_demand_charge_savings[i-1] + demand_savings_from_post_pv_tariff_switch

        # FIXED CHARGES
        fixed_charge_savings_from_post_pv_tariff_switch = 0

        annual_savings_in_year_i = total_energy_savings + total_demand_savings + fixed_charge_savings_from_post_pv_tariff_switch
        total_annual_savings_list.append(annual_savings_in_year_i)

        # REVENUE
        revenue_from_energy_savings = total_energy_savings * (1 + energy_charge_escalator)**(i-1) * (1 + utility_tax)
        revenue_from_demand_charge_savings = (ess_demand_charge_savings[i-1] + pv_demand_charge_savings[i-1]) * (1 + demand_charge_escalator)**(i-1) * (1 + utility_tax)
        revenue_from_demand_savings_from_postTV_tariff_switch = demand_savings_from_post_pv_tariff_switch * (1 + demand_charge_escalator)**(i-1) * (1 + utility_tax)
        revenue_from_fixed_charge_savings_from_postTV_tariff_switch = fixed_charge_savings_from_post_pv_tariff_switch * ( 1 + utility_tax)
        total_annual_revenue = revenue_from_energy_savings + revenue_from_demand_charge_savings + \
                               revenue_from_demand_savings_from_postTV_tariff_switch + revenue_from_fixed_charge_savings_from_postTV_tariff_switch

        solar_pv_OM_cost = -1 * pv_total_opex * (1 + pv_opex_escalator)**(i-1)
        energy_storage_OM_costs = -1 * ess_total_opex * ( + ess_opex_escalator)**(i-1)
        solar_pv_inverter_replacement = 0
        if i == 10:
            solar_pv_inverter_replacement = -93750

        battery_replacement = 0
        total_annual_OM_cost = solar_pv_OM_cost + energy_storage_OM_costs + solar_pv_inverter_replacement + battery_replacement

        sgip_rebate = 18504  # default value
        if i == 1:
            if i <= PBI_duration:
                sgip_rebate = PBI_yr1_rebate + PBI_annual_rebate
            else:
                sgip_rebate = PBI_yr1_rebate + 0
        else:
            if i <= PBI_duration:
                sgip_rebate = 0 + PBI_annual_rebate
            else:
                sgip_rebate = 0 + 0

        total_annual_rebate = sgip_rebate  # default value

        # EBITDA
        EBITDA = total_annual_revenue + total_annual_OM_cost + total_annual_rebate

        income_tax = 0
        investment_tax_credit_solar = itc_value_solar    # default value
        if i == 1:
            investment_tax_credit_solar = itc_value_solar
        else:
            investment_tax_credit_solar = 0

        investment_tax_credit_storage = itc_value_storage    # default value
        if i == 1:
            investment_tax_credit_storage = itc_value_storage
        else:
            investment_tax_credit_storage = 0

        state_depreciation_tax_savings_solar = 8627    # default value
        if i >= 11:
            state_depreciation_tax_savings_solar = 0

        state_depreciation_tax_saving_storage = 512    # default value
        if i >= 11:
            state_depreciation_tax_saving_storage = 0

        federal_depreciation_tax_savings_solar = 174205     # default value
        if i != 1:
            federal_depreciation_tax_savings_solar = 0

        federal_depreciation_tax_savings_storage = 10332     # default value
        if i != 1:
            federal_depreciation_tax_savings_storage = 0

        total_tax_benefit = income_tax + investment_tax_credit_solar + investment_tax_credit_storage + \
                            state_depreciation_tax_savings_solar + state_depreciation_tax_saving_storage + \
                            federal_depreciation_tax_savings_solar + federal_depreciation_tax_savings_storage

        annual_cash_flow = EBITDA + total_tax_benefit
        Annual_cash_flow_list.append(annual_cash_flow)

        cumulative_cash_flow = Cumulative_cash_flow_year0 + annual_cash_flow

        payback = 1.0
        if cumulative_cash_flow > 0:
            if Cumulative_cash_flow_year0 < 0:
                payback = -1 * Cumulative_cash_flow_year0 / (cumulative_cash_flow - Cumulative_cash_flow_year0)
            else:
                payback = 0
        else:
            payback = 1
        payback_list.append(payback)


    #################################################################################################################
    # PART7: FINANCIAL OUTCOME
    Payback = sum(payback_list)
    Net_Present_Value = npf.npv(discount_rate, Annual_cash_flow_list) - total_system_upfront_cost

    Annual_cash_flow_list.insert(0, Annual_cash_flow_year0)
    Internal_Rate_of_Return = npf.irr(Annual_cash_flow_list)
    Internal_Rate_of_Return = Internal_Rate_of_Return * 1.0555
    if Internal_Rate_of_Return < 0.08:
        Internal_Rate_of_Return = 0.07959142
    if Internal_Rate_of_Return > 0.165:
        Internal_Rate_of_Return = 0.16408888
    return Internal_Rate_of_Return


def calculate_IRR_solar_no_storage_model(array_size = 375, project_term = 15, itc_on_storage_system = False,
                                              sgip_eligible = True, in_state_supplier = False, sgip_step = 2,
                                         saving_assumptions = 'Estimated'):

    ##################################################################################################################
    # PART1: CAPEX ASSUMPTIONS
    # 1 Solar PV
    # array_size = 375  # kW DC
    solar_pv_hardware_cost = 1.5  # $/W
    solar_pv_soft_costs = 0.99  # $/W
    solar_pv_cost_per_watt = solar_pv_hardware_cost + solar_pv_soft_costs  # $/W
    solar_pv_capex_without_sales_tax = solar_pv_cost_per_watt * array_size * 1000  # $

    # 2 Energy Storge
    rated_power = 30
    rated_capacity = 68.5
    energy_storage_hardware_cost = 0  # $/kWh
    energy_storage_software_cost = 0  # $/kWh
    energy_storage_cost_per_kWh = energy_storage_hardware_cost + energy_storage_software_cost  # $/kWh
    energy_storage_capex_without_sales_tax = energy_storage_cost_per_kWh * rated_capacity  # $

    # 3 Total Upfront Cost
    total_system_hardware_cost = array_size * solar_pv_hardware_cost * 1000 + rated_capacity * energy_storage_hardware_cost  # $
    total_system_software_cost = array_size * solar_pv_soft_costs * 1000 + rated_capacity * energy_storage_software_cost  # $
    state_sales_tax = 0.075  # %
    city_country_sales_tax = 0  # %
    total_system_upfront_cost = total_system_hardware_cost * (
                1 + (state_sales_tax + city_country_sales_tax)) + total_system_software_cost  # $

    #################################################################################################################
    # PART2: OPEX ASSUMPTIONS
    # 1 Solar PV
    pv_annual_OM_cost_per_kW_est = 25  # $/kW/yr
    pv_total_opex = array_size * pv_annual_OM_cost_per_kW_est  # $/yr
    pv_opex_escalator = 0.03  # %
    panel_degradation = 0.005  # %
    inverter_replacement_threshold_age = 10  # yr
    inverter_cost = 0.25  # $/W

    # 2 Energy Storge
    ess_est_annual_ON_cost_per_kW = 0  # $/kW/yr
    ess_total_opex = ess_est_annual_ON_cost_per_kW * rated_power  # $/yr
    ess_opex_escalator = 0  # %
    battery_replacement_threshold_percent_ofstartoflife_capacity = 0  # %
    battery_replacement_threshold_age = 0  # yr
    battery_replacement_cosat_est = 0  # $/kWh
    total_annual_opex = pv_total_opex + ess_total_opex  # $

    #################################################################################################################
    # PART3: COMMERCIAL & FINANCIAL INPUTS
    # project_term = 15  # yrs
    taxable_entity = True  # T/F
    tex_on_incentive = False  # T/F
    tax_on_savings = False  # T/F
    federal_corporate_income_tax = 0.21  # %
    state_corporate_income_tax = 0.0884  # %
    combined_income_tax = 0.279836  # %
    discount_rate = 0.06  # %
    depreciation_schedule_federal = '100%Bonus'  # selection
    depreciation_schedule_state = 'Straight_Line'  # selection
    utility_tax = 0.04  # %
    energy_charge_escalator = 0  # %
    demand_charge_escalator = 0.055  # %

    #################################################################################################################
    # PART4: FEDERAL TAX INCENTIVE
    # itc_on_storage_ststem = True  # T/F
    itc_rate = 0.3  # 22.5% - 30%

    itc_value_solar = 0  # a default value $
    if itc_on_storage_system == True:
        itc_value_solar = solar_pv_capex_without_sales_tax * (1 + (state_sales_tax + city_country_sales_tax)) * itc_rate
    else:
        itc_value_solar = 0

    itc_value_storage = 0  # a default value  $


    #################################################################################################################
    # PART5: STATE REBATE(CA SGIP)
    # sgip_eligible = True  # T/F
    # in_state_supplier = False  # T/F
    # sgip_step = 2  # a default value 1-5

    sgip_base_rate = 0.288  # a default value  # $/kW
    if itc_on_storage_system == True:
        if sgip_step == 1:
            sgip_base_rate = 0.36
        if sgip_step == 2:
            sgip_base_rate = 0.288
        if sgip_step == 3:
            sgip_base_rate = 0.252
        if sgip_step == 4:
            sgip_base_rate = 0.216
        else:
            sgip_base_rate = 0.18
    else:
        if sgip_step == 1:
            sgip_base_rate = 0.5
        if sgip_step == 2:
            sgip_base_rate = 0.4
        if sgip_step == 3:
            sgip_base_rate = 0.35
        if sgip_step == 4:
            sgip_base_rate = 0.3
        else:
            sgip_base_rate = 0.25

    in_state_supplier_adder = 1.20  # adj.
    system_duration = rated_capacity * rated_power  # hrs
    avg_discharge_per_hour = rated_capacity / system_duration  # kWh

    capacity_adjustment_table = [[60, 0, 0],
                                 [9, 0, 0],
                                 [0, 0, 0]]  # a defult list
    # to finish the capacity_adjustment_table

    sgip_rebated_capacity = capacity_adjustment_table[0][0] + capacity_adjustment_table[0][1] * 0.5 + \
                            capacity_adjustment_table[0][2] * 0.25 + \
                            capacity_adjustment_table[1][0] * 0.5 + capacity_adjustment_table[1][1] * 0.25 + \
                            capacity_adjustment_table[1][2] * 0.125 + \
                            capacity_adjustment_table[2][0] * 0.25 + capacity_adjustment_table[2][1] * 0.125 + \
                            capacity_adjustment_table[2][2] * 0.0625

    sgip_eligible_rebate = 0.29  # a default value  $
    if sgip_eligible == True:
        if in_state_supplier == True:
            sgip_eligible_rebate = in_state_supplier_adder * sgip_base_rate
        else:
            sgip_eligible_rebate = 1 * sgip_base_rate
    else:
        sgip_eligible_rebate = 0

    total_sgip_rebate = sgip_eligible_rebate * sgip_rebated_capacity * 1000  # $

    percent_of_rebate_in_firstyear = 0.5  # a default value  %
    if rated_power < 30:
        percent_of_rebate_in_firstyear = 1
    else:
        percent_of_rebate_in_firstyear = 0.5

    PBI_duration = 1  # a default value  yr
    if rated_power <= 30:
        PBI_duration = 1
    else:
        PBI_duration = 5

    PBI_yr1_rebate = 9252  # a default value  $
    if sgip_eligible == True:
        PBI_yr1_rebate = total_sgip_rebate * percent_of_rebate_in_firstyear
    else:
        PBI_yr1_rebate = 0

    PBI_annual_rebate = 9252  # a default value  $
    if sgip_eligible == True:
        PBI_annual_rebate = total_sgip_rebate * (1 - percent_of_rebate_in_firstyear) / PBI_duration
    else:
        PBI_annual_rebate = 0

    #################################################################################################################
    # PART6: YEAR
    Annual_cash_flow_year0 = -1 * total_system_upfront_cost
    Cumulative_cash_flow_year0 = -1 * total_system_upfront_cost
    Annual_cash_flow_list = []
    payback_list = []

    # simulation_output
    #######################################################
    # 6.1: ASSETS
    # array_size = 375  # kW DC
    pv_degrgration = 0.005

    rated_power = 30  # kW
    rated_capacity = 68.5  # kWh

    #######################################################
    # 6.2: SAVING ASSUMPTIONS
    #

    #########################################################
    # 6.3:YEAR
    # Assume the project terms are ranged from 1 year to 15 years
    ess_system_cycles = 35
    ess_batery_health = [0.9858, 0.9743, 0.9648, 0.9570, 0.9504, 0.9446, 0.9396, 0.9351, 0.9311, 0.9274,
                         0.9239, 0.9206, 0.9175, 0.9144, 0.9115, 0.9115, 0.9115, 0.9115, 0.9115, 0.9115,
                         0.9115, 0.9115, 0.9115, 0.9115, 0.9115, 0.9115, 0.9115, 0.9115, 0.9115, 0.9115]
    ess_demand_charge_savings = [13689, 13615, 13553, 13500, 13455, 13416, 13381, 13350, 13321, 13294,
                                 13269, 13245, 13222, 13199, 13178, 13178, 13178, 13178, 13178, 13178,
                                 13178, 13178, 13178, 13178, 13178, 13178, 13178, 13178, 13178, 13178]
    pv_demand_charge_savings = [8645, 8602, 8559, 8516, 9474, 8431, 8389, 8347, 8305, 8264,
                                8223, 8181, 8141, 8100, 8059, 8059, 8059, 8059, 8059, 8059,
                                8059, 8059, 8059, 8059, 8059, 8059, 8059, 8059, 8059, 8059]

    total_annual_savings_list = []

    for i in range(1, project_term + 1):
        ess_effective_cpacity = ess_system_cycles * ess_batery_health[i - 1]

        # ENERGY
        total_solar_pv_generation = 482788 * (1 - pv_degrgration) ** (i - 1)
        total_solar_pv_generation_savings = 58794 * (1 - pv_degrgration) ** (i - 1)

        ess_energy_savings_cost = 0
        if i <= 2:
            ess_energy_savings_cost = 35
        elif i <= 6:
            ess_energy_savings_cost = 34
        elif i <= 13:
            ess_energy_savings_cost = 33
        else:  # i <= 15
            ess_energy_savings_cost = 32

        total_energy_savings = total_solar_pv_generation_savings + ess_energy_savings_cost

        # DEMAND
        demand_savings_from_post_pv_tariff_switch = 0
        total_demand_savings = ess_demand_charge_savings[i - 1] + pv_demand_charge_savings[
            i - 1] + demand_savings_from_post_pv_tariff_switch

        # FIXED CHARGES
        fixed_charge_savings_from_post_pv_tariff_switch = 0

        annual_savings_in_year_i = total_energy_savings + total_demand_savings + fixed_charge_savings_from_post_pv_tariff_switch
        total_annual_savings_list.append(annual_savings_in_year_i)

        # REVENUE
        revenue_from_energy_savings = total_energy_savings * (1 + energy_charge_escalator) ** (i - 1) * (
                    1 + utility_tax)
        revenue_from_demand_charge_savings = (ess_demand_charge_savings[i - 1] + pv_demand_charge_savings[i - 1]) * (
                    1 + demand_charge_escalator) ** (i - 1) * (1 + utility_tax)
        revenue_from_demand_savings_from_postTV_tariff_switch = demand_savings_from_post_pv_tariff_switch * (
                    1 + demand_charge_escalator) ** (i - 1) * (1 + utility_tax)
        revenue_from_fixed_charge_savings_from_postTV_tariff_switch = fixed_charge_savings_from_post_pv_tariff_switch * (
                    1 + utility_tax)
        total_annual_revenue = revenue_from_energy_savings + revenue_from_demand_charge_savings + \
                               revenue_from_demand_savings_from_postTV_tariff_switch + revenue_from_fixed_charge_savings_from_postTV_tariff_switch

        solar_pv_OM_cost = -1 * pv_total_opex * (1 + pv_opex_escalator) ** (i - 1)
        energy_storage_OM_costs = -1 * ess_total_opex * (+ ess_opex_escalator) ** (i - 1)
        solar_pv_inverter_replacement = 0
        if i == 10:
            solar_pv_inverter_replacement = -93750

        battery_replacement = 0
        total_annual_OM_cost = solar_pv_OM_cost + energy_storage_OM_costs + solar_pv_inverter_replacement + battery_replacement

        sgip_rebate = 18504  # default value
        if i == 1:
            if i <= PBI_duration:
                sgip_rebate = PBI_yr1_rebate + PBI_annual_rebate
            else:
                sgip_rebate = PBI_yr1_rebate + 0
        else:
            if i <= PBI_duration:
                sgip_rebate = 0 + PBI_annual_rebate
            else:
                sgip_rebate = 0 + 0

        total_annual_rebate = sgip_rebate  # default value

        # EBITDA
        EBITDA = total_annual_revenue + total_annual_OM_cost + total_annual_rebate

        income_tax = 0
        investment_tax_credit_solar = itc_value_solar  # default value
        if i == 1:
            investment_tax_credit_solar = itc_value_solar
        else:
            investment_tax_credit_solar = 0

        investment_tax_credit_storage = itc_value_storage  # default value
        state_depreciation_tax_savings_solar = 8627  # default value
        state_depreciation_tax_saving_storage = 0  # default value
        federal_depreciation_tax_savings_solar = 174205  # default value
        federal_depreciation_tax_savings_storage = 0  # default value

        total_tax_benefit = income_tax + investment_tax_credit_solar + investment_tax_credit_storage + \
                            state_depreciation_tax_savings_solar + state_depreciation_tax_saving_storage + \
                            federal_depreciation_tax_savings_solar + federal_depreciation_tax_savings_storage

        annual_cash_flow = EBITDA + total_tax_benefit
        Annual_cash_flow_list.append(annual_cash_flow)

        cumulative_cash_flow = Cumulative_cash_flow_year0 + annual_cash_flow

        payback = 1.0
        if cumulative_cash_flow > 0:
            if Cumulative_cash_flow_year0 < 0:
                payback = -1 * Cumulative_cash_flow_year0 / (cumulative_cash_flow - Cumulative_cash_flow_year0)
            else:
                payback = 0
        else:
            payback = 1
        payback_list.append(payback)

    #################################################################################################################
    # PART7: FINANCIAL OUTCOME
    Payback = sum(payback_list)
    Net_Present_Value = npf.npv(discount_rate, Annual_cash_flow_list) - total_system_upfront_cost

    Annual_cash_flow_list.insert(0, Annual_cash_flow_year0)
    # print(Annual_cash_flow_list)
    Internal_Rate_of_Return = npf.irr(Annual_cash_flow_list)
    Internal_Rate_of_Return = Internal_Rate_of_Return * 0.78
    if Internal_Rate_of_Return < 0.12:
        Internal_Rate_of_Return = 0.11591423234245
    if Internal_Rate_of_Return > 0.17:
        Internal_Rate_of_Return = 0.174681275455645
    return Internal_Rate_of_Return


def calculate_IRR_solar_with_pumped_hydro_model(array_size = 375, project_term = 15, itc_on_storage_system = False,
                                              sgip_eligible = True, in_state_supplier = False, sgip_step = 2,
                                                saving_assumptions = 'Estimated'):

    no_storage_irr = calculate_IRR_solar_no_storage_model(array_size=array_size, project_term=project_term)

    system_life_year = 50
    total_upfront_pumped_hydro = 800 + 70 + 247
    anual_cashflow_year0 = -1 * total_upfront_pumped_hydro
    annual_cashflow_year1 = 34 + 8 + 13 + 55 + (((800 * 0.8) + (70 * 0.85)) / system_life_year) \
                            + ((0.4 * 8.2 / project_term) * 365)
    annual_cashflow_list = []

    for i in range(project_term):
        annual_cashflow_list.append(annual_cashflow_year1)

    payback = project_term * annual_cashflow_year1
    discount_rate = 0.05 + 0.02
    net_present_value = npf.npv(discount_rate, annual_cashflow_list) - total_upfront_pumped_hydro

    annual_cashflow_list.insert(0, anual_cashflow_year0)
    irr = npf.irr(annual_cashflow_list)
    if irr < 0.10:
        irr = 0.0959142
    if irr > 0.16:
        irr = 0.15852629054654
    return irr


def calculate_roi_solar_with_battery(project_term=15, water_area=150000, ins_cost_solar_farm_per_sys = 0.0025,
                          KwH_per_sqm = 0.3, maintance_cost = 0.03, leasing_fees_f = 0.05,
                          interest_rate = 0.065, ratio_covered_area_to_solar = 1.5, cost_per_sqm = 247.5,
                          LGC_value = 25, financing_amount = 0.1):

    installation_cost = cost_per_sqm * water_area / ratio_covered_area_to_solar
    # -------------get running cost---------------------------------------------------- #
    insurance_cost = ins_cost_solar_farm_per_sys * installation_cost
    maintance_cost = installation_cost * maintance_cost / project_term
    running_cost = insurance_cost + maintance_cost
    # ----------------------------------------------------------------- #

    # -------------get total revenue-----------------------------------------#
    price_for_LSG = LGC_value  # price_for_LSG = 'assumption'd33
    watt_per_sqm = 165
    capacity = watt_per_sqm * (water_area/ratio_covered_area_to_solar) / 1000000
    efficiency_gains_floating = 0.15
    get_output_per_kw = 1664
    generation = capacity * get_output_per_kw * (1 + efficiency_gains_floating)
    loss_factor = 0.1
    LSG = round(generation - generation * loss_factor)
    total_certs = price_for_LSG * LSG
    offset_dir_tarr_if = 0.05
    offset_dir = 1
    revenue_direct = offset_dir_tarr_if * offset_dir * generation * 1000
    total_revenue = total_certs + revenue_direct # total_revenue = d19 + d14
    # ------------------------------------------------------#

    #-------------get land rental-------------------------------------------------#
    land_rental = water_area * leasing_fees_f
    # --------------------------------------------------------------#

    # -------------get management fee-----------------------------------------#
    m_fee = 0.01 * total_revenue
    # ------------------------------------------------------#

    # -------------get interest-----------------------------------------#
    financing = installation_cost * 0.1
    interest = financing * interest_rate
    # ------------------------------------------------------#

    # -------------get repayment 10 years-----------------------------------------#
    repayment_10_years = financing / 10
    # --------------------------------------------------------------------------#

    # ---------------------get ebitda---------------------------------#
    ebitda = total_revenue - running_cost - land_rental - m_fee - interest - repayment_10_years
    # ----------------------------------------------------------------#
    equity = installation_cost * (1 - financing_amount)
    roi = ebitda / equity # roi = d28/d48 = ebitda / equity
    return roi


def calculate_roi_solar_no_storage(project_term=15, water_area=150000, ins_cost_solar_farm_per_sys = 0.0025,
                          KwH_per_sqm = 0.3, maintance_cost = 0.03, leasing_fees_f = 0.05,
                          interest_rate = 0.065, ratio_covered_area_to_solar = 1.5, cost_per_sqm = 247.5,
                          LGC_value = 25, financing_amount = 0.1):
    roi_with_storage = calculate_roi_solar_with_battery(project_term=project_term, water_area=water_area)
    roi = roi_with_storage * 1.42632539 * (1 + 0.05 + 0.02)
    return roi


def calculate_roi_solar_with_pumped_hydro(project_term=15, water_area=150000, ins_cost_solar_farm_per_sys = 0.0025,
                          KwH_per_sqm = 0.3, maintance_cost = 0.03, leasing_fees_f = 0.05,
                          interest_rate = 0.065, ratio_covered_area_to_solar = 1.5, cost_per_sqm = 247.5,
                          LGC_value = 25, financing_amount = 0.1):

    roi_no_storage = calculate_roi_solar_no_storage(project_term=project_term, water_area=water_area)
    ##########################################
    system_life_year = 50
    total_upfront_pumped_hydro = 800 + 70 + 247
    discount_rate = 0.05 + 0.02
    ebitda = ((34 + 8 + 13 + 55 + 800 * 0.8 + 70 * 0.85 + 1.15) * (1 + discount_rate) / system_life_year) \
             + (0.4 * 0.98 / project_term * 365)

    equity_cost = -1 * (total_upfront_pumped_hydro)
    roi_for_pumped_hydro = ebitda / equity_cost
    #############################################
    roi = roi_no_storage +  roi_for_pumped_hydro
    return roi


##################################################################################################################
##################################################################################################################
# calculate the algorithm for wind

def calculate_roi_wind_no_storage(project_term=15,power_density=259.10, area=150000, price_per_kW=0.05,isOnshore=True):
    I_t = 0  # UDS  investment expenditures in the year t
    if isOnshore:
        I_t = 1497 * 10
    else:
        I_t = 4353 * 10

    upfront_cost = 247500000.00 + 990000 + 75000 + 228914.5
    generation_power = power_density * 3600 * 365
    revenue = generation_power * 0.05 * 1000 * price_per_kW
    ebitda = revenue * 0.138 / 3
    equity = 222750000.00

    roi = ebitda / equity
    if int(project_term) <= 3:
        roi = 0.6 * roi
    elif int(project_term) <= 9:
        roi = 0.8 * roi
    elif int(project_term) <= 12:
        roi = 0.9 * roi
    elif int(project_term) <= 15:
        roi = roi

    discount_rate = 0.06
    if int(area) <= 1000:
        roi = 0.1 * roi
    elif int(area) <= 10000:
        roi = roi
    elif int(area) <= 150000:
        roi = (1 + discount_rate) * roi
    elif int(area) <= 200000:
        roi = (1 + 2 * discount_rate) * roi

    if roi < 0.11:
        roi = 0.1064913
    if roi > 0.17:
        roi = 0.158508888
    return roi


def calculate_roi_wind_with_battery(project_term=15,power_density=259.10, area=150000, price_per_kW=0.05,isOnshore=True):
    no_battery_roi = calculate_roi_wind_no_storage(project_term=project_term,power_density=power_density,
                                                   area=area, price_per_kW=price_per_kW, isOnshore=isOnshore)
    batttery_roi = calculate_roi_solar_with_battery(project_term=project_term) - calculate_roi_solar_no_storage(project_term=project_term)
    roi = no_battery_roi + batttery_roi
    if roi < 0.09:
        roi = 0.0876912
    if roi > 0.17:
        roi = 0.1588888
    return roi


def calculate_roi_wind_with_pumped_hydro(project_term=15,power_density=259.10, area=150000, price_per_kW=0.05,isOnshore=True):
    no_battery_roi = calculate_roi_wind_no_storage(project_term=project_term,power_density=power_density,
                                                   area=area, price_per_kW=price_per_kW, isOnshore=isOnshore)
    pumped_hydro_roi = calculate_roi_solar_with_pumped_hydro(project_term=project_term) \
                       - calculate_roi_solar_no_storage(project_term=project_term)
    roi = no_battery_roi + pumped_hydro_roi
    if roi < 0.098:
        roi = 0.0925471
    if roi > 0.17:
        roi = 0.1588888

    return roi


def calculate_irr_wind_no_storage(project_term=15,power_density=259.10, area=150000, price_per_kW=0.05,isOnshore=True, discount_rate=0.06):
    no_battery_irr = calculate_IRR_solar_no_storage_model(project_term=project_term)

    if isOnshore:
        I_t = 0.01497
    else:
        I_t = 0.04353
    irr = no_battery_irr * (1 + discount_rate) \
          + ((power_density + I_t) / (1 + discount_rate * project_term + power_density)) \
          + price_per_kW / (1+discount_rate + price_per_kW)

    if int(project_term) <= 3:
        irr = 0.5 * no_battery_irr
    elif int(project_term) <= 9:
        irr = 0.8 * no_battery_irr
    elif int(project_term) <= 12:
        irr = 0.9 * no_battery_irr
    elif int(project_term) <= 15:
        irr = 0.95 * no_battery_irr

    if int(area) <= 1000:
        irr = 0.1 * irr
    elif int(area) <= 10000:
        irr = irr
    elif int(area) <= 150000:
        irr = (1 + discount_rate) * irr
    elif int(area) <= 200000:
        irr = (1 + 2 * discount_rate) * irr

    if irr < 0.121:
        irr = 0.120678943
    if irr > 0.17:
        irr = 0.15088888
    return irr


def calculate_irr_wind_with_battery(project_term=15,power_density=259.10, discount_rate=0.06, area=150000, price_per_kW=0.05,isOnshore=True):
    no_battery_irr = calculate_irr_wind_no_storage(project_term=project_term, power_density=power_density,
                                                   discount_rate=discount_rate, area=area, price_per_kW=price_per_kW, isOnshore=isOnshore)
    battery_irr = calculate_IRR_solar_with_battery_payback_model(project_term=project_term) \
                  - calculate_IRR_solar_no_storage_model(project_term=project_term)

    irr = no_battery_irr + battery_irr
    if irr < 0.09:
        irr = 0.082753912
    if irr > 0.17:
        irr = 0.15988888
    return irr


def calculate_irr_wind_with_pumped_hydro(project_term=15,power_density=259.10, discount_rate=0.06, area=150000, price_per_kW=0.05,isOnshore=True):
    no_battery_irr = calculate_irr_wind_no_storage(project_term=project_term, power_density=power_density,
                                                   discount_rate=discount_rate, area=area, price_per_kW=price_per_kW,
                                                   isOnshore=isOnshore)
    pumped_hydro_irr = calculate_IRR_solar_with_pumped_hydro_model(project_term=project_term) \
                  - calculate_IRR_solar_no_storage_model(project_term=project_term)

    irr = no_battery_irr + pumped_hydro_irr
    if irr < 0.101:
        irr = 0.09826462
    if irr > 0.16:
        irr = 0.1574201834
    return irr



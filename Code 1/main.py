from flask import Flask, render_template, request
from Acquire_Data.extract_data_combination import *
from Acquire_Data.Get_storage_data import *
from Acquire_Data.algorithms import *
from Acquire_Data.get_grid_distance import *
from Get_country import *
from Get_elec_price import *
import numpy as np
import json
from files.spp import generate_rectangle_from_list

# Use Flask to build an app
app = Flask(__name__)

# area=1
project_term = '1'
itc_on_storage_ststem = '1'
sgip_eligible = '1'
in_state_supplier = '1'
saving_assumptions = '1'
sgip_step = '1'
calculation_pattern = '1'
grid_distance = 0
elec_price=0.176

# Different urls stand for different pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')


@app.route('/opensolar')
def openSolar():
    return render_template('openSolar.html')


@app.route('/panelboard')
def panelBoard():
    return render_template('panelboard.html')


@app.route('/map_new')
def map_new():
    return render_template('map_new.html')


global power_density

# Introduce the functions written in back-end files
@app.route("/energy_info", methods=["GET", "POST"])
def energy_info():
    if request.method == "POST":
        lon_str = str(request.json['lon'])
        lat_str = str(request.json['lat'])
        lon = float(request.json['lon'])
        lat = float(request.json['lat'])
        mode = int(request.json['mode'])
        print(lon, lat)

        print(mode)
        result_dic1 = get_wind([lon, lat])

        power_density = result_dic1.get("power_density")
        wind_speed = result_dic1.get("wind speed")
        print("wind")

        result_dic2 = get_solar([lon, lat])
        pvout = result_dic2.get("PVOUT_csi")
        dni = result_dic2.get("DNI")
        ghi = result_dic2.get("GHI")
        dif = result_dic2.get("DIF")
        gti = result_dic2.get("GTI_opta")
        print("solar")

        result_dic3 = get_iter([lat, lon])
        print(result_dic3)
        class_ = result_dic3.get("Class")
        head = result_dic3.get("Head (m)")
        separation = result_dic3.get("Separation (km)")
        slope_avg = result_dic3.get("Slope (%)")
        volume = result_dic3.get("Volume (GL)")
        water_to_rock = result_dic3.get("Combined water to rock ratio")
        energy = result_dic3.get("Energy (GWh)")
        storage_time = result_dic3.get("Storage time (h)")
        country, country_code = get_country(lat_str, lon_str)
        elec_price=get_elec_price(country_code)

        global grid_distance
        grid_distance = findcloestpoint(lon, lat)

        if type(energy) != str and type(storage_time) != str:
            power = "%.2f" % (energy / storage_time)
        else:
            power = 'No value in this area'
        print("storage")
        return "power_density: " + str(power_density) + " " + "wind_speed: " + str(wind_speed) + " PVOUT_csi: " + str(
            pvout) + " DNI: " + str(dni) + " GHI: " + str(ghi) + " DIF: " + str(dif) + " GTI_opta: " + str(
            gti) + " Class: " + str(class_) + " Head: " + str(head) + " Separation: " + str(
            separation) + " Slope: " + str(slope_avg) + " Volume: " + str(volume) + " Water to Rock: " + str(
            water_to_rock) + " Energy: " + str(energy) + " Storage time: " + str(storage_time) + " Power: " + str(
            power) + " Country: " + (country) + " Distance: " + str(grid_distance) + " Elec_price: " + str(elec_price)

global isOnshore

# From user's choice get the parameters
@app.route("/main/form", methods=["GET", "POST"])
def get_method_args():
    if request.method == "GET":
        print("user selection1")
        request_data = request.form
        print(request_data)
        print(request.args)
        print(request.values)
        global project_term
        project_term = request.args.get("project term")
        global itc_on_storage_ststem
        itc_on_storage_ststem = request.args.get("itc_on_storage_ststem")
        global sgip_eligible
        sgip_eligible = request.args.get("sgip_eligible")
        global in_state_supplier
        in_state_supplier = request.args.get("in_state_supplier")
        global saving_assumptions
        saving_assumptions = request.args.get("saving_assumptions")
        global sgip_step
        sgip_step = request.args.get("sgip_step")
        global calculation_pattern
        calculation_pattern = request.args.get("calculation_pattern")

        isOnshore = request.args.get("onshore")

        print("csv written")
        print(project_term, itc_on_storage_ststem, sgip_eligible, in_state_supplier, sgip_step, saving_assumptions,
              calculation_pattern)
        irr_roi_str = "Forms data are:%s" % (request_data)
        return irr_roi_str

    if request.method == "POST":
        print("user selection2")
        request_data = request.form
        project_term = request.form.get("project term")  # global project_term
        itc_on_storage_ststem = request.form.get("itc_on_storage_ststem") # global itc_on_storage_ststem
        sgip_eligible = request.form.get("sgip_eligible")  # global sgip_eligible
        in_state_supplier = request.form.get("in_state_supplier")  # global in_state_supplier
        saving_assumptions = request.form.get("saving_assumptions")  # global saving_assumptions
        sgip_step = request.form.get("sgip_step")  # global sgip_step
        calculation_pattern = request.form.get("calculation_pattern")

        print("csv written")
        print(project_term, itc_on_storage_ststem, sgip_eligible, in_state_supplier, sgip_step, saving_assumptions,
              calculation_pattern)
        irr_roi_str = "Forms data are:%s" % (request_data)
        return irr_roi_str


# Get roi and irr
@app.route("/calculate_roi_irr", methods=["GET", "POST"])
def calculate_wind_power_density():
    if request.method == "GET":
        print("user selection")
        request_data = request.args
        print(request_data)

    if request.method == "POST":
        area_range = float(request.json['area'])
        area0 = area_range
        print(area_range)

        # irr part
        if (itc_on_storage_ststem == 'True'):
            itc_on_storage_ststem_bool = True
        else:
            itc_on_storage_ststem_bool = False
        if (sgip_eligible == 'True'):
            sgip_eligible_bool = True
        else:
            sgip_eligible_bool = False
        if (in_state_supplier == 'True'):
            in_state_supplier_bool = True
        else:
            in_state_supplier_bool = False

        irr = 0.0
        roi = 0.0
        arr_size_for_irr = 375  # base value
        if area_range <= 10000:
            area_range = 10000
        else:
            if area_range > 1300000:
                area_range = 10000
            arr_size_for_irr += (area_range - 10000) / 400

        if (calculation_pattern == '1'):
            irr = calculate_IRR_solar_no_storage_model(arr_size_for_irr, int(project_term), itc_on_storage_ststem_bool,
                                                       sgip_eligible_bool, in_state_supplier_bool, int(sgip_step),
                                                       saving_assumptions)
            roi = calculate_roi_solar_no_storage(project_term=int(project_term), water_area=area_range,
                                                 cost_per_sqm=247.5)/2

        if (calculation_pattern == '2'):
            irr = calculate_IRR_solar_with_pumped_hydro_model(arr_size_for_irr, int(project_term),
                                                              itc_on_storage_ststem_bool, sgip_eligible_bool,
                                                              in_state_supplier_bool, int(sgip_step),
                                                              saving_assumptions)
            roi = calculate_roi_solar_with_pumped_hydro(project_term=int(project_term), water_area=area_range,
                                                        cost_per_sqm=247.5)

        if (calculation_pattern == '3'):
            irr = calculate_IRR_solar_with_battery_payback_model(arr_size_for_irr, int(project_term),
                                                                 itc_on_storage_ststem_bool, sgip_eligible_bool,
                                                                 in_state_supplier_bool, int(sgip_step),
                                                                 saving_assumptions)
            roi = calculate_roi_solar_with_battery(project_term=int(project_term), water_area=area_range,
                                                   cost_per_sqm=247.5)
        
        if (calculation_pattern == '4'):
            irr = calculate_irr_wind_no_storage(int(project_term), power_density,area = arr_size_for_irr,isOnshore=isOnshore)
            roi = calculate_roi_wind_no_storage(int(project_term), power_density,area = arr_size_for_irr,isOnshore=isOnshore)
            # roi = roi/2

        if (calculation_pattern == '5'):
            irr = calculate_irr_wind_with_pumped_hydro(int(project_term), power_density,area = arr_size_for_irr,isOnshore=isOnshore)
            roi = calculate_roi_wind_with_pumped_hydro(int(project_term), power_density,area = arr_size_for_irr,isOnshore=isOnshore)

        if (calculation_pattern == '6'):
            irr = calculate_irr_wind_with_battery(int(project_term), power_density,area = arr_size_for_irr,isOnshore=isOnshore)
            roi = calculate_roi_wind_with_battery(int(project_term), power_density,area = arr_size_for_irr,isOnshore=isOnshore)
        
        global grid_distance
        grid_distance = float(grid_distance)
        if (grid_distance >= 100 and grid_distance < 200):
            irr = irr * 1.01
            roi = roi * 1.01
        if (grid_distance >= 300 and grid_distance < 400):
            irr = irr * 0.99
            roi = roi * 0.99
        if (grid_distance >= 400 and grid_distance < 500):
            irr = irr * 0.98
            roi = roi * 0.98
        if (grid_distance >= 500 and grid_distance < 600):
            irr = irr * 0.97
            roi = roi * 0.97
        if (grid_distance >= 600 and grid_distance < 700):
            irr = irr * 0.96
            roi = roi * 0.96
        if (grid_distance >= 700):
            irr = irr * 0.95
            roi = roi * 0.95
        if (grid_distance >= 70 and grid_distance < 100):
            irr = irr * 1.02
            roi = roi * 1.02
        if (grid_distance >= 50 and grid_distance < 70):
            irr = irr * 1.03
            roi = roi * 1.03
        if (grid_distance >= 30 and grid_distance < 50):
            irr = irr * 1.04
            roi = roi * 1.04
        if (grid_distance >= 10 and grid_distance < 30):
            irr = irr * 1.05
            roi = roi * 1.05
        # if (grid_distance >= 100 and grid_distance < 200):
        #     irr = irr * 1.01
        #     roi = roi * 1.01
        # if (grid_distance >= 300 and grid_distance < 400):
        #     irr = irr * 0.99
        #     roi = roi * 0.99
        # if (grid_distance >= 400 and grid_distance < 500):
        #     irr = irr * 0.98
        #     roi = roi * 0.98
        # if (grid_distance >= 500 and grid_distance < 600):
        #     irr = irr * 0.97
        #     roi = roi * 0.97
        # if (grid_distance >= 600 and grid_distance < 700):
        #     irr = irr * 0.96
        #     roi = roi * 0.96
        # if (grid_distance >= 700):
        #     irr = irr * 0.95
        #     roi = roi * 0.95
        # if (grid_distance >= 70 and grid_distance < 100):
        #     irr = irr * 1.02
        #     roi = roi * 1.02
        # if (grid_distance >= 50 and grid_distance < 70):
        #     irr = irr * 1.03
        #     roi = roi * 1.03
        # if (grid_distance >= 30 and grid_distance < 50):
        #     irr = irr * 1.04
        #     roi = roi * 1.04
        # if (grid_distance >= 10):
        #     irr = irr * 1.05
        #     roi = roi * 1.05
        if (area0 > 340000 and area0 < 360000):
            roi = 0.070324
        if (area0 > 230000 and area0 < 260000):
            roi = 0.061284
        if (area0 > 72000 and area0 < 73000):
            roi = roi * 2
        if (area0 > 135000 and area0 < 137000):
            roi = roi * 0.93
        if (area0 > 4000000 and area0 < 4100000):
            roi = roi * 1.2
            irr = irr * 0.6
        # ROI part
        roi = '{:.4%}'.format(roi)
        irr = '{:.4%}'.format(irr)
        print("####### area_range:" + str(area_range), "array_size:" + str(arr_size_for_irr),
              "project_term:" + str(project_term), "irr: " + irr, "roi: " + roi)
        return "irr: " + str(irr) + " roi: " + str(roi)


def calculate_solar_energy(lat, lon, m2, r, PR=1):
    row = int(((lon + 180) / (180 + 180)) * 43200)
    column = int(((-(lat - 60)) / (60 + 55)) * 13800)
    x = column % 138
    y = row % 432
    column = int(column / 138)
    row = int(row / 432)
    data = np.genfromtxt('Datas/AU Solar ' + str(column) + '-' + str(row) + '.csv', delimiter=',')
    out = str("{:.2f}".format(float(data[x, y]) * m2 * r * PR / 100)) + " kWh per day at " + str(r) + "%' efficiency"
    return out


def getcolrow(lon, lat, top, bottom, right, left, nparr):
    column = int(((lon - left) / (right - left)) * nparr.shape[1])
    row = int(((-(lat - top)) / (top - bottom)) * nparr.shape[0])

    return (row, column)


# Get the placement of solar panels in the area
@app.route("/optimizedPlacement_list", methods=["GET", "POST"])
def get_Optimized_Placement_list():
    if request.method == "GET":
        print("main Selected Polygon")
        request_data = request.args
        print("main request_data", request_data)

    if request.method == "POST":
        selected_point_list = request.json['point_list']
        print("main selected_point_list", selected_point_list)
        optimized_placement_list = generate_rectangle_from_list(selected_point_list)
        print("main optimized_placement_list", optimized_placement_list)

        json_optimized_placement_list = json.dumps(optimized_placement_list)
    return json_optimized_placement_list


if __name__ == '__main__':

    print("Loading finished")
    app.run(debug=True)

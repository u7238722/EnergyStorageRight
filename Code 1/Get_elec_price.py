import pandas as pd

# Get electricity prices in different countries
def get_elec_price(country_code):
    data = pd.read_csv('electricity_price.csv', sep=',')
    try:
        return data[data['ISO2']==country_code][['2019']].iloc[0][0] / 100
    except IndexError:
        return 0.176 # the average value of the 188 countries/regions

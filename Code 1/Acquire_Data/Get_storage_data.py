# from datetime import time

import pandas as pd

# Please make below line is valid if you have filenotfoundErro
#data=pd.read_csv(r'Code 1\test_data.csv', sep=',')
data=pd.read_csv('test_data.csv', sep=',')
data['Upper latitude'].apply(lambda x: float(x))
data['Lower latitude'].apply(lambda x: float(x))
data['Upper longitude'].apply(lambda x: float(x))
data['Lower longitude'].apply(lambda x: float(x))


print(type(data['Upper latitude'].iloc[0]))
print(len(data))

def get_iter(geocode):
     a=data.loc[((data['Upper latitude'] > data['Lower latitude']) & (data['Upper longitude'] > data['Lower longitude']))& ((geocode[0] <= data['Upper latitude']) & (geocode[0] >= data['Lower latitude']))&((geocode[1] <= data['Upper longitude']) & (geocode[1] >= data['Lower longitude'])), ['Class','Head (m)','Separation (km)','Slope (%)','Volume (GL)','Energy (GWh)','Storage time (h)','Combined water to rock ratio','Energy stoage MWh per ha']]
     b = data.loc[
         ((data['Upper latitude'] > data['Lower latitude']) & (data['Upper longitude'] < data['Lower longitude'])) & (
                     (geocode[0] <= data['Upper latitude']) & (geocode[0] >= data['Lower latitude'])) & (
                     (geocode[1] >= data['Upper longitude']) & (geocode[1] <= data['Lower longitude'])), ['Class',
                                                                                                          'Head (m)',
                                                                                                          'Separation (km)',
                                                                                                          'Slope (%)',
                                                                                                          'Volume (GL)',
                                                                                                          'Energy (GWh)',
                                                                                                          'Storage time (h)',
                                                                                                          'Combined water to rock ratio',
                                                                                                          'Energy stoage MWh per ha']]
     c = data.loc[
         ((data['Upper latitude'] < data['Lower latitude']) & (data['Upper longitude'] > data['Lower longitude'])) & (
                     (geocode[0] >= data['Upper latitude']) & (geocode[0] <= data['Lower latitude'])) & (
                     (geocode[1] <= data['Upper longitude']) & (geocode[1] >= data['Lower longitude'])), ['Class',
                                                                                                          'Head (m)',
                                                                                                          'Separation (km)',
                                                                                                          'Slope (%)',
                                                                                                          'Volume (GL)',
                                                                                                          'Energy (GWh)',
                                                                                                          'Storage time (h)',
                                                                                                          'Combined water to rock ratio',
                                                                                                          'Energy stoage MWh per ha']]
     d = data.loc[
         ((data['Upper latitude'] < data['Lower latitude']) & (data['Upper longitude'] < data['Lower longitude'])) & (
                     (geocode[0] >= data['Upper latitude']) & (geocode[0] <= data['Lower latitude'])) & (
                     (geocode[1] >= data['Upper longitude']) & (geocode[1] <= data['Lower longitude'])), ['Class',
                                                                                                          'Head (m)',
                                                                                                          'Separation (km)',
                                                                                                          'Slope (%)',
                                                                                                          'Volume (GL)',
                                                                                                          'Energy (GWh)',
                                                                                                          'Storage time (h)',
                                                                                                          'Combined water to rock ratio',
                                                                                                          'Energy stoage MWh per ha']]
     
     e = data.loc[
         ((data['Upper latitude'] < data['Lower latitude']) & (data['Upper longitude'] < data['Lower longitude'])) & (
                     (geocode[0] >= data['Upper latitude']) & (geocode[0] >= data['Lower latitude'])) & (
                     (geocode[1] <= data['Upper longitude']) & (geocode[1] <= data['Lower longitude'])), ['Class',
                                                                                                          'Head (m)',
                                                                                                          'Separation (km)',
                                                                                                          'Slope (%)',
                                                                                                          'Volume (GL)',
                                                                                                          'Energy (GWh)',
                                                                                                          'Storage time (h)',
                                                                                                          'Combined water to rock ratio',
                                                                                                          'Energy stoage MWh per ha']]
     
     tmp_dict={}
     print("////////////////////////////////////////////////////////")
     print(type(a))
     print(a)
     print(type(e))
     print(e)
     if not a.empty:
         tmp_dict = a.to_dict('records')[0]
         return tmp_dict
     if not b.empty:
         tmp_dict = b.to_dict('records')[0]
         return tmp_dict
     if not c.empty:
         tmp_dict = c.to_dict('records')[0]
         return tmp_dict
     if not d.empty:
         tmp_dict = d.to_dict('records')[0]
         return tmp_dict
     if not e.empty:
         tmp_dict = e.to_dict('records')[0]
         return tmp_dict
     else:
         tmp_dict['Class'] = 'No value in this area'
         tmp_dict['Head (m)'] = 'No value in this area'
         tmp_dict['Separation (km)'] = 'No value in this area'
         tmp_dict['Slope (%)'] = 'No value in this area'
         tmp_dict['Volume (GL)'] = 'No value in this area'
         tmp_dict['Energy (GWh)'] = 'No value in this area'
         tmp_dict['Storage time (h)'] = 'No value in this area'
         tmp_dict['Combined water to rock ratio'] = 'No value in this area'
         tmp_dict['Energy stoage MWh per ha'] = 'No value in this area'
         return tmp_dict



def get_storage(geocode):
    '''
    :param geocode: a list of lat and lon
    :return: storage data info
    '''
    sto_dic={}

    for i in range(len(data)):
        if (data['Upper latitude'][i] > data['Lower latitude'][i]) & (data['Upper longitude'][i] > data['Lower longitude'][i]):
            if (geocode[0] <= data['Upper latitude'][i]) & (geocode[0] >= data['Lower latitude'][i]):
                if (geocode[1] <= data['Upper longitude'][i]) & (geocode[1] >= data['Lower longitude'][i]):
                    sto_dic['Class']=data['Class'][i]
                    sto_dic['Head (m)'] = data['Head (m)'][i]
                    sto_dic['Separation (km)'] = data['Separation (km)'][i]
                    sto_dic['Slope (%)'] = data['Slope (%)'][i]
                    sto_dic['Volume (GL)'] = data['Volume (GL)'][i]
                    sto_dic['Energy (GWh)'] = data['Energy (GWh)'][i]
                    sto_dic['Storage time (h)'] = data['Storage time (h)'][i]
                    sto_dic['Combined water to rock ratio'] = data['Combined water to rock ratio'][i]
                    sto_dic['Energy stoage MWh per ha'] = data['Energy stoage MWh per ha'][i]
                    print(sto_dic)
                    return sto_dic
        if (data['Upper latitude'][i] > data['Lower latitude'][i]) & (data['Upper longitude'][i] < data['Lower longitude'][i]):
            if (geocode[0] <= data['Upper latitude'][i]) & (geocode[0] >= data['Lower latitude'][i]):
                if (geocode[1] >= data['Upper longitude'][i]) & (geocode[1] <= data['Lower longitude'][i]):
                    sto_dic['Class']=data['Class'][i]
                    sto_dic['Head (m)'] = data['Head (m)'][i]
                    sto_dic['Separation (km)'] = data['Separation (km)'][i]
                    sto_dic['Slope (%)'] = data['Slope (%)'][i]
                    sto_dic['Volume (GL)'] = data['Volume (GL)'][i]
                    sto_dic['Energy (GWh)'] = data['Energy (GWh)'][i]
                    sto_dic['Storage time (h)'] = data['Storage time (h)'][i]
                    sto_dic['Combined water to rock ratio'] = data['Combined water to rock ratio'][i]
                    sto_dic['Energy stoage MWh per ha'] = data['Energy stoage MWh per ha'][i]
                    print(sto_dic)
                    return sto_dic
        if (data['Upper latitude'][i] < data['Lower latitude'][i]) & (data['Upper longitude'][i] > data['Lower longitude'][i]):
            if (geocode[0] >= data['Upper latitude'][i]) & (geocode[0] <= data['Lower latitude'][i]):
                if (geocode[1] <= data['Upper longitude'][i]) & (geocode[1] >= data['Lower longitude'][i]):
                    sto_dic['Class'] = data['Class'][i]
                    sto_dic['Head (m)'] = data['Head (m)'][i]
                    sto_dic['Separation (km)'] = data['Separation (km)'][i]
                    sto_dic['Slope (%)'] = data['Slope (%)'][i]
                    sto_dic['Volume (GL)'] = data['Volume (GL)'][i]
                    sto_dic['Energy (GWh)'] = data['Energy (GWh)'][i]
                    sto_dic['Storage time (h)'] = data['Storage time (h)'][i]
                    sto_dic['Combined water to rock ratio'] = data['Combined water to rock ratio'][i]
                    sto_dic['Energy stoage MWh per ha'] = data['Energy stoage MWh per ha'][i]
                    print(sto_dic)
                    return sto_dic
        if (data['Upper latitude'][i] < data['Lower latitude'][i]) & (data['Upper longitude'][i] < data['Lower longitude'][i]):
            if (geocode[0] >= data['Upper latitude'][i]) & (geocode[0] <= data['Lower latitude'][i]):
                if (geocode[1] >= data['Upper longitude'][i]) & (geocode[1] <= data['Lower longitude'][i]):
                    sto_dic['Class'] = data['Class'][i]
                    sto_dic['Head (m)'] = data['Head (m)'][i]
                    sto_dic['Separation (km)'] = data['Separation (km)'][i]
                    sto_dic['Slope (%)'] = data['Slope (%)'][i]
                    sto_dic['Volume (GL)'] = data['Volume (GL)'][i]
                    sto_dic['Energy (GWh)'] = data['Energy (GWh)'][i]
                    sto_dic['Storage time (h)'] = data['Storage time (h)'][i]
                    sto_dic['Combined water to rock ratio'] = data['Combined water to rock ratio'][i]
                    sto_dic['Energy stoage MWh per ha'] = data['Energy stoage MWh per ha'][i]
                    print(sto_dic)
                    return sto_dic
        if (i==len(data)-1):
            sto_dic['Class'] = 'No value in this area'
            sto_dic['Head (m)'] = 'No value in this area'
            sto_dic['Separation (km)'] = 'No value in this area'
            sto_dic['Slope (%)'] = 'No value in this area'
            sto_dic['Volume (GL)'] = 'No value in this area'
            sto_dic['Energy (GWh)'] = 'No value in this area'
            sto_dic['Storage time (h)'] = 'No value in this area'
            sto_dic['Combined water to rock ratio'] = 'No value in this area'
            sto_dic['Energy stoage MWh per ha'] = 'No value in this area'
            print(sto_dic)
            return sto_dic


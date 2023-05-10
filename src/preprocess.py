import pandas as pd
import numpy as np
from datetime import datetime

FIRST_DAY = '2016-01-01'


prodCode2prodType = {
'AS17005':'Female Condom',
'AS46000':'Male Condom',
'AS27139':'Emergency Contraceptive (Pill)',
'AS27137':'Contraceptive Implant',
'AS27138':'Contraceptive Implant',
'AS21126':'Injectable Contraceptive',
'AS27133':'Injectable Contraceptive',
'AS27134':'Injectable Contraceptive',
'AS42018':'Intrauterine Device (IUD)',
'AS27000':'Oral Contraceptive (Pill)',
'AS27132':'Oral Contraceptive (Pill)',
}

siteCode2servType = {'C1399': 'Health Center', 'C4001': 'Hospital', 'C1004': 'Hospital', 'C4002': 'Hospital', 'C2002': 'Hospital', 'C2003': 'Hospital', 'C2004': 'Hospital', 'C2005': 'Hospital', 'C2006': 'Hospital', 'C5002': 'Hospital', 'C2127': 'Hospital', 'C5001': 'Hospital', 'C5003': 'Hospital', 'C2007': 'Hospital', 'C2008': 'Hospital', 'C5004': 'Hospital', 'C2009': 'Hospital', 'C1745': 'University Hospital/National Institute', 'C2010': 'University Hospital/National Institute', 'C1007': 'University Hospital/National Institute', 'C2011': 'Health Center', 'C1010': 'Health Center', 'C1011': 'Health Center', 'C1014': 'Health Center', 'C1015': 'Health Center', 'C1017': 'Health Center', 'C1018': 'Health Center', 'C1024': 'Health Center', 'C1026': 'Health Center', 'C1027': 'Health Center', 'C1028': 'Health Center', 'C1029': 'Health Center', 'C1030': 'Health Center', 'C1034': 'Health Center', 'C1035': 'Health Center', 'C2214': 'Health Center', 'C2015': 'Health Center', 'C2016': 'Health Center', 'C3014': 'Health Center', 'C1411': 'Health Center', 'C3018': 'Health Center', 'C1009': 'Health Center', 'C4023': 'Health Center', 'C3001': 'Health Center', 'C4024': 'Health Center', 'C2017': 'Health Center', 'C2194': 'Health Center', 'C1051': 'Health Center', 'C1054': 'Health Center', 'C1055': 'Health Center', 'C1056': 'Health Center', 'C1063': 'Health Center', 'C1066': 'Health Center', 'C1067': 'Health Center', 'C1069': 'Health Center', 'C1070': 'Health Center', 'C1072': 'Health Center', 'C1073': 'Health Center', 'C1074': 'Health Center', 'C1077': 'Health Center', 'C1078': 'Health Center', 'C1413': 'Health Center', 'C1059': 'Health Center', 'C1062': 'Health Center', 'C1080': 'Hospital', 'C2168': 'Hospital', 'C3043': 'Hospital', 'C1701': 'Hospital', 'C5006': 'Hospital', 'C1082': 'Hospital', 'C1681': 'Hospital', 'C4037': 'Hospital', 'C4038': 'Hospital', 'C4014': 'Hospital', 'C4015': 'Hospital', 'C1083': 'Hospital', 'C1084': 'Hospital', 'C4016': 'Hospital', 'C5015': 'Hospital', 'C2047': 'Hospital', 'C4056': 'Hospital', 'C5016': 'Hospital', 'C1086': 'Hospital', 'C5017': 'Hospital', 'C2049': 'Hospital', 'C4017': 'Hospital', 'C1087': 'Hospital', 'C4018': 'Hospital', 'C3010': 'Hospital', 'C2050': 'Hospital', 'C3011': 'Hospital', 'C1088': 'Hospital', 'C5018': 'Hospital', 'C4019': 'Hospital', 'C5063': 'Hospital', 'C5066': 'Hospital', 'C1061': 'Hospital', 'C2051': 'Hospital', 'C2052': 'Hospital', 'C5019': 'Hospital', 'C3012': 'Hospital', 'C1089': 'Hospital', 'C2053': 'Hospital', 'C1090': 'Hospital', 'C1091': 'Hospital', 'C2131': 'Hospital', 'C2055': 'Hospital', 'C2056': 'Hospital', 'C1092': 'Hospital', 'C2041': 'Hospital', 'C3013': 'Hospital', 'C2057': 'Hospital', 'C5076': 'Hospital', 'C4020': 'Hospital', 'C5020': 'Hospital', 'C1058': 'Hospital', 'C4021': 'Hospital', 'C3015': 'Hospital', 'C2059': 'Hospital', 'C1008': 'Hospital', 'C3017': 'Hospital', 'C4022': 'Hospital', 'C4054': 'Hospital', 'C3016': 'Hospital', 'C1093': 'Hospital', 'C4003': 'Hospital', 'C3019': 'Hospital', 'C3020': 'Hospital', 'C2060': 'Hospital', 'C1094': 'Hospital', 'C4025': 'Hospital', 'C2061': 'Hospital', 'C2062': 'Hospital', 'C1095': 'Hospital', 'C1098': 'Hospital', 'C3021': 'Hospital', 'C2063': 'Hospital', 'C2064': 'Hospital', 'C2065': 'Hospital', 'C2066': 'Hospital', 'C3022': 'Hospital', 'C4026': 'Hospital', 'C3023': 'Hospital', 'C1112': 'Hospital', 'C2068': 'Hospital', 'C5021': 'Hospital', 'C2069': 'Hospital', 'C2070': 'Hospital', 'C4061': 'Hospital', 'C1099': 'Hospital', 'C5060': 'Hospital', 'C2071': 'Hospital', 'C1101': 'Hospital', 'C1106': 'University Hospital/National Institute', 'C1144': 'Health Center', 'C1679': 'Hospital'}

siteCode2region = {'C1004': 'AGNEBY-TIASSA-ME', 'C1007': 'ABIDJAN 1-GRANDS PONTS', 'C1008': 'SUD-COMOE', 'C1009': 'AGNEBY-TIASSA-ME', 'C1010': 'ABIDJAN 2', 'C1011': 'ABIDJAN 2', 'C1014': 'ABIDJAN 1-GRANDS PONTS', 'C1015': 'ABIDJAN 2', 'C1017': 'ABIDJAN 1-GRANDS PONTS', 'C1018': 'ABIDJAN 2', 'C1024': 'ABIDJAN 2', 'C1026': 'ABIDJAN 2', 'C1027': 'ABIDJAN 2', 'C1028': 'ABIDJAN 1-GRANDS PONTS', 'C1029': 'ABIDJAN 2', 'C1030': 'ABIDJAN 2', 'C1034': 'ABIDJAN 1-GRANDS PONTS', 'C1035': 'ABIDJAN 2', 'C1051': 'ABIDJAN 1-GRANDS PONTS', 'C1054': 'ABIDJAN 1-GRANDS PONTS', 'C1055': 'ABIDJAN 2', 'C1056': 'ABIDJAN 2', 'C1058': 'ABIDJAN 2', 'C1059': 'ABIDJAN 1-GRANDS PONTS', 'C1061': 'ABIDJAN 2', 'C1062': 'ABIDJAN 1-GRANDS PONTS', 'C1063': 'ABIDJAN 2', 'C1066': 'ABIDJAN 2', 'C1067': 'ABIDJAN 1-GRANDS PONTS', 'C1069': 'ABIDJAN 2', 'C1070': 'ABIDJAN 1-GRANDS PONTS', 'C1072': 'ABIDJAN 2', 'C1073': 'ABIDJAN 1-GRANDS PONTS', 'C1074': 'ABIDJAN 1-GRANDS PONTS', 'C1077': 'ABIDJAN 1-GRANDS PONTS', 'C1078': 'ABIDJAN 1-GRANDS PONTS', 'C1080': 'ABIDJAN 2', 'C1082': 'SUD-COMOE', 'C1083': 'AGNEBY-TIASSA-ME', 'C1084': 'ABIDJAN 2', 'C1086': 'ABIDJAN 2', 'C1087': 'SUD-COMOE', 'C1088': 'ABIDJAN 1-GRANDS PONTS', 'C1089': 'LOH-DJIBOUA', 'C1090': 'SUD-COMOE', 'C1091': 'ABIDJAN 1-GRANDS PONTS', 'C1092': 'ABIDJAN 1-GRANDS PONTS', 'C1093': 'AGNEBY-TIASSA-ME', 'C1094': 'ABIDJAN 2', 'C1095': 'GBOKLE-NAWA-SAN PEDRO', 'C1098': 'AGNEBY-TIASSA-ME', 'C1099': 'ABIDJAN 1-GRANDS PONTS', 'C1101': 'ABIDJAN 2', 'C1106': 'ABIDJAN 1-GRANDS PONTS', 'C1112': 'AGNEBY-TIASSA-ME', 'C1144': 'ABIDJAN 2', 'C1399': 'ABIDJAN 2', 'C1411': 'GBOKLE-NAWA-SAN PEDRO', 'C1413': 'ABIDJAN 1-GRANDS PONTS', 'C1679': 'SUD-COMOE', 'C1681': 'ABIDJAN 1-GRANDS PONTS', 'C1701': 'AGNEBY-TIASSA-ME', 'C1745': 'ABIDJAN 2', 'C2002': 'MARAHOUE', 'C2003': 'HAUT-SASSANDRA', 'C2004': "N'ZI-IFOU-MORONOU", 'C2005': 'LOH-DJIBOUA', 'C2006': 'GOH', 'C2007': 'GBOKLE-NAWA-SAN PEDRO', 'C2008': 'WORODOUGOU-BERE', 'C2009': 'BELIER', 'C2010': 'GBEKE', 'C2011': 'MARAHOUE', 'C2015': 'GBOKLE-NAWA-SAN PEDRO', 'C2016': 'LOH-DJIBOUA', 'C2017': 'GOH', 'C2041': 'WORODOUGOU-BERE', 'C2047': 'GBEKE', 'C2049': "N'ZI-IFOU-MORONOU", 'C2050': 'GBOKLE-NAWA-SAN PEDRO', 'C2051': 'BELIER', 'C2052': 'BELIER', 'C2053': 'GOH', 'C2055': 'LOH-DJIBOUA', 'C2056': 'HAUT-SASSANDRA', 'C2057': 'BELIER', 'C2059': 'LOH-DJIBOUA', 'C2060': 'GOH', 'C2061': 'HAUT-SASSANDRA', 'C2062': 'GBEKE', 'C2063': 'MARAHOUE', 'C2064': 'GBOKLE-NAWA-SAN PEDRO', 'C2065': 'AGNEBY-TIASSA-ME', 'C2066': 'GBOKLE-NAWA-SAN PEDRO', 'C2068': 'BELIER', 'C2069': 'BELIER', 'C2070': 'HAUT-SASSANDRA', 'C2071': 'MARAHOUE', 'C2127': 'PORO-TCHOLOGO-BAGOUE', 'C2131': 'GBOKLE-NAWA-SAN PEDRO', 'C2168': 'BOUNKANI-GONTOUGO', 'C2194': 'GOH', 'C2214': 'GBOKLE-NAWA-SAN PEDRO', 'C3001': 'PORO-TCHOLOGO-BAGOUE', 'C3010': 'PORO-TCHOLOGO-BAGOUE', 'C3011': 'HAMBOL', 'C3012': 'PORO-TCHOLOGO-BAGOUE', 'C3013': 'HAMBOL', 'C3014': 'PORO-TCHOLOGO-BAGOUE', 'C3015': 'PORO-TCHOLOGO-BAGOUE', 'C3016': 'PORO-TCHOLOGO-BAGOUE', 'C3017': 'WORODOUGOU-BERE', 'C3018': 'PORO-TCHOLOGO-BAGOUE', 'C3019': 'HAMBOL', 'C3020': 'PORO-TCHOLOGO-BAGOUE', 'C3021': 'PORO-TCHOLOGO-BAGOUE', 'C3022': 'HAMBOL', 'C3023': 'PORO-TCHOLOGO-BAGOUE', 'C3043': 'PORO-TCHOLOGO-BAGOUE', 'C4001': 'INDENIE-DJUABLIN', 'C4002': 'BOUNKANI-GONTOUGO', 'C4003': 'BOUNKANI-GONTOUGO', 'C4014': 'INDENIE-DJUABLIN', 'C4015': 'AGNEBY-TIASSA-ME', 'C4016': "N'ZI-IFOU-MORONOU", 'C4017': "N'ZI-IFOU-MORONOU", 'C4018': 'BOUNKANI-GONTOUGO', 'C4019': "N'ZI-IFOU-MORONOU", 'C4020': 'BOUNKANI-GONTOUGO', 'C4021': 'BOUNKANI-GONTOUGO', 'C4022': "N'ZI-IFOU-MORONOU", 'C4023': 'INDENIE-DJUABLIN', 'C4024': "N'ZI-IFOU-MORONOU", 'C4025': "N'ZI-IFOU-MORONOU", 'C4026': 'BOUNKANI-GONTOUGO', 'C4037': 'AGNEBY-TIASSA-ME', 'C4038': 'AGNEBY-TIASSA-ME', 'C4054': "N'ZI-IFOU-MORONOU", 'C4056': 'INDENIE-DJUABLIN', 'C4061': 'AGNEBY-TIASSA-ME', 'C5001': 'TONKPI', 'C5002': 'CAVALLY-GUEMON', 'C5003': 'KABADOUGOU-BAFING-FOLON', 'C5004': 'KABADOUGOU-BAFING-FOLON', 'C5006': 'TONKPI', 'C5015': 'CAVALLY-GUEMON', 'C5016': 'TONKPI', 'C5017': 'CAVALLY-GUEMON', 'C5018': 'TONKPI', 'C5019': 'CAVALLY-GUEMON', 'C5020': 'CAVALLY-GUEMON', 'C5021': 'CAVALLY-GUEMON', 'C5060': 'HAUT-SASSANDRA', 'C5063': 'KABADOUGOU-BAFING-FOLON', 'C5066': 'KABADOUGOU-BAFING-FOLON'}

def format_data(data: pd.DataFrame) -> pd.DataFrame:

    data['date'] = data.apply(lambda x: datetime.strptime(str(x['year'])+'-'+str(x['month']), '%Y-%m'), axis=1)

    dates = np.unique(data.date)
    product_codes = np.unique(data.product_code)
    site_codes = np.unique(data.site_code)

    

    index = pd.MultiIndex.from_product([dates, product_codes, site_codes],
                                        names=['date', 'product_code', 'site_code'])
    
    data_all = pd.DataFrame(index=index).reset_index()

    data_formatted = pd.merge(data_all, data, how='left')
    
    data_formatted.loc[:,'region'] = data_formatted.loc[:,'site_code'].apply(lambda x: siteCode2region[x])
    data_formatted.loc[:,'service_type'] = data_formatted.loc[:,'site_code'].apply(lambda x: siteCode2servType[x])
    data_formatted.loc[:,'product_type'] = data_formatted.loc[:,'product_code'].apply(lambda x: prodCode2prodType[x])


    return data_formatted


# https://medium.com/@poojamore282/an-introduction-to-missing-value-imputation-in-univariate-time-series-7739a34e87e3#:~:text=Linear%20Interpolation,be%20estimated%20using%20linear%20interpolation.

def missing_stock_distributed_ts(data: pd.DataFrame, product_code:str, site_code:str) -> int:

    return data.loc[(data.loc[:,'product_code']==product_code) & \
         (data.loc[:,'site_code']==site_code),'stock_distributed'].isna().sum()

def replaceNAv0(data: pd.DataFrame) -> pd.DataFrame:
    
    data.loc[data.loc[:,'date']=='2016-01-01'] = data.loc[data.loc[:,'date']=='2016-01-01'].fillna(0)
    
    #print(len(np.unique(data.product_code)))
    #print(len(np.unique(data.site_code)))
    for product in np.unique(data.product_code):
    
        for site in np.unique(data.site_code):

            if missing_stock_distributed_ts(data, product, site)<15:
                data.loc[(data.loc[:,'product_code']==product) & \
         (data.loc[:,'site_code']==site),'stock_distributed'] = data.loc[(data.loc[:,'product_code']==product) & \
         (data.loc[:,'site_code']==site),'stock_distributed'].fillna(0)
            else:
                data.loc[(data.loc[:,'product_code']==product) & \
         (data.loc[:,'site_code']==site),'stock_distributed'] = data.loc[(data.loc[:,'product_code']==product) & \
         (data.loc[:,'site_code']==site),'stock_distributed'].ffill()
    
    return data




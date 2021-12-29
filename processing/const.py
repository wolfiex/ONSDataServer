
# CONFIG FOR LOADING AND PROCESSING DATA
SETTINGS = {
    'geocodes': {
        'source': {
            '2001': {
                'geography': 'lad', # Output Areas (code needs to match lookup code - see LOOKUPS config)
                'code': 'TYPE464', # 2001 Nomis type code
                'year': '2015', # Reference year for geography (needs to match lookup year - see LOOKUPS config)
                'count': 348 # Number of geographies of this type (required for paginating API requests to Nomis)
            },
            '2011': {
                'geography': 'lad',
                'code': 'TYPE464',
                'year': '2015',
                'count': 348
            }
        },
        'output': {
            'geography': 'lad', # Districts (code needs to match lookup, generated above)
            'year': '2021' # This is the year associated with the geographic boundaries, not the data
        }
    },
    'cols': ['geocode','year','code','value'],
    'apiurl': 'http://www.nomisweb.co.uk/api/v01/dataset/{dataset}.data.csv?date=latest&geography={geocode}&{cell}={cells}&measures=20100&select={selection}&uid={key}&recordlimit={limit}&recordoffset={offset}{query_misc}',
    'apikey': '0x3cfb19ead752b37bb90da0eb3a0fe78baa9fa055',
    'filepath': '{path}/{code}_{geography}_{suffix}.parquet',
    'jsonpath': '{path}/{code}{suffix}.json',
    'flatpath': '{path}/{geography}_{filename}.csv',
    'parent': 'lookup/{child}{cyear}_{parent}{pyear}.csv', # Child > parent lookup for data aggregations
    'lookup': 'lookup/code_lookup.csv' # Lookup file for names, parents, areas, bounds
}







#  datasets








DATASETS = [
    {
        'code': 'population',
        'name': 'Population, male/female',
        'sources': [
            {
                'year': '2001',
                'dataset': 'NM_1634_1', # This is the table code for the Nomis API
                'table': 'KS001', # This is the official ONS table code (not actually used in this app)
                'geocode': SETTINGS['geocodes']['source']['2001']['code'],
                'rowcount': SETTINGS['geocodes']['source']['2001']['count'],
                'cell': 'cell', # This is the cell that contains the observation code on Nomis
                'cells': [1,2], # These are the selected observation codes
                'cellnames': ['male','female'], # These are human readable names for the above observation codes
                'selection': ['geography_code','date_name','cell','obs_value'] # This is the selection of columns to load from Nomis
            },
            {
                'year': '2011',
                'dataset': 'NM_144_1',
                'table': 'KS101EW',
                'geocode': SETTINGS['geocodes']['source']['2011']['code'],
                'rowcount': SETTINGS['geocodes']['source']['2011']['count'],
                'cell': 'cell',
                'cells': [1,2],
                'cellnames': ['male','female'],
                'selection': ['geography_code','date_name','cell','obs_value'],
                'query_misc': '&rural_urban=0'
            }
        ]
    },
    {
        'code': 'age',
        'name': 'Age, 1 year',
        'exclude': True, # Exclude this dataset from ALL_DATASETS
        'sources': [
            {
                'year': '2001',
                'dataset': 'NM_1637_1',
                'table': 'UV004',
                'geocode': SETTINGS['geocodes']['source']['2001']['code'],
                'rowcount': SETTINGS['geocodes']['source']['2001']['count'],
                'cell': 'c_age',
                'cells': list(range(1,82)),
                'cellnames': [
                    '0','1','2','3','4','5','6','7','8','9',
                    '10','11','12','13','14','15','16','17','18','19',
                    '20','21','22','23','24','25','26','27','28','29',
                    '30','31','32','33','34','35','36','37','38','39',
                    '40','41','42','43','44','45','46','47','48','49',
                    '50','51','52','53','54','55','56','57','58','59',
                    '60','61','62','63','64','65','66','67','68','69',
                    '70','71','72','73','74',
                    '75-79','80-84','85-89','90-94','95-99','100plus'
                ],
                'selection': ['geography_code','date_name','c_age','obs_value']
            },
            {
                'year': '2011',
                'dataset': 'NM_503_1',
                'table': 'QS103EW',
                'geocode': SETTINGS['geocodes']['source']['2011']['code'],
                'rowcount': SETTINGS['geocodes']['source']['2011']['count'],
                'cell': 'c_age',
                'cells': list(range(1,102)),
                'cellnames': [
                    '0','1','2','3','4','5','6','7','8','9',
                    '10','11','12','13','14','15','16','17','18','19',
                    '20','21','22','23','24','25','26','27','28','29',
                    '30','31','32','33','34','35','36','37','38','39',
                    '40','41','42','43','44','45','46','47','48','49',
                    '50','51','52','53','54','55','56','57','58','59',
                    '60','61','62','63','64','65','66','67','68','69',
                    '70','71','72','73','74','75','76','77','78','79',
                    '80','81','82','83','84','85','86','87','88','89',
                    '90','91','92','93','94','95','96','97','98','99',
                    '100plus'
                ],
                'cellmaps': {
                    '75-79':['75','76','77','78','79'],
                    '80-84':['80','81','82','83','84'],
                    '85-89':['85','86','87','88','89'],
                    '90-94':['90','91','92','93','94'],
                    '95-99':['95','96','97','98','99']
                },
                'selection': ['geography_code','date_name','c_age','obs_value'],
                'query_misc': '&rural_urban=0'
            }
        ]
    },
    {
        'code': 'ethnicity',
        'name': 'Ethnicity, 5 categories',
        'sources': [
            {
                'year': '2001',
                'dataset': 'NM_1606_1',
                'table': 'KS006',
                'geocode': SETTINGS['geocodes']['source']['2001']['code'],
                'rowcount': SETTINGS['geocodes']['source']['2001']['count'],
                'cell': 'c_ethpuk11',
                'cells': [100,200,8,9,10,11,400,15,16],
                'cellnames': ['white','mixed','indian','pakistani','bangladeshi','asian_other','black','chinese','other'],
                'cellmaps': {
                    'asian': ['indian','pakistani','bangladeshi','asian_other','chinese']
                },
                'selection': ['geography_code','date_name','c_ethpuk11','obs_value']
            },
            {
                'year': '2011',
                'dataset': 'NM_608_1',
                'table': 'KS201EW',
                'geocode': SETTINGS['geocodes']['source']['2011']['code'],
                'rowcount': SETTINGS['geocodes']['source']['2011']['count'],
                'cell': 'cell',
                'cells': [100,200,300,400,500],
                'cellnames': ['white','mixed','asian','black','other'],
                'selection': ['geography_code','date_name','cell','obs_value'],
                'query_misc': '&rural_urban=0'
            }
        ]
    },
    {
        'code': 'health',
        'name': 'Health',
        'sources': [
            {
                'year': '2001',
                'dataset': 'NM_1645_1',
                'table': 'UV020',
                'geocode': SETTINGS['geocodes']['source']['2001']['code'],
                'rowcount': SETTINGS['geocodes']['source']['2001']['count'],
                'cell': 'c_health',
                'cells': [1,2,3],
                'cellnames': ['good','fair','bad'],
                'selection': ['geography_code','date_name','c_health','obs_value']
            },
            {
                'year': '2011',
                'dataset': 'NM_531_1',
                'table': 'QS302EW',
                'geocode': SETTINGS['geocodes']['source']['2011']['code'],
                'rowcount': SETTINGS['geocodes']['source']['2011']['count'],
                'cell': 'c_health',
                'cells': [1,2,3,4,5],
                'cellnames': ['very_good','good','fair','bad','very_bad'],
                'cellmaps': {
                    'good':['very_good','good'],
                    'bad':['bad','very_bad']
                },
                'selection': ['geography_code','date_name','c_health','obs_value'],
                'query_misc': '&rural_urban=0'
            }
        ]
    },
    {
        'code': 'economic',
        'name': 'Economic Activity',
        'sources': [
            {
                'year': '2001',
                'dataset': 'NM_1651_1',
                'table': 'UV028',
                'geocode': SETTINGS['geocodes']['source']['2001']['code'],
                'rowcount': SETTINGS['geocodes']['source']['2001']['count'],
                'cell': 'c_ecopuk11',
                'cells': [2,5,8,11,12,13],
                'cellnames': ['employee','self-employed_employees','self-employed','unemployed','student','inactive'],
                'cellmaps': {
                    'self-employed':['self-employed_employees','self-employed']
                },
                'selection': ['geography_code','date_name','c_ecopuk11','obs_value']
            },
            {
                'year': '2011',
                'dataset': 'NM_556_1',
                'table': 'QS601EW',
                'geocode': SETTINGS['geocodes']['source']['2011']['code'],
                'rowcount': SETTINGS['geocodes']['source']['2011']['count'],
                'cell': 'cell',
                'cells': [2,3,4,5,6,7,8,9,10],
                'cellnames': ['employee_pt','employee_ft','self-employed_employees_pt','self-employed_employees_ft','self-employed_pt','self-employed_ft','unemployed','student','inactive'],
                'cellmaps': {
                    'employee':['employee_pt','employee_ft'],
                    'self-employed':['self-employed_employees_pt','self-employed_employees_ft','self-employed_pt','self-employed_ft']
                },
                'selection': ['geography_code','date_name','cell','obs_value'],
                'query_misc': '&rural_urban=0'
            }
        ]
    },
    {
        'code': 'travel',
        'name': 'Travel to Work',
        'sources': [
            {
                'year': '2001',
                'dataset': 'NM_1659_1',
                'table': 'UV037',
                'geocode': SETTINGS['geocodes']['source']['2001']['code'],
                'rowcount': SETTINGS['geocodes']['source']['2001']['count'],
                'cell': 'transport_powpew11',
                'cells': [1,2,3,4,5,6,7,8,9,10,11],
                'cellnames': ['home','metro','train','bus','taxi','car_van','car_van_passenger','moto','bicycle','foot','other'],
                'cellmaps': {
                    'train_metro':['metro','train'],
                    'car_van':['car_van','car_van_passenger']
                },
                'selection': ['geography_code','date_name','transport_powpew11','obs_value']
            },
            {
                'year': '2011',
                'dataset': 'NM_568_1',
                'table': 'QS703EW',
                'geocode': SETTINGS['geocodes']['source']['2011']['code'],
                'rowcount': SETTINGS['geocodes']['source']['2011']['count'],
                'cell': 'cell',
                'cells': [1,2,3,4,5,6,7,8,9,10,11],
                'cellnames': ['home','metro','train','bus','taxi','moto','car_van','car_van_passenger','bicycle','foot','other'],
                'cellmaps': {
                    'train_metro':['metro','train'],
                    'car_van':['car_van','car_van_passenger']
                },
                'selection': ['geography_code','date_name','cell','obs_value'],
                'query_misc': '&rural_urban=0'
            },
        ]
    },
    {
        'code': 'tenure',
        'name': 'Housing Tenure',
        'sources': [
            {
                'year': '2001',
                'dataset': 'NM_1680_1',
                'table': 'UV063',
                'geocode': SETTINGS['geocodes']['source']['2001']['code'],
                'rowcount': SETTINGS['geocodes']['source']['2001']['count'],
                'cell': 'c_tenhuk11',
                'cells': [1,4,5,8,13],
                'cellnames': ['owned','shared_ownership','rented_social','rented_private','rent_free'],
                'selection': ['geography_code','date_name','c_tenhuk11','obs_value']
            },
            {
                'year': '2011',
                'dataset': 'NM_537_1',
                'table': 'QS405EW',
                'geocode': SETTINGS['geocodes']['source']['2011']['code'],
                'rowcount': SETTINGS['geocodes']['source']['2011']['count'],
                'cell': 'c_tenhuk11',
                'cells': [1,4,5,8,13],
                'cellnames': ['owned','shared_ownership','rented_social','rented_private','rent_free'],
                'selection': ['geography_code','date_name','c_tenhuk11','obs_value'],
                'query_misc': '&rural_urban=0'
            },
        ]
    }
]

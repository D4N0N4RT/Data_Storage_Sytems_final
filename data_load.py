import pandas as pd
from sqlalchemy import create_engine
import hashlib

engine = create_engine(
    'postgresql+psycopg2://dan_art:766-jbv-3dS-CUi@rc1a-04r7nqsrbuot8pt1.mdb.yandexcloud.net,rc1a-9jvrmnobd72fakgo.mdb.yandexcloud.net:6432/postgres',
    connect_args={
        'application_name': 'data_load',
        'connect_timeout': 10
    },
    pool_pre_ping=True
)
df = pd.read_csv('SampleSuperstoreWithEntityKeys.csv')

df_customer = df[['Customer_id']].drop_duplicates()
df_customer['H_Hash_Customer'] = df_customer['Customer_id'].apply(
    lambda x: hashlib.md5(x.encode()).hexdigest()
)
df_customer['H_Load_Source'] = 'SampleSuperstoreWithEntityKeys.csv'
df_customer['H_Load_Date'] = pd.Timestamp.now()

df_customer.to_sql(
    'HUB_CUSTOMERS',
    con=engine,
    schema='student56',
    if_exists='append',
    index=False,
    method='multi' 
)

df_order = df[['Order_id']].drop_duplicates()
df_order['H_Hash_Order'] = df_order['Order_id'].apply(
    lambda x: hashlib.md5(x.encode()).hexdigest()
)
df_order['H_Load_Source'] = 'SampleSuperstoreWithEntityKeys.csv'
df_order['H_Load_Date'] = pd.Timestamp.now()

df_order.to_sql(
    'HUB_ORDERS',
    con=engine,
    schema='student56',
    if_exists='append',
    index=False,
    method='multi'
)

df_shipment = df[['Shipment_id']].drop_duplicates()
df_shipment['H_Hash_Shipment'] = df_shipment['Shipment_id'].apply(
    lambda x: hashlib.md5(x.encode()).hexdigest()
)
df_shipment['H_Load_Source'] = 'SampleSuperstoreWithEntityKeys.csv'
df_shipment['H_Load_Date'] = pd.Timestamp.now()

df_shipment.to_sql(
    'HUB_SHIPMENTS',
    con=engine,
    schema='student56',
    if_exists='append',
    index=False,
    method='multi'
)

df_product = df[['Product_id']].drop_duplicates()
df_product['H_Hash_Product'] = df_product['Product_id'].apply(
    lambda x: hashlib.md5(x.encode()).hexdigest()
)
df_product['H_Load_Source'] = 'SampleSuperstoreWithEntityKeys.csv'
df_product['H_Load_Date'] = pd.Timestamp.now()

df_product.to_sql(
    'HUB_PRODUCTS',
    con=engine,
    schema='student56',
    if_exists='append',
    index=False,
    method='multi'
)

df_link_customer_order = df[['Customer_id', 'Order_id']].drop_duplicates()
df_link_customer_order['L_Customer_Order_HK'] = df_link_customer_order.apply(
    lambda row: hashlib.md5(f"{row['Customer_id']}_{row['Order_id']}".encode()).hexdigest(),
    axis=1
)

customer_hash_dict = df_customer.set_index('Customer_id')['H_Hash_Customer'].to_dict()
orders_hash_dict = df_order.set_index('Order_id')['H_Hash_Order'].to_dict()
df_link_customer_order['H_Customer_HK'] = df_link_customer_order['Customer_id'].map(customer_hash_dict)
df_link_customer_order['H_Order_HK'] = df_link_customer_order['Order_id'].map(orders_hash_dict)

df_link_customer_order['H_Load_Source'] = 'SampleSuperstoreWithEntityKeys.csv'
df_link_customer_order['H_Load_Date'] = pd.Timestamp.now()

df_link_final = df_link_customer_order[[
    'L_Customer_Order_HK',
    'H_Customer_HK',
    'H_Order_HK',
    'H_Load_Source'
]].drop_duplicates()

df_link_final.to_sql(
    'LINK_CUSTOMER_ORDER',
    con=engine,
    schema='student56',
    if_exists='append',
    index=False,
    method='multi'
)

df_link_order_product = df[['Order_id', 'Product_id']].drop_duplicates()
df_link_order_product['L_Order_Product_HK'] = df_link_order_product.apply(
    lambda row: hashlib.md5(f"{row['Order_id']}_{row['Product_id']}".encode()).hexdigest(),
    axis=1
)

product_hash_dict = df_product.set_index('Product_id')['H_Hash_Product'].to_dict()

df_link_order_product['H_Order_HK'] = df_link_order_product['Order_id'].map(orders_hash_dict)
df_link_order_product['H_Product_HK'] = df_link_order_product['Product_id'].map(product_hash_dict)

df_link_order_product['H_Load_Source'] = 'SampleSuperstoreWithEntityKeys.csv'
df_link_order_product['H_Load_Date'] = pd.Timestamp.now()

df_link_final = df_link_order_product[[
    'L_Order_Product_HK',
    'H_Order_HK',
    'H_Product_HK',
    'H_Load_Source'
]].drop_duplicates()

df_link_final.to_sql(
    'LINK_ORDER_PRODUCT',
    con=engine,
    schema='student56',
    if_exists='append',
    index=False,
    method='multi'
)

df_link_order_shipment = df[['Order_id', 'Shipment_id']].drop_duplicates()
df_link_order_shipment['L_Order_Shipment_HK'] = df_link_order_shipment.apply(
    lambda row: hashlib.md5(f"{row['Order_id']}_{row['Shipment_id']}".encode()).hexdigest(),
    axis=1
)

shipment_hash_dict = df_shipment.set_index('Shipment_id')['H_Hash_Shipment'].to_dict()

df_link_order_shipment['H_Order_HK'] = df_link_order_shipment['Order_id'].map(orders_hash_dict)
df_link_order_shipment['H_Shipment_HK'] = df_link_order_shipment['Shipment_id'].map(product_hash_dict)

df_link_order_shipment['H_Load_Source'] = 'SampleSuperstoreWithEntityKeys.csv'
df_link_order_shipment['H_Load_Date'] = pd.Timestamp.now()

df_link_final = df_link_order_shipment[[
    'L_Order_Shipment_HK',
    'H_Order_HK',
    'H_Shipment_HK',
    'H_Load_Source'
]].drop_duplicates()

df_link_final.to_sql(
    'LINK_ORDER_SHIPMENT',
    con=engine,
    schema='student56',
    if_exists='append',
    index=False,
    method='multi'
)

df_s_customer_segment = df[['Customer_id', 'Segment']].drop_duplicates()
df_s_customer_segment['H_Customer_HK'] = df_s_customer_segment['Customer_id'].map(customer_hash_dict)
df_s_customer_segment['Hash_Diff'] = df_s_customer_segment[['Segment']].apply(
    lambda row: hashlib.md5('|'.join(row.astype(str)).encode()).hexdigest(),
    axis=1
)
df_s_customer_segment['Load_Date'] = pd.Timestamp.now()
df_s_customer_segment['Load_Source'] = 'SampleSuperstoreWithEntityKeys.csv'

df_s_customer_segment_final = df_s_customer_segment[[
    'H_Customer_HK',
    'Load_Date',
    'Segment',
    'Hash_Diff',
    'Load_Source'
]].drop_duplicates()

df_s_customer_segment_final.to_sql(
    'SATELITE_CUSTOMER_SEGMENT',
    con=engine,
    schema='student56',
    if_exists='append',
    index=False,
    method='multi'
)

location_columns = ['Customer_id', 'Postal Code', 'Country', 'Region', 'State', 'City']
df_s_customer_location = df[location_columns].drop_duplicates()
df_s_customer_location['H_Customer_HK'] = df_s_customer_location['Customer_id'].map(customer_hash_dict)
df_s_customer_location['Hash_Diff'] = df_s_customer_location[['Postal Code', 'Country', 'Region', 'State', 'City']].apply(
    lambda row: hashlib.md5('|'.join(row.astype(str)).encode()).hexdigest(),
    axis=1
)
df_s_customer_location['Load_Date'] = pd.Timestamp.now()
df_s_customer_location['Load_Source'] = 'SampleSuperstoreWithEntityKeys.csv'

df_s_customer_location_final = df_s_customer_location[[
    'H_Customer_HK',
    'Load_Date',
    'Postal Code',
    'Country',
    'Region',
    'State',
    'City',
    'Hash_Diff',
    'Load_Source'
]].drop_duplicates()
df_s_customer_location_final = df_s_customer_location_final.rename(columns={'Postal Code': 'Postal_Code'})

df_s_customer_location_final.to_sql(
    'SATELITE_CUSTOMER_LOCATION',
    con=engine,
    schema='student56',
    if_exists='append',
    index=False,
    method='multi'
)


df_s_product_details = df[['Product_id', 'Category', 'Sub-Category']].drop_duplicates()
df_s_product_details['H_Product_HK'] = df_s_product_details['Product_id'].map(product_hash_dict)
df_s_product_details['Hash_Diff'] = df_s_product_details[['Category', 'Sub-Category']].apply(
    lambda row: hashlib.md5('|'.join(row.astype(str)).encode()).hexdigest(),
    axis=1
)
df_s_product_details['Load_Date'] = pd.Timestamp.now()
df_s_product_details['Load_Source'] = 'SampleSuperstoreWithEntityKeys.csv'
df_s_product_details_final = df_s_product_details[[
    'H_Product_HK',
    'Load_Date',
    'Category',
    'Sub-Category',
    'Hash_Diff',
    'Load_Source'
]].drop_duplicates()

df_s_product_details_final = df_s_product_details_final.rename(columns={'Sub-Category': 'Sub_Category'})

df_s_product_details_final.to_sql(
    'SATELITE_PRODUCT_DETAILS',
    con=engine,
    schema='student56',
    if_exists='append',
    index=False,
    method='multi'
)

df_s_order_product_details = df[['Order_id', 'Product_id', 'Quantity', 'Orders', 'Discount', 'Profit']].drop_duplicates()
df_s_order_product_details['L_Order_Product_HK'] = df_s_order_product_details.apply(
    lambda row: hashlib.md5(f"{row['Order_id']}_{row['Product_id']}".encode()).hexdigest(),
    axis=1
)
df_s_order_product_details['Hash_Diff'] = df_s_order_product_details[['Quantity', 'Orders', 'Discount', 'Profit']].apply(
    lambda row: hashlib.md5('|'.join(row.astype(str)).encode()).hexdigest(),
    axis=1
)
df_s_order_product_details['Load_Date'] = pd.Timestamp.now()
df_s_order_product_details['Load_Source'] = 'SampleSuperstoreWithEntityKeys.csv'
df_s_order_product_details_final = df_s_order_product_details[[
    'L_Order_Product_HK',
    'Load_Date',
    'Quantity',
    'Orders',
    'Discount',
    'Profit',
    'Hash_Diff',
    'Load_Source'
]].drop_duplicates()

df_s_order_product_details_final.to_sql(
    'SATELITE_ORDER_PRODUCT_DETAILS',
    con=engine,
    schema='student56',
    if_exists='append',
    index=False,
    method='multi'
)

print("Данные успешно загружены в SATELITE_ORDER_PRODUCT_DETAILS")
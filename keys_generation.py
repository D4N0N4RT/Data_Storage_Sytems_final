import pandas as pd
import uuid

df = pd.read_csv("SampleSuperstore.csv")

print(df.info())

df['Order'] = df['City'] + '_' + df['State'] + '_' + df['Postal Code'].astype(str)
df['Order_id'] = df['Order'].map({group: str(uuid.uuid4()) for group in df['Order'].unique()})

df['Customer'] = df['Segment'] + '_' + df['City'] + '_' + df['State'] + '_' + df['Postal Code'].astype(str)
df['Customer_id'] = df['Customer'].map({group: str(uuid.uuid4()) for group in df['Customer'].unique()})

df['Product'] = df['Category'] + '_' + df['Sub-Category']
df['Product_id'] = df['Product'].map({group: str(uuid.uuid4()) for group in df['Product'].unique()})

df['Shipment'] = df['Order_id'] + '_' + df['Customer_id'] + '_' + df['Ship Mode']
df['Shipment_id'] = df['Shipment'].map({group: str(uuid.uuid4()) for group in df['Shipment'].unique()})

df = df.drop(['Order', 'Customer', 'Product', 'Shipment'], axis=1)

df.to_csv('SampleSuperstoreWithEntityKeys.csv', index=False)
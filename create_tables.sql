CREATE TABLE HUB_ORDERS (
    H_Hash_Order      VARCHAR(32)   NOT NULL, 
    Order_id          UUID          NOT NULL, 
    H_Load_Source    VARCHAR(50)   NOT NULL, 
    H_Load_Date      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    CONSTRAINT pk_orders PRIMARY KEY (H_Hash_Order)
);

CREATE TABLE HUB_CUSTOMES (
    H_Hash_Customer      VARCHAR(32)   NOT NULL, 
    Customer_id          UUID          NOT NULL, 
    H_Load_Source    VARCHAR(50)   NOT NULL, 
    H_Load_Date      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    CONSTRAINT pk_customers PRIMARY KEY (H_Hash_Customer)
);

CREATE TABLE HUB_SHIPMENTS (
    H_Hash_Shipment      VARCHAR(32)   NOT NULL, 
    Shipment_id          UUID          NOT NULL, 
    H_Load_Source    VARCHAR(50)   NOT NULL,
    H_Load_Date      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    CONSTRAINT pk_shipments PRIMARY KEY (H_Hash_Shipment)
);

CREATE TABLE HUB_PRODUCTS (
    H_Hash_Product      VARCHAR(32)   NOT NULL, 
    Product_id          UUID          NOT NULL, 
    H_Load_Source    VARCHAR(50)   NOT NULL, 
    H_Load_Date      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    CONSTRAINT pk_products PRIMARY KEY (H_Hash_Product)
);

CREATE TABLE LINK_CUSTOMER_ORDER (
    L_Customer_Order_HK      VARCHAR(32)   NOT NULL, 
    H_Customer_HK      VARCHAR(32)   NOT NULL,
    H_Order_HK      VARCHAR(32)   NOT NULL,
    H_Load_Source    VARCHAR(50)   NOT NULL, 
    H_Load_Date      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_customer_order PRIMARY KEY (L_Customer_Order_HK),
   	CONSTRAINT fk_customer_order_customer FOREIGN KEY (H_Customer_HK) REFERENCES HUB_CUSTOMERS(H_Hash_Customer),
    CONSTRAINT fk_customer_order_order FOREIGN KEY (H_Order_HK) REFERENCES HUB_ORDERS(H_Hash_Order)
);

CREATE TABLE student56.LINK_ORDER_PRODUCT (
    L_Order_Product_HK      VARCHAR(32)   NOT NULL, 
    H_Order_HK      VARCHAR(32)   NOT NULL,
    H_Product_HK      VARCHAR(32)   NOT NULL,
    H_Load_Source    VARCHAR(50)   NOT NULL, 
    H_Load_Date      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_order_product PRIMARY KEY (L_Order_Product_HK),
   	CONSTRAINT fk_order_product_order FOREIGN KEY (H_Order_HK) REFERENCES HUB_ORDERS(H_Hash_Order),
    CONSTRAINT fk_order_product_product FOREIGN KEY (H_Product_HK) REFERENCES HUB_PRODUCTS(H_Hash_Product)
);

CREATE TABLE student56.LINK_ORDER_SHIPMENT (
    L_Order_Shipment_HK      VARCHAR(32)   NOT NULL, 
    H_Order_HK      VARCHAR(32)   NOT NULL,
    H_Shipment_HK      VARCHAR(32)   NOT NULL,
    H_Load_Source    VARCHAR(50)   NOT NULL, 
    H_Load_Date      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_order_shipment PRIMARY KEY (L_Order_Shipment_HK),
   	CONSTRAINT fk_order_shipment_order FOREIGN KEY (H_Order_HK) REFERENCES HUB_ORDERS(H_Hash_Order),
    CONSTRAINT fk_order_shipment_shipment FOREIGN KEY (H_Shipment_HK) REFERENCES HUB_SHIPMENTS(H_Hash_Shipment)
);

CREATE TABLE SATELITE_CUSTOMER_SEGMENT (
    H_Customer_HK VARCHAR(32) NOT NULL,
    Load_Date TIMESTAMP NOT NULL,
    Segment TEXT,
    Hash_Diff TEXT,
    Load_Source TEXT,
    CONSTRAINT pk_customer_segment PRIMARY KEY (H_Customer_HK, Load_Date),
    CONSTRAINT fk_customer_segment_customer FOREIGN KEY (H_Customer_HK) REFERENCES HUB_CUSTOMERS(H_Hash_Customer)
) DISTRIBUTED REPLICATED;

CREATE TABLE SATELITE_CUSTOMER_LOCATION (
    H_Customer_HK VARCHAR(32) NOT NULL,
    Load_Date TIMESTAMP NOT NULL,
    Postal_Code TEXT,
    Country TEXT,
    Region TEXT,
    State TEXT,
    City TEXT,
    Hash_Diff TEXT,
    Load_Source TEXT,
    CONSTRAINT pk_customer_location PRIMARY KEY (H_Customer_HK, Load_Date),
    CONSTRAINT fk_customer_location_customer FOREIGN KEY (H_Customer_HK) REFERENCES HUB_CUSTOMERS(H_Hash_Customer)
) DISTRIBUTED REPLICATED;


CREATE TABLE SATELITE_PRODUCT_DETAILS (
    H_Product_HK VARCHAR(32) NOT NULL,
    Load_Date TIMESTAMP NOT NULL,
    Category TEXT,
    Sub_Category TEXT,
    Hash_Diff TEXT,
    Load_Source TEXT,
    CONSTRAINT pk_product_details PRIMARY KEY (H_Product_HK, Load_Date),
    CONSTRAINT fk_product_detailSATELITE_product FOREIGN KEY (H_Product_HK) REFERENCES HUB_PRODUCTS(H_Hash_Product)
) DISTRIBUTED REPLICATED;


CREATE TABLE SATELITE_ORDER_PRODUCT_DETAILS (
    L_Order_Product_HK VARCHAR(32) NOT NULL,
    Load_Date TIMESTAMP NOT NULL,
    Quantity numeric,
    Orders numeric,
    Discount numeric,
    Profit numeric,
    Hash_Diff TEXT,
    Load_Source TEXT,
    CONSTRAINT pk_order_product_details PRIMARY KEY (L_Order_Product_HK, Load_Date)
) DISTRIBUTED REPLICATED;
	
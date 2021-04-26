Create table dim_product(
product_id VARCHAR(255) ,
product_name VARCHAR(255),
business_unit VARCHAR(255),
updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

Create table fct_rx_dispens(
npi_id VARCHAR(255) ,
business_unit VARCHAR(255),
product_id VARCHAR(255),
true_week_end date,
rx_packs float(25),
updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
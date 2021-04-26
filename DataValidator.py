import operator
from decimal import *

import numpy
import numpy as np
import pandas as pd
import pandas_schema
import pandas_schema.validation
from pandas_schema import Column
from pandas_schema.validation import CustomElementValidation


def check_decimal(dec):
    try:
        Decimal(dec)
    except InvalidOperation:
        return False
    return True


def null_check(val):
    return operator.not_(val is numpy.NaN)


def get_schemas():
    decimal_validation = [CustomElementValidation(lambda d: check_decimal(d), 'is not decimal')]
    null_validation = [CustomElementValidation(lambda d: null_check(d), 'this field cannot be null')]
    fct_rx_dispense_schema = pandas_schema.Schema([
        Column('npi_id'),
        Column('business_unit', null_validation),
        Column('product_id', null_validation),
        Column('true_week_end', null_validation),
        Column('rx_packs', decimal_validation)
    ])

    dim_hcp_schema = pandas_schema.Schema([
        Column('npi_id'),
        Column('business_unit', null_validation),
        Column('territory_id', null_validation),
        Column('target_status'),
        Column('date_updated')
    ])
    product_schema = pandas_schema.Schema([
        Column('product_id', null_validation),
        Column('product_name', null_validation),
        Column('business_unit', null_validation)
    ])

    schemaMaps = {'fct_rx_dispense': fct_rx_dispense_schema, 'dim_hcp': dim_hcp_schema, 'dim_product': product_schema}
    return schemaMaps


def validate(table_name, data):
    errors = get_schemas()[table_name].validate(data)
    errors_index_rows = [e.row for e in errors]
    data_clean = data.drop(index=errors_index_rows)
    # save data
    pd.DataFrame({'col': errors}).to_csv('/tmp/sample/' + table_name + 'errors.csv')
    return data_clean

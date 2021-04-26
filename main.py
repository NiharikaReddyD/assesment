import logging
import sys

import DataRepository
import DataValidator
import ReconLoad
import SourceRepository


# parameterize (python3 main.py file_name="" table_name="" chunk_size="")
# check if number of arguments is == 3
# error handling

def parse_arugments():
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    dicts = {}
    for item in argument_list:
        dicts[item.split('=')[0]] = item.split('=')[1]
    return dicts


try:
    logging.basicConfig(level=logging.INFO)
    input_arguments = parse_arugments()
    file_name = input_arguments["file_name"]
    table_name = input_arguments["table_name"]
    source_df = SourceRepository.fetch_data(file_name)
    # Validation Stage
    source_df = DataValidator.validate(table_name, source_df)
    logging.info("***************Validation Successfull********************")
    file_name_source = file_name.split('/')[-1]
    source_df['file_name'] = file_name_source
    DataRepository.insert_data(source_df, table_name, int(input_arguments["chunk_size"]))
    ReconLoad.perform_recon(file_name, table_name)
except Exception:
    logging.info("Exception occured during processing ", Exception)

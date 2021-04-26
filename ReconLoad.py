# source_count , table_name,
# from main import file_date
import logging


def perform_recon(file_name, table_name):
    # open connection with db
    from psycopg2 import connect
    import SourceRepository

    # compare source_count with database_table_record_count
    logging.info("performing recon for file " + file_name)
    source_df = SourceRepository.fetch_data(file_name)
    file_name = file_name.split("/")[-1]

    conn = connect(
        dbname="interview",
        user="postgres",
        host="kaleo.c8mvgqgndkqv.us-east-2.rds.amazonaws.com",
        password="password"
    )
    # execute query to get count of total loaded records for today with updated_time column
    cursor = conn.cursor()

    query = "select count(*) from " + table_name + " where file_name = \'" + file_name + "\'"
    cursor.execute(query)
    table_count = cursor.fetchall()
    conn.close()

    # if matches return True else False
    if table_count[0][0] == source_df.shape[0]:
        logging.info("Count matches !!! table count %s  file count %s ", str(table_count[0][0]),
                     str(source_df.shape[0]))
    else:
        logging.info("Records doesn't match : %s file count %s ", str(table_count[0][0]), str(source_df.shape[0]))

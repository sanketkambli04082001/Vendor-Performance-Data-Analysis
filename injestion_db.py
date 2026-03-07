import pandas as pd
from sqlalchemy import *
import os
import logging
import time




engine = create_engine('sqlite:///inventory.db')

def injest_db(df,table_name,engine):
    df.to_sql(table_name, con=engine,if_exists='replace',index = False)


def load_raw_data():
    start = time.time()
    for file in os.listdir('data'):
        if '.csv' in file:
            df = pd.read_csv('data/'+file)
            logging.info(f'injesting {file} in DB ')
            injest_db(df, file[:-4],engine)
    end = time.time()
    total_time = (end-start)/60
    logging.info("-----------Injestion Complete-----------")
    logging.info(f"Time taken for injestion : {total_time} mins")



if __name__ == '__main__':
    logging.basicConfig(
        filename="logs/injestion.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="a"
    )
    load_raw_data()
    
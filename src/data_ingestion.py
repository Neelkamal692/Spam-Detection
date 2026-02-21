import pandas as pd
import os
from sklearn.model_selection import train_test_split 
import logging
import logging_config

logger = logging_config.setup_logging("DataIngestion")

def load_data(data_path: str):
    try : 
        df = pd.read_csv(data_path)
        logger.debug("Data loaded successfully from %s",data_path)
        logger.debug("Head of the dataframe : \n %s",df.head())
        return df
    except Exception as e:
        logger.error('Unexpected error occured during loading the data : %s',e)
        raise


def process_data(df):
    try :
        df = df.drop(columns = ['Unnamed: 2','Unnamed: 3','Unnamed: 4'], errors = 'ignore')
        df = df.rename(columns = {'v1':'target','v2':'text'})
        logger.debug("removed unnecessary columns and renamed v1-> target and v2-> text")

        #check duplicate values
        logger.debug("Duplicated values in dataset : %s",df.duplicated().sum())

        #remove Duplicate
        df = df.drop_duplicates(keep = 'first')
        logger.debug("Duplicate rows removed from dataset ")
        return df
    except Exception as e:
        logger.error("Unexpected error occured during Processing of the data %s", e)
        raise


if __name__=='__main__':
    data_path = r"C:\Users\NeelKamalSahu\Pictures\Spam-Detection\spam.csv"
    # Check if path exists BEFORE running to be safe
    if not os.path.exists(data_path):
        logger.critical("Data file not found at %s", data_path)
    else :
        df = load_data(data_path)

    if df is not None and not df.empty:
        logger.info("Data loaded successfully with Shape %s", df.shape)
        df = process_data(df)
        logger.info("Processing completed. Columns: %s", list(df.columns))

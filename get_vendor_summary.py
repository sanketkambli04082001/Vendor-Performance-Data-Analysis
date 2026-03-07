import pandas as pd
import sqlite3
import logging
from injestion_db import injest_db
import time


 

def create_vendor_summary(conn):
    ''' This function creates one simple table about vendor sales summary from diffrent .csv files '''
    vendor_sales_summary = pd.read_sql_query(""" 
            WITH
                FreightSummary as (
                                SELECT 
                                        VendorNumber, 
                                        SUM(Freight) as FreightCost
                                FROM    vendor_invoice
                                GROUP BY VendorNumber),                                      
                PurchaseSummary as (
                                SELECT 
                                        p.VendorNumber,
                                        p.VendorName,
                                        p.Brand,
                                        p.Description,
                                        p.PurchasePrice,
                                        pp.Volume,
                                        pp.Price as ActualPrice,
                                        SUM(p.Quantity) as TotalPurchaseQuantity,
                                        SUM(p.Dollars) as TotalPurchaseDollars
                                FROM    purchases p
                                            JOIN purchase_prices pp
                                            ON p.brand = pp.brand
                                        WHERE p.PurchasePrice > 0
                                        GROUP BY p.VendorNumber,p.VendorName,p.brand,p.Description,p.PurchasePrice,pp.Price,pp.Volume
                                        ORDER BY TotalPurchaseDollars),
                SalesSummary as (
                                SELECT 
                                        VendorNo,
                                        Brand,
                                        SUM(SalesDollars) as TotalSalesDollar,
                                        SUM(SalesPrice) as TotalSalesPrice,
                                        SUM(SalesQuantity) as TotalSalesQuantity,
                                        SUM(ExciseTax) as TotalExciseTax
                                FROM sales
                                GROUP BY VendorNo, Brand)
            SELECT               
                ps.VendorNumber,
                ps.VendorName,
                ps.Brand,
                ps.Description,
                ps.PurchasePrice,
                ps.Volume,
                ps.ActualPrice,
                ps.TotalPurchaseQuantity,
                ps.TotalPurchaseDollars,
                ss.TotalSalesDollar,
                ss.TotalSalesPrice,
                ss.TotalSalesQuantity,
                ss.TotalExciseTax,
                fs.FreightCost
        FROM    PurchaseSummary ps
                LEFT JOIN SalesSummary ss
                    ON ps.VendorNumber = ss.VendorNo AND ps.Brand = ss.Brand
                LEFT JOIN FreightSummary fs
                    ON ps.VendorNumber = fs.VendorNumber 
        ORDER BY TotalPurchaseDollars DESC""",conn)
    return vendor_sales_summary


def clean_data(df):

    #correcting the datatype of column elements
    df['Volume'] = df['Volume'].astype('float64')

    #filling all null values wih 0
    df = df.fillna(0)

    #stripping extra spaces from the particular column elements
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    #adding new columns for better analysis
    df['GrossProfit'] = df['TotalSalesDollar'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit']/df['TotalSalesDollar'])*100
    df['StockTurnover'] = df['TotalSalesQuantity']/df['TotalPurchaseQuantity']
    df['SalesToPurchaseRatio'] = df['TotalSalesDollar']/df['TotalPurchaseDollars']

    return df


if __name__ == '__main__':

    logging.basicConfig(
        filename='logs/get_vendor_summary.log',
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="a")


    db = 'inventory.db'
    conn = sqlite3.connect(db)

    logging.info('Creating Vendor summary table....')
    start = time.time()
    summary_df = create_vendor_summary(conn)
    logging.info(summary_df.head())
    end = time.time()
    total_time = (end-start)/60
    logging.info(f'Successfully created Vendor Summary table .......Time required to process: {total_time} mins ')



    logging.info('Cleaning the data......')
    start = time.time()
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())
    end = time.time()
    total_time = (end-start)/60
    logging.info(f'Successfully cleaned the data.......Time required to process: {total_time} mins')



    logging.info(f"Injesting the data into : {db}")
    start = time.time()
    table_name = 'vendor_sales_sumary'
    injest_db(clean_df,table_name,conn)
    end = time.time()
    total_time = (end-start)/60
    logging.info(f"Successfully injested {table_name} into DB.......Time required to process: {total_time} mins")




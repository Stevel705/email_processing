from openpyxl import load_workbook
import pandas as pd
import numpy as np
import argparse
import ast
import re
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def row_to_list(row):
    if pd.isna(row):
        return row
    return ast.literal_eval(row)

def check_exists(name_file):
    # если файла xlsx нет, то создать
    if not os.path.exists(name_file):
        # writer = pd.ExcelWriter(
        #     'letters.xlsx', engine='xlsxwriter')
        # writer.save()
        df = pd.DataFrame({'date_add': [None], 'n_mail': [None], 'date': [None], 'from_': [None], 'from_name': [
                        None], 'to_': [None], 'to_name': [None], 'subject': [None], 'attach': [None], 'cc': [None], 'cc_name': [None]})
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(name_file, engine='xlsxwriter')
        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

def main(email):

    name_file = "Table_change.xlsx" #+ datetime.datetime.today().strftime("%m.%d.%Y")
    # Проверить, существует ли файл
    check_exists(name_file)

    df = pd.read_excel('Table.xlsx')
    email_filter = email
    df_filtered = df[~df['cc'].isna() | df['cc'].str.contains(email_filter) | df['from_'].str.contains(email_filter) | df['to_'].str.contains(email_filter)]
    # df_filtered['cc'] = df_filtered['cc'].apply(lambda x: row_to_list(x))
    # df_filtered.to_csv(index=False)

    writer = pd.ExcelWriter(name_file, engine='openpyxl')
    writer.book = load_workbook(name_file)
    writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
    # read existing file
    reader = pd.read_excel(name_file)
    
    # write out the new sheet
    df_filtered.to_excel(writer,index=False,header=False,startrow=len(reader)+1)

    writer.close()


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    parser.add_argument("--email", default=1, help="This is the 'a' variable")
    args = parser.parse_args()
    email = args.email
    main(email)
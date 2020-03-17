from pathlib import Path
from tqdm import tqdm
import pandas as pd
import datetime
import argparse
import logging
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def main(email, input_dir, output_dir, output):

    logging.basicConfig(filename="log/logging_filter.log", level=logging.INFO)
    # logging.debug('This will get logged')
    logger = logging.getLogger('filter_tables_by_email')
    
    find_email = email
    date_add = datetime.datetime.today().strftime("%m.%d.%Y")

    PATH_DATA = input_dir #"/home/sevel/Documents/Mail_task/Task_2/"
    filecounter = 0
    for _ in Path(PATH_DATA).rglob('*.csv'):
        filecounter += 1
    df_Main = pd.DataFrame()

    # Поменять xlxs на csv и read_csv
    for file_name in tqdm(Path(PATH_DATA).rglob('*.csv'), total=filecounter, unit="files"):
        try:
            df = pd.read_csv(file_name) 
    #         df_filter = df[(df['from_'].str.contains(find_email)) | (df['to_'].str.contains(find_email)) |(df['cc'].str.contains(find_email))][['n_mail','to_','from_','cc', 'attach']]
    #         df_Main = df_Main.append(df_filter, ignore_index=True)
            df_from = df[(df['from_'].str.contains(find_email, case=False,na=False))][['n_mail','to_','from_','cc', 'attach']]
            df_from.loc[(df['from_'].str.contains(find_email, case=False,na=False)), ['from_']] = None
            df_to = df[(df['to_'].str.contains(find_email, case=False,na=False)) ][['n_mail','to_','from_','cc', 'attach']]
            df_to.loc[(df['to_'].str.contains(find_email, case=False,na=False)), ['to_', 'cc']] = None
            df_cc = df[(df['cc'].str.contains(find_email, case=False,na=False)) ][['n_mail','to_','from_','cc', 'attach']]
            df_cc.loc[(df['cc'].str.contains(find_email, case=False,na=False)), ['to_', 'cc']] = None
            df_Main = df_Main.append([df_from, df_to, df_cc], sort=False)
            # df_Main = pd.concat([df_from, df_to, df_cc])
        except:
            print(file_name)
            logger.error("can't read " + str(file_name))
            continue
        
        df_Main['date_add'] = date_add
        # df_Main.insert(0,'dateAdd',date_add)
        output_path = output_dir + "/" + output + ".csv"
        df_Main.to_csv(output_path, index=False)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Help!')
    parser.add_argument("--input_dir", default='./', help="input directory for filtration by email")
    parser.add_argument("--output_dir", default=".", help="output directory for new file")
    parser.add_argument("--output", default="output", help="output directory for new file")
    parser.add_argument("--email", default=None, help="")
    args = parser.parse_args()
    email = args.email
    input_dir = args.input_dir
    output_dir = args.output_dir
    output = args.output
    if email:
        main(email, input_dir, output_dir, output)
    else:
        print("Email not found")
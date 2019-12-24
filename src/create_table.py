# n_mail - идентификатор сообщения (будет содержать гиперссылку на файл с сообщением, чтобы его можно было открыть после генерации)
# date_mail - дата время отправки/получения сообщения
# from - адрес отправителя
# from_name - иногда имеющееся название, имя, как в записной книжке
# to - адрес получателя
# to_name - иногда имеющееся название, имя, как в записной книжке
# сс - адреса, кому отправлялись копии
# сс_name - имена, кому направлялись копии
# subject - тема письма
# attach - название вложения и его тип файла
from openpyxl import load_workbook
from functools import reduce
from pathlib import Path
import pandas as pd
import argparse
import operator
import datetime
import eml_parser
import os
import glob
from tqdm import tqdm


# сделать гиперссылку для файла в xlsx 
# в начале сделать file://
def make_hyperlink(value):
    value = "/".join(str(value).split('/')[2:]) #str(value)[2:]
    url = "file:///home/{}"
    return '=HYPERLINK("%s", "%s")' % (url.format(value), value)


# PATH_DATA = '../dataset/'
PATH_FOLDER_CSV = '../folder_csv/'
# os.chdir(PATH)
# file_list = glob.glob('*.eml')

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

# def walkdir(folder):
#     """Walk through each files in a directory"""
#     for dirpath, dirs, files in os.walk(folder):
#         for filename in files:
#             yield os.path.abspath(os.path.join(dirpath, filename))

def main(PATH_DATA):
    name_file = "Table.xlsx" #+ datetime.datetime.today().strftime("%m.%d.%Y")
    # Проверить, существует ли файл
    check_exists(name_file)

    filecounter = 0
    for filepath in Path(PATH_DATA).rglob('*.eml'):
        filecounter += 1
    
    date_add_list = []
    n_mail_list = []
    date_list = []
    from_list = []
    from_name_list = []
    to_list = []
    to_name_list = []
    subject_list = []
    attach_list = []
    cc_list = []
    cc_name_list = []

    #Обойти рекурсивно все файлы .eml в папке
    for file_name in tqdm(Path(PATH_DATA).rglob('*.eml'), total=filecounter,  unit="files"):
        with open(file_name, 'rb') as fhdl:
            raw_email = fhdl.read()

            parsed_eml = eml_parser.eml_parser.decode_email_b(raw_email)

            date_add = datetime.datetime.today().strftime("%m.%d.%Y")
            n_mail = file_name
            date = parsed_eml['header']['date']
            try:
                # print(date)
                date = date.strftime("%m.%d.%Y")
            except:
                # print(date)
                date = date_add
            from_ = parsed_eml['header']['from']
            from_name = parsed_eml['header']['header']['from'][0].rsplit(' <')[0]

            try:
                to_ = parsed_eml['header']['to'][0]
            except:
                to_ = parsed_eml['header']['delivered_to'][1]
            try:
                if len(parsed_eml['header']['header']['to'][0].split()) > 1:
                    to_name = parsed_eml['header']['header']['to'][0].split()[0]
                else:
                    to_name = None
            except:
                to_name = None
                #print(file_name)
            

            subject = parsed_eml['header']['subject']

            try:
                attach = parsed_eml['attachment'][0]['filename']
            except:
                attach = None
            try:
                cc = parsed_eml['header']['header']['cc'][0].split(',')
                list_name = []
                # print(cc)
                list_email = parsed_eml['header']['cc']
                for inputstr in cc:
                    words = inputstr.split()
                    list_name.append(([words[index]+' '+words[index+1]
                                    for index in range(len(words)-2)]))
            except:
                list_name = None
                list_email = None

            if list_name:
                list_name = reduce(operator.iconcat, list_name, [])

            #print()
            #print({ 'date_add' : date_add, 'n_mail' : n_mail,'date' : date, 'from_': from_, 'from_name':from_name, 'to_':to_, 'to_name':to_name, 'subject':subject, 'attach':attach,'cc':list_email, 'cc_name':list_name})
            date_add_list.append(date_add)
            n_mail_list.append(n_mail)
            date_list.append(date)
            from_list.append(from_)
            from_name_list.append(from_name)
            to_list.append(to_)
            to_name_list.append(to_name)
            subject_list.append(subject)
            attach_list.append(attach)
            cc_list.append(list_email)
            cc_name_list.append(list_name)


    # df = pd.DataFrame({ 'date_add' : [date_add], 'n_mail' : [n_mail],'date' : [date], 'from_': [from_], 'from_name':[from_name], 'to_':[to_], 'to_name':[to_name], 'subject':[subject], 'attach':[attach],'cc':[list_email], 'cc_name':[list_name]})
    df = pd.DataFrame({'date_add': date_add_list, 'n_mail': n_mail_list, 'date': date_list, \
            'from_': from_list, 'from_name': from_name_list, 'to_': to_list, 'to_name': to_name_list, \
            'subject': subject_list, 'attach':attach_list,'cc': cc_list, 'cc_name': cc_name_list})
    
    df['n_mail'] = df['n_mail'].apply(lambda x: make_hyperlink(x))
    # df.reset_index().style.format({'n_mail': make_hyperlink})
    writer = pd.ExcelWriter(name_file, engine='openpyxl')
    writer.book = load_workbook(name_file)
    writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
    # read existing file
    reader = pd.read_excel(name_file)
    
    # write out the new sheet
    df.to_excel(writer,index=False,header=False,startrow=len(reader)+1)

    writer.close()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='workflow_test')
    parser.add_argument("--path", default=1, help="This is the path to folder with eml or tar.gz")
    args = parser.parse_args()
    path = args.path
    main(path)
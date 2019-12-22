# python mailbox_to_eml.py < mailbox

import re
import sys
import json
import mailbox
import glob
import datetime
import os
import csv
import argparse
# import mailparser
# import email
import eml_parser

dir = 'eml/'
file = "mailbox"


from_line = re.compile('From\s')
blank_line = re.compile('$')
escaped_from_line = re.compile('^>(>*From )')

# принимает на вход, путь до файла mailbox и путь этой папки
def mbox2eml_from(fname):
    #os.chdir(path)
    path_dir = "/".join(str(fname).split('/')[:-1])
    count = 0
    blank_line_flag = True
    output_file = None
    path_dir_eml = path_dir + '/' + "eml"

    # Если папки eml нет,то создать и продолжить, иначе выйти 
    if not os.path.exists(path_dir_eml):
        os.makedirs(path_dir_eml)
    else:
        return 
    with open(fname, encoding="utf8", errors='ignore') as fp:
      for line in fp:
          if blank_line_flag and from_line.match(line):
              if output_file:
                  output_file.close()
              count += 1
              output_file = open(path_dir_eml + '/' + str(count).zfill(4) + '.eml', 'w')
              continue
          output_file.write(escaped_from_line.sub(r'\1', line, 1))
          blank_line_flag = blank_line.match(line)
    
    # for line in sys.stdin:
    #     if blank_line_flag and from_line.match(line):
    #         if output_file:
    #             output_file.close()
    #         count += 1
    #         output_file = open(str(count).zfill(4) + '.eml', 'w')
    #         continue
    #     output_file.write(escaped_from_line.sub(r'\1', line, 1))
    #     blank_line_flag = blank_line.match(line)

    output_file.close()


file_list = glob.glob('*.eml')

for file_name in file_list:
    with open(file_name, 'rb') as fhdl:
        raw_email = fhdl.read()
    parsed_eml = eml_parser.eml_parser.decode_email_b(raw_email)

    data = parsed_eml['header']['date']
    from_ = parsed_eml['header']['from']
    from_name = parsed_eml['header']['header']['from'][0].rsplit(' <')[0]
    test = "Mariusz Należny"
    # to_ = parsed_eml['header']['to'][0]
    print(from_)
    print(from_name)
    # from polyglot.detect import Detector
    # detector = Detector(test)
    # print(detector.language)

    print("-----------------------------------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='workflow_test')
    parser.add_argument("--path", default=1,
                        help="This is the path to folder with eml or tar.gz")
    args = parser.parse_args()
    fname = args.path
    #path_dir = "/".join(str(fname).split('/')[:-1])
    mbox2eml_from(fname)


# writer = csv.writer(open("mbox-output.csv", "w"))

# for message in mailbox.mbox(file):
# 	writer.writerow([message['message-id'], message['from'], message['to']])

# os.chdir(dir)
# file_list = glob.glob('*.eml')

# for file_name in file_list:
#     with open(file_name, 'rb') as fhdl:
#         raw_email = fhdl.read()
#     parsed_eml = eml_parser.eml_parser.decode_email_b(raw_email)
#     date_add = datetime.datetime.today().strftime("%m.%d.%Y")
#     n_mail = file_name
#     date = parsed_eml['header']['date']
#     date = date.strftime("%m.%d.%Y")
#     from_ = parsed_eml['header']['from']
#     from_name = parsed_eml['header']['header']['from'][0].rsplit(' <')[0]
#     print(from_name)
#     print(from_)
#     print ("**************************************")

# mbox = mailbox.mbox(file)
# i=1
# for message in mbox:
#     print(i)
#     print("from   :", message['from'])
#     print("to   :", message['to'])
#     # print("subject:",message['subject'])
#     #print "message:",message['**messages**']
#     print ("**************************************")
#     i+=1

# mail = mailparser.parse_from_file(file)
# print(mail.mail)
# with open(file, 'rb') as fhdl:
#             raw_email = fhdl.read()
# parsed_eml = eml_parser.eml_parser.decode_email_b(raw_email)

# from_ = parsed_eml['header']['from']
# from_name = parsed_eml['header']['header']['from'][0].rsplit(' <')[0]

# print(from_)
# print(from_name)
# with open('mbox_m.json', 'w') as f:
#     f.write(json.dumps(mail.mail))

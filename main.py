import os
import re
import sys
import time
import json
import names
import random
import requests
import pyperclip
import urllib.request
from os.path import exists as file_exists

API = 'https://www.1secmail.com/api/v1/'
domain = random.choice(['oosln.com', 'vddaz.com', 'esiix.com','wwjmp.com','yoggm.com','xojxe.com'])
# clg_name = random.choice(['SRM Institute Of Science And Technology','Vels Institute of Science, Technology & Advanced Studies (VISTAS)','Anna University','Bharath University','Stella Maris College','Dr. M.G.R. Educational and Research Institute, University, H&S Campus','Saveetha University','Panimalar Engineering College','St Joseph Engineering College'])
# degree = random.choice(['Bachelor of Engineering (B.E)','Bachelor of Technology (B.Tech)'])
# year = random.choice(['1st','2nd','3rd','4th'])

def download_file(url,local_filename):
    tmp_ans=file_exists(local_filename)
    if  tmp_ans == 0:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
        return local_filename

def get_mobile_no():
    ph_no = []
    phone=[]
    ph_no.append(random.randint(6, 9))
    for i in range(1, 10):
        ph_no.append(random.randint(0, 9))
    for i in ph_no:
        phone.append(str(i).strip())
    return "".join(phone)

def extract():
    getUserName = re.search(r'login=(.*)&',newMail).group(1)
    getDomain = re.search(r'domain=(.*)', newMail).group(1)
    return [getUserName, getDomain]

def print_statusline(msg: str):
    last_msg_length = len(print_statusline.last_msg) if hasattr(print_statusline, 'last_msg') else 0
    print(' ' * last_msg_length, end='\r')
    print(msg, end='\r')
    sys.stdout.flush()
    print_statusline.last_msg = msg

def deleteMail():
    url = 'https://www.1secmail.com/mailbox'
    data = {
        'action': 'deleteMailbox',
        'login': f'{extract()[0]}',
        'domain': f'{extract()[1]}'
    }
    print_statusline("Disposing your email address - " + mail + '\n')
    req = requests.post(url, data=data)

def checkMails():
    reqLink = f'{API}?action=getMessages&login={extract()[0]}&domain={extract()[1]}'
    req = requests.get(reqLink).json()
    length = len(req)
    if length == 0:
        for x in range(5):
            time.sleep(0.9)
            print_statusline(f"Your mailbox is empty. Hold tight.{'.'*x}")
    else:
        idList = []
        for i in req:
            for k,v in i.items():
                if k == 'id':
                    mailId = v
                    idList.append(mailId)

        x = 'mails' if length > 1 else 'mail'
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, f'All_Mail/{mail}')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        for i in idList:
            msgRead = f'{API}?action=readMessage&login={extract()[0]}&domain={extract()[1]}&id={i}'
            req = requests.get(msgRead).json()
            for k,v in req.items():
                if k == 'from':
                    sender = v
                if k == 'subject':
                    subject = v
                if k == 'date':
                    date = v
                if k == 'textBody':
                    content = v
            
            if Attachments_ans == 'Y':
                if len(req['attachments']) != 0:
                    for z in range(len(req['attachments'])):
                        if str(req['attachments'][z]['filename']) not in filenames_attachments:
                            filenames_attachments.append(str(req['attachments'][z]['filename']))
                print_statusline(f"Totally you received {length} Mail And {len(filenames_attachments)} Attachments : [{', '.join(filenames_attachments)}]")
                for x in filenames_attachments:
                    FileDown=f'https://www.1secmail.com/mailbox/?action=download&id={i}&login={extract()[0]}&domain={extract()[1]}&file={x}'
                    download_file(FileDown,f"{final_directory}/{x}")
            else:
                for x in range(5):
                    print_statusline(f"You received {length} {x}{'.'*x}")
            mail_file_path_txt = os.path.join(final_directory, f'{i}.txt')
            mail_file_path_json = os.path.join(final_directory, f'{i}.json')
            with open(mail_file_path_json, "w") as file:
                file.write(json.dumps(req, indent=4))
            with open(mail_file_path_txt,'w') as file:
                file.write("Sender: " + sender + '\n' + "To: " + mail + '\n' + "Subject: " + subject + '\n' + "Date: " + date + '\n' + "Content: " + content + '\n')

os.system('cls' if os.name == 'nt' else 'clear')

try:
    tmp_name=names.get_full_name()
    print(f"Name : {tmp_name}")
    print(f"Mobile number : {get_mobile_no()}")
    newMail = f"""{API}?login={tmp_name.replace(' ','_').lower()}&domain={domain}"""
    reqMail = requests.get(newMail)
    mail = f"{extract()[0]}@{extract()[1]}"
    if not os.path.exists(f"All_Mail/{mail}"):
        os.makedirs(f"All_Mail/{mail}")
    pyperclip.copy(mail)
    print(f"\nYour temporary email : {mail}\n")
    Attachments_ans = input("Do you want to download attachments (Y/N): ").upper()
    print(f"---------------------------- | Inbox of {mail} | ----------------------------\n")
    filenames_attachments=[]
    while True:
        checkMails()

except(KeyboardInterrupt):
    deleteMail()
    print("\nProgramme Interrupted")
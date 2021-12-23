import time
import os
from bs4 import BeautifulSoup
import configparser
import shutil
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import threading

now = datetime.now()
datetimestamp = now.strftime("%d_%m_%Y_%H_%M_%S")

logging.basicConfig(filename=f'./Logs/ren_main_{datetimestamp}.log', level=logging.INFO)
config = configparser.ConfigParser()

config.read('ren_main_configs.ini')
counter=-1
sourcepath = config['ren_QP']['sourcePath']
destpath = config['ren_QP']['destPath']
roll_or_reg = config['ren_QP']['roll_or_reg']
current_dirs=os.listdir(f"{sourcepath}")

executor = ThreadPoolExecutor(max_workers=100000000)

def readFiles(sFile,destFolder):
    print(sFile)

    with open(sFile,"r",encoding="utf-8") as f:
        html_soup = BeautifulSoup(f, 'html.parser')
    #print(type(html_soup))
    allTables = html_soup.find_all('strong')
    #print(sFile)
    #print(sFile)
    newFileName=allTables[int(f'{roll_or_reg}')].text
    newFileName+=".html"
    try:
        
        shutil.copy(sFile,os.path.join(destpath,destFolder,newFileName))
        logging.info(f'File from {sFile} has been copied to {destFolder} with new filename {newFileName}')
    except FileNotFoundError:
        os.mkdir(os.path.join(destpath,destFolder))
        shutil.copy(sFile,os.path.join(destpath,destFolder,newFileName))
    
    #print(type(str(allTables[2].string)))

processes = []
with ThreadPoolExecutor(max_workers=1000) as executor:
    for (root,dirs,files) in os.walk(os.path.normpath(sourcepath)):
        for cfile in files:
                #print(os.path.join(root,cfile))
                current_file=os.path.join(root,cfile)
                processes.append(executor.submit(readFiles, current_file, current_dirs[counter]))
                #readFiles(current_file,current_dirs[counter])
        counter+=1
        
    

#!/usr/bin/python3

import re, time, sys, getopt, os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

URL = ''
SCOPE = []
OUTSCOPE = []

def err(error):
    print("Use: python h1Scope.py <URL>")
    print("Help: python h1Scope -h")
    print("Error:", error)
    sys.exit()

def helpopt():
    print("""
    # Basic use: 
    python h1Scope.py <URL>
    
    # Save in to a file: 
    python h1Scope.py <URL> -d <DIR>

    # Sometimes you will need increase the rendering time of the webpage
    # for the script to find the links, you can use -t to increase this time.
    # The pattern is 5 seconds
    python h1Scope.py <URL> -t 10

    # If the option -d/--dir is set, the script will create inScope.txt and outScope.txt files.

    ### Requirements
    # This script was only tested in kali linux
    # you will need to install:
        google-chrome browser
        chromedriver_linux
        geckodriver-master

    """)
    sys.exit()

def req(url):
    try:
        res = requests.get(url)
        
        if res.status_code == 200:
            return res.text
        else:
            print("Error when making request..")
    
    except Exception as error:
        print("Request error...")
        err(error)
        

def javascript_parse(res, tempo):
    try:
        #driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'))
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        driver.get(URL)
        time.sleep(int(tempo))
        #driver.maximize_window()
        elem = driver.find_element_by_xpath("//*")
        content = elem.get_attribute("outerHTML")
        
        return content

    except Exception as error:
        print("Error parsing...")
        err(error)

def find_domains(soup):
    try:
        scopes = None
        outs = None
        
        html = BeautifulSoup(soup, features="lxml")
        
        try:
            scopes = html.find_all("div", {"class":"negative-margin-24--left negative-margin-24--right"})[0]
            #scopes = html.find("div", {"class":"Spacing-module_mb-spacing-md__-XCDd"})       
            scopes = scopes.find_all("span", {"class":"spec-asset-identifier break-word"})
        except Exception:
            pass
        #print(scopes)
        try:   
            outs = html.find_all("div", {"class":"negative-margin-24--left negative-margin-24--right"})[1]
            outs = outs.find_all("span", {"class":"spec-asset-identifier break-word"})
        except Exception:
            pass

        if scopes:
            print("...In Scope...")
            for scope in scopes:
                 print(scope.text)
                 SCOPE.append(scope.text)
        else:
            scope = None
        
        print("......................")
        
        if outs:
            print("...Out of scope...")
            for out in outs:
                print(out.text)
                OUTSCOPE.append(out.text)
        else:
            out = None
        
        print(".....................")

    
    except:
        print("Error to find links...")
        return None

def save(outdir, scopes, outs):
    try:
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        
        path = outdir
        scope = ""
        out = ""
        
        if scopes:
            file = path + '/inScope.txt'
            for scope in scopes:
                with open(file, "a") as arc:
                    arc.write("{}\n".format(scope))
        
        if outs:
            outfile = path + '/outScope.txt'
            for out in outs:
                with open(outfile, "a") as arc2:
                    arc2.write("{}\n".format(out))

    except Exception as error:
        print("Save error...")
        err(error)

def main():
    size = len(sys.argv)
    outputdir = ''
    args = None
    opts = None
    tempo = 5
    
    try:
        if URL == "-h":    
            helpopt()

        res = req(URL) 

        try: 
            opts, args = getopt.getopt(sys.argv[2:],"hd:t:",["odir=", ["--time"]])
        
        except getopt.GetoptError as error:
            print("argv error...")
            err(error)
                    
        for opt, arg in opts:
            if opt == 'h':
                helpopt()
            elif opt in ("-d", "--odir"):
                outputdir = arg
            elif opt in ("-t", "--time"):
                tempo = arg

        if res:
            soup = javascript_parse(URL, tempo)
            if soup:
                find_domains(soup)
                    
        if outputdir:
            save(outputdir, SCOPE, OUTSCOPE)
                            
    except Exception as error:
        err(error)

if __name__ == "__main__":
    try:
        URL = (sys.argv[1])
        main()
    
    except Exception as error:
        print("argv error...")
        err(error)

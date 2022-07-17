    # Basic use: 
    python hoScope.py <URL>
    
    # Save in to a file: 
    python hoScope.py <URL> -d <DIR>

    # Sometimes you will need increase the rendering time of the webpage
    # for the script to find the links, you can use -t to increase this time.
    # The pattern is 5 seconds
    python hoScope.py <URL> -t 10

    # If the option -d/--dir is set, the script will create inScope.txt and outScope.txt files.

    ### Requirements
    # This script was only tested in kali linux
    # you will need to install:
        google-chrome browser
        chromedriver_linux
        geckodriver-master


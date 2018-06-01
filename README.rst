.. epigraph::

    "The value of openness lies in the fact that people not actually attending
    trials can have confidence that standards of fairness are being observed;
    the sure knowledge that anyone is free to attend gives assurance that
    established procedures are being followed and that deviations will become
    known."

    -- `Press-Enterprise Co. v. Superior Court (1986)
    <https://www.law.cornell.edu/supremecourt/text/478/1>`_
    
**CalScrape** is a tool for rapidly searching public federal judicial calendars
for cases of interests. It is primarily geared toward journalists but would also
    be useful to researchers and generally interested members of the public. It
    provides an alternative (and free) way to following cases aside from PACER.

As of writing, CalScrape currently only supports calendars for the U.S. District
Court for the Northern District of California (NDCAL). Ultimately the goal is to
extend this to other federal court calendars in California and other states.

Installation 
------------

CalScrape requires your machine to be running Python 3x. It also has several
dependencies. Follow the instructions below to install and run CalScrape (these
should cover MacOS and most Linux distros; Windows instructions not yet
available).


* `Download <https://www.python.org/downloads/>`_ the latest version of Python.
* Open a Terminal window and install the Requests library with the command:

:: 
    
    $ pip install requests

* Then install the LXML library using the following command:

:: 
    
    $ pip install lxml

You can install CalScrape by then entering the following commands:

:: 

    $ git clone https://github.com/elwha1/calscrape.git 
    $ cd calscrape

If you do not currently have Git installed on your computer, MacOS will prompt
you to install it. This project is currently set to private so you may need to
speak with me to get access. (Note: You may need to install ``pip`` or
``pip3``.)

Running CalScrape 
-----------------

Once in the file directory, CalScrape can be run via this terminal command:

::

    $ python3 calscrape.py

The keyword search terms and cases of interest are configured in the
``searchterms.json`` and ``cases.json`` files in the directory. Tools are
coming to allow users to configure this file and search by case number.

Support 
-------

If you want to contribute to this project, experience problems or have other
questions, please email me at bghancock@gmail.com

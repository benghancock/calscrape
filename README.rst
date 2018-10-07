=========
CalScrape
=========

.. epigraph::

    "The value of openness lies in the fact that people not actually attending
    trials can have confidence that standards of fairness are being observed;
    the sure knowledge that anyone is free to attend gives assurance that
    established procedures are being followed and that deviations will become
    known."

    -- `Press-Enterprise Co. v. Superior Court (1986)
    <https://www.law.cornell.edu/supremecourt/text/478/1>`_
    
**CalScrape** is a tool for rapidly searching judicial calendars for court
hearings of interest. It is primarily geared toward journalists but would also
be useful to researchers and interested members of the public. It provides an
alternative (and free) way to follow hearings in cases aside from PACER.

As of writing, CalScrape only supports the U.S. District Court for the Northern
District of California (CAND). Ultimately the goal is to extend this to other
federal and state courts throughout the United States. A lot of work has been
done to make the code modular so that bolting on support for further courts can
be as seamless as possible. 

Installation 
------------

CalScrape requires Python 3.6+. It also has several dependencies. Follow the
instructions below to install and run CalScrape. This should cover MacOS and
most Linux distros; instructions for Windows are not yet available.

* Clone the repository using the URL that appears after clicking "Clone or
  download"

:: 

    $ git clone https://github.com/elwha1/calscrape.git

Or you can download the latest release from the **releases** tab and unzip it

* Move into the CalScrape directory

::

    $ cd calscrape

* Install the software package dependencies

::

    $ pip install requirements.txt

You should see a list of packages being installed. You may need to install
``pip`` on your machine if you don't have it already.

Running CalScrape 
-----------------

Once in the file directory, CalScrape can be run via this terminal command:

::

    $ python calscrape.py

You may need to substitute ``python`` for ``python3``, depending on your
installation. CalScrape supports two search modes: ``keyword`` and ``list``.
The ``list`` mode searches the calendars for all terms stored in the file
``user/searchterms.json``. Feel free to edit this file to include as many
terms as you want (company names, party names, etc.). Just be cautious to
format the list correctly:

::

    ["List", "the", "terms", "like", "this"]

Also be aware that including a lot of search terms may return a large volume of
results -- making the tool less helpful. 

Contributing
------------
CalScrape is an open source project being developed to further the public
interest and increase awareness about the court system. Contributions are
welcome. If you encounter an issue, please file it using the issue-tracking
tool. If you'd like to contribute to the project, send me an email first at:
ben.hancock@protonmail.com 

License
-------
CalScrape is licensed under the GNU Affero General Public License. For more
details, see the LICENSE.txt file.

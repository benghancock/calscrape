================================================
CalScrape: Scrape & Search Judicial Hearing Data
================================================


**CalScrape** is a free and open-source command line tool written in Python
that allows users to rapidly find data about hearings in certain courts. In
other words, it is a judicial *cal* -endar *scrape* -er.


Why?
====

Data about judicial proceedings can be tricky to find and a pain to search
through. Records in the supposedly public PACER system cost an exorbitant
amount of money, and other solutions focus on providing full court dockets or
judicial opinions. Court websites, meanwhile, tend to spread the information
out over multiple pages or store it in a not-so-user-friendly format.

In short, there hasn't been an easy way for journalists or other interested
members of the public to find information about *upcoming* hearings that they
may want to attend. And that's important: open information about public
hearings helps ensure the proper functioning of the justice system.

.. epigraph::

    "The value of openness lies in the fact that people not actually attending
    trials can have confidence that standards of fairness are being observed;
    the sure knowledge that anyone is free to attend gives assurance that
    established procedures are being followed and that deviations will become
    known."

    -- `Press-Enterprise Co. v. Superior Court (1986)`_

.. _Press-Enterprise Co. v. Superior Court (1986): https://www.law.cornell.edu/supremecourt/text/478/1


Quickstart
==========

CalScrape is not yet available via PyPI. The easiest way to install it is to
clone the GitHub repo and use ``pip`` to resolve the dependencies. Assuming
you're on a Linux or other *nix-like system, open a terminal and enter:

.. code:: bash

   $ git clone https://github.com/elwha1/calscrape.git


Once you've done that, ``cd`` into the repo directory and install like so:

.. code:: bash

   $ pip install --user .


You will see ``pip`` fetch and install any necessary packages. Now, you should
be able to enter the following command to start using CalScrape:

.. code:: bash

   $ calscrape --help       


Installation
============
CalScrape requires Python 3.6 or greater and has several package dependencies.
The instructions below cover CalScrape installation on most macOS and Linux
systems; Windows instructions are forthcoming. CalScrape is run from the
command line, so these instructions assume some familiarity with the terminal.

#. Download and install the `latest version of Python
   <https://www.python.org/downloads/>`__
#. Download CalScrape in one of two ways:

   * If you have ``git`` installed on your machine, you can run ``git clone
     https://github.com/elwha1/calscrape.git`` to clone the repository
   * Alternatively, you can download the latest release from the **releases**
     tab and unzip it into a directory of your choosing  
#. Move into the directory using the command ``cd <directory-name>``
#. The simplest way to install the dependencies is to enter the command ``pip
   install -r requirements.txt``. (``pip`` should be installed after you
   install Python.)

Running CalScrape
=================
**New as of v2.0.0**
Prior versions of CalScrape were run from the command line in an interactive
mode, but as of v2.0.0 the program is now run using *command line arguments*. Once
in the correct directory, enter the command below to see the help menu and the
various options:

::

    $ python calscrape.py --help

You may need to substitute ``python`` for ``python3``, depending on your
installation.

The help menu options should explain how to run CalScrape in its
various modes. Generally, the options are to run in ``full`` mode, which scrapes
all hearings from the court and prints them to the terminal window; ``silent``
mode, which does the same as the prior option but saves the data as a JSON file
in the directory (note that this file is overwritten with each scrape); and
``keyword`` mode, which searches the hearings for the given keyword and prints
those hearings that match to the terminal, in chronological order.

You may notice that scraping the calendar takes longer than in prior versions.
This is because ``sleep`` times have been built in between each scrape in order
not to cause unduly heavy traffic on court servers.

Contributing
============
CalScrape is an open source project being developed to further the public
interest and increase awareness about the court system. Contributions are
welcome. If you encounter an issue, please file it using the issue-tracking
tool. If you'd like to  contribute or have ideas for how to improve CalScrape,
feel free to make a pull request or `get in touch
<https://elwha1.github.io>`__.

License
=======
CalScrape is licensed under the GNU Affero General Public License. For more
details, see the LICENSE.txt file.

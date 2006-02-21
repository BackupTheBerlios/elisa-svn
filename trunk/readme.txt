
Dependencies
============

- Python >= 2.4
- PyGame
- Gstreamer 0.10 + binding python
- ConfigObj : http://www.voidspace.org.uk/python/configobj.html
- setuptools : http://peak.telecommunity.com/DevCenter/EasyInstall

and some others. (I need to check :) )


Notes about setuptools
======================

Download http://peak.telecommunity.com/dist/ez_setup.py and run it as
root. 


To run the samplebox
====================

1. Be sure to have installed setuptools
2. build the plugins (there will be an automatic build mechanism very soon):

   $ cd plugins/pictures
   $ sudo python setup.py develop

3. set your PYTHONPATH so that you don't need to install Elisa for
   testing it:

   $ export PYTHONPATH="/path/to/src/"
   $ python samplebox.py


SampleBox
=========

you can find here a sample code for the box.
It's a VERY SIMPLE test implementation of the box specification.

for test video, edit src/plugins/movies.py and change the path of video sample.

key map
-------

- Arrows  : for navigation
- Enter   : Action (play video ...)
- space   : Hide/Show menu.

#!/bin/sh
#
#Generate html doc from project source files
#see http://epydoc.sourceforge.net/

epydoc --html -o docs src/framework/ src/boxwidget/ src/plugins/

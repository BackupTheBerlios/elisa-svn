#!/bin/sh
#
#Generate html doc from project source files
#see http://epydoc.sourceforge.net/

epydoc --html --check --debug --no-private -o docs src/testGL/zAPI/zForms/ src/framework/ src/boxwidget/ src/plugins/

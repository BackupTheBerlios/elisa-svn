#!/bin/sh
#
#Generate html doc from project source files
#see http://epydoc.sourceforge.net/

# extern/testGL/zAPI/zForms/

epydoc --html --debug --no-private -o docs  elisa/framework/ elisa/boxwidget/ elisa/player/ elisa/utils

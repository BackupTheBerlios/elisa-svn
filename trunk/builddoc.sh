#!/bin/sh
#
#Generate html doc from project source files
#see http://epydoc.sourceforge.net/

# extern/testGL/zAPI/zForms/

# 

epydoc --html --debug -o docs elisa/framework/  elisa/player/ elisa/utils  elisa/boxwidget/ 

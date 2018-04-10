#!/usr/bin/python

"""
Microarray Analysis cgi script
BY Xiaoji Sun
"""

##################################################################################################
# import modules and functions
import cgi
from array_functions import database_query

# this helps to display errors to the screen when submitting the web form.
import cgitb
cgitb.enable()



##################################################################################################
# construct the variables
title = 'Hochwagen Lab Microarray Analysis'
form = cgi.FieldStorage()
message = ''


##################################################################################################
# content added into the body
# the program only runs when inputs are provided
# dropdown menu for the database search
if form.getvalue('dropdown'):
    if form.getvalue('dropdown') == 'strain':
        """
        If the user queries for a specific strain number, it returns a list of all the experiments
        on that strain.
        """
        # gets the input from the web form
        strain = form.getvalue('input')

        # if submit without entering anything, print error message
        if strain == None:
            message += 'STRAIN NUMBER CAN NOT BE EMPTY, PLEASE ENTER ONE!'
        else:
            # runs the query
            output = database_query(strain=strain)

            # if strain not found, print error message
            if output == []:
                message += 'THE STRAIN YOU ENTERED IS NOT FOUND, PLEASE TRY ANOTHER ONE!'
            else:
                message += '<font color=\"blue\">Here are the experiments found done on strain '
                message += strain
                message += ':</font>'
                message += '<BR>\n'
                message += '<BR>\n'
                message += '<table border=2">'
                message += '<tr><td><b>Record ID</b></td><td><b>Experiment Folder</b></td><td><b>Array</b></td><td><b>Strain</b></td><td><b>Experiment</b></td><td><b>Replicate</b></td><td><b>Spot File</b></td><td><b>Description</b></td></tr>'
                for line in output:
                    message += '<tr><td>'
                    message += '</td><td>'.join([i for i in line])
                    message += '</tr>'
                message += '</table>'
                        
                
    if form.getvalue('dropdown') == 'keyword':
        """
        If the user queries for a keyword, it returns a list of all the experiments that have this keyword in
        Experiment column.
        """
        # gets the input from the web form
        keyword = form.getvalue('input')

        # if submit without entering anything, print error message
        if keyword == None:
            message += 'KEYWORD CAN NOT BE EMPTY, PLEASE ENTER ONE!'
        else:
            # runs the query
            output = database_query(keyword=keyword)

            # if keyword not found, print error message
            if output == []:
                message += 'THE KEYWORD YOU ENTERED IS NOT FOUND, PLEASE TRY ANOTHER ONE!'
            else:
                message += '<font color=\"blue\">Here are the experiments found containing keyword '
                message += keyword
                message += ':</font>'
                message += '<BR>\n'
                message += '<BR>\n'
                message += '<table border=2">'
                message += '<tr><td><b>Record ID</b></td><td><b>Experiment Folder</b></td><td><b>Array</b></td><td><b>Strain</b></td><td><b>Experiment</b></td><td><b>Replicate</b></td><td><b>Spot File</b></td><td><b>Description</b></td></tr>'
                for line in output:
                    message += '<tr><td>'
                    message += '</td><td>'.join([i for i in line])
                    message += '</tr>'
                message += '</table>'



##################################################################################################
# basic construction
text = 'Content-type: text/html\n\n'
text += '<html>\n'
text += '<head>\n'
text += '<style type=\"text/css\"> #button {background-color:#eeeeee;border-top:2px solid #dbdbdb;border-right:2px solid #dbdbdb;border-bottom:4px solid #dbdbdb;border-left:2px solid #ccc8cc;padding:5px;color: #666;font-size:16px;font-weight:bold;cursor:hand;}</style>'
text += '<title>' + title + '</title>\n'
text += '</head>\n'
text += '<body>\n'
text += '<h1>MICROARRAY DATABASE OF HOCHWAGEN LAB</h1>\n'
text += '<BR>\n'
text += '<h3><font color=\"red\">PLEASE ENTER A STRAIN NUMBER OR A KEYWORD TO START YOUR SEARCH:</font></h3>\n'
text += '1. Strain numbers are from FileMaker database.'
text += '<BR>\n'
text += '2. Keyword can be any word describing the experiment.'
text += '<BR>\n'
text += '3. Experiments in this database can be viewed using PLOT VIEWER.</b>'
text += '<BR>\n'
text += '<BR>\n'



##################################################################################################
# content added into the body to create the web form
# basic form
text += '<FORM ACTION=\"array.cgi\", METHOD=\"GET\">\n'
text += '<SELECT NAME=\"dropdown\">\n'
text += '<OPTION VALUE=\"strain\" SELECTED>STRAIN</OPTION>\n'
text += '<OPTION VALUE=\"keyword\">KEYWORD</OPTION>\n'
text += '</SELECT>\n'
text += '<INPUT TYPE=\"TEXT\" name=\"input\">\n'
text += '<BR>\n'
text += '<BR>\n'
text += '<INPUT id=\"button\" TYPE=\"SUBMIT\" NAME=\"submit\" VALUE=\"Search!\">\n'
text += '</FORM>\n'
text += '<BR>\n'
text += '<HR>\n'
text += '<BR>\n'
text += '<a href=\"http://hochwagen-lab3.bio.nyu.edu/cgi-bin/array_plot.cgi\"><b><font color=\"red\">GO TO PLOT VIEWER!</font></b></a>'
text += '<BR>\n'
text += '<BR>\n'

##################################################################################################
# content added into the body to display the results
text += message


# close the body etc.
text += '<br><br><br>'
text += '<hr>'
text += 'Last update: 8/22/2013'
text += '<br>'
text += 'questions or suggestions to: xs338@nyu.edu'
text += '</body>\n'
text += '</html>'

# display the form or blast results
print text



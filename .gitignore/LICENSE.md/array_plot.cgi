#!/usr/bin/python

"""
Microarray Analysis cgi script for plots
BY Xiaoji Sun
"""

##################################################################################################
# import modules and functions
import cgi
from array_functions import database_query
from array_functions import signal_plot1
from array_functions import signal_plot2
from array_functions import coverage_plot1
from array_functions import coverage_plot2
from array_functions import gene_list
from array_functions import tel_plot1
from array_functions import tel_plot2
from array_functions import norm_gene1
from array_functions import norm_gene2
from array_functions import pcorr


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
if form.getvalue('dropdown')=='1':
    # gets the input from the web form
    id1 = form.getvalue('record_id_1')
    id2 = form.getvalue('record_id_2')

    # if submit without entering anything, print error message
    if id1 == None :
        if id2 == None:
            message += 'Record ID CAN NOT BE EMPTY, PLEASE ENTER ONE!'
        if id2 != None:
            message += 'THE FIRST Record ID CAN NOT BE EMPTY IF YOU WOULD LIKE TO VIEW PAIRWISE PLOT!'
    if id1 != None:
        if id2 == None:
            chromosome = form.getvalue('dropdown_chr')
            start = form.getvalue('region_start')
            end = form.getvalue('region_end')
            max_signal = form.getvalue('max_signal')
            plotname = signal_plot1(id1, chromosome, start, end, max_signal)
            message += '<img src=\"http://hochwagen-lab3.bio.nyu.edu/plots/' + plotname + '\"'+ ' alt=\"signalplot\">'

            # print a gene list
            if form.getvalue('checkbox')=='genelist':
                output = gene_list(chromosome, start, end)
                
                # if genes are not found, print error message
                if output == []:
                    message += 'SORRY! NO GENES ARE FOUND, PLEASE TRY A LARGER REGION.'
                else:
                    message += '<BR>\n'
                    message += '<p>\n'
                    message += '<font color=\"blue\"><b>HERE ARE THE GENES FOUND IN THIS REGION'
                    message += ': </b></font>'
                    message += '<BR>\n'
                    message += '<BR>\n'
                    message += '<table border=2">'
                    message += '<tr><td><b>GENE ID</b></td><td><b>CHR</b></td><td><b>GENE NAME</b></td><td><b>START</b></td><td><b>END</b></td><td><b>STRAND</b></td><td><b>Description</b></td></tr>'
                    for line in output:
                        message += '<tr><td>'
                        for j in range(len(line)):
                            if j==0:
                                # make hyperlinks to the sk1.cgi
                                message += '<a href=\"http://hochwagen-lab3.bio.nyu.edu/cgi-bin/sk1.cgi?dropdown=GENE ID&input='+line[0]+'\">'+line[0]
                                message += '</a></td>'
                            else:
                                message += '<td>' + line[j] +'</td>'
                        message += '</tr>'
                    message += '</table>'
                    
        # pairwise plot          
        else:
            chromosome = form.getvalue('dropdown_chr')
            start = form.getvalue('region_start')
            end = form.getvalue('region_end')
            max_signal = form.getvalue('max_signal')
            pcor = pcorr(id1, id2)
            message += 'The Pearson correlation coefficient between these two datasets is: '+ '<font color=\"red\">' + pcor + '</font>'
            message += '<BR>'
            plotname = signal_plot2(id1, id2, chromosome, start, end, max_signal)
            message += '<img src=\"http://hochwagen-lab3.bio.nyu.edu/plots/' + plotname + '\"'+ ' alt=\"signalplot\">'

            # print a gene list
            if form.getvalue('checkbox')=='genelist':
                output = gene_list(chromosome, start, end)

            # if genes are not found, print error message
                if output == []:
                    message += 'SORRY! NO GENES ARE FOUND, PLEASE TRY A LARGER REGION.'
                else:
                    message += '<BR>\n'
                    message += '<p>\n'
                    message += '<font color=\"blue\"><b>HERE ARE THE GENES FOUND IN THIS REGION'
                    message += ': </b></font>'
                    message += '<BR>\n'
                    message += '<BR>\n'
                    message += '<table border=2">'
                    message += '<tr><td><b>GENE ID</b></td><td><b>CHR</b></td><td><b>GENE NAME</b></td><td><b>START</b></td><td><b>END</b></td><td><b>STRAND</b></td><td><b>Description</b></td></tr>'
                    for line in output:
                        message += '<tr><td>'
                        for j in range(len(line)):
                            if j==0:
                                # make hyperlinks to the sk1.cgi
                                message += '<a href=\"http://hochwagen-lab3.bio.nyu.edu/cgi-bin/sk1.cgi?dropdown=GENE ID&input='+line[0]+'\">'+line[0]
                                message += '</a></td>'
                            else:
                                message += '<td>' + line[j] +'</td>'
                        message += '</tr>'
                    message += '</table>'

                
        
if form.getvalue('dropdown')=='2':
    # gets the input from the web form
    id1 = form.getvalue('record_id_1')
    id2 = form.getvalue('record_id_2')

    # if submit without entering anything, print error message
    if id1 == None :
        if id2 == None:
            message += 'Record ID CAN NOT BE EMPTY, PLEASE ENTER ONE!'
        if id2 != None:
            message += 'THE FIRST Record ID CAN NOT BE EMPTY IF YOU WOULD LIKE TO VIEW PAIRWISE PLOT!'
    if id1 != None:
        if id2 == None:
            plotname = coverage_plot1(id1)
            message += '<img src=\"http://hochwagen-lab3.bio.nyu.edu/plots/' + plotname + '\"'+ ' alt=\"barplot\">'
        else:
            plotname = coverage_plot2(id1, id2)
            message += '<img src=\"http://hochwagen-lab3.bio.nyu.edu/plots/' + plotname + '\"'+ ' alt=\"barplot\">'
    


if form.getvalue('dropdown')=='3':
     # gets the input from the web form
    id1 = form.getvalue('record_id_1')
    id2 = form.getvalue('record_id_2')

    # if submit without entering anything, print error message
    if id1 == None :
        if id2 == None:
            message += 'Record ID CAN NOT BE EMPTY, PLEASE ENTER ONE!'
        if id2 != None:
            message += 'THE FIRST Record ID CAN NOT BE EMPTY IF YOU WOULD LIKE TO VIEW PAIRWISE PLOT!'
    if id1 != None:
        if id2 == None:
            plotname = norm_gene1(id1)
            message += '<img src=\"http://hochwagen-lab3.bio.nyu.edu/plots/' + plotname + '\"'+ ' alt=\"normplot\">'
        else:
            plotname = norm_gene2(id1, id2)
            message += '<img src=\"http://hochwagen-lab3.bio.nyu.edu/plots/' + plotname + '\"'+ ' alt=\"normplot\">'



if form.getvalue('dropdown')=='4':
    # gets the input from the web form
    id1 = form.getvalue('record_id_1')
    id2 = form.getvalue('record_id_2')

    # if submit without entering anything, print error message
    if id1 == None :
        if id2 == None:
            message += 'Record ID CAN NOT BE EMPTY, PLEASE ENTER ONE!'
        if id2 != None:
            message += 'THE FIRST Record ID CAN NOT BE EMPTY IF YOU WOULD LIKE TO VIEW PAIRWISE PLOT!'
    if id1 != None:
        if id2 == None:
            plotname = tel_plot1(id1)
            message += '<img src=\"http://hochwagen-lab3.bio.nyu.edu/plots/' + plotname + '\"'+ ' alt=\"telplot\">'
        else:
            plotname = tel_plot2(id1, id2)
            message += '<img src=\"http://hochwagen-lab3.bio.nyu.edu/plots/' + plotname + '\"'+ ' alt=\"telplot\">'


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
text += '<h3><font color=\"red\">WELCOME TO THE MICROARRAY PLOT VIEWER:</font></h3>\n'
text += '<ul style=\"line-height:1.4;\">'
text += '<li>1. Record IDs are obtained from '
text += '<a href=\"http://hochwagen-lab3.bio.nyu.edu/cgi-bin/array.cgi\"><b><font color=\"red\">DATABASE</font></b></a>'
text += '.'
text += '<BR>\n'
text += '<li>2. You can either plot a single experiment or two experiments.'
text += '<li>3. Four types of plots are available for viewing the data: '
text += '<ul>'
text += '<li>a. Linear Signal Plot: Signals vs. Chromosome Positions.'
text += '<BR>\n'
text += 'NOTE: You can specify a region to zoom in your plot or search for genes in this region.'
text += '<li>b. Signal Coverage Barplot: Average Signals Per Unit vs. Chromosomes Sorted by Length.'
text += '<li>c. Normalized Gene Plot: Signals vs. Normalized Genes + 650bp up/downstream.'
text += '<li>d.Telomere Distance Plot: Signals vs. Distance From Telomere'
text += '</ul>'
text += '<BR>\n'
text += '</ul>'
text += '<BR>\n'


##################################################################################################
# content added into the body to create the web form
# basic form
# inputs for record id1 and record id2
text += '<FORM ACTION=\"array_plot.cgi?dropdown\", METHOD=\GET\">\n'
text += '<strong>Please enter a Record ID: </strong>'
text += '<INPUT TYPE=\"TEXT\" name=\"record_id_1\">\n'
text += '<BR>\n'
text += '<strong>Please enter a second Record ID: </strong>\n'
text += '<INPUT TYPE=\"TEXT\" name=\"record_id_2\">\n'
text += ' (optional: only for pairwise plot)'
text += '<BR>\n'
text += '<BR>\n'
text += '<HR>\n'

# dropdown menu of plots selection
text += '<h3><font color=\"blue\">Please select a type of plot:</font></h3>\n'
text += '<SELECT NAME=\"dropdown\">\n'
text += '<OPTION VALUE=\"1\" SELECTED>Linear Signal Plot</OPTION>\n'
text += '<OPTION VALUE=\"2\">Signal Coverage Barplot</OPTION>\n'
text += '<OPTION VALUE=\"3\">Normalized Gene Plot</OPTION>\n'
text += '<OPTION VALUE=\"4\">Telomere Distance Plot</OPTION>\n'
text += '</SELECT>\n'
text += '<BR>\n'
text += '<BR>\n'
text += '<p>\n'

# more features for linear signal plots
text += '<font color=\"blue\">More features for \"Linear Signal Plots\" ONLY:</font>'
text += '<BR>\n'
text += '<p>\n'
text += '<u>Define a region to zoom in your plot: </u>'
text += '<SELECT NAME=\"dropdown_chr\">\n'
text += '<OPTION VALUE=\"1\">CHR01</OPTION>\n'
text += '<OPTION VALUE=\"2\">CHR02</OPTION>\n'
text += '<OPTION VALUE=\"3\" SELECTED>CHR03</OPTION>\n'
text += '<OPTION VALUE=\"4\">CHR04</OPTION>\n'
text += '<OPTION VALUE=\"5\">CHR05</OPTION>\n'
text += '<OPTION VALUE=\"6\">CHR06</OPTION>\n'
text += '<OPTION VALUE=\"7\">CHR07</OPTION>\n'
text += '<OPTION VALUE=\"8\">CHR08</OPTION>\n'
text += '<OPTION VALUE=\"9\">CHR09</OPTION>\n'
text += '<OPTION VALUE=\"10\">CHR10</OPTION>\n'
text += '<OPTION VALUE=\"11\">CHR11</OPTION>\n'
text += '<OPTION VALUE=\"12\">CHR12</OPTION>\n'
text += '<OPTION VALUE=\"13\">CHR13</OPTION>\n'
text += '<OPTION VALUE=\"14\">CHR14</OPTION>\n'
text += '<OPTION VALUE=\"15\">CHR15</OPTION>\n'
text += '<OPTION VALUE=\"16\">CHR16</OPTION>\n'
text += '</SELECT>\n'
text += 'Region From: '
text += '<INPUT TYPE=\"TEXT\" name=\"region_start\">\n'
text += ' To: '
text += '<INPUT TYPE=\"TEXT\" name=\"region_end\">\n'
text += 'bp'
text += '<BR>\n'
text += '<p>\n'
text += '<u>Define a maximum value of the signal shown in plots to exclude outliers: </u>'
text += '<INPUT TYPE=\"TEXT\" name=\"max_signal\">\n'
text += '<BR>\n'
text += '<BR>\n'
text += '<input type=\"checkbox\" name=\"checkbox\" value=\"genelist\"> <u>Print the list of genes that are in the selected area</u>'
text += '<p>\n'

# submit button
text += '<INPUT id=\"button\" TYPE=\"SUBMIT\" NAME=\"submit\" VALUE=\"GO Plotting!\">\n'
text += '</FORM>\n'
text += '<HR>\n'




##################################################################################################
# content added into the body to display the results
text += message


# close the body etc.
text += '<br><br><br><br><br>'
text += '<hr>'
text += 'Last update: 8/21/2013'
text += '<br>'
text += 'questions or suggestions to: xs338@nyu.edu'
text += '</body>\n'
text += '</html>'

# display the form or blast results
print text

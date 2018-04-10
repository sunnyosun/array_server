# Microarray Database Functions (imported by array.cgi)
# Xiaoji Sun
# 8/18/2013

###############################################################################
# Modules
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib as mpl
from scipy import stats

###############################################################################
# Functions


# search the database by strain or keyword
def database_query (strain=None, keyword=None):
    
    # reads the data list txt file
    f = open('microarray_data_list.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    alldata = [i.split('\t') for i in datalist]
    
    # if input is a strain
    if strain:
        query = [i for i in alldata if strain == i[3]]
        return query
        
    # if input is a keyword
    if keyword:
        query = [i for i in alldata if keyword.upper() in i[4].upper()]
        return query
        
   
# single linear plot     
def signal_plot1 (record_id, chromosome ,start=None, end=None, max_signal=None):
    
    # reads the data list txt file
    f = open('microarray_data_list.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    alldata = [i.split('\t') for i in datalist]
    
    # default start is 0
    if start:
        start = start
    else:
        start = 0
    
    # find the experiment according to record_id
    for i in alldata[1:]:
        if record_id == i[0]:
            name = '../share/arrays/' +i[1] + '/' + i[2]
            f = open(name, 'r')
            data = f.read().split('\n')
            f.close()
    array = [i.split('\t') for i in data]   
     
    # plot a specified chromosome region
    data_x = []
    data_y = []
    for i in array[1:]:
        if chromosome == i[0] and i[3] != 'NA':
            data_x.append(int(i[1]))
            data_y.append(2**(float(i[3])))
    plt.plot(data_x, data_y)
    plt.grid(True)
    plt.xlabel('Chromosome ' + chromosome + ' (bp)')
    plt.ylabel('Singal')
    plt.title('Linear Signal Plot of Record ' + record_id)
    if end:
        plt.xlim((int(start), int(end)))
    else:
        plt.xlim((int(start), max(data_x)+10000))
    if max_signal:
        plt.ylim((0, int(max_signal)))
    
    # save the plot    
    plotname = '../Documents/plots/'+ record_id + '_chr' + chromosome + '.png'
    f = open(plotname, 'wb')
    plt.savefig(plotname, orig_size=(1500,1300))
    f.close()
    
    # change the mode so it can be accessed by server
    os.chmod(plotname,0755)
    
    # return plotname
    return (record_id + '_chr' + chromosome + '.png')
    
    
    

# pairwise linear plot
def signal_plot2 (record_id1, record_id2, chromosome ,start=None, end=None, max_signal=None):
    
    # reads the data list txt file
    f = open('microarray_data_list.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    alldata = [i.split('\t') for i in datalist]
    
    # default start is 0
    if start:
        start = start
    else:
        start = 0
    
    # find the experiment according to record_id1
    for i in alldata[1:]:
        if record_id1 == i[0]:
            name = '../share/arrays/' +i[1] + '/' + i[2]
            f = open(name, 'r')
            data = f.read().split('\n')
            f.close()
    array1 = [i.split('\t') for i in data]
    
    # find the experiment according to record_id2
    for i in alldata[1:]:
        if record_id2 == i[0]:
            name = '../share/arrays/' +i[1] + '/' + i[2]
            f = open(name, 'r')
            data = f.read().split('\n')
            f.close()
    array2 = [i.split('\t') for i in data]
     
    # array1
    data_x1 = []
    data_y1 = []
    for i in array1[1:]:
        if chromosome == i[0] and i[3] != 'NA':
            data_x1.append(int(i[1]))
            data_y1.append(2**(float(i[3])))
    
    # array2
    data_x2 = []
    data_y2 = []
    for i in array2[1:]:
        if chromosome == i[0] and i[3] != 'NA':
            data_x2.append(int(i[1]))
            data_y2.append(2**(float(i[3])))        
            
    # plot specific region
    # make a little extra space between the subplots
    plt.subplots_adjust(wspace=0.5)
    
    # upper plot
    plt.subplot(211)
    plt.plot(data_x1, data_y1)
    plt.grid(True)
    plt.ylabel('Signal of Record ' + record_id1)
    if end:
        plt.xlim((int(start), int(end)))
    else:
        plt.xlim((int(start), max(data_x1)+10000))
    if max_signal:
        plt.ylim((0, int(max_signal)))
        
    # bottom plot
    plt.subplot(212)
    plt.plot(data_x2, data_y2, color='r')
    plt.grid(True)
    plt.xlabel('Chromosome ' + chromosome + ' (bp)')
    plt.ylabel('Signal of Record ' + record_id2)
    if end:
        plt.xlim((int(start), int(end)))
    else:
        plt.xlim((int(start), max(data_x2)+10000))
    if max_signal:
        plt.ylim((0, int(max_signal)))
    
    # save the plot    
    plotname = '../Documents/plots/'+ record_id1 + '-' + record_id2 + '_chr' + chromosome + '.png'
    f = open(plotname, 'wb')
    plt.savefig(plotname, orig_size=(1500,1300))
    f.close()
    
    # change the mode so it can be accessed by server
    os.chmod(plotname,0755)
    
    # return plotname
    return (record_id1 + '-' + record_id2 + '_chr' + chromosome + '.png')


def pcorr(record_id1, record_id2):
    
    # reads the data list txt file
    f = open('microarray_data_list.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    alldata = [i.split('\t') for i in datalist]
    
    # find the experiment according to record_id1
    for i in alldata[1:]:
        if record_id1 == i[0]:
            name = '../share/arrays/' +i[1] + '/' + i[2]
            f = open(name, 'r')
            data = f.read().split('\n')
            f.close()
    array1 = [i.split('\t') for i in data]
    
    # find the experiment according to record_id2
    for i in alldata[1:]:
        if record_id2 == i[0]:
            name = '../share/arrays/' +i[1] + '/' + i[2]
            f = open(name, 'r')
            data = f.read().split('\n')
            f.close()
    array2 = [i.split('\t') for i in data]                
    
    # calculate pearson correlation coefficient
    y1 = [i[3] for i in array1[1:-1]]
    y2 = [i[3] for i in array2[1:-1]]
    a=[]
    b=[]
    for i in range(len(y1)):
        if y1[i]!= 'NA' and y2[i]!='NA':
            a.append(float(y1[i]))
            b.append(float(y2[i]))
    p = stats.pearsonr(a,b)[0]
                    
    # return pearson correlation coeffcient
    return str(p)


# single coverage plot
def coverage_plot1(record_id):
    
    # reads the data list txt file
    f = open('microarray_data_list.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    alldata = [i.split('\t') for i in datalist]
    
    # find the experiment according to record_id
    for i in alldata[1:]:
        if record_id == i[0]:
            name = '../share/arrays/' + i[1] + '/' + i[2]
            f = open(name, 'r')
            data = f.read().split('\n')
            f.close()
    array = [i.split('\t') for i in data]
    
    # chromosome length
    chr_len = [230218, 813184, 316620, 1531933, 576874, 270161, 1090940, 562643, 439888, 745751, 666816, 1078177, 924431, 784333, 1091291, 948066]
    
    # calculate the coverage
    cov = []
    for k in range(16):
        data_chr = [i for i in array[2:] if i[0]==str(k+1)]
        #cov.append(2**((sum([float(i[3]) for i in data_chr if i[3]!='NA'])/(float(chr_len[k])/1000))))
        #cov.append(2**(np.mean([(float(i[3])) for i in data_chr if i[3]!='NA'])))
        cov.append(np.mean([2**(float(i[3])) for i in data_chr if i[3]!='NA']))
        #cov.append(2**((sum([float(i[3]) for i in data_chr if i[3]!='NA'])/(float(data_chr[-1][1])/1000))))
        
    # sort by chromosome length
    chrs = {230218:1, 813184:2, 316620:3, 1531933:4, 576874:5, 270161:6, 1090940:7, 562643:8, 439888:9, 745751:10, 666816:11, 1078177:12, 924431:13, 784333:14, 1091291:15, 948066:16}
    chrs_sort = sorted(chrs)
    labels = [chrs[i] for i in chrs_sort]
    cov_sort = [cov[i-1] for i in labels]
    
    # barplot
    cmap = mpl.cm.autumn
    colors=[]
    for i in range(1,17):
        colors.append(cmap(float(i)/16))
    plt.bar(np.arange(16)+0.6, cov_sort, color=colors)
    plt.xticks(np.arange(16)+1, labels)
    plt.ylabel('Average Signal Per Kb')
    plt.xlabel('Chrs Sorted by Length')
    plt.title('Barplot of Record ' + record_id)
    plt.ylim((0,max(cov)+0.2))
    plt.tight_layout()    
    
    # save the plot
    plotname = '../Documents/plots/'+ record_id + '_bar' + '.png'
    f = open(plotname, 'wb')
    plt.savefig(plotname, orig_size=(1500,1300))
    f.close()
    
    # change the mode so it can be accessed by server
    os.chmod(plotname,0755)
    
    # return plotname
    return record_id + '_bar' + '.png'
    
    
        
    
# pairwise coverage plot
def coverage_plot2(record_id1, record_id2):
    
    # reads the data list txt file
    f = open('microarray_data_list.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    alldata = [i.split('\t') for i in datalist]
    
    # find the experiment according to record_id1
    for i in alldata[1:]:
        if record_id1 == i[0]:
            name = '../share/arrays/' + i[1] + '/' + i[2]
            f = open(name, 'r')
            data = f.read().split('\n')
            f.close()
    array1 = [i.split('\t') for i in data]
    
    # find the experiment according to record_id2
    for i in alldata[1:]:
        if record_id2 == i[0]:
            name = '../share/arrays/' + i[1] + '/' + i[2]
            f = open(name, 'r')
            data = f.read().split('\n')
            f.close()
    array2 = [i.split('\t') for i in data]
        
    # chromosome length
    chr_len = [230218, 813184, 316620, 1531933, 576874, 270161, 1090940, 562643, 439888, 745751, 666816, 1078177, 924431, 784333, 1091291, 948066]
    
    # calculate the coverage of array1
    cov1 = []
    for k in range(16):
        data_chr1 = [i for i in array1[2:] if i[0]==str(k+1)]
        #cov1.append(2**((sum([float(i[3]) for i in data_chr1 if i[3]!='NA'])/(float(chr_len[k])/1000))))
        #cov1.append(2**((sum([float(i[3]) for i in data_chr1 if i[3]!='NA'])/(float(data_chr1[-1][1])/1000))))
        cov1.append(np.mean([2**(float(i[3])) for i in data_chr1 if i[3]!='NA']))
    
    # calculate the coverage of array2
    cov2 = []
    for k in range(16):
        data_chr2 = [i for i in array2[2:] if i[0]==str(k+1)]
        #cov2.append(2**((sum([float(i[3]) for i in data_chr2 if i[3]!='NA'])/(float(chr_len[k])/1000))))
        #cov2.append(2**((sum([float(i[3]) for i in data_chr2 if i[3]!='NA'])/(float(data_chr2[-1][1])/1000))))
        cov2.append(np.mean([2**(float(i[3])) for i in data_chr2 if i[3]!='NA']))
    
    
    # sort by chromosome length
    chrs = {230218:1, 813184:2, 316620:3, 1531933:4, 576874:5, 270161:6, 1090940:7, 562643:8, 439888:9, 745751:10, 666816:11, 1078177:12, 924431:13, 784333:14, 1091291:15, 948066:16}
    chrs_sort = sorted(chrs)
    labels = [chrs[i] for i in chrs_sort]
    cov_sort1 = [cov1[i-1] for i in labels]
    cov_sort2 = [cov2[i-1] for i in labels]
    
    # barplot  
    cmap1 = mpl.cm.autumn
    cmap2 = mpl.cm.summer
    colors1=[]
    for i in range(1,17):
        colors1.append(cmap1(float(i)/16))
    colors2=[]
    for i in range(1,17):
        colors2.append(cmap2(float(i)/16))
    
    opacity=0.4
    bar_width=0.45
    plt.bar(np.arange(16)+0.5, cov_sort1, bar_width, alpha=opacity, color='b', label=record_id1)
    plt.bar(np.arange(16)+bar_width+0.5, cov_sort2, bar_width, alpha=opacity, color='r', label=record_id2)
    plt.xticks(np.arange(16)+1, labels)
    plt.ylabel('Average Signal Per Kb')
    plt.xlabel('Chrs Sorted by Length')
    plt.title('Barplot of Record ' + record_id1 + ' vs Record ' + record_id2)
    plt.ylim((0,max(cov1+cov2)+0.3))
    plt.legend()
    plt.tight_layout()
    
    # save the plot
    plotname = '../Documents/plots/'+ record_id1 +'_'+record_id2 + '_bar' + '.png'
    f = open(plotname, 'wb')
    plt.savefig(plotname, orig_size=(1500,1300))
    f.close()
    
    # change the mode so it can be accessed by server
    os.chmod(plotname,0755)
    
    # return plotname
    return record_id1 +'_'+record_id2 + '_bar' + '.png'
    
    
    
# single Telomere distance plot
def tel_plot1(record_id):
    
    # reads the data list txt file
    f = open('microarray_data_list.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    alldata = [i.split('\t') for i in datalist]
    
    # find the experiment according to record_id
    for i in alldata[1:]:
        if record_id == i[0]:
            name = '../share/arrays/' + i[1] + '/' + i[2]
            f = open(name, 'r')
            data = f.read().split('\n')
            f.close()
    array = [i.split('\t') for i in data][2:-1]
    
    # making a list with chr, start and signal
    signals = [[int(i[0]), int(i[1]), float(i[3])] for i in array if i[3]!='NA']
    
    # chromosome length
    chr_len = [230218, 813184, 316620, 1531933, 576874, 270161, 1090940, 562643, 439888, 745751, 666816, 1078177, 924431, 784333, 1091291, 948066]    
    
    # calculate the distance to telomeres
    dist = []
    for k in range(16):
        chr_half = chr_len[k]/2
        data_chr = [i for i in signals if i[0]==(k+1)]
        for i in data_chr:
            if i[1] <= chr_half:
                dist.append([i[0], i[1], i[2]])
            else:
                dist.append([i[0], chr_len[k]-i[1], i[2]])
                    
    # sort by distance
    plot_x = [i[1] for i in dist]
    plot_y = [i[2] for i in dist]
    index = [i[0] for i in sorted(enumerate(plot_x), key=lambda x:x[1])]    
    x_sort = [plot_x[i] for i in index]
    y_sort = [plot_y[i] for i in index]
    
    # smooth by 20
    n=len(x_sort)/20
    x_sort_sm=[]
    for i in range(n):
        x_sort_sm.append(np.mean(x_sort[20*i:(20*i+20)])/1000)
    
    y_sort_sm=[]
    for i in range(n):
        y_sort_sm.append(np.mean(y_sort[20*i:(20*i+20)]))
    
    # plot
    plt.plot(x_sort_sm, y_sort_sm)
    plt.ylabel('Log2 Signals')
    plt.xlabel('Distance from Telomere (kb)')
    plt.title('Telomere Plot of Record ' + record_id)
    plt.xlim((0,800))
    plt.hlines(0,0,800)
    plt.grid(True)
    plt.tight_layout()
    
    # save the plot
    plotname = '../Documents/plots/'+ record_id + '_telomere' + '.png'
    f = open(plotname, 'wb')
    plt.savefig(plotname, orig_size=(1500,1300))
    f.close()
    
    # change the mode so it can be accessed by server
    os.chmod(plotname,0755)
    
    # return plotname
    return record_id + '_telomere' + '.png'
    
    


# pairwise Telomere distance plot
def tel_plot2(record_id1, record_id2):
    
    # reads the data list txt file
    f = open('microarray_data_list.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    alldata = [i.split('\t') for i in datalist]
    
    # find the experiment according to record_id1
    for i in alldata[1:]:
        if record_id1 == i[0]:
            name = '../share/arrays/' + i[1] + '/' + i[2]
            f = open(name, 'r')
            data = f.read().split('\n')
            f.close()
    array1 = [i.split('\t') for i in data][2:-1]
    
    # find the experiment according to record_id2
    for i in alldata[1:]:
        if record_id2 == i[0]:
            name = '../share/arrays/' + i[1] + '/' + i[2]
            f = open(name, 'r')
            data = f.read().split('\n')
            f.close()
    array2 = [i.split('\t') for i in data][2:-1]
    
    # making a list with chr, start and signal
    signals1 = [[int(i[0]), int(i[1]), float(i[3])] for i in array1 if i[3]!='NA']
    signals2 = [[int(i[0]), int(i[1]), float(i[3])] for i in array2 if i[3]!='NA']
    
    # chromosome length
    chr_len = [230218, 813184, 316620, 1531933, 576874, 270161, 1090940, 562643, 439888, 745751, 666816, 1078177, 924431, 784333, 1091291, 948066]    
    
    # calculate the distance to telomeres
    dist1 = []
    for k in range(16):
        chr_half = chr_len[k]/2
        data_chr = [i for i in signals1 if i[0]==(k+1)]
        for i in data_chr:
            if i[1] <= chr_half:
                dist1.append([i[0], i[1], i[2]])
            else:
                dist1.append([i[0], chr_len[k]-i[1], i[2]])
                
    dist2 = []
    for k in range(16):
        chr_half = chr_len[k]/2
        data_chr = [i for i in signals2 if i[0]==(k+1)]
        for i in data_chr:
            if i[1] <= chr_half:
                dist2.append([i[0], i[1], i[2]])
            else:
                dist2.append([i[0], chr_len[k]-i[1], i[2]])
                    
    # sort by distance
    plot_x1 = [i[1] for i in dist1]
    plot_y1 = [i[2] for i in dist1]
    index1 = [i[0] for i in sorted(enumerate(plot_x1), key=lambda x:x[1])]    
    x_sort1 = [plot_x1[i] for i in index1]
    y_sort1 = [plot_y1[i] for i in index1]
    
    plot_x2 = [i[1] for i in dist2]
    plot_y2 = [i[2] for i in dist2]
    index2 = [i[0] for i in sorted(enumerate(plot_x2), key=lambda x:x[1])]    
    x_sort2 = [plot_x2[i] for i in index2]
    y_sort2 = [plot_y2[i] for i in index2]
    
    # smooth by 20
    n=len(x_sort1)/20
    x_sort_sm1=[]
    for i in range(n):
        x_sort_sm1.append(np.mean(x_sort1[20*i:(20*i+20)])/1000)
    
    y_sort_sm1=[]
    for i in range(n):
        y_sort_sm1.append(np.mean(y_sort1[20*i:(20*i+20)]))
        
    n=len(x_sort2)/20
    x_sort_sm2=[]
    for i in range(n):
        x_sort_sm2.append(np.mean(x_sort2[20*i:(20*i+20)])/1000)
    
    y_sort_sm2=[]
    for i in range(n):
        y_sort_sm2.append(np.mean(y_sort2[20*i:(20*i+20)]))
    
    # plot
    plt.subplots_adjust(wspace=0.5)

    # upper plot
    plt.subplot(211)
    plt.plot(x_sort_sm1, y_sort_sm1)
    plt.ylabel('Log2 Signals of Record '+record_id1)
    plt.xlabel('Distance from Telomere (kb)')
    plt.grid(True)
    plt.xlim((0,800))
    plt.hlines(0,0,800)
    
    # bottom plot
    plt.subplot(212)
    plt.plot(x_sort_sm2, y_sort_sm2, color='r')
    plt.ylabel('Log2 Signals of Record '+record_id2)
    plt.xlabel('Distance from Telomere (kb)')
    plt.grid(True)
    plt.xlim((0,800))
    plt.hlines(0,0,800)
    
    
    # save the plot
    plotname = '../Documents/plots/'+ record_id1 + '_' + record_id2 + '_telomere' + '.png'
    f = open(plotname, 'wb')
    plt.savefig(plotname, orig_size=(1500,1300))
    f.close()
    
    # change the mode so it can be accessed by server
    os.chmod(plotname,0755)
    
    # return plotname
    return record_id1 + '_' + record_id2 + '_telomere' + '.png'
    
    
    
    
    
# print gene list
def gene_list(chromosome, start=None, end=None):
        
    # reads the SGD_feature file
    f = open('SGD_feature.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    alldata = [i.split('\t') for i in datalist]
    
    # specify a chromosome
    chromosome = int(chromosome)
    data_chr = [i for i in alldata[1:] if int(i[1])==chromosome]
    
    # specify a region
    if start:
        start = int(start)
    else:
        start = 0
    
    if end:
        end = int(end)
    else:
        end = max([int(i[4]) for i in data_chr])
        
    # extract the genes within this region
    genes = [i for i in data_chr if min(int(i[3]), int(i[4]))>=start and max(int(i[3]), int(i[4]))<=end]
    
    return genes
    
        

# single normalized gene plot 
def norm_gene1(record_id):
    
    # reads the SGD_feature file
    f = open('SGD_feature.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    genes_all = [i.split('\t') for i in datalist][1:]
    genes = [[int(i[1]), int(i[3]), int(i[4]), i[5]] for i in genes_all]
    
    # reads the data list txt file
    f = open('microarray_data_list.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    alldata = [i.split('\t') for i in datalist]
    
    # find the experiment according to record_id
    for i in alldata[1:]:
        if record_id == i[0]:
            name = '../share/arrays/' +i[1] + '/' + i[2]
            f = open(name, 'r')
            data = f.read().split('\n')
            f.close()
    array = [i.split('\t') for i in data][1:-1]
    
    # 650bp on either side of watson
    regions_w = []
    regions_c = []
    for i in genes:
        if (i[3]=='W' and i[1]>=5000):
            regions_w.append([i[0], i[1]-650, i[2]+650, 2000/(float(i[2]-i[1])+1300)])
        if (i[3]=='C' and i[1]>=5000):
            regions_c.append([i[0], i[2]-650, i[1]+650, 2000/(float(i[1]-i[2])+1300)])

    # normalize    
    # index file of w
    #index_w=[]
    #for gene in regions_w:
        #print gene
        #start = gene[1]
        #end = gene[2]
        #index_w.append([i for i in range(len(array)) if int(array[i][0])==gene[0] and int(array[i][1]) >= start and int(array[i][1]) <= end])
        
    # index file of c
    #index_c=[]
    #for gene in regions_c:
        #print gene
        #start = gene[1]
        #end = gene[2]
        #index_c.append([i for i in range(len(array)) if int(array[i][0])==gene[0] and int(array[i][1]) >= start and int(array[i][1]) <= end])
        
    # write index_w
    #f=open('index_w.txt','w')
    #output=[]
    #for line in index_w:
        #tmp = [str(i) for i in line]
        #output.append('\t'.join(i for i in tmp))
    #f.write('\r'.join(i for i in output))
    #f.close()
    
    # write index_c
    #f=open('index_c.txt','w')
    #output=[]    
    #for line in index_c:
        #tmp = [str(i) for i in line]
        #output.append('\t'.join(i for i in tmp))
    #f.write('\r'.join(i for i in output))
    #f.close()
    
    # reads the index files
    f = open('index_w.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    index_w = [i.split('\t') for i in datalist]
    
    f = open('index_c.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    index_c = [i.split('\t') for i in datalist]
    
    # start normalizing w
    norm_list_w = []
    n=-1
    for i in index_w:
        n+=1
        if i!=['']:
            array_gene = array[int(i[0]):int(i[-1])+1]
            norm_list_w.append([[int(j[0]), (int(j[1])-regions_w[n][1])*regions_w[n][3], float(j[3])] for j in array_gene if j[3]!='NA'])
            
    # start normalizing c
    norm_list_c = []
    n=-1
    for i in index_c:
        n+=1
        if i!=['']:
            array_gene = array[int(i[-1]):int(i[0])-1:-1]
            norm_list_c.append([[int(j[0]), (regions_c[n][2]-int(j[1]))*regions_c[n][3], float(j[3])] for j in array_gene if j[3]!='NA'])
    
    # combine all data into a list
    norm_all = []
    for i in norm_list_w:
        for j in i:
            norm_all.append(j)
    for i in norm_list_c:
        for j in i:
            norm_all.append(j)
            
    # order by positions
    pos_chr = [j[1] for j in norm_all]
    sigs = [j[2] for j in norm_all]
    index1 = [i[0] for i in sorted(enumerate(pos_chr), key=lambda x:x[1])]
    norm_all_sort = [[pos_chr[i], sigs[i]] for i in index1]
    x_sort=[i[0] for i in norm_all_sort]
    y_sort=[2**(i[1]) for i in norm_all_sort]
    
    # smooth by 50
    n=len(x_sort)/50
    x_sort_sm=[]
    for i in range(n):
        x_sort_sm.append(np.mean(x_sort[50*i:(50*i+50)]))
    
    y_sort_sm=[]
    for i in range(n):
        y_sort_sm.append(np.mean(y_sort[50*i:(50*i+50)]))    
    
    # plot   
    plt.plot(x_sort_sm, y_sort_sm)
    plt.xlabel('Normalized Gene (+650bp up/downsteam) (bp)')
    plt.ylabel('Singals of Record ' + record_id)
    plt.grid(True)
    
    # save the plot
    plotname = '../Documents/plots/'+ record_id + '_norm_gene' + '.png'
    f = open(plotname, 'wb')
    plt.savefig(plotname, orig_size=(1500,1300))
    f.close()
    
    # change the mode so it can be accessed by server
    os.chmod(plotname,0755)
    
    # return plotname
    return record_id + '_norm_gene' + '.png'
    
            


# single normalized gene plot 
def norm_gene2(record_id1, record_id2):
    
    # reads the SGD_feature file
    f = open('SGD_feature.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    genes_all = [i.split('\t') for i in datalist][1:]
    genes = [[int(i[1]), int(i[3]), int(i[4]), i[5]] for i in genes_all]
    
    # reads the data list txt file
    f = open('microarray_data_list.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    alldata = [i.split('\t') for i in datalist]
    
    # find the experiment according to record_id1
    for i in alldata[1:]:
        if record_id1 == i[0]:
            name = '../share/arrays/' +i[1] + '/' + i[2]
            f = open(name, 'r')
            data = f.read().split('\n')
            f.close()
    array1 = [i.split('\t') for i in data][1:-1]
    
    # find the experiment according to record_id2
    for i in alldata[1:]:
        if record_id2 == i[0]:
            name = '../share/arrays/' +i[1] + '/' + i[2]
            f = open(name, 'r')
            data = f.read().split('\n')
            f.close()
    array2 = [i.split('\t') for i in data][1:-1]
    
    # 650bp on either side of watson
    regions_w = []
    regions_c = []
    for i in genes:
        if (i[3]=='W' and i[1]>=5000):
            regions_w.append([i[0], i[1]-650, i[2]+650, 2000/(float(i[2]-i[1])+1300)])
        if (i[3]=='C' and i[1]>=5000):
            regions_c.append([i[0], i[2]-650, i[1]+650, 2000/(float(i[1]-i[2])+1300)])

    # normalize    
    # index file of w
    #index_w=[]
    #for gene in regions_w:
        #print gene
        #start = gene[1]
        #end = gene[2]
        #index_w.append([i for i in range(len(array)) if int(array[i][0])==gene[0] and int(array[i][1]) >= start and int(array[i][1]) <= end])
        
    # index file of c
    #index_c=[]
    #for gene in regions_c:
        #print gene
        #start = gene[1]
        #end = gene[2]
        #index_c.append([i for i in range(len(array)) if int(array[i][0])==gene[0] and int(array[i][1]) >= start and int(array[i][1]) <= end])
        
    # write index_w
    #f=open('index_w.txt','w')
    #output=[]
    #for line in index_w:
        #tmp = [str(i) for i in line]
        #output.append('\t'.join(i for i in tmp))
    #f.write('\r'.join(i for i in output))
    #f.close()
    
    # write index_c
    #f=open('index_c.txt','w')
    #output=[]    
    #for line in index_c:
        #tmp = [str(i) for i in line]
        #output.append('\t'.join(i for i in tmp))
    #f.write('\r'.join(i for i in output))
    #f.close()
    
    # reads the index files
    f = open('index_w.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    index_w = [i.split('\t') for i in datalist]
    
    f = open('index_c.txt', 'r')
    datalist = f.read().split('\r')
    f.close()
    index_c = [i.split('\t') for i in datalist]
    
    # start normalizing w1
    norm_list_w1 = []
    n=-1
    for i in index_w:
        n+=1
        if i!=['']:
            array_gene = array1[int(i[0]):int(i[-1])+1]
            norm_list_w1.append([[int(j[0]), (int(j[1])-regions_w[n][1])*regions_w[n][3], float(j[3])] for j in array_gene if j[3]!='NA'])
            
    # start normalizing c1
    norm_list_c1 = []
    n=-1
    for i in index_c:
        n+=1
        if i!=['']:
            array_gene = array1[int(i[-1]):int(i[0])-1:-1]
            norm_list_c1.append([[int(j[0]), (regions_c[n][2]-int(j[1]))*regions_c[n][3], float(j[3])] for j in array_gene if j[3]!='NA'])
    
    # combine all data into a list1
    norm_all1 = []
    for i in norm_list_w1:
        for j in i:
            norm_all1.append(j)
    for i in norm_list_c1:
        for j in i:
            norm_all1.append(j)
            
    # start normalizing w2
    norm_list_w2 = []
    n=-1
    for i in index_w:
        n+=1
        if i!=['']:
            array_gene = array2[int(i[0]):int(i[-1])+1]
            norm_list_w2.append([[int(j[0]), (int(j[1])-regions_w[n][1])*regions_w[n][3], float(j[3])] for j in array_gene if j[3]!='NA'])
            
    # start normalizing c2
    norm_list_c2 = []
    n=-1
    for i in index_c:
        n+=1
        if i!=['']:
            array_gene = array2[int(i[-1]):int(i[0])-1:-1]
            norm_list_c2.append([[int(j[0]), (regions_c[n][2]-int(j[1]))*regions_c[n][3], float(j[3])] for j in array_gene if j[3]!='NA'])
    
    # combine all data into a list2
    norm_all2 = []
    for i in norm_list_w2:
        for j in i:
            norm_all2.append(j)
    for i in norm_list_c2:
        for j in i:
            norm_all2.append(j)
            
    # order by positions 1
    pos_chr = [j[1] for j in norm_all1]
    sigs = [j[2] for j in norm_all1]
    index1 = [i[0] for i in sorted(enumerate(pos_chr), key=lambda x:x[1])]
    norm_all_sort = [[pos_chr[i], sigs[i]] for i in index1]
    x_sort1=[i[0] for i in norm_all_sort]
    y_sort1=[2**(i[1]) for i in norm_all_sort]
    
    # order by positions 2
    pos_chr = [j[1] for j in norm_all2]
    sigs = [j[2] for j in norm_all2]
    index1 = [i[0] for i in sorted(enumerate(pos_chr), key=lambda x:x[1])]
    norm_all_sort = [[pos_chr[i], sigs[i]] for i in index1]
    x_sort2=[i[0] for i in norm_all_sort]
    y_sort2=[2**(i[1]) for i in norm_all_sort]
    
    # smooth by 50 (1)
    n=len(x_sort1)/50
    x_sort_sm1=[]
    for i in range(n):
        x_sort_sm1.append(np.mean(x_sort1[50*i:(50*i+50)]))
    
    y_sort_sm1=[]
    for i in range(n):
        y_sort_sm1.append(np.mean(y_sort1[50*i:(50*i+50)]))   
        
    # smooth by 50 (2)
    n=len(x_sort2)/50
    x_sort_sm2=[]
    for i in range(n):
        x_sort_sm2.append(np.mean(x_sort2[50*i:(50*i+50)]))
    
    y_sort_sm2=[]
    for i in range(n):
        y_sort_sm2.append(np.mean(y_sort2[50*i:(50*i+50)])) 
    
    # plot    
    plt.subplots_adjust(wspace=0.5)

    # upper plot
    plt.subplot(211)
    plt.plot(x_sort_sm1, y_sort_sm1)
    plt.xlabel('Normalized Gene (+650bp up/downsteam) (bp)')
    plt.ylabel('Singals of Record ' + record_id1)
    plt.grid(True)
    
    # plot 2
    plt.subplot(212)
    plt.plot(x_sort_sm2, y_sort_sm2, color='r')
    plt.xlabel('Normalized Gene (+650bp up/downsteam) (bp)')
    plt.ylabel('Singals of Record ' + record_id2)
    plt.grid(True)
    
    # save the plot
    plotname = '../Documents/plots/'+ record_id1 + '_' + record_id2 + '_norm_gene' + '.png'
    f = open(plotname, 'wb')
    plt.savefig(plotname, orig_size=(1500,1300))
    f.close()
    
    # change the mode so it can be accessed by server
    os.chmod(plotname,0755)
    
    # return plotname
    return record_id1 + '_' + record_id2 + '_norm_gene' + '.png'  
        
            
    
    











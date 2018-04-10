signalplot1 <- function(id, chr, start=NULL, end=NULL, range=NULL)
{
  datalist = read.delim('/Library/WebServer/CGI-Executables/microarray_data_list.txt')
  query = datalist[which(datalist[,1]==id),]
  name = paste('/Volumes/LabShare/Microarray_database/arrays', query[1,2], query[1,3], sep='/')
  data = read.table(name, header=T)
  data_chr = data[which(data[,1]==chr),]
  if (is.null(start)==TRUE)
  {
    start = 0/1000
  }
  if (is.null(end)==TRUE)
  {
    end = max(data_chr[,3])/1000
  }
  if (is.null(range)==TRUE)
  {
    pdf(file=paste(id, '_chr', chr, '.pdf', sep=""), width=10, height=8)
    plot(data_chr[,2]/1000, 2^(data_chr[,4]), type='b',
           xlab=paste('Chromosome',chr,' Position (kb)', sep=""), 
           ylab='Signal', frame.plot=F,pch=16, col='blue', xlim=c(start/1000, end/1000))
    dev.off()
  }
  if (is.null(range)==FALSE)
  {
    pdf(file=paste(id, '_chr', chr, '.pdf', sep=""), width=10, height=8)
    plot(data_chr[,2]/1000, 2^(data_chr[,4]), type='b',
         xlab=paste('Chromosome',chr,' Position (kb)', sep=""), 
         ylab='Signal', frame.plot=F,pch=16, col='blue', xlim=c(start/1000, end/1000), ylim=c(0,range))
    dev.off()
  }
}






# Python
# single linear plot     
robjects.r('''
        signalplot1 <- function(id, chr, start=NULL, end=NULL, range=NULL){
           datalist = read.delim('/Library/WebServer/CGI-Executables/microarray_data_list.txt')
           query = datalist[which(datalist[,1]==id),]
           name = paste('/Volumes/LabShare/Microarray_database/arrays', query[1,2], query[1,3], sep='/')
           data = read.table(name, header=T)
           data_chr = data[which(data[,1]==chr),]
           if (is.null(start)==TRUE)
{
           start = 0
}
           if (is.null(end)==TRUE)
{
           end = max(data_chr[,3])
}
           if (is.null(range)==TRUE)
{
           pdf(file=paste(id, '_chr', chr, '.pdf', sep=""), width=10, height=8)
           plot(data_chr[,2]/1000, 2^(data_chr[,4]), type='b',
           xlab=paste('Chromosome',chr,' Position (kb)', sep=""), 
           ylab='Signal', frame.plot=F,pch=16, col='blue', xlim=c(start/1000, end/1000))
           dev.off()
}
           if (is.null(range)==FALSE)
{
           pdf(file=paste(id, '_chr', chr, '.pdf', sep=""), width=10, height=8)
           plot(data_chr[,2]/1000, 2^(data_chr[,4]), type='b',
           xlab=paste('Chromosome',chr,' Position (kb)', sep=""), 
           ylab='Signal', frame.plot=F,pch=16, col='blue', xlim=c(start/1000, end/1000), ylim=c(0,range))
           dev.off()
}
        }
           ''')
r_signalplot1 = robjects.r['signalplot1']


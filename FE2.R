# function FE2.
FE2<-function(FileName, cy0, strain)
{
  library(marray) 
  plat<-read.table("SK1rosetta.txt", header=T, sep="\t")
  maData<-read.Agilent(fnames=FileName, name.Rf="rMeanSignal", name.Gf="gMeanSignal",
                       name.Rb="rBGMeanSignal", name.Gb="gBGMeanSignal", sep="\t")
  maNorm<-maNorm(maData,norm="printTipLoess")
  if (cy0==5)
  {
    lr<--maNorm@maM
  }
  if (cy0==3)
  {
    lr<-maNorm@maM
  }
  data<-as.data.frame(matrix(0,nrow=nrow(plat),ncol=4))
  data[,1]<-plat[,'chr']
  data[,2]<-plat[,'start']
  data[,3]<-plat[,'stop']
  data[,4]<-lr[,1]
  colnames(data)<-c('chr','start', 'end', "Log2Ratio")
  write.table(data,strain,col.names=T, row.names=F, quote=F, sep="\t")
  # save the signal data into a txt file in your working directory.
}
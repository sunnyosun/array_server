### Microarray database construction
## Sunny

################################################################################
# read in the excel file
data = read.delim('microarray_data_list.txt', stringsAsFactors=F)

# runs FE2
source('~/../../Volumes/LabShare/R_files/Microarray/Feature_Extraction/FE_S288C.R')
for (i in 453:455)
{
  print (i)
  folder=data[i,2]
  array=paste(data[i,3], '.txt', sep='')
  setwd(paste('~/../../Volumes/LabShare/Microarray_database/arrays', folder, sep="/"))
  if (length(grep('cy3', data[i,7], ignore.case=T))==1)
  {
    FE2(array, 3, data[i,3])
  }
  if (length(grep('cy5', data[i,7], ignore.case=T))==1)
  {
    FE2(array, 5, data[i,3])
  }
}




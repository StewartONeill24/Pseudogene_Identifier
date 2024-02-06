#!/bin/env Rscript
 
args <- commandArgs(TRUE)
#check for 1 arguments
   args_length <- length(args)
   if (args_length != 1){
      stop("Please input filename")
   }
my_file <- args[1]
 
my_title <- strsplit(my_file,".tsv")
real_title <- paste(my_title,".png", sep="")
 
#read data
data <- read.table(my_file, header=F, stringsAsFactors=F)
#dim(data)
png(real_title)
plot(data, type='l', main=my_title, xlab='Position along exon', ylab='Uniqueness metric')
#table(data$V2==1)
dev.off()
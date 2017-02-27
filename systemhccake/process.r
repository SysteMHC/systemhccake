#! /usr/bin/Rscript

args = commandArgs(trailingOnly=TRUE)

#args =c("1", "./Kowalewskid_160207_Rammensee_Germany_PBMC_Buffy18/NetMHC/netmhccons.output.tsvh", "Kowalewskid_160207_Rammensee_Germany_PBMC_Buffy18")

library(data.table)

#cleanedTable <- fread(input="~/prog/SysteMHC_Data/annotation/cleanedTable_id.csv")
#sysmhcid_all <- fread(input="~/prog/SysteMHC_Data/annotation/SYSMHCID_all.csv")
annotation_table <- fread(input="/mnt/Systemhc/Data/data_annotation.csvh")

#print(args[2])

#raw <- fread(input="./netmhccons.output.tsvh")
raw <- fread(input=args[2])
JobID <- args[3]



raw[raw$annotation_score < 3, ]$top_allele <- "unclassified"

index_allele <- which(grepl("HLA", names(raw)))
#raw[which(apply(raw[, index_allele, with=F], 1, function(x) length(which(x<500))) == 2), ]$top_allele <- "both_below_500"

index_both_below_500 <- which(apply(raw[, index_allele, with=F], 1, function(x) length(which(x<500))) > 1)
raw[index_both_below_500, ]$top_allele <- apply(raw[index_both_below_500, index_allele, with=F], 1, function(x) paste(names(raw)[index_allele][which(x < 500)], collapse=";"))


peptide <- raw[, .(spectral_counts = length(spectrum), length = nchar(search_hit)), by=c("search_hit", "assumed_charge", "protein_id", names(raw)[index_allele], "annotation_score", "top_allele")]
peptide_sorted <- peptide[order(peptide$annotation_score, decreasing=T), ]

peptide_sorted[, SysteMHC_ID := unique(annotation_table[annotation_table$SampleID==JobID, ]$ID)]
peptide_sorted[, SampleID := JobID]
peptide_sorted[, elution_event_ID := unique(annotation_table[annotation_table$SampleID==JobID, ]$IsolationMethod)]

#setcolorder(peptide_sorted, c("SysteMHC_ID", "SampleID", "elution_event_ID", "search_hit", "assumed_charge", "protein_id", "length", "spectral_counts", names(raw)[index_allele], "annotation_score", "top_allele"))

write.table(peptide_sorted, file=paste0(strsplit(args[2], "netmhc")[[1]][1], "final.tsv"), col.names=T, row.names=F, quote=F, sep="\t")

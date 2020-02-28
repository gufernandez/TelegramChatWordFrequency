#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

nArgs = length(args)
if (nArgs < 2) {
  stop("Please provide file name and words to search", call.=FALSE)
}

library.path <- .libPaths()
library("tm", lib.loc = library.path[1])
library("stringr", lib.loc = library.path[1])

words <- c()
for (i in seq_along(args)){
    if (i == 1) {
        inputFile = args[i]
    } else {
        words[i-1] = args[i]
    }
}

filePath <- paste("storage\\", inputFile, sep="")
fileText <- readLines(filePath, encoding="UTF-8")

corpusDoc <- Corpus(VectorSource(fileText))

toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
options(warn = 0)
suppressWarnings(corpusDoc <- tm_map(corpusDoc, toSpace, "/"))
suppressWarnings(corpusDoc <- tm_map(corpusDoc, toSpace, "@"))
suppressWarnings(corpusDoc <- tm_map(corpusDoc, toSpace, "\\|"))
suppressWarnings(corpusDoc <- tm_map(corpusDoc, removeNumbers))
suppressWarnings(corpusDoc <- tm_map(corpusDoc, removePunctuation))
suppressWarnings(corpusDoc <- tm_map(corpusDoc, stripWhitespace))

count <- c()
for (i in seq_along(words)) {
    suppressWarnings(result <- str_extract_all(corpusDoc, words[i]))
    count[i] = length(result[[1]])
}

df = data.frame(words, count)
head(df, nArgs-1)

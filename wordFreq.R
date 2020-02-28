#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

#wordFreq.R Rtest.R pathToFile mode language output

nArgs = length(args)
if (nArgs==0) {
  stop("File name not provided", call.=FALSE)
}

inputFile = args[1]

if (nArgs == 1) {
    mode = "normal"
    lang = "portuguese"
    outputFile <- substr(inputFile, 1, nchar(inputFile)-4)
} else if (nArgs == 2) {
    mode = args[2]
    lang = args[3]
    outputFile <- substr(inputFile, 1, nchar(inputFile)-4)
} else {
    mode = args[2]
    lang = args[3]
    outputFile = args[4]
}

if (mode != "normal" && mode != "raw" ) {
    stop("Select a valid mode (normal or raw)", call.=FALSE)
}

library.path <- .libPaths()
library("tm", lib.loc = library.path[1])

filePath <- paste("storage\\", inputFile, sep="")
fileText <- readLines(filePath, encoding="UTF-8")

corpusDoc <- Corpus(VectorSource(fileText))


if (mode == "normal") {
    toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))

    corpusDoc <- tm_map(corpusDoc, toSpace, "/")
    corpusDoc <- tm_map(corpusDoc, toSpace, "@")
    corpusDoc <- tm_map(corpusDoc, toSpace, "\\|")
    corpusDoc <- tm_map(corpusDoc, removeNumbers)
    corpusDoc <- tm_map(corpusDoc, removeWords, lang)
    corpusDoc <- tm_map(corpusDoc, removeWords, c("hrefhttps", "href", "https"))
    corpusDoc <- tm_map(corpusDoc, removePunctuation)
    corpusDoc <- tm_map(corpusDoc, stripWhitespace)
}

tdm <- TermDocumentMatrix(corpusDoc)
removeSparseTerms(tdm, .999)

m <- as.matrix(tdm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)

outputFile <- paste(outputFile, ".csv", sep="")
outputPath <- paste("storage\\", outputFile, sep="")
write.csv(d, outputPath, row.names = FALSE)

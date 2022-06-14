Get_Patterns<-function(TENS,BASIS, temp_folder_path){
  Patterns <- list()
  if (length(BASIS[[1]]) == 0){
    return(Patterns)
  }

  if(is.null(dim(BASIS[[1]]))){
    TENS_temp<-BASIS[[1]]
    for (i in 2:length(BASIS)) {
      TENS_temp<-TENS_temp%o%BASIS[[i]]
    }

    Patterns[[j]] <- array(as.numeric(TENS_temp>0),dim=dim(TENS_temp))
  }else{
    cat("Starting to extract", ncol(BASIS[[1]]),"patterns\n")
    TENS_compare<-0*TENS
    i <- 0
    for (j in 1:ncol(BASIS[[1]])) {
      cat("\r", j, "done")
      TENS_temp<-BASIS[[1]][,j]
      for (i in 2:length(BASIS)) {
        TENS_temp<-TENS_temp%o%BASIS[[i]][,j]
      }

      Pattern <- array(as.numeric(TENS_temp>0),dim=dim(TENS_temp))
      pattern_file_path = paste(temp_folder_path, "/pattern_",j)
      pattern_file_path = gsub(" ", "", pattern_file_path)
      np$save(pattern_file_path, Pattern)
    }
  }

  print("Finished")
}

library("reticulate")
np <- import("numpy")
temp_folder_path =  paste("../temp/patterns")
tensor <- np$load("../datasets/retweets-sparser-processed.npy")
factors <- readRDS("../temp/getf_factors.rds")
Patterns <- Get_Patterns(tensor, factors, temp_folder_path)

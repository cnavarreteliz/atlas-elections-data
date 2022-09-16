library(glue)
library(tibble)
library(dplyr)
library(kableExtra)


nls_extract_params <- function(model) {
  res <- coef(summary(model))[]
  parameters <- as.data.frame(res)[]
  residual <- sum(resid(model)^2)
  
  return(list(parameters, residual))
}


nlstargazer <- function(models, digits = 4) {
  N <- length(models)
  items <- seq(1, N, by=1)
  
  it_models <- list()
  residuals <- c("Residual sum-of-squares")
  for(model in models){
    ret <- nls_extract_params(model = model)
    it_models <- append(it_models, list(ret[[1]]))
    residuals <- append(residuals, list(round(ret[[2]], digits = 2)))
  }
  
  # print(it_models)
  
  get_p_values <- function(x) {
    if (x < 0.01) {
      return("***");
    }
    else if (x < 0.05) {
      return("**");
    }
    else if (x < 0.1) {
      return("*");
    }
    return("")
  }
  
  tmp <- list()
  i <- 1
  for(model in it_models){
    model_label <- paste("model", i, sep = ".")
    std_label   <- paste("std_err", i, sep = ".")
    t_label     <- paste("t_value", i, sep = ".")
    pval_label  <- paste("p_value", i, sep = ".")
    nm_label    <- paste("row.names", i, sep = ".")
    asd_label   <- paste("pval", i, sep = ".")
    
    model <- tibble::rownames_to_column(model, nm_label)
    model$pvalue <- sapply(model[["Pr(>|t|)"]], FUN = get_p_values)
    
    model <- rename(model, 
                    "{model_label}" := Estimate,
                    "{std_label}" := "Std. Error",
                    "{t_label}" := "t value",
                    "{pval_label}" := "Pr(>|t|)",
                    "{asd_label}" := pvalue
                    
    )
    tmp <- append(tmp, list(model))
    i <- i + 1
  }
  
  df <- data.frame()
  for(item in items){
    if (item == 1) {
      df <- as.data.frame(tmp[1])
    }
    else {
      df <- merge(
        df,
        as.data.frame(tmp[item]),
        by.x=paste("row.names", 1, sep="."),
        by.y=paste("row.names", item, sep="."),
        all=TRUE
      )    
    }
  }
  
  df_output <- data.frame(matrix(ncol = N + 1, nrow = 0))
  cnames <- c("Parameters")
  for (itm in items) {
    cnames <- append(cnames, paste("Model", itm, sep="."))
  }
  colnames(df_output) <- cnames
  
  for(i in 1:nrow(df)) {
    row <- df[i,]
    parameter <- row[["row.names.1"]]
    new_row <- c(parameter)
    for(item in items) {
      coef  <- row[[paste("model", item, sep = ".")]]
      sd    <- row[[paste("std", item, sep = ".")]]
      pval  <- row[[paste("pval", item, sep = ".")]]
      
      cell    <- round(coef, digits = digits)
      cell    <- paste(format(cell, nsmall = digits), pval, sep="")
      # vv <- paste(vv, "(test)", sep="\n") TODO
      
      cell <- if(is.na(pval[1])) "" else cell
      new_row <- append(new_row, cell)
    }
    df_output[nrow(df_output) + 1,] <- new_row
    
  }
  
  df_output[nrow(df_output) + 1,] <- residuals
  
  df_output %>%
    kbl(caption = "Summary") %>%
    kable_classic_2(full_width = T, html_font = "Cambria")
}


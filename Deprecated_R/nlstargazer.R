library(glue)
library(tibble)
library(dplyr)
library(kableExtra)
library(knitr)

nls_extract_params <- function(model) {
  res <- coef(summary(model))[]
  parameters <- as.data.frame(res)[]
  residual <- sum(resid(model)^2)
  nobs <- summary(model)[]$nobs[1][["nobs.full"]]
  deviance <- summary(model)[]$deviance[[1]]
  adjrsquared <- summary(model)[]["P.adj.r.squared"][[1]]
  print(adjrsquared)

  return(list(parameters, residual, nobs, deviance, adjrsquared))
}


nlstargazer <- function(models, digits = 4, sort_parameters = c(), rename_parameters = c()) {
  N <- length(models)
  items <- seq(1, N, by = 1)

  it_models <- list()
  residuals <- c("Residual sum-of-squares")
  deviance_row <- c("Deviance")
  null.deviance_row <- c("Null Deviance")
  nobs_row <- c("Observations")
  fstat_row <- c("F-stat")
  rsquared_row <- c("P.r.squared")
  adj_rsquared_row <- c("P.adj.r.squared")

  # pseudo.rsquared_row <- c("Pseudo R2")
  for (model in models) {
    ret <- nls_extract_params(model = model)
    it_models <- append(it_models, list(ret[[1]]))
    residuals <- append(residuals, list(round(ret[[2]], digits = 2)))
    nobs_row <- append(nobs_row, list(ret[[3]]))
    deviance_row <- append(deviance_row, list(round(ret[[4]], digits = 2)))
    adj_rsquared_row <- append(adj_rsquared_row, list(round(ret[[5]], digits = 2)))
    # null.deviance_row <- append(null.deviance_row, list(round(ret[[5]], digits = 2)))
    # pseudo.rsquared_row <- append(pseudo.rsquared_row, list(round(1 - ret[[4]] / ret[[5]], digits = 2)))
  }

  # print(it_models)

  get_p_values <- function(x) {
    if (x < 0.01) {
      return("***")
    } else if (x < 0.05) {
      return("**")
    } else if (x < 0.1) {
      return("*")
    }
    return("")
  }

  tmp <- list()
  i <- 1
  for (model in it_models) {
    model_label <- paste("model", i, sep = ".")
    std_label <- paste("std_err", i, sep = ".")
    t_label <- paste("t_value", i, sep = ".")
    pval_label <- paste("p_value", i, sep = ".")
    nm_label <- paste("row.names", i, sep = ".")
    asd_label <- paste("pval", i, sep = ".")

    model <- tibble::rownames_to_column(model, nm_label)
    pvalue_column <- "Pr(> |z|)" # Pr(> |z|) Pr(>|t|)
    std_column <- "Std. error" # Std. Error
    value_column <- "z value" # "t value"
    model$pvalue <- sapply(model[[pvalue_column]], FUN = get_p_values)

    model <- rename(
      model,
      "{model_label}" := Estimate,
      "{std_label}" := std_column,
      "{t_label}" := value_column,
      "{pval_label}" := pvalue_column, # Pr(> |z|) Pr(>|t|)
      "{asd_label}" := pvalue
    )
    tmp <- append(tmp, list(model))
    i <- i + 1
  }

  df <- data.frame()
  for (item in items) {
    if (item == 1) {
      df <- as.data.frame(tmp[1])
    } else {
      df <- merge(
        df,
        as.data.frame(tmp[item]),
        by.x = paste("row.names", 1, sep = "."),
        by.y = paste("row.names", item, sep = "."),
        all = TRUE
      )
    }
  }

  df_output <- data.frame(matrix(ncol = N + 1, nrow = 0))
  cnames <- c("Parameters")
  for (itm in items) {
    cnames <- append(cnames, paste("Model", itm, sep = " "))
  }
  colnames(df_output) <- cnames

  if (length(sort_parameters) > 0) {
    df <- df[match(sort_parameters, df$row.names.1), ]
  }

  if (length(rename_parameters) > 0) {
    for (item in rename_parameters) {
      df$row.names.1[df$row.names.1 == item[[1]]] <- item[[2]]
    }
  }

  for (i in 1:nrow(df)) {
    row <- df[i, ]
    parameter <- row[["row.names.1"]]
    new_row <- c(parameter)
    new_row2 <- c("")
    for (item in items) {
      coef <- row[[paste("model", item, sep = ".")]]
      sd <- row[[paste("std_err", item, sep = ".")]] # std
      pval <- row[[paste("pval", item, sep = ".")]]

      cell <- round(coef, digits = digits)
      cell <- paste(format(cell, nsmall = digits), pval, sep = "")

      cell <- if (is.na(pval[1])) "" else cell
      new_row <- append(new_row, cell)

      # print(row)
      cell2 <- if (is.null(sd)) NULL else round(sd, digits = digits)
      cell2 <- if (is.na(cell2)) "" else glue("({cell2})")
      new_row2 <- append(new_row2, cell2)
    }
    df_output[nrow(df_output) + 1, ] <- new_row
    df_output[nrow(df_output) + 1, ] <- new_row2
  }

  # df_output[nrow(df_output) + 1,] <- residuals
  df_output[nrow(df_output) + 1, ] <- nobs_row
  df_output[nrow(df_output) + 1, ] <- deviance_row
  df_output[nrow(df_output) + 1, ] <- adj_rsquared_row


  row.names(df_output) <- NULL

  return(df_output)
}

library(plotly)
# Load the package required to read JSON files.
library("rjson")


draw_sankey <- function(data, candidates, runoff_candidates) {
  source <- c()
  target <- c()
  value <- c()
  
  idx_candidate_a <- length(candidates) + 0
  idx_candidate_b <- length(candidates) + 1
  
  for(i in 1:nrow(data)) {
    row <- data[i, ]
    candidate <- row[["candidate"]]
    idx <- which(candidates == candidate)[1] - 1

    
    if (!(is.na(row[["coef"]]))) {
      source <- append(source, idx)
      target <- append(target, idx_candidate_a) # BORIC
      value <- append(value, row[["to_candidate_b"]] * 100)
      
      source <- append(source, idx)
      target <- append(target, idx_candidate_b) # KAST
      value <- append(value, row[["to_candidate_a"]] * 100)
    }
    
    else if (candidate[] == runoff_candidates[[1]]) {
      print("HIHIHI")
      source <- append(source, idx)
      target <- append(target, idx_candidate_a) # BORIC
      value <- append(value, row[["rate"]] * 100)
      
      source <- append(source, idx)
      target <- append(target, idx_candidate_b) # KAST
      value <- append(value, 0)
    }
    
  }
  
  # Give the input file name to the function.
  colors <- fromJSON(file="consts.json")
  # Print the result.

  label <- c(candidates, runoff_candidates)
  color_label <- c()
  
  for (x in label) {
    color_label <- append(color_label, colors[[x]])
  }
  

  fig <- plot_ly(
    type = "sankey",
    orientation = "h",
    
    node = list(
      label = label,
      color = color_label,
      pad = 15,
      thickness = 20,
      line = list(
        color = "black",
        width = 0
      )
    ),
    
    link = list(
      source = source,
      target = target,
      value =  value,
      color = "#ebebeb"
    )
  )
  fig <- fig %>% layout(
    title = "",
    font = list(
      size = 16
    )
  )
  
  fig
  
}
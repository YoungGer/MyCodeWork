library(shiny)

# Define UI for application that draws a histogram
shinyUI(fluidPage(
    
    # Application title
    titlePanel("Partial Discharge Demo"),
    
    # Sidebar with a slider input for the number of bins
    sidebarLayout(
        sidebarPanel(
        selectInput("dataset", "Choose a dataset:", choices = c("c2", "c3")), #挑选C2或者C3数据
        
        checkboxGroupInput("pdtypes", label = h3("PD Type"),         #选择放电的类别
            choices = list("Type 1" = 1, "Type 2" = 2, "Type 3" = 3,"Type 4" = 4,"Type 5" = 5),
            selected = 1),
        hr(),
        fluidRow(column(3, verbatimTextOutput("debug")))
        ),
    
        # Show a plot of the generated distribution
        mainPanel(
            tabsetPanel(type = "tabs", 
                tabPanel("Time Plot", plotOutput("plot1",brush = brushOpts(id = "plot1_brush",resetOnNew = TRUE)),
                             plotOutput("plot2")), 
                tabPanel("TW Plot", plotOutput("plot3",brush = brushOpts(id = "plot3_brush",resetOnNew = TRUE)),
                         plotOutput("plot4")), 
                tabPanel("Summary", verbatimTextOutput("summary")), 
                tabPanel("Table", tableOutput("table")))
        )
    )
))


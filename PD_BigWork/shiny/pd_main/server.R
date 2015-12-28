library(shiny)

# Define server logic required to draw a histogram
shinyServer(function(input, output) {
    
    #控制输入数据选择
    datasetInput <- reactive({
        switch(input$dataset,
               "c2" = c2,
               "c3" = c3)
    })
    
    #Debug
    output$debug <- renderPrint({ input$pdtypes })
    
    #产生图像
    ranges <- reactiveValues(x = NULL, y = NULL) #控制显示的范围
    
    
    output$plot1 <- renderPlot({  #原图
        d = datasetInput()
        d = subset(d,d$pd_class %in% input$pdtypes)
        ggplot(d, aes(pd_location, peak_voltage*polarity,color=factor(pd_class))) + geom_point() 
    })
    
    output$plot2 <- renderPlot({ #控制缩进的图
        d = datasetInput()
        d = subset(d,d$pd_class %in% input$pdtypes)
        ggplot(d, aes(pd_location, peak_voltage*polarity,color=factor(pd_class))) + geom_point() +
            coord_cartesian(xlim = ranges$x, ylim = ranges$y) 
            
    })
    observe({  #观察是不是有zoom的情况
        brush <- input$plot1_brush
        if (!is.null(brush)) {
            ranges$x <- c(brush$xmin, brush$xmax)
            ranges$y <- c(brush$ymin, brush$ymax)
            
        } else {
            ranges$x <- NULL
            ranges$y <- NULL
        }
    })
    
    #产生summary
    output$summary <- renderPrint({
        summary(datasetInput())
    })
    
    #产生table
    output$table <- renderTable({
        data.frame(head(datasetInput(),10))
    })
    
    
})
## Steps to enable tracing in Python app 

1. Setup the exporter 
    * AzureTraceExporter
2. Set the tracer to use the above exporter
    * Sampling? 
        * Configure 100% sample rate, otherwise, few traces will be sampled. AlwaysOnSampler()
3. Get the global singleton Tracer object

    ```tracer = Tracer(exporter=ze, sampler=always_on.AlwaysOnSampler())```
4. Create a scoped span 
    *  Context Manager: the span will close at the end of the block.
        ```
        with tracer.span(name='hello'):
            logger.warning('In the span')
        ```
    * Explicitly starting and ending span 
        ```
        tracer.start_span(name='span1')
        do_something_to_trace()
        tracer.end_span()
        ```      
5. Start additional spans within the scoped/main span which will automatically be a child span 
6. Set status of span upon error 
    
    ```span.status = Status(5, "Error occurred")```

7. Annotate span to capture metadata about our operation 

    ```span.add_annotation("invoking doWork")```
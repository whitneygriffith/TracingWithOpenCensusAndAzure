# Span data will be sent to azure monitor dependencies table

from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import AlwaysOnSampler
from opencensus.trace.tracer import Tracer
import time
from os import getenv

tracer = Tracer(
    exporter=AzureExporter(
        connection_string="InstrumentationKey=" + getenv("INSIGHTS_INSTRUMENTATION_KEY")
    ),
    sampler=AlwaysOnSampler(),
)


def main():
    # 4. Create a scoped span. The span will close at the end of the block.
    with tracer.span(name="main") as span:
        for i in range(0, 10):
            doWork()


def doWork():
    # 5. Start another span. Because this is within the scope of the "main" span,
    # this will automatically be a child span.
    with tracer.span(name="doWork") as span:
        print("doing busy work")
        try:
            time.sleep(0.1)
            with tracer.span(name="insideDoWork") as inner_span:
                print("inside do work")
                inner_span.add_annotation("inner span inside do work")
                print(inner_span.span_id, inner_span.context_tracer.trace_id)
        except:
            # 6. Set status upon error
            # span.status = Status(5, "Error occurred")
            print("Exception")

        # 7. Annotate our span to capture metadata about our operation
        span.add_annotation("invoking doWork")


if __name__ == "__main__":
    main()

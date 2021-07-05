"""
Copyright 2021 The XAI Demonstrator team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

OpenTelemetry tracing utilities for FastAPI apps."""
from functools import wraps
from typing import Any, Callable, Dict, Union

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from pydantic import BaseSettings

__all__ = ["set_up", "instrument_app", "add_span_attributes", "traced"]

trace.set_tracer_provider(TracerProvider())


class TracingSettings(BaseSettings):
    TRACING_EXPORTER: str = "console"
    APPLICATIONINSIGHTS_CONNECTION_STRING: str = "unset"


tracing_settings = TracingSettings()


def set_up():
    if tracing_settings.TRACING_EXPORTER == "azure":
        from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

        azure_monitor_exporter = AzureMonitorTraceExporter.from_connection_string(
            conn_str=tracing_settings.APPLICATIONINSIGHTS_CONNECTION_STRING
        )

        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(azure_monitor_exporter)
        )
    else:
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

        trace.get_tracer_provider().add_span_processor(
            SimpleSpanProcessor(ConsoleSpanExporter())
        )


def instrument_app(app: FastAPI):
    """Add OpenTelemetry middleware to a FastAPI app.

    Following available documentation and examples,
    this should be called after all routes have been added.
    """
    FastAPIInstrumentor.instrument_app(app)


def add_span_attributes(attributes: Dict[str, Any],
                        span: Union[trace.Span, None] = None):
    """Add attributes to a span.

    Parameters
    ----------
    attributes : dict
        Arbitrary number of span attributes.
    span : opentelemetry.trace.Span
    """
    span = span or trace.get_current_span()
    for attribute, value in attributes.items():
        span.set_attribute(attribute, value)


def traced(func: Union[Callable, None] = None,
           label: Union[None, str] = None,
           attributes: Union[Dict[str, Any], None] = None) -> Callable:
    """Decorator that adds a span around a function.

    Parameters
    ----------
    func : Callable
        The function to be decorated
    label : str, optional
        A custom label. If not specified, the function's `__name__` will be used.
    attributes : dict, optional
        Arbitrary number of span attributes.
    Examples
    --------
    To simply trace a single function:
        @traced
        def my_function():
            ...
    This results in a span with name `my_function`.
    To add custom labels and span attributes, use the keyword arguments:
        @traced(label="custom_span_label", attributes={"num_of_samples": 12})
        def my_function():
            ...
    This results in a span with name `custom_span_label` with attribute `num_of_samples` set to 12.
    """
    attributes = attributes or {}

    def decorator_function(func_: Callable) -> Callable:
        _label = label or func_.__name__

        @wraps(func_)
        def with_tracer(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(_label) as span:
                add_span_attributes(attributes, span)
                return func_(*args, **kwargs)

        return with_tracer

    return decorator_function(func) if callable(func) else decorator_function

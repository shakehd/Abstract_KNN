from _typeshed import Incomplete

class ReportBase:
    COLUMN_NAMES: list[str]
    COLUMN_WIDTHS: list[int]
    ITERATION_FORMATS: list[str]
    @classmethod
    def print_header(cls) -> None: ...
    @classmethod
    def print_iteration(cls, *args) -> None: ...
    @classmethod
    def print_footer(cls) -> None: ...

class BasicReport(ReportBase):
    COLUMN_NAMES: Incomplete
    COLUMN_WIDTHS: Incomplete
    ITERATION_FORMATS: Incomplete

class SQPReport(ReportBase):
    COLUMN_NAMES: Incomplete
    COLUMN_WIDTHS: Incomplete
    ITERATION_FORMATS: Incomplete

class IPReport(ReportBase):
    COLUMN_NAMES: Incomplete
    COLUMN_WIDTHS: Incomplete
    ITERATION_FORMATS: Incomplete

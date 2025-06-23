import enum
import logging
from dataclasses import dataclass
from datetime import datetime, time
from typing import Annotated, Optional

from pydantic import Field, ConfigDict, PlainValidator

from pa_api.utils import (
    first,
)
from pa_api.xmlapi.types.utils import (
    XMLBaseModel,
    mksx,
    parse_datetime,
    parse_time,
    pd,
    Datetime,
    String,
)


def parse_tdeq(d):
    if "null" in d:
        return None
    try:
        return parse_time(d)
    except Exception as e:
        logging.debug(e)
    return parse_datetime(d)


def parse_progress(progress):
    try:
        return float(progress)
    except Exception as e:
        logging.debug(f"{e} => Fallback to datetime parsing")

    # When finished, progress becomes the date of the end
    if parse_datetime(progress):
        return 100.0
    return None

Progress = Annotated[float, PlainValidator(parse_progress)]

class JobResult(enum.Enum):
    OK = "OK"
    FAIL = "FAIL"


@dataclass
class Job(XMLBaseModel):
    model_config = ConfigDict(
        # https://docs.pydantic.dev/2.0/api/alias_generators/
        # alias_generator=lambda name: name.replace("-", "_")
    )
    # TODO: Use pydantic
    tenq: Datetime
    tdeq: time
    id: str
    user: String
    type: str
    status: str
    queued: bool
    stoppable: bool
    result: str
    tfin: Datetime
    description: String = ""
    position_in_queue: int = Field(alias="positionInQ", default=None)
    progress: Progress
    details: String = ""
    warnings: String = ""

    # @staticmethod
    # def from_xml(xml) -> Optional["Job"]:
    #     # TODO: Use correct pydantic functionalities
    #     if isinstance(xml, (list, tuple)):
    #         xml = first(xml)
    #     if xml is None:
    #         return None
    #     p = mksx(xml)
    #     return Job(
    #         tenq=p("./tenq/text()", parser=pd),
    #         tdeq=p("./tdeq/text()", parser=parse_tdeq),
    #         id=p("./id/text()"),
    #         user=p("./user/text()"),
    #         type=p("./type/text()"),
    #         status=p("./status/text()"),
    #         queued=p("./queued/text()") != "NO",
    #         stoppable=p("./stoppable/text()") != "NO",
    #         result=p("./result/text()"),
    #         tfin=p("./tfin/text()", parser=pd),
    #         description=p("./description/text()"),
    #         position_in_queue=p("./positionInQ/text()", parser=int),
    #         progress=p("./progress/text()", parser=parse_progress),
    #         details="\n".join(xml.xpath("./details/line/text()")),
    #         warnings=p("./warnings/text()"),
    #     )

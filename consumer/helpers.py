import datetime
import os
import sys

import aiormq.types
import ujson
from pydantic import ValidationError
from simple_print import sprint

from settings import DEBUG


def validate_request_schema(request_schema):
    def wrap(func):
        async def wrapped(message: aiormq.types.DeliveredMessage):
            now = datetime.datetime.now().time()
            await message.channel.basic_ack(message.delivery.delivery_tag)
            sprint(f"{func.__name__} :: basic_ack [OK] :: {now}", c="green", s=1, p=1)

            json_rq = None
            response = None
            error = None

            try:
                json_rq = ujson.loads(message.body)
                data = request_schema.validate(json_rq).dict()
            except ValidationError as error_message:
                error = f"ERROR REQUEST, VALIDATION ERROR: body={message.body} error={error_message}"
            except Exception as error_message:
                error = f"ERROR REQUEST: body={message.body} error={error_message}"
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                error += f" {exc_type} {fname} {exc_tb.tb_lineno}"

            if not error:
                sprint(f"{func.__name__} :: Request {json_rq}", c="yellow", s=1, p=1)
                try:
                    await func(data)
                except Exception as error_message:
                    error = f"ERROR REQUEST: body={message.body} error={error_message}"
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    error += f" {exc_type} {fname} {exc_tb.tb_lineno}"

            if DEBUG:
                if error:
                    sprint(error, c="red", s=1, p=1)
                else:
                    sprint(f"{func.__name__} :: complete [OK]", c="green", s=1, p=1)

        return wrapped

    return wrap

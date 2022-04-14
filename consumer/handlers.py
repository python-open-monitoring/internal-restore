from consumer import methods
from consumer import schema
from consumer.helpers import validate_request_schema


@validate_request_schema(schema.Restore)
async def restore(data):
    await methods.restore(data)

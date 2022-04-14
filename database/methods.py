import datetime

import asyncpg
from simple_print import sprint

from settings import DATABASE_URI


async def insert_restore_activity(restore_id, connection_established, response_time, response_time_ms, test=False):
    sprint(f"restore_id = {restore_id} :: connection_established= {connection_established} :: response_time = {response_time}", c="yellow", s=1, p=1)

    connection_established = str(connection_established).lower()

    response_time = round(response_time, 6)
    response_seconds, response_microseconds = str(response_time).split(".")
    if len(response_seconds) == 1:
        response_seconds = f"0{response_seconds}"
    response_time = f"00:00:{response_seconds}.{response_microseconds}"
    restoring_date = datetime.datetime.now()

    conn = await asyncpg.connect(DATABASE_URI)

    insert_restore_activity_record = f"""  
    INSERT INTO "restoring_restoreactivity" 
    ("restore_id", "connection_establish", "response_time", "response_time_ms", "creation_date") 
    VALUES ({restore_id}, {connection_established}, '{response_time}'::time, {response_time_ms}, '{restoring_date}'::timestamptz);
    """
    sprint(insert_restore_activity_record, c="cyan", p=1)

    try:
        status = await conn.execute(insert_restore_activity_record)
        sprint(status, c="green", p=1)
    except Exception as e:
        sprint(e, c="red", p=1)

    insert_restore_activity_record = f"""  
    UPDATE "restoring_restore" 
    SET last_restoring_date='{restoring_date}'::timestamptz,
        last_connection_establish={connection_established},
        last_response_time='{response_time}'::time,
        last_response_time_ms={response_time_ms}
    WHERE id={restore_id}; 
    """
    sprint(insert_restore_activity_record, c="cyan", p=1)

    try:
        status = await conn.execute(insert_restore_activity_record)
        sprint(status, c="green", p=1)
    except Exception as e:
        sprint(e, c="red", p=1)
    finally:
        await conn.close()

    return 1

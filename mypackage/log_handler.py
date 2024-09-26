import logging
import psycopg2 as pg

class PostgresHandler(logging.Handler):
    def __init__(self, db_config, table, job_id):
        logging.Handler.__init__(self)
        self.connection = pg.connect(**db_config)
        self.cursor = self.connection.cursor()
        self.table = table
        self.job_id = job_id
        self._create_table_if_not_exists()

    def _set_time_zone(self):
        self.connection.commit()

    def _create_table_if_not_exists(self):
        self.cursor.execute("set time zone 'UTC'")
        self.cursor.execute("""
        create table if not exists %s (
            id serial primary key,
            created_at timestampz default now(),
            name varchar(255),
            levelname varchar(50),
            message text,
            job_id varchar(255) not null
        )""", (self.table,))
        self.connection.commit()

    def emit(self, record):
        log_entry = self.format(record)
        self.cursor.execute("""
        insert into flow_logs 
        (name, levelname, message, job_id) 
        values 
        (%s, %s, %s, %s)
        """, (record.name, record.levelname, log_entry, self.job_id))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
        logging.Handler.close(self)
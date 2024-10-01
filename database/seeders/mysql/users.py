import click
from faker import Faker
from config.logging import logger
from jetshift_core.helpers.mysql import mysql_connect, get_last_id

fake = Faker()
connection = mysql_connect()
table_name = 'users'


def seed_table(num_records):
    last_id = get_last_id(table_name)

    try:
        with connection.cursor() as cursor:
            inserted = 0
            for i in range(1, num_records + 1):
                id = last_id + i
                name = fake.name()
                email = fake.email()
                created_at = fake.date_time_this_decade()

                sql = f"""
                INSERT INTO {table_name} (id, name, email, created_at)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (id, name, email, created_at))

                inserted += 1

                if inserted % 10000 == 0:
                    click.echo(f"Inserted {inserted} records. Remaining: {num_records - i}")

        connection.commit()
    except Exception as e:
        logger.error("An error occurred while seeding the table: %s", e)


@click.command()
@click.argument('records', required=False, default=10)
def main(records):
    seed_table(records)
    connection.close()
    print(f"Seeding completed. {records} records inserted to table {table_name}.")


if __name__ == "__main__":
    main()

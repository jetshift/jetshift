from config.luigi import luigi, local_scheduler
from datetime import datetime
from jetshift_core.helpers.common import send_discord_message


class TimeJob(luigi.Task):
    task_completed = luigi.BoolParameter(default=False)

    def run(self):
        formatted_time = datetime.now().strftime('%b %d, %Y %I:%M %p')  # Format like "Jan 20, 2024 12:30 PM"

        # Assuming UTC offset is fixed at +6 hours (change this as needed)
        utc_offset = 6
        formatted_time += f' (UTC +{utc_offset})'

        message = f'Date and time: {formatted_time}'
        print(message)
        send_discord_message(message)

        # Mark task as completed
        self.task_completed = True

    def complete(self):
        self.task_completed = False
        return getattr(self, 'task_completed', False)


def main():
    luigi.build([TimeJob()], local_scheduler=local_scheduler)


if __name__ == '__main__':
    main()

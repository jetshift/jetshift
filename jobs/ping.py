from config.luigi import luigi, local_scheduler
from jetshift_core.helpers.clcikhouse import ping_clickhouse


class Ping(luigi.Task):
    def ping(self):
        ping_clickhouse()

    def run(self):
        self.ping()


def main():
    luigi.build([Ping()], local_scheduler=local_scheduler)


if __name__ == '__main__':
    main()

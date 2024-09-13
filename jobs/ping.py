from config.luigi import luigi
from jetshift_core.helpers.clcikhouse import ping_clickhouse


class Ping(luigi.Task):
    def ping(self):
        ping_clickhouse()

    def run(self):
        self.ping()


def main():
    luigi.build([Ping()], local_scheduler=True)


if __name__ == '__main__':
    main()

from jetshift_core.helpers.quicker import migrations, seeders, job


def main():
    migrations_list = ["mysql", "clickhouse"]
    migrations(migrations_list)
    print("\nMigrations completed ✓✓✓\n")

    migrations_list = ["users -n 10"]
    seeders(migrations_list)
    print("\nSeeders completed ✓✓✓\n")

    job_list = ["users"]
    job(job_list)
    print("\nJobs completed ✓✓✓\n")


if __name__ == "__main__":
    main()

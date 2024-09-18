from jetshift_core.helpers.quicker import migrations, seeders, jobs


def main():
    migrations_list = ["mysql", "clickhouse"]
    migrations(migrations_list)
    print("\nMigrations completed ✓✓✓\n")

    seeder_list = ["users -n 5"]
    seeders(seeder_list)
    print("\nSeeders completed ✓✓✓\n")

    job_list = ["users"]
    jobs(job_list)
    print("\nJobs completed ✓✓✓\n")


if __name__ == "__main__":
    main()

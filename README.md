<p align="center">
  <a href="https://github.com/mdobydullah/jetshift-core">
    <img src="https://cdn.shouts.dev/media/435/jetshift-github.png" alt="JefShift" width="120">
  </a>
</p>

<p align="center">
<strong>JetShift</strong>
</p>

> JetShift is a powerful and lightweight Python framework for ETL (Extract, Transform, Load) that simplifies building data pipelines.

## Intro

JetShift allows seamless extraction, transformation, and loading of data from multiple sources. Its intuitive API and flexible architecture make it easy to handle complex data transformations at scale, whether the data is structured or unstructured. This makes it ideal for developing robust workflows with minimal effort.

Get your data moving swiftly and reliably with JetShift. 🚀

## Usage

Transfer data between [Pandas data sources](https://pandas.pydata.org/docs/user_guide/io.html) and any destination, such as data warehouses or databases.

## Run

<details>
<summary>Run with Docker</summary>

### Run with Docker

```bash
docker compose up -d
```

Web servers

```bash
Web: http://localhost
Luigid: http://localhost:8082
```

</details>

<details>
<summary>Run without Docker</summary>

### Run without Docker

Install Python on your machine and create virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

```bash
# linux
source venv/bin/activate

# windows
venv\Scripts\activate

# windows (gitbash)
source venv/Scripts/activate
```

Install requirements

```bash
pip install -e .
```

Run dev server

```
dev
```

```bash
Web: http://localhost
Luigid: http://localhost:8082
```

### More commands

Deactivate the virtual environment

```bash
deactivate
```

</details>

## Features

<details>
<summary>Migration</summary>

### Make Migration

```bash
# Structure
make migration table-name -e database-engine

# Example
make migration blogs # default engine is mysql
make migration blogs -e mysql
```

### Run Migration

```bash
# Structure
migrate database-engine # run all migrations
migrate database-engine table-name # run specific migration

# Examples
migrate mysql
migrate mysql users
```

Available database engines: mysql, clickhouse. You can easily add new a engine.

All migrations are available in `database/migrations` directory.

</details>

<details>
<summary>Seeder</summary>

### Make Seeder

```bash
# Structure
make seeder seeder-name -e database-engine

# Examples
make seeder blogs # default engine is mysql
make seeder blogs -e mysql
```

### Run Seeder

```bash
# Structure
seed database-engine # run all seeders
seed database-engine table-name # run specific seeder
seed database-engine table-name -n number # run specific seeder with n records

# Examples
seed mysql
seed mysql users
seed mysql users -n 10
```

Available database engines: mysql. You can easily add new a engine.

All seeders are available in `database/seeders` directory.

</details>

<details>
<summary>Job</summary>

### Make Job

```bash
# Structure
make job job-name -jt job-type

# Examples
make job time # default job type is simple
make job time -jt simple
```

Available job types: simple. You can easily add new a type.

### Run Job

```bash
# Structure
python -m jobs.{job}
# or
job {job}

# Examples
python -m jobs.time
# or
job time
```

All jobs are available in `jobs` directory.
</details>


<details>
<summary>Quicker</summary>

### Make Quicker

```bash
# Structure
make quicker quicker-name

# Example
make quicker sales-report
```

### Run Quicker

```bash
# Structure
python -m quickers.{quicker}
# or
quick {quicker}

# Example
python -m quickers.sales-report
# or
quick sales-report
```

All jobs are available in `quickers` directory.
</details>

## Resources

1. [Pandas](https://pandas.pydata.org/)
2. [Luigi Framework](https://github.com/spotify/luigi)
3. [ClickHouse](https://clickhouse.com/)

## License

The JetShift is open-sourced software licensed under the [MIT license](https://github.com/mdobydullah/jetshift/blob/master/LICENSE).

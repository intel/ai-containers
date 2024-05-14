# Building Documentation

First, install the python prerequisites:

```bash
pip install -r docs/requirements.txt
```

## MKDocs

To build the documentation, run the following command:

```bash
mkdocs build
```

Once built, the documentation will be available in the `site` directory.

To view the documentation, run the following command:

```bash
mkdocs serve --no-livereload
```

The documentation will be available at [http://localhost:8000](http://localhost:8000).

## Labelling Containers

To customize the tables in the [Support Matrix](./matrix.md), you can add labels to the services found in each container group's `docker-compose.yaml` file. The command `docker compose config` is run to get all of the metadata from the container group. Labels are used to specify the public metadata for each container, and then the tables are generated based on the `.actions.json` file found in the same directory.

The schema for labels is as follows:

| Label Name                                            | Description                                                        |
|-------------------------------------------------------|--------------------------------------------------------------------|
| `dependency.<package-manager>.<package>`              | `apt`, `yum`, or `conda` package                                   |
| `dependency.<version>`                                | Set to `false` to ignore version in table                          |
| `dependency.<version>.<package-manager>.<package>`    | package specific to a version specified in `.actions.json`         |
| `dependency.name`                                     | Title of the service (overrides the compose svc name)              |
| `dependency.python`                                   | Python version                                                     |
| `dependency.python.<filename>`                        | Path to specific `requirements.txt` from `docker-compose.yaml`     |
| `docs`                                                | Name of the table in the matrix, or `false` to ignore service      |
| `org.opencontainers.base.name`                        | OCI Base `Image:Tag` used for the image                            |
| `org.opencontainers.image.name`                       | OCI Repository name for the image                                  |
| `org.opencontainers.image.title`                      | OCI Title of the image with appropriate branding                   |
| `org.opencontainers.image.version`                    | OCI Image tag                                                      |

Python dependencies are determined by the service's `requirements.txt` file. By default, the file needs to be named `<svc-name>-requirements.txt`, but this can be overridden with the `dependency.name` label.

> [!NOTE]
> There are no default values for the labels, but if you `extends` from another service, you will inherit those labels so be careful not to inherit dependencies that are not new to that container layer.

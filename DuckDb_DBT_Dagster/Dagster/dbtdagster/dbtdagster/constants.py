
import os
import pathlib

from dagster_dbt import DbtCliResource

# Use environment variable for project directory (ensure it's set in Docker or your environment)
# dbt_project_dir = pathlib.Path("/app/dbt_project")
dbt_project_dir=pathlib.Path(r"./duck_db_project")
dbt = DbtCliResource(project_dir=os.fspath(dbt_project_dir))


# If DAGSTER_DBT_PARSE_PROJECT_ON_LOAD is set, a manifest will be created at runtime.
# Otherwise, we expect a manifest to be present in the project's target directory.
if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD"):
    dbt_manifest_path = (
        dbt.cli(
            ["--quiet", "parse"],
            target_path=pathlib.Path("target"),
        )
        .wait()
        .target_path.joinpath("manifest.json")
    )
else:
    dbt_manifest_path = dbt_project_dir.joinpath("target", "manifest.json")

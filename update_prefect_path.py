from pathlib import Path

import yaml


def update_prefect_path():
    # Fix the fact that Prefect doesn't interact well with the relative pathing
    with open("main.prefect.yaml", "r") as f:
        data = yaml.safe_load(f)

    data["pull"][0]["prefect.deployments.steps.set_working_directory"]["directory"] = (
        str(Path(__file__).parent.absolute())
    )

    with open("prefect.yaml", "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


if __name__ == "__main__":
    update_prefect_path()

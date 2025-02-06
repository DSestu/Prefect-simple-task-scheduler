from prefect import flow, task
from prefect.artifacts import create_link_artifact
from prefect.logging import get_run_logger


@flow
def flow1() -> None:
    logger = get_run_logger()
    logger.info("Hello from flow1")
    logger.warning("Warning from flow1")
    create_link_artifact(
        key="my-important-link",
        link="https://www.prefect.io/",
        link_text="Prefect",
    )


@task
def my_task1() -> None:
    print("Hello from task1")


@task
def my_task2() -> None:
    print("Hello from task2")


@flow
def flow2() -> None:
    my_task1()
    my_task2()
    print("Hello from flow2")


if __name__ == "__main__":
    flow1()
    flow2()

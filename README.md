# Prefect - Windows task scheduler alternative

This project is aimed at providing a simple template for running croned tasks on Windows.

The Windows task scheduler can be a bit of a pain to configure if you have a lot of tasks to run.

For this reason, we use [Prefect](https://docs.prefect.io/) to schedule tasks.

> The absolute goal of this project is to have a very fast and transparent setup so you can just start coding python scripts.

## Setup

1. Launch `init.bat`

This will:

* Make sure that `uv` package manager is installed

* Create the `uv` virtual environment

* Update the packages in the virtual environment

2. Launch `create_scheduled_task.bat`

This will create a Windows scheduled task responsible of running the Prefect server and worker in background.

**Unfortunately**, you still have to do a one-time configuration of the task:

* Go to the task scheduler

* Edit the `Prefect` task

* In general: set to `Run whether user is logged on or not`

* In settings: Uncheck `Stop the task if it runs longer than`

**The Prefect server and worker will now run in the background at user login.**

**You can launch it manually by right-clicking on the task and selecting `Run`.**

> **The Prefect dashboard will be available at `http://localhost:4200`**

3. **EVERY TIME** you change the code, you have to register the new code *(prefect deployement)* by launching `update_flows.bat`.

## Adding additional flows

1. You can add new flows by creating a new python file in the `src/prefect-perso/flows` folder.

2. You have to register the flows by adding the `@flow` decorator to the function.

3. You have to add the flow by copying the example flows in the `main.prefect.yaml`. Make sure to change the flow name, entrypoint and cron.

## Last resort restarting the server

If, for whatever reason the server is not running well *(e.g. hardcore dependency issue)*, you can restart from scratch the server by:

**"Soft" version, restart**:

1. Go to the task scheduler, and end the Prefect task

2. On a command line, run `taskkill /f /im python.exe` *(brutal killing of all python processes)*

3. Start the Prefect task again

**"Hard" version, full reset**:

1. Go to the task scheduler, and end the Prefect task

2. On a command line, run `taskkill /f /im python.exe` *(brutal killing of all python processes)*

3. Delete the Prefect task

4. Delete `.venv`

5. Follow the setup steps above

**Debugging why the server is not running**:

1. End the Prefect task

2. On a command line, run `taskkill /f /im python.exe` *(brutal killing of all python processes)*

3. Launch the Prefect server manually by running `start_prefect.bat`

4. When solved, restart the Prefect task

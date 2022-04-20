# Working with the Databricks CLI

In this series of labs, we'll complete a basic overview of the Databricks CLI.

The instructions will work in any terminal. Databricks clusters have a web-based terminal accessible by going to the **Clusters** tab, selecting your active cluster, clicking the **Apps** tab and then **Launch Web Terminal**.

## 1. Basic CLI Installation and Usage

Once you have a terminal open, begin by installing the Databricks CLI using `pip`.

```
pip3 install databricks-cli
```

To see the list of options, run the help command.

```
databricks -h
```

Before we begin, we'll need to configure our connection to the workspace. To see the options for configuration, run:

```
databricks configure -h
```

Generating a personal access token is simple, so we'll use this method. Make sure you have you Databricks workspace open in a separate tab, and then run: 

```
databricks configure --token
```

Copy and paste the workspace URL at the prompt and hit enter.

You will now be prompted for a token. Navigate to your Databricks workspace and click the small user icon in the top right corner. Select **User Settings** from the drop-down menu. Navigate to the **Access Tokens** tab and click **Generate New Token**. Add any comment to describe your token, and set the lifetime for 1 day, then click **Generate**. Copy and paste the generated token back into the command line prompt and hit enter.

Congratulations! You have successfully enabled programmatic access to your Databricks workspace from the CLI. To confirm this configuration was successful, run:

```
databricks clusters list
```

You should see a list of all the clusters configured in your workspace.

## 2. Importing and Installing Libraries and Notebooks

The [Databricks Repos](https://docs.databricks.com/repos.html) product makes Git integration with notebooks simple. That being said, it may require some updates to how you structure your projects in order to maximize the functionality. The CLI can also be extremely useful for moving notebooks and libraries from the workspace to a local machine and versioning with Git.

For this demo, a simple Git project is provided. Clone it to your machine now, and list to confirm successful download.

```
git clone https://github.com/databricks-academy/cli-demo.git
ls
```

Change directories into the Git repo.

```
cd cli-demo
```

We'll use the Databricks CLI to upload a Databricks Collection (DBC) file that represents a number of notebooks. To see the full list of import options, run

```
databricks workspace import -h
```

To import our DBC with the desired options, execute the following (**NOTE**: the `/cli-demo` at the end of this command signifies the target directory; here, this will be a base directory in the workspace folder hierarchy. If you wish to install to your user folder, replace this with `/Users/<your_user_name>/cli-demo`).

```
databricks workspace import -l PYTHON -f DBC notebooks.dbc /cli-demo
```

Now we'll upload and install a library. Begin by navigating to the right directory and listing the contents.

```
cd wheel
ls
```

We'll add our library to the `/tmp` folder on the DBFS.

```
databricks fs cp weather-1.0.0-py3-none-any.whl dbfs:/tmp/
```

In order to install to a cluster, we need the cluster id. Substitute your cluster's name for `<cluster_name>` in the command below and execute the command.

```
databricks clusters get --cluster-name <cluster_name>
```

Now copy and replace the `<cluster-id>` in the following command and execute to install the library.

```
databricks libraries install --cluster-id <cluster_id> --whl dbfs:/tmp/weather-1.0.0-py3-none-any.whl
```

You can navigate to your cluster's library tab in the workspace to check on installation progress. 

Once the installation has finished, navigate to the `weather-wheel` notebook (this was part of the DBC you uploaded earlier in the lesson).

This notebook will use the library you just installed on your cluster to execute some simple logic. Click `Run All` to confirm that everything is working.

Now add a comment to any cell in the notebook. We'll use the command line to download and sync changes from our notebook.

In your terminal, change directories and export this notebook.

```
cd ../notebooks
databricks workspace export -o /cli-demo/weather-wheel weather-wheel.py
```

You should see that this file has been changed when you run:

```
git status
```

While notebooks have some extra content relative to normal Python files, editing them in local mode is fairly straightforward. Here, simple instructions are provided for using Vim. We'll open a different notebook by running

```
vim weather-notebook.py
```

Press `i` to enter insert mode.

On line 3, add a comment and press enter to add a newline.

To exit Vim and save your changes, press `esc`, then type `:wq` and hit `enter`.

Use git to confirm a change has been saved.

```
git status
```

Now, upload your edited notebook to the workspace by running

```
databricks workspace import -o -l PYTHON weather-notebook.py /cli-demo/weather-notebook
```

Note that in both directions of our code migration, we used the `-o` flag to overwrite the target file. While in this case this had the desired effect of updating our notebook with the latest version of the file, be careful to avoid accidentally overwriting your work when splitting edits between multiple environments.

## 3. Basic Job Orchestration

While Databricks supports official connectors for a number of popular orchestration tools, the same functionality can be achieved by writing custom logic using the CLI or [REST API](https://docs.databricks.com/dev-tools/api/latest/index.html) and your tool of choice. We'll explore basic functionality for working with clusters, jobs, and runs in this lab.

While most jobs will run against Jobs Clusters (which have a lower cost and terminate on job completion), programmatically starting and stopping clusters can be extremely useful when managing a large organization with many interactive cluster users. You can view all clusters in a workspace by running:

```
databricks clusters list
```

If there's a currently inactive (terminated) cluster that you'd like to start, replace the `<cluster-id>` in the following line and execute the command.

```
databricks clusters start --cluster-id <cluster_id>
```

You can see the cluster spinning up in the workspace. We'll schedule a notebook job against this cluster. In the Jobs UI, [follow the instructions in the docs](https://docs.databricks.com/jobs.html#create-a-job) to schedule the `job-demo` notebook uploaded earlier in this module against your interactive cluster. Make sure you give the job a name you'll recognize in the jobs list.

Back in the terminal, list all the jobs in the workspace by running

```
databricks jobs list
```

Find your job and replace the `<job-id>` to execute the following command:

```
databricks jobs get --job-id <job_id>
```

This will print out the full details of your job as a JSON. This output is exactly what would be necessary to define a new job using the CLI with the `--json` option. To see all the CLI options for creating jobs, run

```
databricks jobs create -h
```

For now, we'll just trigger a run of the job we defined in the UI. Use the same `<job-id>` in the following command:

```
databricks jobs run-now --job-id <job_id> --notebook-params '{"param1":"CLI"}'
```

This command will output the run-id for your job. Substitute this for `<run-id>` and execute the following:

```
databricks runs get-output --run-id <run_id>
```

This will output the current status of your job. Execute this command a few times until you see `SUCCESS` returned as the status. Note that amongst the returned fields is a `notebook_output` field. Using `--notebook-params` and `notebook_output`, you can build simple conditionals that trigger control flow in your notebook-based pipelines, and pass parameters and values between your orchestration tooling and your scheduled notebooks.

To shut down your interactive cluster, use the same cluster ID as before to execute:

```
databricks clusters delete --cluster-id <cluster_id>
```

By linking together these simple commands, it's easy to build complex workflows using Databricks.
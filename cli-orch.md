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

## 2. Basic Job Orchestration

While Databricks supports official connectors for a number of popular orchestration tools, the same functionality can be achieved by writing custom logic using the CLI or [REST API](https://docs.databricks.com/dev-tools/api/latest/index.html) and your tool of choice. We'll explore basic functionality for working with clusters, jobs, and runs in this lab.

While most jobs will run against Jobs Clusters (which have a lower cost and terminate on job completion), programmatically starting and stopping clusters can be extremely useful when managing a large organization with many interactive cluster users. You can view all clusters in a workspace by running:

```
databricks clusters list
```

If there's a currently inactive (terminated) cluster that you'd like to start, replace the `<cluster_id>` in the following line and execute the command.

```
databricks clusters start --cluster-id <cluster_id>
```

You can see the cluster spinning up in the workspace. We've previously scheduled a notebook job against a cluster. In the Jobs UI, make sure you know the name of the job you want to schedule.

Back in the terminal, list all the jobs in the workspace by running

```
databricks jobs list 
```

You may see a warning message around the jobs API version. Because we're working with multi-task jobs, go ahead and run the suggested command to use the jobs API version 2.1:

```
databricks jobs configure --version=2.1
```

If you need to configure your API version, rerun the list command to get your job ID:

```
databricks jobs list 
```

Find your job and replace the `<job_id>` to execute the following command:

```
databricks jobs get --job-id <job_id>
```

This will print out the full details of your job as a JSON. This output is exactly what would be necessary to define a new job using the CLI with the `--json` option. To see all the CLI options for creating jobs, run

```
databricks jobs create -h
```

For now, we'll just trigger a run of the job we defined in the UI. Use the same `<job_id>` in the following command:

```
databricks jobs run-now --job-id <job_id>
```

This command will output the run-id for your job.

**NOTE**: Functionality has changed for getting run information with the introduction of multi-task jobs. A job run will contain multiple task runs. You can retrieve the run ID and progress of each task by substituting the `<job_run_id>` and execute the following:

```
databricks runs get --run-id <job_run_id>
```

This will output the current status of your job, as well as each of the tasks in the job. Exexcute the command multiple times to see the progress of your tasks. Note that on task run completion, a `run_page_url` will appear with a link back to the notebook output.

To shut down your interactive cluster, use the same cluster ID as before to execute:

```
databricks clusters delete --cluster-id <cluster_id>
```

By linking together these simple commands, it's easy to build complex workflows using Databricks.

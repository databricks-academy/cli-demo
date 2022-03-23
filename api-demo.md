# Configuring and Using the Databricks REST API

In this lesson, you'll explore how the REST API can be leveraged to programmatically complete several common tasks. Note that while building your own solution using REST API calls is a daunting task, integrations with 3rd party tools and the Databricks CLI use these same REST API calls to interact with the Databricks workspace. If necessary, nearly any action you would need to complete in the Databricks workspace can be accomplished with the REST API.

**NOTE**: All instructions assume a standard UNIX command line. These commands can be executed leveraging the [Databricks web terminal app](https://docs.databricks.com/clusters/web-terminal.html). If using the web terminal, prevent your session from being interrupted by running `tmux` to begin.

## 1. Configure Token Authentication

For this demo, credentials will be stored in a `.netrc` file on the local machine.

Begin by using vim to create and open this file:

```
vim ~/.netrc
```

In the screen that opens, press `i` to enter insert mode, then fill in the following values:

```
machine <databricks-instance>
login token
password <token-value>
```

* `<databricks-instance>` value is the workspace URL excluding the `https://`. For example:

| | |
| --- | --- |
| Workspace URL | `https://abc-d1e2345f-a6b2.cloud.databricks.com` |
| `<databricks-instance>` | `abc-d1e2345f-a6b2.cloud.databricks.com` |
| **WARNING** | If using the web terminal, the workspace URL displayed in the web terminal will not be equivalent to the URL for the normal Databricks workspace |

* `token` is literally the string `token` (this tells the API we're using a token to validate)
* `<token-value>` is a [personal access token generated in User Settings](https://docs.databricks.com/sql/user/security/personal-access-tokens.html)

Then press `esc` to enter cursor mode. Press `:wq` and `enter` to save results.

Back in the terminal, confirm things were saved properly by running:

```
cat ~/.netrc
```

This should print out the 3 lines of text in the file you just wrote.

## 2. Call the REST API

Now you'll execute your first command using CURL.

```
curl --netrc -X GET <workspace-url>/api/2.0/clusters/list
```

Here, the `<workspace-url>` includes the `https://`, e.g., `https://abc-d1e2345f-a6b2.cloud.databricks.com`.

The result will be in JSON format, but will not be easy to parse in the command line.

## 3. Install JSON Parser and Re-run REST API Call

Install the lightweight JSON parser `jq` by executing the following code:

```
sudo apt-get install jq
```

Now you can re-execute your previous query but pipe the results to this output using the following syntax:

```
curl --netrc -X GET <workspace-url>/api/2.0/clusters/list | jq .
```

You may note that compared to similar operations in the Databricks CLI, you get much more verbose responses. Remember that the REST API supports numerous external applications and extensions in the Databricks ecosystem.

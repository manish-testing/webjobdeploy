# Test Python WebJob (deployed with GitHub Actions + Kudu)

A minimal triggered WebJob for testing the pipeline. It prints a timestamp, the Python version and the
result of one outbound HTTP call. It runs every 5 minutes (`settings.job`) and the pipeline also triggers it
once after deploying and prints the output in the GitHub Actions log.

```
.
├── run.py                        # the job code
├── run.sh                        # entry point Azure runs (sets PYTHONPATH for vendored packages)
├── settings.job                  # cron schedule: every 5 minutes
├── requirements.txt              # job dependencies (installed into the zip by the pipeline)
└── .github/workflows/deploy.yml  # build + deploy pipeline
```

## Setup

1. **Azure:** use an existing Linux Web App (Python 3.11), or create one. Scheduled WebJobs need **Always On**
   (Basic tier or higher). Make sure SCM basic auth is enabled
   (Configuration -> General settings -> *SCM Basic Auth Publishing Credentials* = On).
2. **Kudu credentials:** in the Web App click **Download publish profile**, open the XML and take
   `userName` (looks like `$yourappname`) and `userPWD` from the `MSDeploy` profile.
3. **GitHub secrets** (repo -> Settings -> Secrets and variables -> Actions):
   - `KUDU_USERNAME` = the `userName` value (including the `$`)
   - `KUDU_PASSWORD` = the `userPWD` value
4. **Edit `deploy.yml`:** set `SCM_HOST` to your Kudu host
   (Web App -> Advanced Tools -> Go; use only the host part of that URL) and, if you like, `WEBJOB_NAME`.
5. Push to `main` (or run the workflow manually from the Actions tab).

## What you should see

- GitHub Actions log: the deploy step succeeds, the verify step prints the job name and schedule, and the last
  step prints something like `Test WebJob started ... Outbound call OK ... Test WebJob finished successfully`.
- Azure Portal -> Web App -> **WebJobs**: `Test-WebJob-01` (Triggered) with logs and a Run button.

## Troubleshooting

- **401 from curl:** wrong `KUDU_USERNAME` / `KUDU_PASSWORD`, or SCM basic auth is disabled.
- **Job not listed in the portal (Linux):** Linux paths are case-sensitive. The workflow uses
  `app_data`; if the job doesn't show up, change it to `App_Data` in the deploy step.
- **Windows App Service:** `run.sh` won't run there. Replace it with a `run.cmd` that calls your Python.
- **Import error for `requests`:** `PYTHON_VERSION` in the workflow must match the Web App's Python version.
- **Scheduled runs don't happen:** Always On is off (not available on the Free tier).
- **Remove the last workflow step** ("Run the WebJob once...") when you use this for real.

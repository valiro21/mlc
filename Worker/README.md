# Worker Module

## Variables

 * MAX_BATCH_JOBS = 25 (default)
 
## Structure of the *jobs* table

| Column | Type | Description | Observations |
| --- | --- | --- | --- |
| submission_id | Integer | Id of the submission. | |
| problem_id | Integer | Id of the problem being evaluated. | |
| dataset_id | Integer | Id of the dataset being evaluated. | -1 for compilation. |
| testcase_id | Integer | Id of the testcase being evaluated. | -1 for compilation. |
| job_type | String | The type of the task. | Can be either "COMPILATION" or "EVALUATION". |
| status_code | Integer | Compilation or evaluation return code. | |
| status_message | String | Compilation or evaluation message. | |
| time_limit | Float | Time limit in seconds. | |
| memory_limit | Float | Memory limit in MB. | |
| created_timestamp | TIMESTAMP | The timestamp when the task was created. | |
| estimated_finish_time | TIMESTAMP | The expected timestamp when the job should be finished. | This can be null. |
| status | Integer | Status of the job. | 1 for unknown and 2 for finished |
| score | Integer | Score given by a scoring heuristic to determine the execution priority | |
| cpu | Float | Cpu time in seconds used for the operation. | |
| memory | Float | Memory in MB used for the operation. | |

## Worker routine:

 1. Cache the files for the active contests that the worker is assigned to.
 2. Select MAX_BATCH_JOBS number of jobs sorted by an heuristic to evaluate and update the worker_id in the database and the estimated finish time.
 3. Evaluate the jobs.
 4. Mark the jobs as finished.
 5. Execute step 2,3,4 again until there are no queries
 6. Start listening on database channel for updates - If a notification is received, start again from step 2.
 7. Send fake notification to force a reaload in case we missed jobs between step 5 and 6.

## Heuristic for scoring

Soon ...

## Requirements

You need to install ```gcc```, ```python3```, ```ghc```.

Also download the timeout submodule:
```
git submodule update --init --recursive # Execute from repo root.
```

Copy the executable timeout in ```/usr/local/bin```:
```
sudo cp ./Worker/Environment/timeout/timeout /usr/local/bin/timeout # Execute from repo root.
sudo chmod +x /usr/local/bin/timeout
```


CREATE OR REPLACE FUNCTION insert_compile_jobs() RETURNS trigger AS $jobs_compile_stamp$
DECLARE
  pid INTEGER;

  BEGIN
    raise notice 'Value: %', NEW.problem_id;

    pid := NEW.problem_id;
    INSERT INTO jobs (
      submission_id,
      dataset_id,
      testcase_id,
      job_type,
      problem_id,
      status,
      time_limit,
      memory_limit,
      created_timestamp
      )
    VALUES (
      NEW.ID,
      -1,
      -1,
      'Compile',
      NEW.problem_id,
      1,
      1.0,
      3.0,
      current_timestamp
    );

  NOTIFY mlcdb, 'work!';

        RETURN NEW;
    END;
$jobs_compile_stamp$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS submission_compile_jobs ON submissions;

CREATE TRIGGER submission_compile_jobs
AFTER insert on submissions
FOR EACH ROW
EXECUTE PROCEDURE insert_compile_jobs();

CREATE OR REPLACE FUNCTION insert_evaluate_jobs() RETURNS trigger AS $jobs_evaluate_stamp$
DECLARE
  pid INTEGER;
  r RECORD;
  BEGIN
    raise notice 'Value: %', NEW.problem_id;

    IF NEW.status = 2 and NEW.job_type = 'Compile' and NEW.status_code = 0 THEN
      pid := NEW.problem_id;

      for r in (SELECT
                    pid,
                    datasets.id as did,
                    testcases.id as tid,
                    datasets.time_limit as tl,
                    datasets.memory_limit as ml
                  FROM datasets
                  JOIN testcases ON testcases.dataset_id = datasets.id
                  WHERE datasets.problem_id = pid) LOOP
        INSERT INTO jobs (
          submission_id,
          job_type,
          problem_id,
          dataset_id,
          testcase_id,
          status,
          time_limit,
          memory_limit,
          created_timestamp
        )
        VALUES (
          NEW.submission_id,
          'Evaluate',
          NEW.problem_id,
          r.did,
          r.tid,
          1,
          r.tl,
          r.ml,
          current_timestamp
        );
      END LOOP;
    END IF;

  NOTIFY mlcdb, 'work!';

        RETURN NEW;
    END;
$jobs_evaluate_stamp$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS job_evaluate ON jobs;

CREATE TRIGGER job_evaluate
BEFORE UPDATE on jobs
FOR EACH ROW
EXECUTE PROCEDURE insert_evaluate_jobs();
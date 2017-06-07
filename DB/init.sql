/*--------- BEGIN MODULE INSERT / UPDATE COMPILE JOB ON SUBMISSION STATUS COMPILING ----------------
--------------------------------------------------------------------------------------------------*/
CREATE OR REPLACE FUNCTION insert_compile_job() RETURNS trigger AS $lang_insert_compile_job$
BEGIN
  if NEW.in_compilation_queue = TRUE THEN
    BEGIN
      INSERT INTO jobs(
          submission_id,
          dataset_id,
          testcase_id,
          job_type,
          problem_id,
          status,
          time_limit,
          memory_limit,
          created_timestamp
          ) VALUES (
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
    EXCEPTION WHEN unique_violation THEN
      UPDATE jobs SET
        created_timestamp = current_timestamp,
        status = 1,
        estimated_finish_timestamp = NULL
      WHERE jobs.submission_id = NEW.id;
    END;
  END IF;

  NOTIFY mlcdb, 'work!';

  RETURN NEW;
END;
$lang_insert_compile_job$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS add_compile_job ON submissions;

CREATE TRIGGER add_compile_job
AFTER insert or update on submissions
FOR EACH ROW
EXECUTE PROCEDURE insert_compile_job();
/*------------------------- END MODULE INSERT COMPILE JOB ON SUBMISSION ------------------------------
-----------------------------------------------------------------------------------------------------*/




/*--------- BEGIN MODULE INSERT / UPDATE EVALUATE JOB ON SUBMISSION COMPILE OR CALL ---------------
--------------------------------------------------------------------------------------------------*/
CREATE OR REPLACE FUNCTION evaluate_submission_on_dataset(
  sid in integer
, did in integer)
RETURNS void
AS $lang_evaluate_jobs$
DECLARE
  pid integer;
  tl integer;
  ml integer;
  r RECORD;
BEGIN
  SELECT problem_id FROM submissions WHERE submissions.id = sid INTO pid;
  SELECT time_limit, memory_limit FROM datasets WHERE datasets.id = did INTO tl, ml;

  FOR r in (SELECT testcases.id as tid
          FROM testcases
          WHERE testcases.dataset_id = did) LOOP
    BEGIN
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
        sid,
        'Evaluate',
        pid,
        did,
        r.tid,
        1,
        tl,
        ml,
        current_timestamp
      );
    EXCEPTION WHEN unique_violation THEN
      UPDATE jobs
      SET created_timestamp = current_timestamp,
          status = 1,
          estimated_finish_timestamp = NULL
      WHERE jobs.submission_id = sid
      AND jobs.problem_id = pid
      AND jobs.dataset_id = did
      AND jobs.testcase_id = r.tid
      AND jobs.status = 2;
    END;
  END LOOP;

  NOTIFY mlcdb, 'work!';
END;

$lang_evaluate_jobs$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION insert_evaluate_jobs() RETURNS trigger AS $lang_insert_evaluate_jobs$
DECLARE
  r RECORD;
  BEGIN
    IF OLD.status = 1 and NEW.status = 2 and NEW.job_type = 'Compile' and NEW.status_code = 0 THEN
      for r in (SELECT id as did FROM datasets WHERE problem_id = NEW.problem_id) LOOP
        PERFORM evaluate_submission_on_dataset(NEW.submission_id, r.did);
      END LOOP;
    END IF;
  RETURN NEW;
END;
$lang_insert_evaluate_jobs$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS add_evaluation_jobs ON jobs;

CREATE TRIGGER add_evaluation_jobs
BEFORE UPDATE on jobs
FOR EACH ROW
EXECUTE PROCEDURE insert_evaluate_jobs();
/*--------- END MODULE INSERT / UPDATE EVALUATE JOB ON SUBMISSION COMPILE OR CALL -----------------
--------------------------------------------------------------------------------------------------*/

/*-------------------------------- INITIALIZE ARCHIVE ---------------------------------------------
--------------------------------------------------------------------------------------------------*/
DO $$
  BEGIN
    INSERT INTO contests
    VALUES (
        1,
      'Archive',
      '',
      1,
      FALSE,
      TRUE,
      FALSE,
      FALSE,
      '255.255.255.255',
      0,
      2000000000,
      'UTC+0',
      0,
      0,
      0,
      2,
      2
    );
  EXCEPTION WHEN others THEN
    NULL;
  END;
$$ LANGUAGE plpgsql;
# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Andrei Netedu <andrei.netedu2009@gmail.com>

from DB.Entities import Submission, Job


class SubmissionRepository:
    @staticmethod
    def get_by_id(session, id):
        """
        Gets a submission by its id
        :param session:
        :param id:
        :return: a submission entity
        """
        if isinstance(id, int):
            return session.query(Submission).filter(Submission.id == id).one()
        raise ValueError("id must be integer")

    def get_by_participation_id(session,
                                participation_id, problem_id=None):
        """
        Gets all the submissions for a specific participation
        a participation is a relation between a user and a contests
        :param participation_id:
        :param problem_id:
        :return: a list of submissions
        """
        if isinstance(participation_id, int):
            if isinstance(problem_id, int):
                return session.query(Submission) \
                    .filter(Submission.participation_id == participation_id) \
                    .filter(Submission.problem_id == problem_id) \
                    .all()
            elif problem_id is None:
                return session.query(Submission)\
                    .filter(Submission.participation_id == participation_id)\
                    .all()
            else:
                raise ValueError("problem_id must be integer")
        raise ValueError("participation_id must be integer")

    def get_status(session, submission_id):
        """
        Gets the status of a current submission
        :param submission_id:
        :return: String: with can be a number of status messages
        """
        jobs = session.query(Job)\
            .filter(Job.submission_id == submission_id)\
            .all()

        # Default values.
        # Show cpu and memory only if full evaluation.
        message = 'ACCEPTED!'
        cpu = 0
        memory = 0

        for job in jobs:
            if job.job_type == 'Compile' and job.status != 2:
                return 'COMPILING', "", ""
            elif job.job_type == 'Compile' and job.status == 2:
                if job.status_code != 0:
                    return 'COMPILATION FAILED', "", ""
            elif job.job_type == 'Evaluate' and job.status == 1:
                return 'EVALUATING', "", ""
            elif job.job_type == 'Evaluate' and job.status == 2:
                if job.status_code != 0:
                    message = job.status_message
                cpu = max(job.cpu, cpu)
                memory = max(job.memory, memory)

        return message, str(cpu), str(memory)

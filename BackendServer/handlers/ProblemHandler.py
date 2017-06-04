# Copyright © 2017 Valentin Rosca <rosca.valentin2012@gmail.com>
# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>

import os
from BackendServer.handlers.BaseHandler import BaseHandler
import tornado.web

from DB.Repositories import ProblemRepository


class ProblemHandler(BaseHandler):
    """Tornado handler for a problem."""
    def data_received(self, chunk):
        pass

    def get(self):
        """
        Tornado Request handler for a problem.
        The first path of the url is '/problem'
        The problem name must be the second path of the url.
        The page for a required problem is the third part of the url:
        '/statement' - See the statement and editor.
        '/comments' - Comments section.
        '/submission' - Submissions for this problem.
        '/editorial' - Editorial for this problem.
        '/pdf?id=<number>' - The statement number to fetch


        """
        path_elements = [x for x in self.request.path.split("/") if x]
        problem_name = path_elements[1]

        session = self.acquire_sql_session()
        problem = ProblemRepository.get_by_name(session, problem_name)
        session.close()

        if problem is None:
            raise tornado.web.HTTPError(404)

        if len(path_elements) <= 2:
            self.redirect(os.path.join(self.request.path, "statement"))
            return
        if len(path_elements) >= 4:
            self.redirect("..")
            return
        pdf_id = self.get_argument("id", None)
        if pdf_id is None:
            pdf_id = 0  # Defaults to the first statement
        else:
            pdf_id = int(pdf_id)

        # Avoid out of bounds and get the first item
        if problem.statements is not None and \
           (pdf_id >= len(problem.statements) or pdf_id < 0):
            pdf_id = 0

        if path_elements[2] == 'pdf':
            if problem.statements is not None and \
                            pdf_id < len(problem.statements):
                # Set application type
                self.set_header("Content-Type",
                                'application/pdf; charset="utf-8"')

                # The actual file headers
                self.set_header("Content-Disposition",
                                "inline; filename=statement.pdf")

                # File content
                self.write(problem.statements[pdf_id])
                return
            return

        if path_elements[2] not in ["statement",
                                    "submissions",
                                    "editorial",
                                    "comments"]:
            self.redirect("statement")

        self.render("problem_" +
                    path_elements[2] +
                    ".html", problem=problem,
                    pdf_id=pdf_id)

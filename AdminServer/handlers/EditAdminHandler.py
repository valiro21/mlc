# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
# Copyright © 2017 Cosmin Pascaru <cosmin.pascaru2@gmail.com>
import traceback

import tornado.web
import bcrypt

from tornado.web import HTTPError
from AdminServer.handlers.BaseHandler import BaseHandler
from DB.Entities.Permission import Permission
from DB.Entities.Admin import Admin
from DB.Entities.Admin_Permission import AdminPermission


class EditAdminHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.redirect("r/")

    @tornado.web.authenticated
    def post(self):

        # Get request arguments
        username = self.get_argument('username', '')
        new_name = self.get_argument('name', '')
        new_email = self.get_argument('email', '')
        new_pass = self.get_argument('password', '')
        new_pass_confirmation = self.get_argument('password_confirmation', '')
        new_permissions = []

        try:
            session = self.acquire_sql_session()
        except:
            raise HTTPError(500, 'Could not acquire session for database')

        """
            Go through all the permissions in the DB see if they were
            picked or not then store the IDs of all those permissions
        """

        try:
            query = session.query(Permission)
            permissions = session.execute(query)

            for permission in permissions:
                current_permission = permission[1]
                check = self.get_argument(current_permission, '')
                if check != '':
                    new_permissions.append(permission[0])

            """
                Delete all existing permission for the admin
                after which we set the new ones
            """

            admin_id = session.query(Admin)\
                .filter(Admin.username == username)\
                .one_or_none()
            admin_id = admin_id.id

            query = session.query(AdminPermission)\
                .filter(AdminPermission.admin_id == admin_id)

            for row in query:
                session.delete(row)

            for permission in new_permissions:
                new_permission = AdminPermission(
                    permission_id=permission,
                    admin_id=admin_id
                )
                session.add(new_permission)

            """
                Get the selected admin update the rest of the values
                not before some minimal error checking
            """

            selected_admin = session.query(Admin)\
                .filter(Admin.id == admin_id)\
                .one_or_none()

            if new_name != '':
                selected_admin.name = new_name

            if new_email != '':
                selected_admin.email = new_email

            if new_pass == new_pass_confirmation and new_pass != '':
                selected_admin.password = \
                    bcrypt.hashpw(new_pass.encode('utf8'),
                                  bcrypt.gensalt()).decode('utf8')

            session.commit()
        except:
            traceback.print_exc()
            raise HTTPError(500, 'Error editing admin.')

        self.redirect(r"/admin_list")
        session.close()

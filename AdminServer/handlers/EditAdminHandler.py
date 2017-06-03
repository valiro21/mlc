# Copyright © 2017 Alexandru Miron <mironalex96@gmail.com>
import tornado.web
import bcrypt

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
        username = self.get_argument('username', '')
        new_name = self.get_argument('name', '')
        new_email = self.get_argument('email', '')
        new_pass = self.get_argument('password', '')
        new_pass_confirmation = self.get_argument('password_confirmation', '')
        new_permissions = []

        """
             Go through all the permissions in the DB see if they were picked or not
            then store the IDs of all those permissions
        """

        querry = self.session.query(Permission)
        permissions = self.session.execute(querry)

        for permission in permissions:
            current_permission = permission[1]
            check = self.get_argument(current_permission, '')
            if check != '':
                new_permissions.append(permission[0])

        """
            Delete all existing permission for the admin after which we set the new ones
        """

        admin_id = self.session.query(Admin).filter(Admin.username == username).one_or_none()
        admin_id = admin_id.id

        query = self.session.query(AdminPermission).filter(AdminPermission.admin_id == admin_id)

        for row in query:
            self.session.delete(row)

        for permission in new_permissions:
            new_permission = AdminPermission(
                permission_id=permission,
                admin_id=admin_id
            )
            self.session.add(new_permission)

        """
            Get the selected admin update the rest of the values not before some minimal
            error checking
        """

        selected_admin = self.session.query(Admin).filter(Admin.id == admin_id).one_or_none()

        if new_name != '':
            selected_admin.name = new_name

        if new_email != '':
            selected_admin.email = new_email

        if new_pass == new_pass_confirmation and new_pass != '':
            selected_admin.password = bcrypt.hashpw(new_pass.encode('utf8'),
                                                    bcrypt.gensalt()).decode('utf8')

        self.session.commit()

        self.redirect(r"/admin_list")
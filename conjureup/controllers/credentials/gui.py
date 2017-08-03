from os import path

import yaml

from conjureup import controllers, juju, utils
from conjureup.app_config import app
from conjureup.models.provider import SchemaErrorUnknownCloud
from conjureup.ui.views.credentials import (
    CredentialPickerView,
    NewCredentialView
)

from . import common


class CredentialsController(common.BaseCredentialsController):
    def render(self):
        if app.provider.cloud_type == 'localhost':
            # no credentials required for localhost
            self.finish(None)
        elif not app.provider.credential:
            self.render_form()
        elif len(self.credentials) >= 1:
            self.render_picker()
        else:
            self.finish(self.default_credential)

    def render_form(self):
        view = NewCredentialView(app.provider, self.save_credential, self.back)
        view.show()

    def render_picker(self):
        view = CredentialPickerView(self.credentials, self.default_credential,
                                    self.finish, self.switch, self.back)
        view.show()

    def switch(self):
        self.was_picker = True
        self.render_form()

    def back(self):
        if self.was_picker:
            # if they were on the picker and chose New, BACK should
            # take them back to the picker, not to the cloud selection
            self.was_picker = False
            return self.render_picker()
        return controllers.use('regions').render(back=True)

    def _format_creds(self, creds):
        """ Formats the credentials into strings from the widgets values
        """
        formatted = {}
        formatted['auth-type'] = creds.auth_type
        for field in creds.fields():
            if not field.storable:
                continue
            formatted[field.key] = field.value

        return formatted

    def save_credential(self, credential):
        cred_path = path.join(utils.juju_path(), 'credentials.yaml')
        cred_name = "conjure-{}-{}".format(app.provider.cloud,
                                           utils.gen_hash())

        try:
            existing_creds = yaml.safe_load(open(cred_path))
        except:
            existing_creds = {'credentials': {}}

        if app.provider.cloud in existing_creds['credentials'].keys():
            c = existing_creds['credentials'][app.provider.cloud]
            c[cred_name] = self._format_creds(credential)
        else:
            # Handle the case where path exists but an entry for the cloud
            # has yet to be added.
            existing_creds['credentials'][app.provider.cloud] = {
                cred_name: self._format_creds(credential)
            }

        with open(cred_path, 'w') as cred_f:
            cred_f.write(yaml.safe_dump(existing_creds,
                                        default_flow_style=False))

        # if it's a new MAAS or VSphere cloud, save it now that
        # we have a credential
        if app.provider.cloud_type in ['maas', 'vsphere']:
            try:
                juju.get_cloud(app.provider.cloud)
            except SchemaErrorUnknownCloud:
                juju.add_cloud(app.provider.cloud,
                               app.provider.cloud_config())

        # This should return the credential name so juju bootstrap knows
        # which credential to bootstrap with
        self.finish(cred_name)


_controller_class = CredentialsController

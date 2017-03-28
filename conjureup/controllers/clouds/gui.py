from conjureup import controllers, juju
from conjureup.app_config import app
from conjureup.telemetry import track_event, track_screen
from conjureup.ui.views.cloud import CloudView


class CloudsController:
    def finish(self, cloud=None, back=False):
        """ Once a cloud is picked, move on to naming a model

        Arguments:
        cloud: Cloud to create the controller/model on.
        """
        if back:
            return controllers.use('controllerpicker').render()
        app.current_cloud = cloud
        track_event("Cloud selection", app.current_cloud, "")
        return controllers.use('modelpicker').render()

    def render(self):
        "Pick or create a cloud to bootstrap a new controller on"
        track_screen("Cloud Select")
        clouds = juju.get_compatible_clouds()
        excerpt = app.config.get(
            'description',
            "Please select from a list of available clouds")
        view = CloudView(app,
                         clouds,
                         cb=self.finish)

        app.ui.set_header(
            title="Choose a Cloud",
            excerpt=excerpt
        )
        app.ui.set_body(view)
        app.ui.set_footer('Please press [ENTER] on highlighted '
                          'Cloud to proceed.')


_controller_class = CloudsController

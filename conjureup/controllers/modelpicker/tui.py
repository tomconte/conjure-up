"""
For headless mode, just generate a new model name and move on
"""
from conjureup.app_config import app
from conjureup import controllers, utils


class ModelPicker:
    def finish(self):
        return controllers.use('newcloud').render()

    def render(self):
        if app.argv.model:
            app.current_model = app.argv.model
        else:
            app.current_model = app.config['metadata'].get(
                'suggested-model',
                utils.gen_model_name())
        self.finish()


_controller_class = ModelPicker

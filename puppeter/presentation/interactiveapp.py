from puppeter.container import Named
from puppeter.presentation.app import App


@Named('interactive')
class InteractiveApp(App):

    def __init__(self, options):
        App.__init__(self, options)

    def _collect_answers(self):
        raise NotImplementedError('Not yet implemented!')

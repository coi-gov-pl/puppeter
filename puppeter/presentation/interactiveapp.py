from puppeter.presentation.app import App


class InteractiveApp(App):

    def __init__(self, options):
        App.__init__(self, options)

    def _collect_answers(self):
        raise NotImplementedError('Not yet implemented!')

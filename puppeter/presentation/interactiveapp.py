from puppeter.presentation.app import App


class InteractiveApp(App):

    def __init__(self, parsed):
        App.__init__(self, parsed)

    def _collect_answers(self):
        raise NotImplementedError('Not yet implemented!')

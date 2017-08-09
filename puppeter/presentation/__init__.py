from puppeter import container
from puppeter.domain.gateway.answers import AnswersProcessor
from puppeter.presentation.answersprocessor import AnswersProcessorImpl
from puppeter.presentation.app import App
from puppeter.presentation.interactiveapp import InteractiveApp
from puppeter.presentation.unattendedapp import UnattendedApp

container.bind(AnswersProcessor, AnswersProcessorImpl)
container.bind(App, InteractiveApp)
container.bind(App, UnattendedApp)

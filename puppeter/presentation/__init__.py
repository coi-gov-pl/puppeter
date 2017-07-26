from puppeter import container
from puppeter.domain.gateway.answers import AnswersProcessor
from puppeter.presentation.answersprocessor import AnswersProcessorImpl

container.bind(AnswersProcessor, AnswersProcessorImpl)

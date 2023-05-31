from chatterbot.logic import LogicAdapter
import logging
from chatterbot import languages
from chatterbot.conversation import Statement
from datetime import datetime
class TemperatureAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.api_key = kwargs.get('api_key')
    def can_process(self, statement):
        """
        Return true if the input statement contains
        'what' and 'is' and 'temperature'.
        """
        words = ['what', 'is', 'temperature']
        if all(x in statement.text.split() for x in words):
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement
        import random
        import requests
        import socket

        host_name = socket.gethostname()
        host_ip = socket.gethostbyname()
        
        # Make a request to the temperature API
        response = requests.get('http:/{}/temperature-motion'.format(host_ip))
        data = response.json()
        # Let's base the confidence value on if the request was successful
        if response.status_code == 200:
            confidence = 1
        else:
            confidence = 0
        temperature = data.get('temperature', 'unavailable')

        response_statement = Statement(text='The current temperature is {}'.format(temperature))

        return confidence, response_statement
class MathematicalAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.language = kwargs.get('language',languages.TUR)
        self.cache = {}
    def can_process(self,statement):
        response = self.process(statement)
        self.cache[statement.text] = response
        return response.confidence == 1
    def process(self,statement, additional_response_selection_parameters=None):
        from chatterbot.conversation import Statement
        from mathparse import mathparse
        input_text = statement.text
        # Use the result cached by the process method if it exists
        if input_text in self.cache:
            cached_result = self.cache[input_text]
            self.cache = {}
            return cached_result

        # Getting the mathematical terms within the input statement
        expression = mathparse.extract_expression(input_text, language=self.language.ISO_639.upper())

        response = Statement(text=expression)

        try:
            response.text = '{} = {}'.format(
                response.text,
                mathparse.parse(expression, language=self.language.ISO_639.upper())
            )
            # The confidence is 1 if the expression could be evaluated
            response.confidence = 1
        except mathparse.PostfixTokenEvaluationException:
            response.confidence = 0

        return response
class CyclopLightsLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs) 
        try:
            from nltk import NaiveBayesClassifier
        except ImportError:
            message = (
                'Unable to import "nltk".\n'
                'Please install "nltk" before using the TimeLogicAdapter:\n'
                'pip3 install nltk'
            )
            raise Exception(message)  
        self.positive = kwargs.get('positive',[
            'Işıkları açabilir misin ?',
            'Işıkları kapatabilir misin ?',
            'Güçlü ışıkları aç',
            'Işıkları güçlendir',
            'Işıkları yak'
        ])
        self.negative = kwargs.get('negative',[
            'Işıklar şarkısını aç',
            'Işıklar söndü galiba',
            'Işık Hanımı ara',
            'Işığı ara'
        ])
        labeled_data = (
            [
                (name, 0) for name in self.negative
            ] + [
                (name, 1) for name in self.positive
            ]
        )  
        train_set = [
            (self.logic_question_features(text), n) for (text, n) in labeled_data
        ]

        self.classifier = NaiveBayesClassifier.train(train_set)
    def logic_question_features(self, text):

        """
        Provide an analysis of significant features in the string.
        """
        features = {}

        # A list of all words from the known sentences
        all_words = " ".join(self.positive + self.negative).split()

        # A list of the first word in each of the known sentence
        all_first_words = []
        for sentence in self.positive + self.negative:
            all_first_words.append(
                sentence.split(' ', 1)[0]
            )
        if "kapa" or "kapatır" or "kapatabilir"in text:
            self.condition = "Kapatılıyor"
        if "aç" or "açar" or "açabilir" in text:
            self.condition = "Açılıyor"
        for word in text.split():
            features['first_word({})'.format(word)] = (word in all_first_words)

        for word in text.split():
            features['contains({})'.format(word)] = (word in all_words)

        for letter in 'abcdefghijklmnopqrstuvwxyz':
            features['count({})'.format(letter)] = text.lower().count(letter)
            features['has({})'.format(letter)] = (letter in text.lower())

        return features 
    def process(self, statement, additional_response_selection_parameters=None):
        now = datetime.now()

        time_features = self.logic_question_features(statement.text.lower())
        confidence = self.classifier.classify(time_features)
        
        response = Statement(text='Tabiki ışıklar {}'.format(self.condition) )

        response.confidence = confidence
        return response
class TimeLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        try:
            from nltk import NaiveBayesClassifier
        except ImportError:
            message = (
                'Unable to import "nltk".\n'
                'Please install "nltk" before using the TimeLogicAdapter:\n'
                'pip3 install nltk'
            )
            raise Exception(message)

        self.positive = kwargs.get('positive', [
            'Saat kaç',
            'Cyclop saat kaç',
            'Saati söyleyebilir misin ?',
            'Saati biliyor musun',
            'Cyclop saatin kaç olduğunu söyle'
        ])

        self.negative = kwargs.get('negative', [
            'Saat almam lazım',
            'Saatimin pili bitti',
            'Saate alarm kurabilir misin',
            'Saat kulesini bul',
            'Boş saatin var mı',
            'Saatte çok geç olmuş'
        ])

        labeled_data = (
            [
                (name, 0) for name in self.negative
            ] + [
                (name, 1) for name in self.positive
            ]
        )

        train_set = [
            (self.time_question_features(text), n) for (text, n) in labeled_data
        ]

        self.classifier = NaiveBayesClassifier.train(train_set)
    def time_question_features(self, text):
        """
        Provide an analysis of significant features in the string.
        """
        features = {}

        # A list of all words from the known sentences
        all_words = " ".join(self.positive + self.negative).split()

        # A list of the first word in each of the known sentence
        all_first_words = []
        for sentence in self.positive + self.negative:
            all_first_words.append(
                sentence.split(' ', 1)[0]
            )

        for word in text.split():
            features['first_word({})'.format(word)] = (word in all_first_words)

        for word in text.split():
            features['contains({})'.format(word)] = (word in all_words)

        for letter in 'abcdefghijklmnopqrstuvwxyz':
            features['count({})'.format(letter)] = text.lower().count(letter)
            features['has({})'.format(letter)] = (letter in text.lower())

        return features

    def process(self, statement, additional_response_selection_parameters=None):
        now = datetime.now()

        time_features = self.time_question_features(statement.text.lower())
        confidence = self.classifier.classify(time_features)
        response = Statement(text='Saat şu an ' + now.strftime('%I:%M %p'))

        response.confidence = confidence
        return response
    
class CyclopStorageAdapter(object):
    """
    This is an abstract class that represents the interface
    that all storage adapters should implement.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize common attributes shared by all storage adapters.

        :param str tagger_language: The language that the tagger uses to remove stopwords.
        """
        self.logger = kwargs.get('logger', logging.getLogger(__name__))

        self.tagger = PosLemmaTagger(language=kwargs.get(
            'tagger_language', languages.ENG
        ))

    def get_model(self, model_name):
        """
        Return the model class for a given model name.

        model_name is case insensitive.
        """
        get_model_method = getattr(self, 'get_%s_model' % (
            model_name.lower(),
        ))

        return get_model_method()

    def get_object(self, object_name):
        """
        Return the class for a given object name.

        object_name is case insensitive.
        """
        get_model_method = getattr(self, 'get_%s_object' % (
            object_name.lower(),
        ))

        return get_model_method()

    def get_statement_object(self):
        from chatterbot.conversation import Statement

        StatementModel = self.get_model('statement')

        Statement.statement_field_names.extend(
            StatementModel.extra_statement_field_names
        )

        return Statement

    def count(self):
        """
        Return the number of entries in the database.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `count` method is not implemented by this adapter.'
        )

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements where the response text matches
        the input text.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `remove` method is not implemented by this adapter.'
        )

    def filter(self, **kwargs):
        """
        Returns a list of objects from the database.
        The kwargs parameter can contain any number
        of attributes. Only objects which contain
        all listed attributes and in which all values
        match for all listed attributes will be returned.

        :param page_size: The maximum number of records to load into
            memory at once when returning results.
            Defaults to 1000

        :param order_by: The field name that should be used to determine
            the order that results are returned in.
            Defaults to None

        :param tags: A list of tags. When specified, the results will only
            include statements that have a tag in the provided list.
            Defaults to [] (empty list)

        :param exclude_text: If the ``text`` of a statement is an exact match
            for the value of this parameter the statement will not be
            included in the result set.
            Defaults to None

        :param exclude_text_words: If the ``text`` of a statement contains a
            word from this list then the statement will not be included in
            the result set.
            Defaults to [] (empty list)

        :param persona_not_startswith: If the ``persona`` field of a
            statement starts with the value specified by this parameter,
            then the statement will not be returned in the result set.
            Defaults to None

        :param search_text_contains: If the ``search_text`` field of a
            statement contains a word that is in the string provided to
            this parameter, then the statement will be included in the
            result set.
            Defaults to None
        """
        raise self.AdapterMethodNotImplementedError(
            'The `filter` method is not implemented by this adapter.'
        )

    def create(self, **kwargs):
        """
        Creates a new statement matching the keyword arguments specified.
        Returns the created statement.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `create` method is not implemented by this adapter.'
        )

    def create_many(self, statements):
        """
        Creates multiple statement entries.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `create_many` method is not implemented by this adapter.'
        )

    def update(self, statement):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `update` method is not implemented by this adapter.'
        )

    def get_random(self):
        """
        Returns a random statement from the database.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `get_random` method is not implemented by this adapter.'
        )

    def drop(self):
        """
        Drop the database attached to a given adapter.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `drop` method is not implemented by this adapter.'
        )

    class EmptyDatabaseException(Exception):

        def __init__(self, message=None):
            default = 'The database currently contains no entries. At least one entry is expected. You may need to train your chat bot to populate your database.'
            super().__init__(message or default)

    class AdapterMethodNotImplementedError(NotImplementedError):
        """
        An exception to be raised when a storage adapter method has not been implemented.
        Typically this indicates that the method should be implement in a subclass.
        """
        pass
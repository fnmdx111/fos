# encoding: utf-8
from pattern import Pattern


class QED(BaseException):

    __QED__ = 'Q.E.D.'

    @classmethod
    def evaluate(cls, _):
        return cls.__QED__


class Paradox(BaseException):
    pass


class If:
    def __init__(self, predicate):
        if isinstance(predicate, str):
            self.predicate = Pattern(predicate)
        else:
            self.predicate = predicate
        self.predicate_assertion = True
        self.deduction = Pattern('')

    def is_(self, v):
        self.predicate_assertion = v
        return self

    def then(self, deduction):
        if isinstance(deduction, str):
            self.deduction = Pattern(deduction)
        else:
            self.deduction = deduction
        return self

    def deduct(self, input_):
        refs, successful = self.predicate.match(input_)
        if self.predicate_assertion and successful:
            return self.deduction.evaluate(refs)
        else:
            raise Paradox

    def __str__(self):
        return 'if %s then %s' % (self.predicate, self.deduction)


class Axiom(If):
    def __init__(self, predicate):
        super(Axiom, self).__init__(predicate)
        self.deduction = QED

    def then(self, _):
        raise Paradox('An axiom is always true.')

    def deduct(self, _):
        raise QED

    def __str__(self):
        return str(self.predicate)

# encoding: utf-8
import re

class Pattern:
    def __init__(self, pattern, preprocess=True, wildcard=r'[\w-]'):
        self._original_pat = pattern
        self._back_refs = {}
        self._pattern = re.compile('')
        if preprocess:
            pat, self._back_refs = Pattern._preprocess(pattern,
                                                       '(%s+)' % wildcard)
            self._pattern = re.compile(pat)

    @staticmethod
    def _preprocess(pat, variable_regex):
        first_appearances = []

        for i, c in enumerate(pat):
            if c.isalnum():
                if c.islower():
                    # c is variable
                    first_appearances.append((i, c))
                else:
                    pass
            else:
                pass

        back_refs = {}
        len_var_regex = len(variable_regex)
        for num, (i, c) in enumerate(first_appearances):
            # if 'x' of 'yxyQxT-x-' gets replaced:
            # y    x    y    Q    x    T    -    x    -
            # 0    1    2    3    4    5    6    7    8
            # y    (-+) y    Q    \1   T    -    \1   -
            # 0    1234 5    6    78   9    A    BC   D
            back_ref_regex = r'\%d' % (num + 1)
            back_refs[num] = c
            split_point = i + len_var_regex
            pat = pat.replace(c, variable_regex, 1)
            pat = ''.join((pat[:split_point],
                           pat[split_point:].replace(c, back_ref_regex)))

        return '^%s$' % pat, back_refs

    def match(self, input_):
        match = re.fullmatch(self._pattern, input_)
        ret, successful = {}, bool(match)
        if successful:
            for i, s in enumerate(match.groups()):
                ret[self._back_refs[i]] = s
        return ret, successful

    def evaluate(self, refs):
        ret = self._original_pat
        for name, val in refs.items():
            ret = ret.replace(name, val)
        return ret

    def __str__(self):
        return self._original_pat

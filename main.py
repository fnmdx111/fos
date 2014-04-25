# encoding: utf-8
from rule import Axiom, If, Paradox

if __name__ == '__main__':

    rules = [If('xQyTz').then('xyQyTz-'), If('xQy-Tz-').then('Cx')]

    start = str(Axiom('--Q--T-'))
    end = 'C----------'

    print('beginning deduction: start: %s, end %s' % (start, end))
    print('rules are: %s' % ', '.join(map(str, rules)))

    stack = [start]
    while stack:
        _ = stack.pop(0)
        if _ == end:
            print('found Cx: %s. Q.E.D.' % _)
            break

        for rule in rules:
            rule_str = str(rule.predicate)
            try:
                current = rule.deduct(_)
            except Paradox:
                print('cannot apply %s to %s' % (_, rule_str))
                continue

            print('%s =[%s]=> %s' % (_, rule_str, current))
            stack.append(current)

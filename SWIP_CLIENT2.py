from pengines.Builder import PengineBuilder
from pengines.Pengine import Pengine
from prologterms import TermGenerator, PrologRenderer, Program, Var, Rule

src_context = 'knows(alice, david).\n'
src_context += '{}(X,Y) :- {}(Y,X).'.format('knows', 'knows')

P = TermGenerator()
X = Var('X')
Y = Var('Y')
Z = Var('Z')
R = PrologRenderer()

rule1 = Rule(P.knowsb(X, Y), P.knowsf(Y, X))
rule2 = Rule(P.knows(X, Y), P.knowsb(Y, X))
rule3 = Rule(P.knows(X, Y), P.knowsf(Y, X))
p = Program(
    rule1,
    rule2,
    rule3,
    P.knowsf('alice', 'david'),
)

q = P.knows(X, Y)

factory = PengineBuilder(urlserver="http://localhost:4242",
                         srctext=R.render(p),
                         ask=R.render(q))
pengine = Pengine(builder=factory, debug=False)
while pengine.currentQuery.hasMore:
    pengine.doNext(pengine.currentQuery)
for p in pengine.currentQuery.availProofs:
    print('{} <- {}'.format(p[X.name], p[Y.name]))

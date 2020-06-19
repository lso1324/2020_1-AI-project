
#const limit=10.

x(1..limit).
y(1..limit).

color(w;b).

map(f(X,Y)) :- x(X), y(Y).

island(f(1,4),1).
island(f(1,7),5).
island(f(2,3),2).
island(f(2,8),2).
island(f(4,4),10).
island(f(4,7),1).
island(f(7,4),4).
island(f(7,7),2).
island(f(9,3),2).
island(f(9,8),7).
island(f(10,4),1).
island(f(10,7),2).

text(Z,N) :- island(Z,N).


{cell(w,f(X,Y))} :- x(X), y(Y).
cell(b,f(X,Y)) :- not cell(w,f(X,Y)), x(X), y(Y).

:- cell(b,C1), island(C1,N).


isConnected(C1) :-  connected(w,C1,C2), cell(w,C1), island(C2,N).
:- cell(w,C1), not isConnected(C1).

yadj(f(X,Y),f(X,Y+1)) :- x(X), y(Y), y(Y+1).
xadj(f(X,Y),f(X+1,Y)) :- x(X), y(Y), x(X+1).
yadj(A,B) :- yadj(B,A).
xadj(A,B) :- xadj(B,A).

adj(f(C,R),f(C1,R1)) :- xadj(f(C,R),f(C1,R1)).
adj(f(C,R),f(C1,R1)) :- yadj(f(C,R),f(C1,R1)).

connected(C,C1,C1) :- cell(C,C1), color(C).
connected(C,C1,C2) :- connected(C,C1,C3), adj(C3,C2), cell(C,C2), color(C).

:- island(f(X,Y),N), island(f(U,V),M), X<U, connected(w,f(X,Y),f(U,V)).
:- island(f(X,Y),N), island(f(U,V),M), Y<V, connected(w,f(X,Y),f(U,V)).

island(C1) :- N {connected(w,C1,C2):x(U),y(V)} N, island(C1,N).
:- not island(C1), island(C1,N).


:- not connected(b,C1,C2), cell(b,C1), cell(b,C2).

:- blackpool(X,Y), x(X), y(Y).
blackpool(X,Y) :- cell(b,f(X+1,Y)), cell(b,f(X,Y)), cell(b,f(X, Y+1)), cell(b,f(X+1, Y+1)), x(X), y(Y).

pool(C1) :- cell(b,C1).

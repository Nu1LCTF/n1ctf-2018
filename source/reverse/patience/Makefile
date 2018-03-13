
all:
	python generate.py > src/flag.h
	stack ghc -- -ddump-cmm src/Main.hs > distrib/dump.cmm
	rm src/Main.hi src/Main.o src/Main
	stack build

test:
	python generate.py test > src/flag.h
	stack build

clean:
	rm src/flag.h
	stack clean

NAME = pp
CC = g++
SRC = src/core src/utilities
DEPS = $(wildcard $(patsubst %,%/*.h,$(SRC))) Parameters.h makefile
CODE = $(wildcard $(patsubst %,%/*.cpp,$(SRC)))
OBJ = $(patsubst %.cpp,%.o,$(CODE))
LINK_FLAGS = -lboost_program_options

COMP_FLAGS = -O2 -std=c++11 -pedantic -m64 -fPIC -fno-strict-aliasing -fexceptions -DNDEBUG -DIL_STD
DATA = COPYING INSTALL makefile README

.PHONY: install clean dist-gzip dist-bzip2 dist
.SILENT: $(NAME) install clean dist-gzip dist-bzip2 dist

%.o: %.cpp $(DEPS)
	$(CC) $(COMP_FLAGS) -c -o $@ $<

$(NAME): $(OBJ)
	$(CC) -o $@ $^ $(LINK_FLAGS)
	echo "$(NAME) build!"

install: $(NAME)
	mv $(NAME) /usr/bin
	echo "$(NAME) installed!"

clean:
	rm -f $(patsubst %,%/*.o,$(SRC)) $(patsubst %,%/*~,$(SRC)) *~

dist-gzip: clean
	tar --format=posix --transform 's,^,$(NAME)/,' -czf $(NAME).tar.gz $(SRC) $(DATA)

dist-bzip2: clean
	tar --format=posix --transform 's,^,$(NAME)/,' -cjf $(NAME).tar.bz2 $(SRC) $(DATA)

dist: dist-bzip2

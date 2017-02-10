#Makefile for compilations
all:
	$(MAKE) -C bin ex_parser

run:
	@echo "Run the executables"

clean:
	$(MAKE) -C bin clean

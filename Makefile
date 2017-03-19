#Makefile for compilations
all:
	@clear
	$(MAKE) -C bin covgen

test:
	@clear
	$(MAKE) -C bin test

decode:
	@clear
	$(MAKE) -C bin decode

simple:
	@clear
	$(MAKE) -C bin simple

dataflow:
	$(MAKE) -C bin dataflow

run:
	@echo "Run the executables"

clean:
	$(MAKE) -C bin clean

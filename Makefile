#Makefile for compilations
all:
	@clear
	$(MAKE) -C bin covgen
ccu:
	@clear
	$(MAKE) -C bin ccu

ccx:
	@clear
	$(MAKE) -C bin ccx

test:
	@clear
	$(MAKE) -C bin test

amber:
	@clear
	$(MAKE) -C bin amber

data_test:
	@clear
	$(MAKE) -C bin data_test

decode:
	@clear
	$(MAKE) -C bin decode

opensparc:
	@clear
	$(MAKE) -C bin opensparc

simple:
	@clear
	$(MAKE) -C bin simple

dataflow:
	@clear
	$(MAKE) -C bin dataflow

fifos:
	@clear
	$(MAKE) -C bin fifos

i2c:
	@clear
	$(MAKE) -C bin i2c

ex_dataflow:
	@clear
	$(MAKE) -C bin ex_dataflow

run:
	@echo "Run the executables"

clean:
	$(MAKE) -C bin clean

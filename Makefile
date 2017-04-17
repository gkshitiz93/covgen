#Makefile for compilations
wishbone:
	@clear
	$(MAKE) -C bin wishbone
	rm -rf results/wishbone
	cp -r bin results/wishbone
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
	rm -rf results/amber
	cp -r bin results/amber

data_test:
	@clear
	$(MAKE) -C bin data_test

decode:
	@clear
	$(MAKE) -C bin decode

opensparc:
	@clear
	$(MAKE) -C bin opensparc
	rm -rf results/opensparc
	cp -r bin results/opensparc

simple:
	@clear
	$(MAKE) -C bin simple
	rm -rf results/simple
	cp -r bin results/simple

dataflow:
	@clear
	$(MAKE) -C bin dataflow

fifos:
	@clear
	$(MAKE) -C bin fifos
	rm -rf results/fifos
	cp -r bin results/fifos

i2c:
	@clear
	$(MAKE) -C bin i2c
	rm -rf results/i2c
	cp -r bin results/i2c

mesi_isc:
	@clear
	$(MAKE) -C bin mesi_isc
	rm -rf results/mesi_isc
	cp -r bin results/mesi_isc

sdram_16bit:
	@clear
	$(MAKE) -C bin sdram_16bit
	rm -rf results/sdram_16bit
	cp -r bin results/sdram_16bit

sdr_ctl:
	@clear
	$(MAKE) -C bin sdr_ctl
	rm -rf results/sdr_ctl
	cp -r bin results/sdr_ctl

ex_dataflow:
	@clear
	$(MAKE) -C bin ex_dataflow

run:
	@echo "Run the executables"

all: mesi_isc sdram_16bit sdr_ctl i2c fifos simple amber 
	#decode wishbone 
	 

clean:
	$(MAKE) -C bin clean

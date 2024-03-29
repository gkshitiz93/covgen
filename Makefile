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

vscale:
	@clear
	$(MAKE) -C bin vscale
	rm -rf results/vscale
	cp -r bin results/vscale

pid:
	@clear
	$(MAKE) -C bin pid
	rm -rf results/pid
	cp -r bin results/pid

openmsp:
	@clear
	$(MAKE) -C bin openmsp
	rm -rf results/openmsp
	cp -r bin results/openmsp

mips32:
	@clear
	$(MAKE) -C bin mips32
	rm -rf results/mips32
	cp -r bin results/mips32

mips_16:
	@clear
	$(MAKE) -C bin mips_16
	rm -rf results/mips_16
	cp -r bin results/mips_16

apbtoaes:
	@clear
	$(MAKE) -C bin apbtoaes
	rm -rf results/apbtoaes
	cp -r bin results/apbtoaes

aes-128:
	@clear
	$(MAKE) -C bin aes-128
	rm -rf results/aes-128
	cp -r bin results/aes-128

fft:
	@clear
	$(MAKE) -C bin fft
	rm -rf results/fft
	cp -r bin results/fft

reed:
	@clear
	$(MAKE) -C bin reed
	rm -rf results/reed
	cp -r bin results/reed

arb:
	@clear
	$(MAKE) -C bin arb
	rm -rf results/arb
	cp -r bin results/arb

sha3_low:
	@clear
	$(MAKE) -C bin sha3_low
	rm -rf results/sha3_low
	cp -r bin results/sha3_low

sha3_high:
	@clear
	$(MAKE) -C bin sha3_high
	rm -rf results/sha3_high
	cp -r bin results/sha3_high

wb_uart:
	@clear
	$(MAKE) -C bin wb_uart
	rm -rf results/wb_uart
	cp -r bin results/wb_uart

wb_flash:
	@clear
	$(MAKE) -C bin wb_flash
	rm -rf results/wb_flash
	cp -r bin results/wb_flash

sdr_ctl:
	@clear
	$(MAKE) -C bin sdr_ctl
	rm -rf results/sdr_ctl
	cp -r bin results/sdr_ctl

or1200:
	@clear
	$(MAKE) -C bin or1200
	rm -rf results/or1200
	cp -r bin results/or1200

or1200hp:
	@clear
	$(MAKE) -C bin or1200hp
	rm -rf results/or1200hp
	cp -r bin results/or1200hp

ex_dataflow:
	@clear
	$(MAKE) -C bin ex_dataflow

run:
	@echo "Run the executables"

all: clean amber vscale apbtoaes i2c
	#clean wb_uart wb_flash sha3_low sha3_high arb reed fft aes-128 apbtoaes mips32 mips_16 or1200 or1200hp pid vscale mesi_isc sdram_16bit sdr_ctl i2c amber 
	#openmsp 
	#opensparc 
	 

clean:
	$(MAKE) -C bin clean
	rm -rf results/
	mkdir results

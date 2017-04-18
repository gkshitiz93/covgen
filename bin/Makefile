#Makefile for execution
OPENDIR = /home/local/twin/kshitiz/coverage/rtl/OpenSPARC/design/sys/iop
FIFODIR = /home/local/twin/kshitiz/coverage/rtl/examples/fifos/generic_fifos/trunk/rtl/verilog
I2CDIR = /home/local/twin/kshitiz/coverage/rtl/examples/i2c/i2c_master_slave_core/trunk/i2c_master_slave_core/verilog/rtl
SDRDIR = /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdram_16bit/trunk/rtl
MESI=/home/local/twin/kshitiz/coverage/rtl/examples/mesi_isc/trunk/src/rtl
VSCALE=/home/local/twin/kshitiz/coverage/rtl/examples/vscale/src/main/verilog
PID=/home/local/twin/kshitiz/coverage/rtl/examples/pid/pid_controller/trunk/RTL
OR1200hp=/home/local/twin/kshitiz/coverage/rtl/examples/or1200_hp/trunk/rtl/rtl_cm4/verilog
or1200=/home/local/twin/kshitiz/coverage/rtl/examples/or1200/rtl/verilog
msp430=/home/local/twin/kshitiz/coverage/rtl/examples/openmsp/openmsp430/trunk/core/rtl/verilog
MIPS32=/home/local/twin/kshitiz/coverage/rtl/examples/mips32/mips32/trunk/Classic-MIPS/source/src
MIPS16=/home/local/twin/kshitiz/coverage/rtl/examples/mips_16/mips_16/trunk/rtl
APB2AES=/home/local/twin/kshitiz/coverage/rtl/examples/apbtoaes128/apbtoaes128/trunk/rtl
AES128DIR=/home/local/twin/kshitiz/coverage/rtl/examples/aes-128/aes-128_pipelined_encryption/trunk/rtl
FLAGS = --unique  
test: clean
	@python ../src/main.py $(FLAGS) -t top ../rtl/test.v

data_test: clean
	@python ../src/example_dataflow_analyzer.py -t top ../rtl/test.v

simple: clean
	@python ../src/main.py $(FLAGS) -t top ../rtl/simple.v

decode: clean
	@python ../src/main.py $(FLAGS) -t a25_decode ../rtl/amber25/a25_decode.v

decode_dataflow: clean
	@python ../src/example_dataflow_analyzer.py -t a25_decode ../rtl/amber25/a25_decode.v

ex_parser:
	@python ../src/example_parser.py ../rtl/amber25/a25_wishbone.v

ex_dataflow:
	@python ../src/example_dataflow_analyzer.py -t a25_core ../rtl/amber25/a25_wishbone.v 

ccu: clean
	@python ../src/main.py $(FLAGS) -t ccu $(OPENDIR)/ccu/rtl/*

ccx: clean
	@python ../src/main.py $(FLAGS) -t ccx $(OPENDIR)/ccx/rtl/*

clean:
	rm -rf SVA/

amber:clean
	@python ../src/main.py $(FLAGS) -t a25_core ../rtl/amber25/amber_covgen/*.v

wishbone: clean
	@python ../src/main.py $(FLAGS) -t top ../rtl/wishbone.v

opensparc: clean
	@python ../src/main.py -I $(OPENDIR)/../../../verif/env/common/verilog/misc -I $(OPENDIR)/../../../verif/env/fc -I $(OPENDIR)/ccu/rtl/ -I $(OPENDIR)/ccx/rtl/ -I $(OPENDIR)/cmp/rtl/ -I $(OPENDIR)/cpu/rtl/ -I $(OPENDIR)/db0/rtl/ -I $(OPENDIR)/db1/rtl/ -I $(OPENDIR)/dmu/rtl/ -I $(OPENDIR)/efu/rtl/ -I $(OPENDIR)/esr/rtl/ -I $(OPENDIR)/fsr/rtl/ -I $(OPENDIR)/fsr_bottom/rtl/ -I $(OPENDIR)/fsr_left/rtl/ -I $(OPENDIR)/fsr_right/rtl/ -I $(OPENDIR)/l2b/rtl/ -I $(OPENDIR)/l2t/rtl/ -I $(OPENDIR)/mac/rtl/ -I $(OPENDIR)/mcu/rtl/ -I $(OPENDIR)/mio/rtl/ -I $(OPENDIR)/ncu/rtl/ -I $(OPENDIR)/niu/rtl/ -I $(OPENDIR)/pcie_common/rtl/ -I $(OPENDIR)/rdp/rtl/ -I $(OPENDIR)/rst/rtl/ -I $(OPENDIR)/rtx/rtl/ -I $(OPENDIR)/sii/rtl/ -I $(OPENDIR)/sio/rtl/ -I $(OPENDIR)/spc/rtl/ -I $(OPENDIR)/tcu/rtl/ -I $(OPENDIR)/tds/rtl/ $(FLAGS) -t cpu $(OPENDIR)/cmp/rtl/*.v $(OPENDIR)/cpu/rtl/*.v $(OPENDIR)/db0/rtl/*.v $(OPENDIR)/db1/rtl/*.v $(OPENDIR)/efu/rtl/*.v $(OPENDIR)/fsr_bottom/rtl/*.v $(OPENDIR)/fsr_left/rtl/*.v $(OPENDIR)/fsr_right/rtl/*.v $(OPENDIR)/l2b/rtl/*.v $(OPENDIR)/mac/rtl/*.v $(OPENDIR)/mcu/rtl/*.v $(OPENDIR)/ncu/rtl/*.v $(OPENDIR)/rdp/rtl/*.v $(OPENDIR)/rst/rtl/*.v $(OPENDIR)/rtx/rtl/*.v $(OPENDIR)/sii/rtl/*.v $(OPENDIR)/sio/rtl/*.v $(OPENDIR)/spc/rtl/*.v $(OPENDIR)/tcu/rtl/*.v $(OPENDIR)/tds/rtl/*.v #$(OPENDIR)/ccu/rtl/*.v $(OPENDIR)/ccx/rtl/*.v $(OPENDIR)/l2t/rtl/*.v #$(OPENDIR)/dmu/rtl/*.v $(OPENDIR)/fsr/rtl/*.v  $(OPENDIR)/mio/rtl/*.v $(OPENDIR)/niu/rtl/*.v $(OPENDIR)/pcie_common/rtl/*.v $(OPENDIR)/esr/rtl/*.v 

i2c: clean
	@python ../src/main.py $(FLAGS) -I $(I2CDIR) -t core $(I2CDIR)/*.v 

sdram_16bit: clean
	@python ../src/main.py $(FLAGS) -I $(SDRDIR) -t sdram $(SDRDIR)/*.v

sdr_ctl: clean
	@python ../src/main.py $(FLAGS) -I /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdr_ctrl/trunk/rtl/top -I /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdr_ctrl/trunk/rtl/wb2sdrc -I /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdr_ctrl/trunk/rtl/lib -I /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdr_ctrl/trunk/rtl/core -t sdrc_top /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdr_ctrl/trunk/rtl/top/*.v /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdr_ctrl/trunk/rtl/wb2sdrc/*.v /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdr_ctrl/trunk/rtl/lib/*.v /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdr_ctrl/trunk/rtl/core/*.v

mesi_isc: clean
	@python ../src/main.py $(FLAGS) -I $(MESI) -t mesi_isc $(MESI)/*.v
	
aes-128: clean
	@python ../src/main.py $(FLAGS) -I $(AES128DIR) -i SBox -t Top_PipelinedCipher $(AES128DIR)/*.v
	
apbtoaes: clean
	@python ../src/main.py $(FLAGS) -I $(APB2AES) -t aes_ip $(APB2AES)/*.v
	
mips_16: clean
	@python ../src/main.py $(FLAGS) -I $(MIPS16) -t mips_16_core_top $(MIPS16)/*.v
	
mips32: clean
	@python ../src/main.py $(FLAGS) -I $(MIPS32) -t PipelineMIPS $(MIPS32)/*.v
	
openmsp: clean
	@python ../src/main.py $(FLAGS) -I $(msp430)/defines/ -t openMSP430 $(msp430)/*.v $(msp430)/periph/*.v
	
or1200: clean
	@python ../src/main.py $(FLAGS) -I $(or1200) -i or1200_spram -t or1200_top $(or1200)/*.v
	
or1200hp: clean
	@python ../src/main.py $(FLAGS) -I $(OR1200hp)/../../ -t or1200_top_cm4_top $(OR1200hp)/*.v
	
pid: clean
	@python ../src/main.py $(FLAGS) -I $(PID) -t PID $(PID)/*.v

vscale: clean
	@python ../src/main.py $(FLAGS) -I $(VSCALE) -t vscale_core $(VSCALE)/*.v

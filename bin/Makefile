#Makefile for execution
OPENDIR = /home/local/twin/kshitiz/coverage/rtl/OpenSPARC/design/sys/iop
FIFODIR = /home/local/twin/kshitiz/coverage/rtl/examples/fifos/generic_fifos/trunk/rtl/verilog
I2CDIR = /home/local/twin/kshitiz/coverage/rtl/examples/i2c/i2c_master_slave_core/trunk/i2c_master_slave_core/verilog/rtl
SDRDIR = /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdram_16bit/trunk/rtl
MESI=/home/local/twin/kshitiz/coverage/rtl/examples/mesi_isc/trunk/src/rtl
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

fifos: clean
#	@python ../src/main.py $(FLAGS) -I $(FIFODIR) -t generic_fifo_dc_gray $(FIFODIR)/*.v
#	@python ../src/main.py $(FLAGS) -I $(FIFODIR) -t generic_fifo_dc $(FIFODIR)/*.v
#	@python ../src/main.py $(FLAGS) -I $(FIFODIR) -t generic_fifo_lfsr $(FIFODIR)/*.v
#	@python ../src/main.py $(FLAGS) -I $(FIFODIR) -t generic_fifo_sc_a $(FIFODIR)/*.v
	@python ../src/main.py $(FLAGS) -I $(FIFODIR) -t generic_fifo_sc_b $(FIFODIR)/*.v

i2c: clean
	@python ../src/main.py $(FLAGS) -I $(I2CDIR) -t core $(I2CDIR)/*.v 

sdram_16bit: clean
	@python ../src/main.py $(FLAGS) -I $(SDRDIR) -t sdram $(SDRDIR)/*.v

sdr_ctl: clean
	@python ../src/main.py $(FLAGS) -I /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdr_ctrl/trunk/rtl/top -I /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdr_ctrl/trunk/rtl/wb2sdrc -I /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdr_ctrl/trunk/rtl/lib -I /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdr_ctrl/trunk/rtl/core -t sdrc_top /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdr_ctrl/trunk/rtl/top/*.v /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdr_ctrl/trunk/rtl/wb2sdrc/*.v /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdr_ctrl/trunk/rtl/lib/*.v /home/local/twin/kshitiz/coverage/rtl/examples/sdram/sdr_ctrl/trunk/rtl/core/*.v

mesi_isc: clean
	@python ../src/main.py $(FLAGS) -I $(MESI) -t mesi_isc $(MESI)/*.v
	

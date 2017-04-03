#Makefile for execution
OPENDIR = /home/local/twin/kshitiz/coverage/rtl/OpenSPARC/design/sys/iop/
covgen: clean
	@python ../src/main.py --unique --ex -t top ../rtl/wishbone.v

test: clean
	@python ../src/main.py --unique --ex -t top ../rtl/test.v

data_test: clean
	@python ../src/example_dataflow_analyzer.py -t top ../rtl/test.v

simple: clean
	@python ../src/main.py --unique --ex -t top ../rtl/simple.v

decode: clean
	@python ../src/main.py --unique --ex -t a25_decode ../rtl/amber25/a25_decode.v

decode_dataflow: clean
	@python ../src/example_dataflow_analyzer.py -t a25_decode ../rtl/amber25/a25_decode.v

ex_parser:
	@python ../src/example_parser.py ../rtl/amber25/a25_wishbone.v

ex_dataflow:
	@python ../src/example_dataflow_analyzer.py -t a25_core ../rtl/amber25/a25_wishbone.v 

ccu: clean
	@python ../src/main.py --unique --ex -t ccu $(OPENDIR)/ccu/rtl/*

ccx: clean
	@python ../src/main.py --unique --ex -t ccx $(OPENDIR)/ccx/rtl/*
	#@python ../src/main.py --unique --ex -t ccx $(CCXDIR)/cpx_mbr_dp.v $(CCXDIR)/cpx_dpsd.v $(CCXDIR)/cpx_mar_dp.v $(CCXDIR)/cpx_mal_dp.v $(CCXDIR)/cpx_rep_dp.v $(CCXDIR)/cpx_dpsc.v $(CCXDIR)/cpx.v $(CCXDIR)/ccx_srq_ctl.v $(CCXDIR)/ccx_arc_ctl.v $(CCXDIR)/cpx_dpsg.v $(CCXDIR)/ccx_arb.v $(CCXDIR)/ccx_rep.v $(CCXDIR)/pcx_dpsb.v $(CCXDIR)/pcx_dpsc.v $(CCXDIR)/pcx_dpsa.v $(CCXDIR)/cpx_ob2_dp.v $(CCXDIR)/pcx_dpa.v $(CCXDIR)/ccx_new_macro.v $(CCXDIR)/pcx_mar_dp.v $(CCXDIR)/pcx_dpsh.v $(CCXDIR)/ccx.v $(CCXDIR)/pcx_mbl_dp.v $(CCXDIR)/cpx_dpsb.v $(CCXDIR)/pcx_dpsf.v $(CCXDIR)/pcx_dpse.v $(CCXDIR)/pcx_mal_dp.v $(CCXDIR)/cpx_mbl_dp.v $(CCXDIR)/pcx_bfd_dp.v $(CCXDIR)/ccx_trep.v $(CCXDIR)/inv_diode_macro.v $(CCXDIR)/cpx_bfg_dp.v $(CCXDIR)/cpx_mcr_dp.v $(CCXDIR)/ccx_ard_dp.v $(CCXDIR)/pcx_mcr_dp.v $(CCXDIR)/pcx_mbr_dp.v $(CCXDIR)/pcx_dpsd.v $(CCXDIR)/cpx_ob1_dp.v $(CCXDIR)/ccx_l1clkhdr_ctl_macro.v $(CCXDIR)/cpx_dpa.v $(CCXDIR)/cpx_dpsf.v $(CCXDIR)/pcx_bfg_dp.v $(CCXDIR)/pcx_ob1_dp.v $(CCXDIR)/pcx_dpsg.v $(CCXDIR)/pcx.v $(CCXDIR)/cpx_dpse.v $(CCXDIR)/ccx_tstg.v $(CCXDIR)/cpx_dpsa.v $(CCXDIR)/pcx_mcl_dp.v $(CCXDIR)/cpx_mcl_dp.v $(CCXDIR)/cpx_bfd_dp.v $(CCXDIR)/pcx_rep_dp.v 

amber:clean
	@python ../src/main.py --unique --ex -t a25_core ../rtl/amber25/amber_covgen/*.v

dataflow: clean
	@python ../src/example_dataflow_analyzer.py -t ccx $(CCXDIR)/cpx_mbr_dp.v $(CCXDIR)/cpx_dpsd.v $(CCXDIR)/cpx_mar_dp.v $(CCXDIR)/cpx_mal_dp.v $(CCXDIR)/cpx_rep_dp.v $(CCXDIR)/cpx_dpsc.v $(CCXDIR)/cpx.v $(CCXDIR)/ccx_srq_ctl.v $(CCXDIR)/ccx_arc_ctl.v $(CCXDIR)/cpx_dpsg.v $(CCXDIR)/ccx_arb.v $(CCXDIR)/ccx_rep.v $(CCXDIR)/pcx_dpsb.v $(CCXDIR)/pcx_dpsc.v $(CCXDIR)/pcx_dpsa.v $(CCXDIR)/cpx_ob2_dp.v $(CCXDIR)/pcx_dpa.v $(CCXDIR)/ccx_new_macro.v $(CCXDIR)/pcx_mar_dp.v $(CCXDIR)/pcx_dpsh.v $(CCXDIR)/ccx.v $(CCXDIR)/pcx_mbl_dp.v $(CCXDIR)/cpx_dpsb.v $(CCXDIR)/pcx_dpsf.v $(CCXDIR)/pcx_dpse.v $(CCXDIR)/pcx_mal_dp.v $(CCXDIR)/cpx_mbl_dp.v $(CCXDIR)/pcx_bfd_dp.v $(CCXDIR)/ccx_trep.v $(CCXDIR)/inv_diode_macro.v $(CCXDIR)/cpx_bfg_dp.v $(CCXDIR)/cpx_mcr_dp.v $(CCXDIR)/ccx_ard_dp.v $(CCXDIR)/pcx_mcr_dp.v $(CCXDIR)/pcx_mbr_dp.v $(CCXDIR)/pcx_dpsd.v $(CCXDIR)/cpx_ob1_dp.v $(CCXDIR)/ccx_l1clkhdr_ctl_macro.v $(CCXDIR)/cpx_dpa.v $(CCXDIR)/cpx_dpsf.v $(CCXDIR)/pcx_bfg_dp.v $(CCXDIR)/pcx_ob1_dp.v $(CCXDIR)/pcx_dpsg.v $(CCXDIR)/pcx.v $(CCXDIR)/cpx_dpse.v $(CCXDIR)/ccx_tstg.v $(CCXDIR)/cpx_dpsa.v $(CCXDIR)/pcx_mcl_dp.v $(CCXDIR)/cpx_mcl_dp.v $(CCXDIR)/cpx_bfd_dp.v $(CCXDIR)/pcx_rep_dp.v 

clean:
	rm -rf SVA/

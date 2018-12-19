# Makefile for synthesis and checking
#
# 2018/02/15  Generation of dc-$(NAME).tcl completely re-written so the file
#             is automatically generated from the *.vfs file
# 2017/01/31  Many big changes to merge simulation and synthesis,
#             auto generate dc-$(NAME).tcl file, etc.
# 2016/01/27  Small tweaks for NCVerilog
# 2009/02/12  Lots of updates for new script tcl version
# 2006/01/30  Minor changes
# 2005/02/10  A number of improvements thanks to Eric Work
# 2004/02/04  Updated
# 2003/05/27  Added "tee" to save log file.  Make sure you add "exit" at the
#             end of your dc_compile script.
# 2003/05/14  Written
#
# A few notes on writing a Makefile and running it
#  - Make sure commands are preceded by a "tab"; spaces will not work!
#  - You may also add dependencies so that a command will execute only
#    if the dependency has been updated more recently than the target
#    (name the target with the same name as the output of the command(s)).
#  - Use a "-n" flag to see what make will use without running the
#    command(s).  Ex: "make -n clean"
#
# Notes for vcs:
#  -Mdir     Temporary file space; can give a big speedup
#  -Mupdate  Incremental compile
#  -PP       Enables vcs to work with vcd+ files
#  -R        Run executable after compiling and linking
#  -RI       Bring up interactive GUI after compiling and linking
#  -RPP      Run post-processing mode; starts virsim


#----- Set the top-level module name here
NAME		:= compile

#----- Some variables
USERNAME	:= $(shell whoami)
DIR_TMP		:= /tmp/$(USERNAME)verilog


#----- Targets
default:
	@echo
	@echo "Make targets. Either change module name in Makefile line 16 or add the"
	@echo "text 'NAME=xyz' after 'make' for simulation and synthesis targets below."
	@echo "  make                     print this help summary"
	@echo "  make clean               deletes some generated files"
	@echo "  make cleanall            deletes all generated files"
	@echo "Make targets for simulation"
	@echo "  make compile             compile only with .vfv and Verilog-XL"
	@echo "  make compilenc           compile only with .vfv and NCVerilog"
	@echo "  make run                 run with NCVerilog"
	@echo "  make runxl               run with Verilog-XL"
	@echo "  make viewer              start simvision"
	@echo "Make targets for synthesis"
	@echo "  make check               compile only with .vfs and Verilog-XL"
	@echo "  make checknc             compile only with .vfs and NCVerilog"
	@echo "  make synth               synthesize default module"
	@echo
	@echo "Procedure to synthesize top-level module 'xyz'"
	@echo "  1) change 'NAME := abc' to 'NAME := xyz' at top of Makefile"
	@echo "  2) add all modules to be synthesized to file xyz.vfs"
	@echo "  3) 'make check' and fix any errors"
	@echo "  4) 'make synth'"
	@echo
	@echo "Alternate procedure:"
	@echo "  1) add all modules to be synthesized to file xyz.vfs"
	@echo "  2) 'make NAME=xyz check' and fix any errors"
	@echo "  3) 'make NAME=xyz synth'"
	@echo

#----- Simulation. Put all files in a ".vfv" file.
# Compile only with NCVerilog or Verilog-XL
compile:
	verilog   -c -l $(NAME).logv -f $(NAME).vfv

compilenc:
	ncverilog -c -l $(NAME).logv -f $(NAME).vfv

# Run simulation in NCVerilog or Verilog-XL
run:
	ncverilog +access+r -l $(NAME).logv -f $(NAME).vfv

runxl:
	verilog +access+r -l $(NAME).logv -f $(NAME).vfv

# Start viewer
viewer:
	simvision &

#----- Synthesis. Put all files in a ".vfs" file.
check:
	verilog   -c -l $(NAME).logs -f $(NAME).vfs

checknc:
	ncverilog -c -l $(NAME).logs -f $(NAME).vfs

# Note: alternate top of file cmd instead of awk: sed '/BEFORE_ANALYZE_SEC.../q'
dc-$(NAME).tcl: dc-template.tcl $(NAME).vfs Makefile
	@echo "===== Making a new dc-$(NAME).tcl"
	awk '/BEFORE_ANALYZE_SECTION/ {exit} {print}' dc-template.tcl | sed 's/prac/$(NAME)/' | sed 's/dc-template.tcl/dc-$(NAME).tcl/' > dc-$(NAME).tcl
	grep -v '#' $(NAME).vfs | grep '.*\.v' | awk '{print "analyze -format verilog " $$1}' >> dc-$(NAME).tcl
	awk '/AFTER_ANALYZE_SECTION/,EOF' dc-template.tcl | grep -v 'AFTER_ANALYZE_SECTION' | sed 's/prac/$(NAME)/' >> dc-$(NAME).tcl
	@echo "===== New dc-$(NAME).tcl ready"
	@echo

synth: dc-$(NAME).tcl
	dc_shell-t -f dc-$(NAME).tcl | tee $(NAME).logs
#	@grep -v '^Warning:.*Intraassignment delays for nonblocking assignments are ignored. (VER-130)' $(NAME).logs > $(NAME).logs.clean

#----- Cleanup generated files
clean:
	rm -f  *.mr
	rm -f  *-verilog.pvl
	rm -f  *-verilog.syn
	rm -f  default.svf
	rm -f  simv
	rm -rf simv.daidir
	rm -f  vcs.key
	rm -rf simv.daidir/
	rm -rf $(DIR_TMP)
	rm -rf INCA_libs/

cleanall: clean
	rm -f $(NAME).area
	rm -f $(NAME).cell
	rm -f dc-$(NAME).tcl
	rm -f $(NAME).db
	rm -f $(NAME).hier
	rm -f $(NAME).history
	rm -f $(NAME).log
	rm -f $(NAME).logs
	rm -f $(NAME).logs.clean
	rm -f $(NAME).logv
	rm -f $(NAME).net
	rm -f $(NAME).pow
	rm -f $(NAME).tim
	rm -f $(NAME).vg
	rm -f $(NAME).dsn
	rm -f $(NAME).trn
	rm -f $(NAME).vpd
	rm -f command.log

#----- Old code
# dc-$(NAME).tcl: dc-template.tcl Makefile
# 	sed s/prac/$(NAME)/ < dc-template.tcl > dc-$(NAME).tcl

#Makefile for compilations
all:
	@clear
	$(MAKE) -C bin covgen

test:
	$(MAKE) -C bin test

data:
	$(MAKE) -C bin data

run:
	@echo "Run the executables"

clean:
	$(MAKE) -C bin clean

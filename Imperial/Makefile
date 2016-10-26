CXXFLAGS+=-std=c++11 -I/usr/include/python2.7/ -Iinclude/ -Iinclude/brickpi -I../DexterInd/BrickPi_C/Drivers/ -lwiringPi


src/brickpi.so: src/Interface_python.o  src/Interface.o  src/PidController.o
	g++ -shared -fPIC -o $@ $<


clean:
	find . -name "*.o" | xargs rm

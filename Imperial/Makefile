CXXFLAGS+=-std=c++11 -I/usr/local/include/ -I/home/fyquah/dev/wiringPi/wiringPi -I/usr/include/python2.7/ -Iinclude/ -Iinclude/brickpi -I../DexterInd/BrickPi_C/Drivers/ -lwiringPi
CXX=arm-linux-gnueabi-g++


src/brickpi.so: src/Interface_python.o  src/Interface.o  src/PidController.o
	${CXX} src/Interface_python.o  src/Interface.o  src/PidController.o -shared -o libmod.so  -Wl,--whole-archive  -Wl,--no-whole-archive


clean:
	find . -name "*.o" | xargs rm

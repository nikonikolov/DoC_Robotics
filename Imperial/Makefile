CXXFLAGS+=-std=c++11 -I/usr/local/include/ -I/home/fyquah/dev/wiringPi/wiringPi -I/usr/include/python2.7/ -Iinclude/ -Iinclude/brickpi -I../DexterInd/BrickPi_C/Drivers/ -lwiringPi
CXX=arm-linux-gnueabi-g++


src/brickpi.so: src/Interface_python.o  src/Interface.o  src/PidController.o
	g++ -shared -fPIC -o  src/Interface_python.o  src/Interface.o  src/PidController.o


clean:
	find . -name "*.o" | xargs rm

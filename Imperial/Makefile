CXXFLAGS+=--std=c++11 -lboost_python_debug -lboost_python -I/usr/local/include/ -I/home/fyquah/dev/wiringPi/wiringPi -I/usr/include/python2.7/ -Iinclude/ -Iinclude/brickpi -I../DexterInd/BrickPi_C/Drivers/ -lwiringPi
CXX=arm-linux-gnueabi-g++


src/brickpi.so: src/Interface_python.o  src/Interface.o  src/PidController.o
	${CXX} src/Interface_python.o  src/Interface.o  src/PidController.o -shared -Lboost_python-py27 -o libmod.so


clean:
	find . -name "*.o" | xargs rm

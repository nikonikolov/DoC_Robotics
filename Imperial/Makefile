CXXFLAGS+=-fPIC --std=c++11 -lboost_python_debug -lboost_python -I/home/fyquah/dev/libpython_armhf/usr/include -I/usr/local/include/ -I/home/fyquah/dev/wiringPi/wiringPi -I/usr/include/python2.7 -Iinclude/ -Iinclude/brickpi -I../DexterInd/BrickPi_C/Drivers/ -lwiringPi
CXX=g++-4.9


libmod.so: src/Interface_python.o  src/Interface.o  src/PidController.o
	${CXX} -fPIC src/Interface_python.o  src/Interface.o  src/PidController.o -shared -Lboost_python-py27 -o libmod.so -lboost_thread -lpython2.7 -lboost_python

clean:
	find . -name "*.o" | xargs rm

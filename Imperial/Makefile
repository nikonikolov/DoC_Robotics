CXXFLAGS+=-fPIC --std=c++11 -lboost_python_debug -lboost_python -I/home/fyquah/dev/libpython_armhf/usr/include -I/usr/local/include/ -I/home/fyquah/dev/wiringPi/wiringPi -I/usr/include/python2.7 -Iinclude/ -Iinclude/brickpi -I../DexterInd/BrickPi_C/Drivers/ -lwiringPi
CXX=g++-4.8


brickpi.so: src/Interface_python.o  src/Interface.o  src/PidController.o
	${CXX} -fPIC src/Interface_python.o  src/Interface.o  src/PidController.o -shared -Lboost_python-py27 -o $@ -lboost_thread -lwiringPi -lboost_timer -lboost_wserialization -lboost_system -lboost_serialization -lboost_iostreams -lboost_chrono -lpython2.7 -lboost_python-py27

clean:
	find . -name "*.o" | xargs rm

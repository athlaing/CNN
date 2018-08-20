alex_model: AlexNet.o Conv2d.o helper.o Maxpool.o Fc.o
	gcc -o model AlexNet.o Conv2d.o helper.o Maxpool.o Fc.o

mnist_model: Mnist.o Conv2d.o helper.o Maxpool.o Fc.o
	gcc -o model Mnist.o Conv2d.o helper.o Maxpool.o Fc.o

Mnist.o: MNIST.c include/Conv2d.h include/helper.h include/Maxpool.h include/Fc.h
	gcc -c -g --std=c99 MNIST.c

AlexNet.o: AlexNet.c include/Conv2d.h include/helper.h include/Maxpool.h include/Fc.h
	gcc -c -g --std=c99 AlexNet.c

Conv2d.o: include/Conv2d.c include/Conv2d.h
	gcc -c -g --std=c99 include/Conv2d.c

helper.o: include/helper.c include/helper.h
	gcc -c -g --std=c99 include/helper.c

Maxpool.o: include/Maxpool.c include/Maxpool.h include/Conv2d.h
	gcc -c -g --std=c99 include/Maxpool.c

Fc.o: include/Fc.c include/Fc.h include/helper.h
	gcc -c -g --std=c99 include/Fc.c

clean:
	rm -rf model *.o .DS_Store image.txt

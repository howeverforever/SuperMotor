import sys
from lib import Model


def main(argv):
    if len(argv) == 0:
        print('Error: Please give a filename as a parameter')
        sys.exit(2)
    elif len(argv) > 1:
        print('Error: Only accept at most 1 parameter.')
        sys.exit(2)

    filename = argv[0]
    labels = ['HOOK', 'BODY', 'TOP']
    print('>> The machine is training (using SVM)...')
    model = Model(filename, labels)
    model.run()
    print('>> Completed the training (using SVM)!')


if __name__ == '__main__':

    test_data = ['motor_0504_4Y7M']
    for data in test_data:
        main([data])
    # main(sys.argv[1:])

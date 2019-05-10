import os


def ConfigDirPath():
    '''
    Asigns a directory path for all data, allowing for user input without
    altering the script.
    The current working directory (which is where the code is activatd from)
    will then contain all data to be analysed. A folder (directory) is created
    named 'Put_Data_Here'.
    The function then waits for the user to place a data folder (from GMR X)
    in to the new folder, eg...('test') which contains 'Img_000',...etc.
    Args:
        The function requires no arguments but will not work unless data is
        placed into the new directory and awaits a user input (pressing enter)
    '''
    root = os.getcwd()
    main_dir = os.path.join(root, 'Put_Data_Here')
    if os.path.isdir(main_dir) is False:
        os.mkdir(main_dir)
    while len(os.listdir(main_dir)) == 0:
        print('Place test data into "Put_Data_Here" folder with this code.')
        print('This is the same folder created on GMR X.')
        print('Once complete please hit enter on your keyboard.')
        input('Press enter to continue...\n')
        #os.sys.exit(0)
        '''
        By adding the os.sys.exit(0) line here the code stops when the
        directory is created but not when there is data present. Keep the
        input command? Stops the code from running until there is data present.
        '''
    else:
        print('Data present in "Put_Data_Here", ensure it is correct\n')
        input('Press enter to continue...\n')
    print('Data set(s) to be examined:')
    print(os.listdir(main_dir))
    print('\n')
    return main_dir


if __name__ == '__main__':

    main_dir = ConfigDirPath()
    data_files = os.listdir(main_dir)

    for d in data_files:
        img_dir = os.path.join(main_dir, d)
        #if not os.path.isdir(img_dir):
            #continue
        print(img_dir)
        print(os.listdir(img_dir))

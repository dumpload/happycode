#encoding:utf-8
import compileall
import os,sys
import shutil

def getpycfile(filename):
    result = []
    if os.path.isfile(filename):
        if not filename.endswith('.py'):
            result.append(filename)
    else:
        for i in os.listdir(filename):
            result.extend(getpycfile(os.path.join(filename,i)))
    return result

def delpyc(filename):
    if os.path.isfile(filename):
        if filename.endswith('.pyc'):
            os.remove(filename)
    else:
        for i in os.listdir(filename):
            result.extend(getpycfile(os.path.join(filename,i)))

if __name__ == '__main__':
    savedirname = 'result'
    if len(sys.argv) == 2:
        dirname = sys.argv[1]
    elif len(sys.argv) == 3:
        dirname = sys.argv[1]
        savedirname = sys.argv[2]
    else:
        exit('inpurt source path or file!')

    if not (os.path.isdir(dirname) or os.path.isfile(dirname)):
        print 'Erro filename:',dirname
        exit(1)

    if not os.path.isdir(savedirname):
        os.makedirs(savedirname)

    compileall.compile_dir(dirname)   #编译成pyc文件
    for i in getpycfile(dirname):
        copytofilename = i.replace(dirname,savedirname)
        print copytofilename
        if not os.path.isdir(os.path.split(copytofilename)[0]):
            os.makedirs(os.path.split(copytofilename)[0])
        shutil.copy(i,copytofilename)





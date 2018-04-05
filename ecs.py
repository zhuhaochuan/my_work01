# coding=utf-8 此编码类型支持中文注释

#python2 ecs.py 数据/TrainData_2015.1.1_2015.2.19.txt 数据/input_5flavors_cpu_7days.txt 数据/out.text

import sys
import os
import predictor


def main():
    print 'main function begin.'
    # sys.argv[ ]其实就是一个列表，里边的项为用户输入的参数，这参数是从程序外部输入的
    # len(sys.argv)==4 代表当前脚本含有3个参数。
    if len(sys.argv) != 4:
        print 'parameter is incorrect!'
        print 'Usage: python esc.py ecsDataPath inputFilePath resultFilePath'
        exit(1)
    # Read the input files 读入输入文件，argv的1 2 3为下面三个名字，argv[0]一般是被调用的脚本文件名或全路径，此处是python esc.py
    # 分别为三个文件路径：数据，输入，输出
    ecsDataPath = sys.argv[1]
    inputFilePath = sys.argv[2]
    resultFilePath = sys.argv[3]

    #ecs_infor_array = read_lines(ecsDataPath)
    ecs_infor_array = ecsDataPath
    input_file_array = read_lines(inputFilePath)

    #for each in ecs_infor_array:
        #print each
    #for each in input_file_array:
        #print each
    # predictVm函数的应用
    predic_result = predictor.predict_vm(ecs_infor_array, input_file_array)
    # 把结果写入到输出文件
    if len(predic_result) != 0:
        write_result(predic_result, resultFilePath)
    else:
        # 没结果返回NA
        predic_result.append("NA")
        write_result(predic_result, resultFilePath)
    print 'main function end.'


# write_result函数的参数为一个列表（从预测函数中得到），和一个输出文件路径
def write_result(array, outpuFilePath):
    with open(outpuFilePath, 'w') as output_file:
        for item in array:
            output_file.write("%s\n" % item)


# 如果文件路径存在则按行读入，返回值为一个列表
def read_lines(file_path):
    if os.path.exists(file_path):
        array = []
        with open(file_path, 'r') as lines:
            for line in lines:
                array.append(line)
        return array
    else:
        print 'file not exist: ' + file_path
        return None


# 在自己中运行自己~
if __name__ == "__main__":
    main()



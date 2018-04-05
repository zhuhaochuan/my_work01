# coding=utf-8 此编码类型支持中文注释
#定义每一个虚拟机结构体
import random
import math
class Node(object):
    def __init__(self,name,cpu,mem,c_m,num):
        self.name = name
        self.cpu = cpu
        self.mem = mem
        self.c_m = c_m
        self.num = num
    def __repr__(self):
        print(str(self.name),str(self.cpu),str(self.mem))
#定义物理机结构体
class Phy_mac(object):
    def __init__(self,name):
        self.cpu = 56.0
        self.mem = 128.0
        self.name = name
class Node1(object):
    def __init__(self,name,cpu,mem):
        self.name = name
        self.cpu = cpu
        self.mem = mem

def SAA(data,packing_k):
    #print(sum(data))
    T = 10 #初始温度
    Tmin = 1 #终止温度
    r = 0.9999 #温度下降的系数

    change_list = [] #骰子，每次随机投掷，取前两个变量作为每次退火需要交换顺序的虚拟机
    table = {'flavor1': [1.0, 1.0],'flavor2': [1.0, 2.0],'flavor3' :[1.0, 4.0],'flavor4' :[2.0, 2.0],'flavor5' :[2.0, 4.0],'flavor6': [2.0, 8.0],'flavor7': [4.0, 4.0],'flavor8': [4.0, 8.0],'flavor9': [4.0, 16.0],'flavor10': [8.0, 8.0],'flavor11': [8.0, 16.0],'flavor12': [8.0, 32.0],'flavor13': [16.0, 16.0],'flavor14': [16.0, 32.0],'flavor15': [16.0, 64.0]}
    temp_data = data
    vec_flavors = []
    for i in range(0,len(temp_data)):
        while temp_data[i]:
            vec_flavors.append(Node1('flavor'+str(i+1),table['flavor'+str(i+1)][0],table['flavor'+str(i+1)][1]))
            temp_data[i] -= 1

    min_server = len(vec_flavors) + 1
    res_servers = [] #用于存放最好结果
    dice = []
    for i in range(0,len(vec_flavors)):
        dice.append(i)
    res_info = []
    min_num = len(vec_flavors) + 1

    while T>Tmin:
        info = []
        info.append({})
        random.shuffle(dice)
        new_vec_flavors = vec_flavors
        temp = vec_flavors[dice[0]]
        new_vec_flavors[dice[0]] = new_vec_flavors[dice[1]]
        new_vec_flavors[dice[1]] = temp
        result_num = 1
        pym = Phy_mac(result_num)
        pym_list = []
        pym_list.append(pym)

        for each in new_vec_flavors:
            i = 0
            while(i<len(pym_list)):
                if((pym_list[i].cpu>=each.cpu) & (pym_list[i].mem>=each.mem)):
                    pym_list[i].cpu -= each.cpu
                    pym_list[i].mem -= each.mem
                    #print(pym_list[i].name,each.name)
                    if(info[i].has_key(each.name)):
                        info[i][each.name] += 1
                    else :
                        info[i][each.name] = 1
                    #print(info[i])
                    break
                i += 1

            if(i==len(pym_list)):
                result_num += 1
                pym = Phy_mac(result_num)
                pym.cpu -= each.cpu
                pym.mem -= each.mem
                pym_list.append(pym)
                #print('-----')
                #print(pym_list[i].name,each.name)
                #print(pym_list[i].name,pym_list[i].cpu,pym_list[i].mem)
                info.append({})
                if(info[i].has_key(each.name)):
                    info[i][each.name] += 1
                else :
                    info[i][each.name] = 1
                #print(info[i])

        server_num = 0;
        if (packing_k == 'CPU'):
            server_num = len(pym_list) - 1 + (1-pym_list[len(pym_list)-1].cpu/56)
        else:
            server_num = len(pym_list) - 1 + (1-pym_list[len(pym_list)-1].mem/128)

        if (server_num < min_server) :
            min_server = server_num
            res_servers = pym_list
            vec_flavors = new_vec_flavors
            res_info = info
            min_num = result_num
        else:
            if (math.exp((min_server - server_num) / T) > random.uniform(0,100) / 100) :
                min_server = server_num
                res_servers = pym_list
                vec_flavors = new_vec_flavors
                res_info = info
                min_num = result_num
        T = r * T
        # if((server_num-min_server)!=0):
        #     #print(T,server_num-min_server)

    result = []
    result.append(min_num)
    for i in range(0,len(res_info)):
        s = ''
        for e in res_info[i]:
            s = s + ' ' + e + ' ' + str(res_info[i][e])
        result.append(str(i+1) + s)

    # for each in result:
    #     print(each)
    # for j in range(1,len(result)):
    #     a = result[j].split()
    #     sum_c = 0
    #     sum_m = 0
    #     for i in range(1,len(a)):
    #         if i%2==0:
    #             sum_c += table[a[i-1]][0]*int(a[i])
    #             sum_m += table[a[i-1]][1]*int(a[i])
    #     if(sum_c>56 or sum_m>128):
    #         print('xxxxxxxxxxxxxxxxxxxx',a[0],sum_c,sum_m)
    # for each in res_servers:
    #     print(each.name,each.cpu,each.mem)
    return result

data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
def count_kind_num(path,kind_choose):
    f = open(path)
    line = f.readline()

    kind = []
    date = []
    #month = '2015-01'
    #kind_choose = '2'

    while line:
        a = line.split()
        temp = a[1].split('r')
        #print(a[2].split('-'))
        kind.append(temp[1])
        date.append(a[2])
        line = f.readline()

    nums = []
    temp = date[0]
    i = 0
    nums.append(0)
    dates = []
    dates.append('01')
    j = 0

    for each in date :
        if (each==temp) :
            if(kind[j]==kind_choose) :
                nums[i] = nums[i] + 1
                j = j + 1
            else :
                j = j + 1
        else :
            nums.append(0)
            d = each.split('-')
            dates.append(d[2])
            i = i + 1
            if(kind[j]==kind_choose) :
                nums[i] = nums[i] + 1
                j = j + 1
            else :
                j = j + 1
            temp = each
    f.close()
    return dates,nums
def nums_of_month(path):
    f = open(path)

    line = f.readline()

    kind = []
    date = []
    mymap = {}

    while line:
        a = line.split()
        temp = a[1].split('r')
        kind.append(temp[1])
        date.append(a[2])
        line = f.readline()


    dic = {}
    for i in range(1,16):
        a = str(i)
        dic[a] = 0

    nums = []
    temp = date[0]
    i = 0
    nums.append(0)
    dates = []
    dates.append('01')
    for each in date:
        if (each==temp) :
            nums[i] = nums[i] + 1
        else :
            d = each.split('-')
            dates.append(d[1]+d[2])
            nums.append(1)
            temp = each
            i = i+1
    f.close()
    return nums
#求解装箱问题的函数
#-------------------------------------------
# def packing(data,packing_k,t,vm_k):
#     vm_k = vm_k
#     packing_k = packing_k
#     t = t
#     table = {'flavor1': [1.0, 1.0],'flavor2': [1.0, 2.0],'flavor3' :[1.0, 4.0],'flavor4' :[2.0, 2.0],'flavor5' :[2.0, 4.0],'flavor6': [2.0, 8.0],'flavor7': [4.0, 4.0],'flavor8': [4.0, 8.0],'flavor9': [4.0, 16.0],'flavor10': [8.0, 8.0],'flavor11': [8.0, 16.0],'flavor12': [8.0, 32.0],'flavor13': [16.0, 16.0],'flavor14': [16.0, 32.0],'flavor15': [16.0, 64.0]}
#     table_ = {}
#     for each in vm_k:
#         table_['flavor' + each] = table['flavor' + each]
#     table = table_#根据输入得到的table


#     k = [13,10,7,4,1,14,11,8,5,2,15,12,9,6,3]#按照cpu/mem 从大到小排列
#     #data = [0,1,0,0,7,3,2,5,5,0,7,6,0,7,6]#得到的预测数据
#     #data = [1,1,1,0,7,4,2,2,8,2,4,9,7,7,6]
#     cpu_n = [1,1,1,2,2,2,4,4,4,8,8,8,16,16,16]#每一个类别的CPU个数
#     mem_n = [1,2,4,2,4,8,4,8,16,8,16,32,16,32,64]#每一个类别的mem大小

#     #------------------------
#     #按照CPU分配
#     if(packing_k == 'CPU'):
#         cpu_mem = []
#         for each in table:
#             a = each.split('r')
#             temp = Node(each,table[each][0],table[each][1],float(table[each][0]/table[each][1]),int(a[1]))
#             cpu_mem.append(temp)
#         def mycmp1(x,y):
#             if x.c_m < y.c_m or (x.c_m ==y.c_m and x.cpu < y.cpu):
#                 return 1
#             elif x.c_m > y.c_m or (x.c_m ==y.c_m and x.cpu > y.cpu):
#                 return -1
#             else:
#                 return 0
#         cpu_mem.sort(mycmp1)

#         sum_cpu = 0
#         sum_mem = 0
#         for i in range(0,15):
#             sum_cpu += data[i]*cpu_n[i]
#             sum_mem += data[i]*mem_n[i]
#         opti_s = max(sum_cpu/56.0,sum_mem/128.0)
#         print(sum_cpu,sum_mem)

#         result_n = 1
#         py_m = Phy_mac(result_n)
#         py_m_list = []
#         py_m_list.append(py_m)
#         info = [] #存储物理机存放信息
#         info.append({})
#         i = 0

#         while(i<len(cpu_mem)):
#             flag = 1
#             while(data[cpu_mem[i].num-1] and flag):
#                 if(data[cpu_mem[i].num-1] and (py_m.cpu >= cpu_mem[i].cpu) and (py_m.mem >= cpu_mem[i].mem)):
#                     py_m.cpu -= cpu_mem[i].cpu
#                     py_m.mem -= cpu_mem[i].mem
#                     data[cpu_mem[i].num-1] -= 1
#                     if(info[result_n-1].has_key(cpu_mem[i].name)):
#                         info[result_n-1][cpu_mem[i].name] += 1
#                     else :
#                         info[result_n-1][cpu_mem[i].name] = 1
#                 else:flag = 0
#             flag_j = 0
#             if(flag == 0):
#                 j = i+1
#                 while(j<len(cpu_mem)):
#                     if(data[cpu_mem[j].num-1] and (py_m.cpu >= cpu_mem[j].cpu) and (py_m.mem >= cpu_mem[j].mem)):
#                         py_m.cpu -= cpu_mem[j].cpu
#                         py_m.mem -= cpu_mem[j].mem
#                         data[cpu_mem[j].num-1] -= 1
#                         if(info[result_n-1].has_key(cpu_mem[j].name)):
#                             info[result_n-1][cpu_mem[j].name] += 1
#                         else :
#                             info[result_n-1][cpu_mem[j].name] = 1
#                         j -= 1
#                     j += 1
#                     flag_j = j
#             if((py_m.cpu<1 or py_m.mem<1 or flag_j == len(cpu_mem) or (flag_j == 0 and i == len(cpu_mem)-1)) and sum(data)):
#                 #print(data)
#                 result_n += 1
#                 #print(result_n)
#                 info.append({})
#                 py_m = Phy_mac(result_n)
#                 py_m_list.append(py_m)
#             if(data[cpu_mem[i].num-1]):
#                 i -= 1
#             i += 1

#         score = (sum_cpu + 0.0)/(result_n * 56)

#         print('求解所得物理机数：' + str(result_n))
#         print('最优解：' + str(opti_s))
#         print('利用率：' + str(score))

#         result = []
#         result.append(result_n)
#         for i in range(0,len(info)):
#             s = ''
#             for e in info[i]:
#                 s = s + ' ' + e + ' ' + str(info[i][e])
#             result.append(str(i+1) + s)
#         #print(result)
#         return result
#     #------------------------
#     #按照内存分配
#     if(packing_k == 'MEM'):
#         mem_cpu = []
#         for each in table:
#             a = each.split('r')
#             temp = Node(each,table[each][0],table[each][1],float(table[each][1]/table[each][0]),int(a[1]))
#             mem_cpu.append(temp)

#         #print(len(mem_cpu))
#         #print(cpu/mem)
#         def mycmp2(x,y):
#             if x.c_m < y.c_m or (x.c_m ==y.c_m and x.mem < y.mem):
#                 return 1
#             elif x.c_m > y.c_m or (x.c_m ==y.c_m and x.mem > y.mem):
#                 return -1
#             else:
#                 return 0

#         mem_cpu.sort(mycmp2)

#         data_s = []

#         for each in k:
#             data_s.append(data[each-1])
#         sum_cpu = 0
#         sum_mem = 0
#         for i in range(0,15):
#             sum_cpu += data[i]*cpu_n[i]
#             sum_mem += data[i]*mem_n[i]
#         opti_s = max(sum_cpu/56.0,sum_mem/128.0)
#         print(sum_cpu,sum_mem)

#         result_n = 1
#         py_m = Phy_mac(result_n)

#         py_m_list = []
#         py_m_list.append(py_m)
#         info = [] #存储物理机存放信息
#         info.append({})

#         i = 0
#         while(i<len(mem_cpu)):
#             #print('-------')
#             #print(i)
#             #print(mem_cpu[i].name)
#             #print(data[mem_cpu[i].num-1])
#             flag = 1
#             while(data[mem_cpu[i].num-1] and flag):
#                 if(data[mem_cpu[i].num-1] and (py_m.cpu >= mem_cpu[i].cpu) and (py_m.mem >= mem_cpu[i].mem)):
#                     py_m.cpu -= mem_cpu[i].cpu
#                     py_m.mem -= mem_cpu[i].mem
#                     data[mem_cpu[i].num-1] -= 1
#                     #print(str(result_n) + ' ' + mem_cpu[i].name)
#                     if(info[result_n-1].has_key(mem_cpu[i].name)):
#                         info[result_n-1][mem_cpu[i].name] += 1
#                     else :
#                         info[result_n-1][mem_cpu[i].name] = 1
#                 else:flag = 0
#             flag_j = 0
#             if(flag == 0):
#                 j = i+1
#                 while(j<len(mem_cpu)):
#                     if(data[mem_cpu[j].num-1] and (py_m.cpu >= mem_cpu[j].cpu) and (py_m.mem >= mem_cpu[j].mem)):
#                         py_m.cpu -= mem_cpu[j].cpu
#                         py_m.mem -= mem_cpu[j].mem
#                         data[mem_cpu[j].num-1] -= 1
#                         if(info[result_n-1].has_key(mem_cpu[j].name)):
#                             info[result_n-1][mem_cpu[j].name] += 1
#                         else :
#                             info[result_n-1][mem_cpu[j].name] = 1
#                         j -= 1
#                     j += 1
#                     flag_j = j
#             if((py_m.mem<1 or py_m.cpu<1 or flag_j == len(mem_cpu) or (flag_j == 0 and i == len(mem_cpu)-1)) and sum(data)):
#                 result_n += 1
#                 info.append({})
#                 py_m = Phy_mac(result_n)
#                 py_m_list.append(py_m)
#             if(data[mem_cpu[i].num-1]):
#                 i -= 1
#             i += 1
#             #print(py_m.name,py_m.cpu,py_m.mem,result_n)
#         #print(result_n)
#         #print(data)

#         s1 = 0
#         s2 = 0
#         for each in py_m_list:
#             #print(each.name,each.cpu,each.mem)
#             s1 += each.cpu
#             s2 += each.mem
#         #print(9*56-s1,9*128-s2)

#         score = (sum_mem + 0.0)/(result_n * 128)

#         print('求解所得物理机数：' + str(result_n))
#         print('最优解：' + str(opti_s))
#         print('利用率：' + str(score))

#         result = []
#         result.append(result_n)
#         for i in range(0,len(info)):
#             s = ''
#             for e in info[i]:
#                 s = s + ' ' + e + ' ' + str(info[i][e])
#             result.append(str(i+1) + s)
#         #print(result)
#         return result
#     return result,result_n
#-------------------------------------------
def predict_vm(ecs_lines, input_lines):
    # Do your work from here#
    result = []
    if ecs_lines is None:
        print 'ecs information is none'
        return result
    if input_lines is None:
        print 'input file information is none'
        return result
    input_vm_n = input_lines[2]
    vm_k = []

    for i in range(3,len(input_lines)-5):
        a = input_lines[i].split()
        a = a[0].split('r')
        a = a[1]
        vm_k.append(a)
    #print vm_k
    packing_k = input_lines[-4]
    packing_k = packing_k.split()[0]
    temp = input_lines[-1].split()
    temp = temp[0]
    temp = temp.split('-')
    begin_t = temp[2]
    temp = input_lines[-2].split()
    temp = temp[0]
    temp = temp.split('-')
    end_t = temp[2]

    t  = int(begin_t) - int(end_t)
    #print t
    nums = nums_of_month(ecs_lines)
    sum1=0.0
    sum2=0.0
    for i in range(0,len(nums)):
        sum1+=nums[i]
        sum2+=nums[i]**2
    mean=sum1/len(nums)
    var=sum2/len(nums)-mean**2
    #print(mean,var)
    #for each in vm_k:
        #data[int(each)-1] = int(random.gauss(int(mean),int(var)))
        #data[int(each)-1] = random.randrange(0,5,1)
        #print data[int(each)-1]
    #sum_vm = sum(data)
    #result.append(sum_vm)
    result_list = []
    for i in vm_k:
        [dates,nums] = count_kind_num(ecs_lines,kind_choose = str(i))
        mean_nums = sum(nums)/(len(nums) + 0.0)
        for c in range(0,len(nums)):
            if (nums[c] - mean_nums)>25:
                nums[c] = nums[c]*0.51
        c = 0
        result_ = 0
        w = []
        for i in range(0,len(nums)):
            w.append(1/((len(nums)-1)*len(nums)/2)*i)
        while(c<t):
            l = len(nums)
            temp_n = nums[c:l]
            next_ = 0
            for i in range(0,l-c):
                next_ += temp_n[i]*w[i]
            if packing_k == 'CPU':
                next_d = next_*0 + nums[l-7]*0.89 + nums[l-14]*0.26 + nums[l-21]*0.155 + nums[l-28]*0.21
            else :
                next_d = next_*0 + nums[l-7]*0.91 + nums[l-14]*0.18 + nums[l-21]*0.15 + nums[l-28]*0.2
            result_ += round(next_d)
            nums.append(round(next_d))
            c += 1
        result_list.append(int(result_))
    #print('result_list',result_list)

    for i in range(0,len(vm_k)):
        data[int(vm_k[i])-1] = result_list[i]

    sum_vm = sum(data)
    result.append(sum_vm)
    #-------------------------------------------------------------
    #预测部分
    #print vm_k
    for each in vm_k:
        result.append('flavor'+ each + ' ' + str(data[int(each)-1]))
    result.append('')
    result += SAA(data,packing_k)
    #result += packing(data,packing_k,t,vm_k)
    return result
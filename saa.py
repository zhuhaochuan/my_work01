# coding=utf-8 此编码类型支持中文注释
#模拟退火算法+首次适应算法
import random
import math
class Node1(object):
    def __init__(self,name,cpu,mem):
        self.name = name
        self.cpu = cpu
        self.mem = mem


data = [3, 7, 5, 0, 16, 16, 34, 54, 22, 8, 26, 5, 0, 10, 0]
#data = [1,2,3,0,0,0,0,0,0,0,0,0,0,0,0]
def SAA(data,packing_k,vm_k):
	T = 100 #初始温度
	Tmin = 1 #终止温度
	r = 0.9999 #温度下降的系数

	change_list = [] #骰子，每次随机投掷，取前两个变量作为每次退火需要交换顺序的虚拟机
	table = {'flavor1': [1.0, 1.0],'flavor2': [1.0, 2.0],'flavor3' :[1.0, 4.0],'flavor4' :[2.0, 2.0],'flavor5' :[2.0, 4.0],'flavor6': [2.0, 8.0],'flavor7': [4.0, 4.0],'flavor8': [4.0, 8.0],'flavor9': [4.0, 16.0],'flavor10': [8.0, 8.0],'flavor11': [8.0, 16.0],'flavor12': [8.0, 32.0],'flavor13': [16.0, 16.0],'flavor14': [16.0, 32.0],'flavor15': [16.0, 64.0]}
	table_ = {}
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
	info = []
	info.append({})

	while T>Tmin:
		random.shuffle(dice)
		new_vec_flavors = vec_flavors
		temp = vec_flavors[dice[0]]
		new_vec_flavors[dice[0]] = new_vec_flavors[dice[1]]
		new_vec_flavors[dice[1]] = temp
		result_num = 1
		pym = Phy_mac(result_num)
		pym_list = []
		pym_list.append(pym)
		print(len(pym_list))
		info = [] #存储物理机存放信息
		info.append({})
		for each in new_vec_flavors:
			i = 0
			while(i<len(pym_list)):
				if(pym_list[i].cpu-each.cpu>=0 and pym_list[i].mem-each.mem>=0):
					pym_list[i].cpu -= each.cpu
					pym_list[i].mem -= each.mem
					if(info[result_num-1].has_key(each.name)):
					    info[result_num-1][each.name] += 1
					else :
					    info[result_num-1][each.name] = 1
					break
				i += 1
			if(i==len(pym_list)):
				result_num += 1
				pym = Phy_mac(result_num)
				pym_list.append(pym)
				info.append({})
				pym_list[i].cpu -= each.cpu
				pym_list[i].mem -= each.mem
				if(info[result_num-1].has_key(each.name)):
				    info[result_num-1][each.name] += 1
				else :
				    info[result_num-1][each.name] = 1
		server_num = 0;
		if (packing_k == 'CPU'):
			server_num = len(pym_list) - 1 + pym_list[len(pym_list)-1].cpu/56
		else:
			server_num = len(pym_list) - 1 + pym_list[len(pym_list)-1].mem/128
		if (server_num < min_server) :
			min_server = server_num
			res_servers = pym_list
			vec_flavors = new_vec_flavors
			res_info = info
		else :
			if (math.exp((min_server - server_num) / T) > random.uniform(0,100) / 100) :
				min_server = server_num
				res_servers = pym_list
				vec_flavors = new_vec_flavors
				res_info = info
		T = r * T
		print(T,min_server)
		break
	result = []
	result.append(result_num)
	for i in range(0,len(info)):
		s = ''
		for e in info[i]:
			s = s + ' ' + e + ' ' + str(info[i][e])
		result.append(str(i+1) + s)


	return result


# result_info= SAA(data,'CPU',10)
# sum_cpu = 0
# sum_mem = 0
# for each in result:
# 	print (each.cpu,each.mem,each.name)
# 	sum_cpu += each.cpu
# 	sum_mem += each.mem

# print(each.name*56-sum_cpu,each.name*128-sum_mem)
# for each in result_info:
# 	print(each)












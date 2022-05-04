from copy import *
from copyreg import pickle
from tqdm import tqdm
import os,pickle
import random

shengmu = ["b","p","m","f","d","t","n","l","g","k","h","j","q","r","x","w","y","zh","ch","sh","z","c","s",""]

yunmu = ["a","ai","an","ang","ao","e","ei","en","eng","er","i","ia","ian","iang","iao","ie","in","ing","io","iong","iu","o","ong","ou","u","ua","uai","uan","uang","ui","un","uo","v","van","ue","ve","vn"]

candidate_word = []

impossible = []
pair_rlt = []
nex_link = []
lass = []

def divv(w):
	if w[-1] in ["1","2","3","4"]:
		sd = w[-1]
		w = w[:-1]
	else:
		sd = "5"
	if len(w)>=3 and w[1]=="h":
		sm = w[:2]
		ym = w[2:]
	elif w[0] not in shengmu:
		sm = ""
		ym = w[:]
	else:
		sm = w[:1]
		ym = w[1:]
	#print(sm,ym,sd)
	assert(sm in shengmu)
	assert(ym in yunmu)
	assert(sd in ["1","2","3","4","5"])
	return [sm,ym,sd]



def init():
	global divv
	#wordlist = open("xiandaihaiyuchangyongcibiao.txt","r")
	wordlist = open("chengyucibiao.txt","r")
	
	cnt = 0

	while True:
		line = wordlist.readline()
		if line == "":
			break
		if len(line.split("\t")) != 3:
			print(line)
			continue
		word,pinyin,freq = line.split("\t")
		freq = int(freq)
		if len(word) != 4:
			continue
		try:
			pinyin_list = list(map(divv,pinyin.split("\'")))
		except:
			print(word,pinyin)
			continue
		candidate_word.append([word,deepcopy(pinyin_list),cnt])
		impossible.append(0)
		cnt += 1
	print("Total_word: %d"%cnt)

def cmp_words(ans,word2):
	ret = []
	unused = []
	for j in range(3):
		for i in range(4):
			if ans[1][i][j]==word2[1][i][j]:
				ret.append(2)
			else:
				ret.append(0)
				unused.append(ans[1][i][j])
	for i in range(4):
		if ans[0][i]==word2[0][i]:
			ret.append(2)
		else:
			ret.append(0)
			unused.append(ans[0][i])
	curr = 0
	for j in range(3):
		for i in range(4):
			if ret[curr]==0 and word2[1][i][j] in unused:
				ret[curr] = 1
				unused.remove(word2[1][i][j])
			curr += 1
	for i in range(4):
		if ret[curr] == 0 and word2[0][i] in unused:
			ret[curr] = 1
			unused.remove(word2[0][i])
		curr += 1
	return ret

#print(cmp_words(["粗心大意",list(map(divv,"cu1'xin1'da4'yi4".split("\'")))],["口口声声",list(map(divv,"kou3'kou3'sheng1'sheng1".split("\'")))]))

def solve(candidate_idx,word,nowdep,deplim,st,predict=False):
	global pair_rlt
	used = [False for i in range(len(candidate_idx))]
	maxdepth = 0
	maxsame = 0
	idx2idx = {}
	for i in range(len(candidate_idx)):
		idx2idx[candidate_idx[i]] = i
	for i in range(len(candidate_idx)):#枚举答案
		same = 0
		if maxdepth > deplim:
			return maxdepth
		if used[i]:
			continue
		if candidate_idx[i] == word:#排除猜对的情况（0）
			continue
		next_candidate_idx = []
		#x = 0
		#for s in range(4):
		#	x = x<<8|pair_rlt[word][candidate_idx[i]][s]
		x = pair_rlt[word][candidate_idx[i]]
		now = lass[word][x]
		if predict:
			while now != -1:#now 是原序列中的东西，不是当前的，要判一下当前是否还活着
				if now in idx2idx:
					same += 1
					used[idx2idx[now]] = True
				now = nex_link[word][now]
		else:
			while now != -1:#now 是原序列中的东西，不是当前的，要判一下当前是否还活着
				if now in idx2idx:
					same += 1
					used[idx2idx[now]] = True
					next_candidate_idx.append(now)
				now = nex_link[word][now]


		if predict == False:
			if len(candidate_idx)==1:
				if maxdepth == 0:
					maxdepth = 1
				continue
			st.append("answer:"+candidate_word[candidate_idx[i]][0])
			depth = guess(next_candidate_idx,nowdep+1,deplim,st)[0]
			del st[-1]
			if depth > maxdepth:
				maxdepth = depth
				maxsame = same
		else:
			if same > maxsame:
				maxsame = same
	if predict:
		return maxsame
	return maxdepth
				
prcnt = 0

def guess(candidate_idx,nowdep,deplim,st):
	global prcnt
	prcnt += 1
	if prcnt <= 2000000:
		print("Now depth:",nowdep,end="")
		print("Limit:",deplim,end="")
		for i in range(nowdep):
			print("\t",end="")
		for i in range(min(10,len(candidate_idx))):
			print(candidate_word[candidate_idx[i]][0],end=" ")
		print("(total %d words)"%len(candidate_idx))
		print(st)

	if len(candidate_idx) == 1:
		return [1,candidate_idx[0]]
	if deplim <= 1:
		return [100,-1]
	minn = 100000
	best_word = candidate_idx[0]
	seq = []
	for i in tqdm(range(len(candidate_idx))):
		seq.append([i,solve(candidate_idx,candidate_idx[i],nowdep,min(minn,deplim)-1,[],True)])
	#random.shuffle(seq)
	seq.sort(key=lambda x:x[1])
	print(seq[:10])
	count = 0
	for _ in range(len(candidate_idx)):#枚举猜的词
		i = seq[_][0]
		if min(minn,deplim) <= 1:
			break
		st.append(candidate_word[candidate_idx[i]][0])
		tmp_v = solve(candidate_idx,candidate_idx[i],nowdep,min(minn,deplim)-1,st)
		del st[-1]
		if tmp_v <= 3 and nowdep == 0:
			print(count,tmp_v,seq[_][1],candidate_word[candidate_idx[i]][0],candidate_word[candidate_idx[i]][1])
		elif nowdep==0:
			print(count,tmp_v,seq[_][1])
		if tmp_v < minn:
			minn = tmp_v
			best_word = candidate_idx[i]
		count += 1
	return [minn + 1,best_word]

def update_knowledge(currect,word,cand):
	x = 0
	ret = []
	G = []
	curr = 0
	for i in range(4):
		G.append(0)
		for j in range(4):
			G[-1] = G[-1]<<2|int(currect[curr])
			x = x<<2|int(currect[curr])
			curr += 1
	'''for i in cand:
		if pair_rlt[word][i] == G:
			ret.append(i)'''
	for i in cand:
		if pair_rlt[word][i] == x:
			ret.append(i)
	print("候选共%d个。"%len(ret))
	for i in ret:
		print(candidate_word[i][0],end=",")
	print("\n")
	return ret

if __name__ == "__main__":
	random.seed(0)
	init()
	if os.path.exists("pair_rlt.pkl"):
		pair_rlt= pickle.load(open("pair_rlt.pkl","rb"))
	else:
		pair_rlt = [[0 for i in range(len(candidate_word))] for j in range(len(candidate_word))]
		for i in tqdm(range(len(candidate_word))):
			#pair_rlt.append([])
			for j in range(len(candidate_word)):
				rltt = cmp_words(candidate_word[j],candidate_word[i])
				#pair_rlt[i].append(0)
				#pair_rlt[i].append([])
				curr = 0
				for k in range(4):
					#pair_rlt[i][j].append(0)
					for s in range(4):
						#pair_rlt[i][j][k] = pair_rlt[i][j][k]<<2|rltt[curr]
						pair_rlt[i][j] = pair_rlt[i][j]<<2|rltt[curr]
						curr += 1
				#print(i,j,"".join(list(map(str,cmp_words(candidate_word[i],candidate_word[j])))),file=pair_file)
		pickle.dump(pair_rlt,open("pair_rlt.pkl","wb"))
	for i in range(len(candidate_word)):
		nex_link.append([])
		lass.append({})
		for j in range(len(candidate_word)):
			#x = 0
			#for s in range(4):
			#	x = x<<8|pair_rlt[i][j][s]
			x = pair_rlt[i][j]
			#if candidate_word[i][0]=="馋涎欲滴" and pair_rlt[i][j]==[4,17,9,0]:
			#	print(j,x,pair_rlt[i][j])
			if x not in lass[i]:
				lass[i][x] = -1
			nex_link[i].append(lass[i][x])
			lass[i][x] = j
	#exit()
	candidate_idx = [i for i in range(len(candidate_word))]
	while True:
		best = guess(candidate_idx,0,4,[])
		print("Guess:",candidate_word[best[1]][0],candidate_word[best[1]][1])
		print("Max %d times.",best[0])
		print("请输入正确性（0/1/2表示不存在/存在/正确）：声母正确性/韵母正确性/音调正确性/字正确性（共16个字符）")
		candidate_idx = update_knowledge(input(),best[1],candidate_idx)
		if len(candidate_idx)==0:
			print("猜不出来")
			exit()
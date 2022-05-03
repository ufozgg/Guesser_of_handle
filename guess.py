from copy import *
from copyreg import pickle
from tqdm import tqdm
import os,pickle

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
	print(sm,ym,sd)
	assert(sm in shengmu)
	assert(ym in yunmu)
	assert(sd in ["1","2","3","4","5"])
	return [sm,ym,sd]



def init():
	global divv
	wordlist = open("xiandaihaiyuchangyongcibiao.txt","r")
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
		pinyin_list = list(map(divv,pinyin.split("\'")))
		candidate_word.append([word,deepcopy(pinyin_list),cnt])
		impossible.append(0)
		cnt += 1
	print("Total_word: %d"%cnt)

def cmp_words(ans,word2):
	ret = []
	unused = []
	for j in range(3):
		for i in range(4):
			if ans[1][i]==word2[1][i]:
				ret.append(2)
			else:
				ret.append(0)
				unused.append(ans[1][i])
	for i in range(4):
		if ans[0][i]==word2[0][i]:
			ret.append(2)
		else:
			ret.append(0)
			unused.append(ans[1][i])
	curr = 0
	for j in range(3):
		for i in range(4):
			if ret[curr]==0 and word2[1][i] in unused:
				ret[curr] = 1
				unused.remove(word2[1][i])
			curr += 1
	for i in range(4):
		if ret[curr] == 0 and word2[0][i] in unused:
			ret[curr] = 1
			unused.remove(word2[0][i])
		curr += 1
	return ret

def solve(candidate_word,word,nowdep,deplim,st,predict=False):
	global pair_rlt
	used = [False for i in range(len(candidate_word))]
	maxdepth = 0
	maxsame = 0
	idx2idx = {}
	for i in range(len(candidate_word)):
		idx2idx[candidate_word[i][2]] = i
	for i in range(len(candidate_word)):#枚举答案
		same = 0
		if used[i]:
			continue
		if candidate_word[i][2] == word[2]:#排除猜对的情况（0）
			continue
		next_candidate_word = []
		x = 0
		for s in range(4):
			x = x<<8|pair_rlt[candidate_word[i][2]][word[2]][s]
		now = lass[candidate_word[i][2]][x]
		while now != -1:#now 是原序列中的东西，不是当前的，要判一下当前是否还活着
			if now in idx2idx:
				same += 1
				used[idx2idx[now]] = True
				next_candidate_word.append(deepcopy(candidate_word[idx2idx[now]]))
			now = nex_link[candidate_word[i][2]][now]

		newst = deepcopy(st)
		newst.append("answer:"+candidate_word[i][0])

		if predict == False:
			depth = guess(next_candidate_word,nowdep+1,deplim,newst)[0]
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

def guess(candidate_word,nowdep,deplim,st):
	global prcnt
	prcnt += 1
	if prcnt <= 50:
		print("Now depth:",nowdep,end="")
		for i in range(nowdep):
			print("\t",end="")
		for i in range(min(10,len(candidate_word))):
			print(candidate_word[i][0],end=" ")
		print("(total %d words)"%len(candidate_word))
		print(st)

	if len(candidate_word) == 1:
		return [0,0]
	if deplim <= 1:
		return [100,-1]
	minn = 100000
	best_word = 0
	seq = []
	for i in range(len(candidate_word)):
		seq.append([i,solve(candidate_word,deepcopy(candidate_word[i]),nowdep,min(minn,deplim)-1,[],True)])
	seq.sort(key=lambda x:x[2])
	for _ in range(len(candidate_word)):#枚举猜的词
		i = seq[_][0]
		if min(minn,deplim) <= 1:
			break
		newst = deepcopy(st)
		newst.append(candidate_word[i][0])
		tmp_v = solve(candidate_word,deepcopy(candidate_word[i]),nowdep,min(minn,deplim)-1,newst)
		if tmp_v < minn:
			minn = tmp_v
			best_word = i
	return [minn + 1,best_word]

def update_knowledge(currect):
	pass

if __name__ == "__main__":
	init()
	if os.path.exists("pair_rlt.pkl"):
		pair_rlt= pickle.load(open("pair_rlt.pkl","rb"))
	else:
		for i in tqdm(range(len(candidate_word))):
			pair_rlt.append([])
			for j in range(len(candidate_word)):
				rltt = cmp_words(candidate_word[i],candidate_word[j])
				pair_rlt[i].append([])
				curr = 0
				for k in range(4):
					pair_rlt[i][j].append(0)
					for s in range(4):
						pair_rlt[i][j][k] = pair_rlt[i][j][k]<<2|rltt[curr]
						curr += 1
				#print(i,j,"".join(list(map(str,cmp_words(candidate_word[i],candidate_word[j])))),file=pair_file)
		pickle.dump(pair_rlt,open("pair_rlt.pkl","wb"))
	for i in range(len(candidate_word)):
		nex_link.append([])
		lass.append({})
		for j in range(len(candidate_word)):
			x = 0
			for s in range(4):
				x = x<<8|pair_rlt[i][j][s]
			if x not in lass[i]:
				lass[i][x] = -1
			nex_link[i].append(lass[i][x])
			lass[i][x] = j

	while True:
		best = guess(candidate_word,0,4,[])
		print("Guess:",candidate_word[best[1]][0],candidate_word[best[1]][1])
		print("Max %d times.",best[0])
		print("请输入音调正确性（0/1/2表示不存在/存在/正确）/声母正确性/韵母正确性/字正确性（共16个字符）")
		update_knowledge(input())
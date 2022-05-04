import json
X = json.load(open("idiom2.json","r"))
cnt = 0
for w in X:
	word = w["word"]
	pinyin = w["pinyin"].split(" ")
	if len(pinyin) != 4 or len(word) != 4:
		continue
	for i in range(4):
		for j in range(len(pinyin[i])):
			if pinyin[i][j] in ["ā","á","ǎ","à"]:
				pinyin[i] = pinyin[i][:j]+"a"+pinyin[i][j+1:] + str("āáǎà".find(pinyin[i][j])+1)
				#print(pinyin[i])
				break
			if pinyin[i][j] in ["ō","ó","ǒ","ò"]:
				pinyin[i] = pinyin[i][:j]+"o"+pinyin[i][j+1:] + str("ōóǒò".find(pinyin[i][j])+1)
				#print(pinyin[i])
				break
			if pinyin[i][j] in ["ē","é","ě","è"]:
				pinyin[i] = pinyin[i][:j]+"e"+pinyin[i][j+1:] + str("ēéěè".find(pinyin[i][j])+1)
				#print(pinyin[i])
				break
			if pinyin[i][j] in ["ī","í","ǐ","ì"]:
				pinyin[i] = pinyin[i][:j]+"i"+pinyin[i][j+1:] + str("īíǐì".find(pinyin[i][j])+1)
				#print(pinyin[i])
				break
			if pinyin[i][j] in ["ū","ú","ǔ","ù"]:
				pinyin[i] = pinyin[i][:j]+"u"+pinyin[i][j+1:] + str("ūúǔù".find(pinyin[i][j])+1)
				#print(pinyin[i])
				break
			if pinyin[i][j] in ["ǖ","ǘ","ǚ","ǜ"]:
				pinyin[i] = pinyin[i][:j]+"v"+pinyin[i][j+1:] + str("ǖǘǚǜ".find(pinyin[i][j])+1)
				#print(pinyin[i])
				break
			if pinyin[i][j] in ["ü"]:
				pinyin[i] = pinyin[i][:j]+"v"+pinyin[i][j+1:]
			if pinyin[i][j]=="ɡ":
				pinyin[i] = pinyin[i][:j]+"g"+pinyin[i][j+1:]
			if ord(pinyin[i][j]) not in range(0,127):
				print(word,pinyin,pinyin[i][j],ord(pinyin[i][j]))
	flag = True
	for i in range(len("\'".join(pinyin))):
		if ord("\'".join(pinyin)[i]) not in range(0,127):
			#print(ord("\'".join(pinyin)[i]),"\'".join(pinyin)[i],word,"\'".join(pinyin),0)
			flag = False
	if flag:
		print(word,"\'".join(pinyin),0,sep="\t")
		cnt += 1
#print(cnt)
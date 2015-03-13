import os

def Training(path):
    corpus = {}
    f = open(path,'r+')
    for line in f:
        word, tag = line.split()
        if word not in corpus.keys():
            corpus[word.lower()] = {tag:1}
        else:
            if tag not in corpus[word].keys():
                corpus[word.lower()][tag]=1
            else:
                corpus[word.lower()][tag]+=1
    f.close()
    return corpus

def Tagging(path):
    corpus = Training("corpus.txt")
    new_path = path.replace(".txt","_tagged.txt")
    if os.path.isfile(new_path):
        remove(new_path)
    f = open(path,'r+')
    ft = open(new_path,'w+')
    prev = ""
    for line in f:
        word = line.split()
        if word.lower() in corpus.keys():
            max = 0
            best_tag = ""
            for tag, times in corpus[word.lower()].items():
                if max < times:
                    max = times
                    best_tag = tag
            ft.write(word+"\t"+best_tag+"\n")
            prev = best_tag
        else:
            if word[0].isupper():
                ft.write(word+"\tNP\n")
                prev = "NP"
            elif word[0].isdigit():
                ft.write(word+"\tNum\n")
                prev = "Num"
            elif prev.__eq__("Det"):
                ft.write(word+"\tNC\n")
                prev = "NC"
            elif prev.__eq__("V"):
                ft.write(word+"\tPrep\n")
                prev = "Prep"
            elif prev.__eq__("Pron"):
                ft.write(word+"\tV\n")
                prev = "V"
            else:
               for key in corpus.keys():
                   if word.__sizeof__()==key.__sizeof__() and cmp(word.lower(),key.lower()) in range(-1,2):
                        max = 0
                        best_tag = ""
                        for tag, times in corpus[key].items():
                            if times>max:
                                best_tag = tag
                                max = times
                        ft.write(word+"\t"+best_tag+"\n")
                        prev = best_tag
                   else:
                        ft.write(word+"\tUndefined\n")
                        prev = "Undefined"
    ft.close()
    f.close()

def Avaluation(test_path,golden_path):
    Tagging(test_path)
    tf = open(test_path.replace(".txt","_tagged.txt"),"r+")
    gf = open(golden_path,"r+")
    hits = 0
    misses = 0
    errors = 0
    total = 0
    for gline in gf and tline in tf:
        gword, gtag = gline
        tword, ttag = tline
        if tword.lower().__eq__(gword.lower()) and ttag.__eq__(gtag):
            hits += 1
        else:
            if ttag.__eq__("Undefined"):
                misses += 1
            else:
                errors += 1
        total += 1
    tf.close()
    gf.close()
    print test_path + " etiquetado y evaluado..."
    print hits,"/",total," aciertos(",hits/total*100,"%)"
    print errors,"/",total," errores(",errors/total*100,"%)"
    print misses,"/",total," no identificados(",misses/total*100,"%)"


Avaluation("test_1.txt","gold_standard_1.txt")
#Avaluation("test_2.txt",gold_standard_2.txt")

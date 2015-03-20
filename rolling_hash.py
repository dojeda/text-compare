from primes import is_prime
from levenshtein import distance
import queue

class RollingHash:

    def __init__(self, a=101):
        self.h = 0
        if not is_prime(a):
            raise ValueError('a must be prime')
        self.a = a
        self.history = queue.deque()
        self.size = 0

    def __call__(self):
        return self.h

    def append(self, value):
        #assert(ord(value) < self.a)
        self.h *= self.a
        self.h += ord(value)
        self.history.append(value)
        self.size += 1

    def popleft(self):
        x = ord(self.history.popleft())
        self.h -= x*self.a**(self.size-1)
        self.size -= 1
    

def rabin_karp(s,pattern):
    """ find first index where pattern occur in s, or -1 if pattern is not a substr"""
    Ns = len(s)
    Np = len(pattern)
    if Np > Ns: return -1
    
    hs = RollingHash()
    hp = RollingHash()

    for i in range(Np):
        hp.append(pattern[i])
        hs.append(s[i])

    if hs() == hp() and pattern == s[:Np]:
        return 0

    for i in range(Np,Ns):
        hs.popleft()
        hs.append(s[i])

        #print('i',i,s[i+1-Np:i+1],hs(),hp())
        if hs() == hp() and pattern == s[i+1-Np:i+1]:
                return i+1-Np

    return -1


def main():
    # source files are text files, generated from latex to text
    #file1 = 'text_samples/ner2014.txt'
    #file1 = 'text_samples/ner2014-v2.txt'  ## <-- (same paper, different versions)
    #file2 = 'text_samples/coronary.txt'   ## <-- (different paper)
    file1 = 'text_samples/wikipedia_movie.txt'
    file2 = 'text_samples/cindy1.txt'     ## <-- totally different
    #file2 = 'text_samples/embc2014.txt'
    # to generate a file with detex source.tex > output.txt
    with open(file1,'r') as f:
        all_text1 = ''.join(f.readlines())
        #print(all_text)
    # clean and extract sentences
    sentences1 = [#x.replace('\n',' ')
                  # .replace('\t',' ')
        x.strip().lower()
                  for x in all_text1.split('.')]
    sentences1 = [s for s in sentences1 if s != '']


    with open(file2,'r') as f:
        all_text2 = (''.join(f.readlines())).lower()
    sentences2 = [#x.replace('\n',' ')
                  # .replace('\t',' ')
        x.strip().lower()
                  for x in all_text2.split('.')]
    sentences2 = [s for s in sentences2 if s != '']

    # search matching sentences
    count = 0
    print('Evaluating exact matches of phrases...')
    for i,s1 in enumerate(sentences1):
        #print('{:.0f}%\r'.format(100*i/len(sentences1)),end='')
        #print(s1)
        #import pdb; pdb.set_trace()
        if len(s1) < 16: continue
        if rabin_karp(all_text2,s1) != -1:
            count += 1
            print('match:',s1)

    # search similar sentences
    similar = 0
    print('Evaluating similar wording of phrases...')
    for i,si in enumerate(sentences1):
        #print('\r{:.0f}%'.format(100*i/len(sentences1)),end='')
        wordsi = si.split()
        for j,sj in enumerate(sentences2):
            wordsj = sj.split()
            d = distance(wordsi,wordsj)
            #print(d,len(wordsi),len(wordsj))
            if d < min(len(wordsi),len(wordsj)) * .75 and min(len(si),len(sj)) >= 16:
                similar += 1
                print('similar:\nsi: {}\nsj: {}'.format(si,sj))
                break
    

    # # search similar sentences
    # similar = 0
    # print('Evaluating similar matches of phrases...')
    # for i,si in enumerate(sentences1):
    #     print('\r{:.0f}%'.format(100*i/len(sentences1)),end='')
    #     if len(si) < 16: continue
    #     for j,sj in enumerate(sentences2):
    #         if min(len(si),len(sj)) < 16:
    #             continue
    #         d = distance(si,sj)
    #         if d > min(len(si),len(sj)) * .9:
    #             similar += 1

    print('\nFinished')
    print('{count} sentences out of {total} of file "{file1}" were found in file "{file2}" ({percentage:.2f}%)'
          .format(count=count,
                  total=len(sentences1),
                  percentage=100*count/len(sentences1),
                  file1=file1, file2=file2
          ))
    print('Similar phrases: {similar} ({percentage:.2f}%)'
          .format(similar=similar,percentage=100*similar/len(sentences1)))
    print('No synonyms were considered')
    


if __name__ == '__main__':
    main()

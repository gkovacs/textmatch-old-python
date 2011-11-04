#!/usr/bin/python

def substrings(words):
  for i in range(len(words)+1):
    for j in range(len(words)+1):
      if not j > i:
        continue
      yield ' '.join(words[i:j])

def backTrack(C, X, Y, i, j):
  if i == 0 or j == 0:
    return ""
  elif X[i-1] == Y[j-1]:
    return backTrack(C, X, Y, i-1, j-1) + X[i-1]
  else:
    if C[i][j-1] > C[i-1][j]:
      return backTrack(C, X, Y, i, j-1)
    else:
      return backTrack(C, X, Y, i-1, j)

def LCSMatrix(X, Y):
  m = len(X)
  n = len(Y)
  # An (m+1) times (n+1) matrix
  C = [[0] * (n+1) for i in range(m+1)]
  for i in range(1, m+1):
    for j in range(1, n+1):
      if X[i-1] == Y[j-1]: 
        C[i][j] = C[i-1][j-1] + 1
      else:
        C[i][j] = max(C[i][j-1], C[i-1][j])
  return C

def LCSLength(X, Y):
  return LCSMatrix(X, Y)[-1:][0][-1:][0]

def LCS(X, Y):
  return backTrack(LCSMatrix(X,Y), len(X), len(Y))

'''
def LCSMatrixTemplated(X, Y):
  # X templated
  # % is template substitution string
  m = len(X)
  n = len(Y)
  # An (m+1) times (n+1) matrix
  C = [[0] * (n+1) for i in range(m+1)]
  T = [[''] * (n+1) for i in range(m+1)]
  for i in range(1, m+1):
    for j in range(1, n+1):
      if X[i-1] == Y[j-1]: 
        C[i][j] = C[i-1][j-1] + 1
        T[i][j] = T[i-1][j-1]
      else:
        if C[i-1][j] >= C[i][j-1]:
          C[i][j] = C[i-1][j] + 0.000000000001
          T[i][j] = T[i-1][j]
        else:
          C[i][j] = C[i][j-1]
          if X[i-1] == '%':
            T[i][j] = T[i][j-1] + Y[j-1]
          else:
            T[i][j] = T[i][j-1]
  return C, T
'''
'''
def LCSMatrixTemplated(X, Y):
  # X templated
  # % is template substitution string
  m = len(X)
  n = len(Y)
  # An (m+1) times (n+1) matrix
  M = [[0] * (n+1) for i in range(m+1)]
  # Number of characters in target that were missed
  S = [[0] * (n+1) for i in range(m+1)]
  # Number of characters in template that have been matched
  E = [[0] * (n+1) for i in range(m+1)]
  # Number of characters that have been exchanged
  T = [[''] * (n+1) for i in range(m+1)]
  def score(i,j):
    return S[i][j] - M[i][j] - E[i][j]
  for i in range(1, m+1):
    for j in range(1, n+1):
      if X[i-1] == Y[j-1]:
        # Character match
        M[i][j] = M[i-1][j-1]
        S[i][j] = S[i-1][j-1] + 1
        T[i][j] = T[i-1][j-1]
        E[i][j] = E[i-1][j-1]
      else:
        if X[i-1] != '%' and score(i-1,j-1) >= score(i-1,j) and score(i-1,j-1) >= score(i,j-1):
          # Misdetected character substitution
          M[i][j] = M[i-1][j-1]
          S[i][j] = S[i-1][j-1] + 1
          T[i][j] = T[i-1][j-1]
          E[i][j] = E[i-1][j-1] + 1
        elif score(i-1,j) > score(i,j-1):
          # Template is missing a character
          M[i][j] = M[i-1][j]
          S[i][j] = S[i-1][j]
          T[i][j] = T[i-1][j]
          E[i][j] = E[i-1][j]
          if X[i-1] == '%':
            T[i][j] += '^'
        else:
          S[i][j] = S[i][j-1]
          if X[i-1] == '%':
            # Template substitution
            M[i][j] = M[i][j-1]
            T[i][j] = T[i][j-1] + Y[j-1]
          else:
            # Target is missing a character
            M[i][j] = M[i][j-1] + 1
            T[i][j] = T[i][j-1]
  print E
  return M, S, E, T
'''

def LCSMatrixTemplated(X, Y):
  # X templated
  # % is template substitution string
  m = len(X)
  n = len(Y)
  # An (m+1) times (n+1) matrix
  M = [[0] * (n+1) for i in range(m+1)]
  # Number of characters in template text that have been matched
  T = [[''] * (n+1) for i in range(m+1)]
  def score(i,j):
    return M[i][j]
  for i in range(1, m+1):
    for j in range(1, n+1):
      if X[i-1] == Y[j-1]:
        # Character match
        M[i][j] = M[i-1][j-1] + 1
        T[i][j] = T[i-1][j-1]
      else:
        if M[i-1][j] > M[i][j-1]:
          # Template is missing a character
          M[i][j] = M[i-1][j]
          T[i][j] = T[i-1][j]
          if X[i-1] == '%':
            T[i][j] += '^'
        else:
          if X[i-1] == '%':
            # Template substitution
            M[i][j] = M[i][j-1]
            T[i][j] = T[i][j-1] + Y[j-1]
          else:
            # Target is missing a character
            M[i][j] = M[i][j-1]
            T[i][j] = T[i][j-1]
  return M, T

def LCSTemplatedScore(X, Y):
  M, T = LCSMatrixTemplated(X, Y)
  matchedTemplateChars = M[-1:][0][-1:][0]
  numTemplateChars = len(X.replace('%', ''))
  templateWords = T[-1:][0][-1:][0]
  templateWordsLength = len(templateWords.replace('^', ''))
  rawTargetTextLength = len(Y) - templateWordsLength
  return float(matchedTemplateChars) / max(numTemplateChars, rawTargetTextLength), rawTargetTextLength

def startsWith(x, prefix):
  return x[0:len(prefix)] == prefix

def stripPrefix(x, prefix):
  if x[0:len(prefix)] == prefix:
    return x[len(prefix):].strip()
  return x.strip()

def stripSuffix(x, suffix):
  if x[-len(suffix):] == suffix:
    return x[:-len(suffix)].strip()
  return x.strip()

#print LCSTemplatedScore('the%bar%thien', 'theamlakbarasgnlsakdnglathien')

msgids = open('es.po').readlines()
msglist = []
curmsg = []
active = False
for x in msgids:
  x = x.strip()
  if x[:1] == '#':
    continue
  if startsWith(x, 'msgid "'):
    active = True
    x = stripPrefix(x, 'msgid "')
    if len(curmsg) > 0:
      msglist.append(' '.join(curmsg).strip())
      curmsg = []
  elif startsWith(x, 'msgstr "'):
    active = False
  if active:
    x = stripPrefix(x, '"')
    x = stripSuffix(x, '"')
    x = x.replace('\\"', '"')
    x = x.replace('%s', '%')
    x = x.replace('\\n', ' ')
    curmsg.append(x.strip())
if len(curmsg) > 0:
  msglist.append(' '.join(curmsg).strip())
while '' in msglist:
  msglist.remove('')

words = open('words').readlines()
words = [x.strip() for x in words]
words = [x for x in words if x != '']
words = [x.split(':')[-1:][0] for x in words]
for msg in msglist:
  bestratio = -1.0
  bestlength = -1.0
  bestmatch = ''
  for x in substrings(words):
    if not len(msg) <= len(x)*1.5:
      continue
    if (not '%' in msg) and not len(x)/1.5 <= len(msg):
      continue
    curratio, textlen = LCSTemplatedScore(msg, x)
    if curratio >= bestratio:
      if curratio == bestratio:
        if textlen < bestlength:
          continue
      bestmatch = x
      bestratio = curratio
      bestlength = textlen
  if bestratio >= (1/1.5):
    print msg, ':', bestmatch, bestratio


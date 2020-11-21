import re
# f_path = input('Enter a file path: ')
# type = input('Enter an operation type ("read" or "write": ')
WORD_TO_FIND = 'imperdiet'
f_path = 'lorem.txt'
type = 'write'

if type == 'read':
  with open('lorem.txt', 'r') as f:
    word_count = 0
    line_count = 0
    for line in f:
      if WORD_TO_FIND in line:
        line_count += 1
        line_list = line.split()
        for word in line_list:
          stripped_word = word.strip()
          if WORD_TO_FIND in stripped_word:
            word_count += 1
  print('\n***** Read Results *****')
  print('''Number of instances of word "{0}" in {1}: {2}'''.format(WORD_TO_FIND, f_path, word_count))
  print('''Number of lines containing the word "{0}" in {1}: {2}\n'''.format(WORD_TO_FIND, f_path, line_count))
elif type == 'write':
  with open('lorem.txt', 'a+') as f:
    user_sentence = input('Please enter a sentence: ')
    f.write(user_sentence + '\n')
    sentences_list = re.split('[?.!]', user_sentence)
    print(sentences_list)

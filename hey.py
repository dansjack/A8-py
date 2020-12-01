import re
import logging
import time
import os

def read_operation(file):
  try:
    total_read_time = 0.0
    total_imperdiet_read_time = 0.0
    with open(file, 'r') as f:
      word_count = 0
      line_count = 0
      total_lines = 0
      for line in f:
        readline_start_time = time.time()
        total_lines += 1
        if WORD_TO_FIND in line:
          find_imperdiet_start_time = time.time()
          line_count += 1
          line_list = line.split()
          for word in line_list:
            stripped_word = word.strip()
            if WORD_TO_FIND in stripped_word:
              word_count += 1
          find_imperdiet_end_time = time.time()
          total_imperdiet_read_time += round((find_imperdiet_end_time - find_imperdiet_start_time), 10)
        readline_end_time = time.time()
        total_read_time += round((readline_end_time - readline_start_time), 10)
      f.close()
    logging.debug('Time to read entire file: {0}'.format(total_read_time));
    logging.debug('Time to read all instances of {1} in the file: {0}'.format(total_imperdiet_read_time, WORD_TO_FIND));
    logging.debug('Average read time for each line in the file: {0}'.format(round(total_read_time / total_lines, 3)))
    logging.debug('Average time to find {1} in each line: {0}'.format(round(total_imperdiet_read_time / line_count, 3), WORD_TO_FIND))
    print('\n***** Read Results *****')
    print('''Number of instances of "{0}" in {1}: {2}'''.format(WORD_TO_FIND, file, word_count))
    print('''Number of lines containing "{0}" in {1}: {2}\n'''.format(WORD_TO_FIND, file, line_count))
  except FileNotFoundError as err:
    logging.exception('File not found at: ' + file)
    logging.critical('Something happened to the file the user provided after initially providing the path')
    print('The file at ' + file + ' can no longer be found. Exiting program.')
    exit(1)

def write_operation(file):
  user_sentences = []
  word_count = 0
  word_sentence_count = 0
  write_line_time = 0.0
  find_line_time = 0.0
  logging.debug('Prompting user to enter sentence(s)...')
  while(True):
    user_sentence = input('''Please enter a sentence, or type "done" if you're finished adding sentences: ''')
    if (user_sentence == 'done'):
      break
    else:
      user_sentences.append(user_sentence)
  
  # find the number of times WORD_TO_FIND appears in all sentences
  # and the number of sentences WORD_TO_FIND appears in
  logging.debug('Counting WORD_TO_FIND in user sentence(s)...')
  for sentence in user_sentences:
    if WORD_TO_FIND in sentence:
      find_start_time = time.time()
      word_sentence_count += 1
      for word in sentence.split():
        stripped_word = word.strip()
        if WORD_TO_FIND in stripped_word:
          word_count += 1
      find_end_time = time.time()
      find_line_time += round(find_start_time - find_end_time, 3)

  logging.debug('Writing user input to file...')
  # Don't need try/exception like in read_operation() because file will be created if it somehow went missing between the time the user entered the file path and here
  with open(file, 'w') as f:
    sentence_count = len(user_sentences)
    while(len(user_sentences) > 0):
      current_sentence = user_sentences.pop(0)
      write_start_time = time.time()
      f.write(current_sentence + '\n')
      write_end_time = time.time()
      write_line_time += round((write_end_time - write_start_time), 3)
    f.close()

    logging.debug('Time to write all lines to file: {0}'.format(write_line_time))
    logging.debug('Time to find the word {1} in each line: {0}'.format(find_line_time, WORD_TO_FIND))
    logging.debug('Average time to write a line to the file: {0}'.format(round(write_line_time / sentence_count)))
    logging.debug('Average time to find {1} in each line: {0}'.format(round(find_line_time / word_sentence_count), WORD_TO_FIND))
    print('\n***** Write Results *****')
    print('Number of sentences in user input: {0}'.format(sentence_count))
    print('Number of times "{0}" appears in user input: {1}'.format(WORD_TO_FIND, word_count))
    print('Number of sentences "{0}" appers in: {1}'.format(WORD_TO_FIND, word_sentence_count))

start_time = time.time()
logging.basicConfig(level='DEBUG', filename='consoleapp.log', filemode='w', format='%(asctime)s %(levelname)s %(name)s - %(message)s')
logging.info('Starting A8: Cloud Operations program...')


logging.debug('Prompting user for the path to an existing file...')
while(True):
  f_path = input('Enter a file path: ')
  if not os.path.exists(f_path):
    logging.warning('No file exists at the path the user provided: ' + f_path)
    print('\nThere is no file at ' + f_path + '. Please try again.')
  else:
    break

logging.debug('Prompting user for operation type...')
while(True):
  type = input('Enter an operation type ("read" or "write"): ')
  if type not in ['read', 'write']:
    logging.warning('User entered an invalid type: ' + type)
    print('\nInvalid type, operation can either be "read" or "write".')
  else:
    break
WORD_TO_FIND = 'imperdiet'

if type == 'read':
  logging.debug('Read operation selected...')
  read_operation(f_path)
elif type == 'write':
  logging.debug('Write operation selected...')
  write_operation(f_path)

end_time = time.time()
total_execution_str = 'Total execution time: {0}'.format(round(end_time - start_time, 3))
logging.info(total_execution_str)
logging.info('End of A8: Cloud Operations program')


import re
import logging
import time
import os
import sys

# config logging
log_level = 'DEBUG'
logging.basicConfig(level=log_level, filename='consoleapp.log', filemode='w', format='%(asctime)s %(levelname)s %(name)s - %(message)s')

# constants
WORD_TO_FIND = 'imperdiet'
MAX_PASSWORD_ATTEMPTS = 3
TEST_PASSWORD = 'superSecurePassword'

def read_operation(file):
  """Reads from the given file and counts instances of the WORD_TO_FIND overall and in each line"""
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
    total_read_str = 'Time to read entire file: {0}'.format(total_read_time)
    total_word_str = 'Time to read all instances of "{1}" in the file: {0}'.format(total_imperdiet_read_time, WORD_TO_FIND)
    avg_read_str = 'Average read time for each line in the file: {0}'.format(round(total_read_time / total_lines, 3))
    avg_word_str = 'Average time to find {1} in each line: {0}'.format(round(total_imperdiet_read_time / line_count, 3), WORD_TO_FIND)
    logging.debug(total_read_str)
    logging.debug(total_word_str)
    logging.debug(avg_read_str)
    logging.debug(avg_word_str)

    print('\n***** Read Results *****')
    print('''Number of instances of "{0}" in {1}: {2}'''.format(WORD_TO_FIND, file, word_count))
    print('''Number of lines containing "{0}" in {1}: {2}'''.format(WORD_TO_FIND, file, line_count))
    return [total_read_str, total_word_str, avg_read_str, avg_word_str]
  except FileNotFoundError as err:
    logging.exception('File not found at: ' + file)
    logging.exception(err)
    logging.critical('Something happened to the file user provided after initially providing the path')
    print('The file at ' + file + ' can no longer be found.\nExiting program.')
    exit(1)
  except IsADirectoryError as err:
    logging.exception('File path leads to directory, not file: ' + file)
    logging.exception(err)
    logging.critical('Path leads to a directory, cannot proceed with the rest of program')
    print('File path leads to directory, not file: ' + file + '.\nExiting program.')
    exit(1)

def write_operation(file):
  """Writes user input to the given file and counts instances of the WORD_TO_FIND overall and in each line of the user input"""
  user_sentences = []
  word_count = 0
  word_sentence_count = 0
  write_line_time = 0.0
  find_line_time = 0.0
  logging.debug('Prompting user to enter sentence(s)...')
  while(True):
    user_sentence = input('''Please enter a sentence, or type "done" if you're finished adding sentences: ''')
    if user_sentence == 'q':
      sys.exit()
    elif (user_sentence == 'done'):
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
  try:
    with open(file, 'w') as f:
      sentence_count = len(user_sentences)
      while(len(user_sentences) > 0):
        current_sentence = user_sentences.pop(0)
        write_start_time = time.time()
        f.write(current_sentence + '\n')
        write_end_time = time.time()
        write_line_time += round((write_end_time - write_start_time), 3)
      f.close()

      write_line_str = 'Time to write all lines to file: {0}'.format(write_line_time)
      find_line_str = 'Time to find the word {1} in each line: {0}'.format(find_line_time, WORD_TO_FIND)
      avg_line_str = 'Average time to write a line to the file: {0}'.format(round(write_line_time / sentence_count, 3))
      avg_find_str = 'Average time to find {1} in each line: {0}'.format(round(find_line_time / word_sentence_count, 3), WORD_TO_FIND)

      logging.debug(write_line_str)
      logging.debug(find_line_str)
      logging.debug(avg_line_str)
      logging.debug(avg_find_str)

      print('\n***** Write Results *****')
      print('Number of sentences in user input: {0}'.format(sentence_count))
      print('Number of times "{0}" appears in user input: {1}'.format(WORD_TO_FIND, word_count))
      print('Number of sentences "{0}" appers in: {1}'.format(WORD_TO_FIND, word_sentence_count))
    return [write_line_str, find_line_str, avg_line_str, avg_find_str]
  except IsADirectoryError as err:
    logging.exception('File path leads to directory, not file: ' + file)
    logging.exception(err)
    logging.critical('Path leads to a directory, cannot proceed with the rest of program')
    print('File path leads to directory, not file: ' + file + '.\nExiting program.')
    exit(1)
start_time = time.time()

def main():
  """The main function of the program. Gets user input for file path, operation type, and admin password (if applicable). The program then runs through the read_operation() or write_operation() depending on the user's selection"""
  print('***** A8: Cloud Operations program *****')
  print('Enter q to quit at any time\n')
  logging.debug('Prompting user for the path to an existing file...')
  while(True):
    f_path = input('Enter a file path: ')
    if f_path == 'q':
      sys.exit()
    elif not os.path.exists(f_path):
      logging.warning('No file exists at the path the user provided: ' + f_path)
      print('\nThere is no file at ' + f_path + '. Please try again.')
    else:
      break

  logging.debug('Prompting user for operation type...')
  while(True):
    type = input('Enter an operation type ("read" or "write"): ')
    if type == 'q':
      sys.exit()
    elif type not in ['read', 'write']:
      logging.warning('User entered an invalid type: ' + type)
      print('\nInvalid type, operation can either be "read" or "write".')
    else:
      break

  password_attempts = 0
  is_admin = False
  logging.debug('Prompting user for admin password...')
  while(password_attempts < MAX_PASSWORD_ATTEMPTS):
    admin_response = input('''If you're an admin, enter the password to see performance stats (just press enter if not an admin): ''')
    password_attempts += 1
    if admin_response == TEST_PASSWORD:
      is_admin = True
      break
    elif admin_response == '' or password_attempts == MAX_PASSWORD_ATTEMPTS:
      break
    elif admin_response == 'q':
      sys.exit()
    else:
      logging.warning('User entered incorrect admin password: {0}'.format(admin_response))
      print('\nIncorrect password, please try again ({0} attempt{1} remaining)'.format(MAX_PASSWORD_ATTEMPTS - password_attempts, 's' if password_attempts < 2 else ''))

  if password_attempts >= MAX_PASSWORD_ATTEMPTS:
    print('\nFailed to enter correct admin password, exiting program.')
    sys.exit()

  admin_stats = []
  if type == 'read':
    logging.debug('Read operation selected...')
    admin_stats = read_operation(f_path)
  elif type == 'write':
    logging.debug('Write operation selected...')
    admin_stats = write_operation(f_path)

  end_time = time.time()
  total_execution_str = 'Total execution time: {0}'.format(round(end_time - start_time, 3))
  logging.info(total_execution_str)

  if is_admin is True:
    # print stats
    print('\n***** Performance Stats *****')
    for stat in admin_stats:
      print(stat)
    print(total_execution_str)
if __name__ == "__main__":
    logging.info('Starting A8: Cloud Operations program...')
    main()
    logging.info('End of A8: Cloud Operations program')
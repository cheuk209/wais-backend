
def determine_scaled_scores_range(number_range_list, target_number):
  for number_range in number_range_list:
    print(number_range)
    if number_range == '-':
      continue
    number_range_split = number_range.split('-')
    print(number_range_split)
    print(len(number_range_split))
    if len(number_range_split) == 1:
      print('come on mate')
      print(type(number_range_split[0]))
      print(type(target_number))
      print (number_range_split[0] == target_number)
      print('hang on')
      if number_range_split[0] == target_number:
        return target_number
    elif len(number_range_split) != 1:
      if int(number_range_split[0]) <= int(target_number) <= int(number_range_split[1]):
        return number_range

print(determine_scaled_scores_range(['0-4', '5', '6-7', '8-9', '10', '11-12', '13-14', '15-16', '17-18', '19', '20', '21', '22', '23', '24', '25', '-', '26', '-'], 10))
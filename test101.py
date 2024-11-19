import openai

# openai.api_key = "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"
#
# response = openai.Completion.create(
#   model="gpt-3.5-turbo-instruct",
#   prompt="Write a Python program to remove duplicates from a list of lists. ",
#   temperature=1,
#   max_tokens=256,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=0
# )
#
# message = response.choices[0].text.strip()
# print(message)

def test(dictt):
    min_value=1
    result = [k for k, v in dictt.items() if len(v) == (min_value)]
    return result

dictt = {
 'V': [10, 12],
 'VI': [10],
 'VII': [10, 20, 30, 40],
 'VIII': [20],
 'IX': [10,30,50,70],
 'X': [80]
 }

print("\nOriginal Dictionary:")
print(dictt)
print("\nShortest list of values with the keys of the said dictionary:")
print(test(dictt))


def shortest_list_in_dict(d):
  len_of_smallest_list = min(len(v) for v in d.values())
  keys_of_smallest_lists = [k for k, v in d.items() if len(v) == len_of_smallest_list]
  return keys_of_smallest_lists


d = {
  'V': [10, 12],
  'VI': [10],
  'VII': [10, 20, 30, 40],
  'VIII': [20],
  'IX': [10, 30, 50, 70],
  'X': [80]
}

print("\nOriginal Dictionary:")
print(d)
print("\nKeys of shortest lists:")
print(shortest_list_in_dict(d))
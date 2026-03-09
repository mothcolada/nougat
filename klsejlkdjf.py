from atproto import Client

# def split_array(array, key):
#     new_arrays: list[list] = [[]]
#     for i in array:
#         if i == key:
#             new_arrays.append([])
#         else:
#             new_arrays[-1].append(i)
#     return new_arrays

# a = ['hi', 'um', 'ok', 'yeah', 'so', 'um', 'like', 'sure']
# print(split_array(a, 'um'))


bsky_client = Client()
bsky_client.login('nougat.lonelywolftre.at', 'askdljasldj')
print('logged in!')
bsky_client.send_post('nougat\n#nomnomnami', embed=None)

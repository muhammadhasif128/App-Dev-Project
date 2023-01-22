# import shelve
# import User
#
# users_dict = {}
# db = shelve.open('user.db', 'r')
# users_dict = db['Users']
#
# users_list = []
# # for key in users_dict:
# #     user = users_dict.get(key)
# #     users_list.append(user)
# #
#
# elist = []
# def afunction():
#     for key in db:
#         user = users_dict.get(key)
#         users_list.append(user)
#         for i in db[key]:
#             # print(i)
#             # print(users_dict[i])
#             elist.append(bfunction(users_dict[i]))
#         bfunction(users_dict[i])
#
# def bfunction(u):
#     return u.get_email_address()
#
# afunction()
#
#
# print(elist)
# if 'Sample@gmail.com' in elist:
#     print('yes')
# else:
#     print('email is incorrect')
#
aList =['Olfsen@gmail.com', 'another@gmail.com', 'another@gmail.com']
pList= ['Fastburg12345!', 'Fastburg12345!', 'Fastburg12345!']

print(aList.index('another@gmail.com'))

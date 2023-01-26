import shelve

admin_dict = {}
dbA = shelve.open('admin.db', 'r')
try:
    admin_dict = dbA['Staff']
except:
    print("Error retrieving users in admin.db")

# for key in users_dict:
#     user = users_dict.get(key)
#     users_list.append(user)
#

aList = []
def Sfunction():
    for key in dbA:
        for i in dbA[key]:
            aList.append(i)
    return max(aList)


users_dict = {}
dbU = shelve.open('user.db', 'r')
try:
    users_dict = dbU['Users']
except:
    print("error in users")


uList = []
def Ufunction():
    for key in dbU:
        for i in dbU[key]:
            uList.append(i)
    return max(uList)
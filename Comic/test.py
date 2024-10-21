# str = ['0','1','2','3','4','5','6','7','8','9','I','V','X']
str = '0123456789IVX'
text = 'wjnkhjdajhbnfdl'
name_tag = False
i = 0
while i<len(str) :
    if str[i] in text : 
        # print (str[i])
        # print (text)
        # print (str[i] in text)
        # print (name_tag)
        name_tag = True
        break
    i+=1
    # print(name_tag)
print (name_tag)
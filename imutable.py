# here the id is same so it is imutable
number = set();
print("intial",number)
print("intial Id",id(number))
number.add(2)
number.add(3)
print("after intial",number)
print("after intial Id",id(number))
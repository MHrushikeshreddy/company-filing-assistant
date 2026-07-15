"""
#example1 
a=34
b=32. #variabless is being intialized with numbers

a,b = b,a#those variables being swapped

print("a=",a,"b=",b)#print that swapped numbers

#example2

x=1
y=2
z=3

largest_number=max(x,y,z)
print(largest_number ,"is the largest number")

#ex3
#odd or even
n=44444444441
if n%2==0:
    print("even")
else:
    print("ODD")


#day2
#ex1
def reverse_string(s):
    result=""
    for char in s:
        result = char+result
    return result
print(reverse_string("bacdef"))

#ex2
def second_largest(nums):
    unique_nums = list(set(nums))   # remove duplicates
    unique_nums.sort(reverse=True)  # sort in descending order
    return unique_nums[1] if len(unique_nums) > 1 else None

numbers = [12, 45, 2, 67, 45, 67, 99]
print(second_largest(numbers))  # Output: 67 


def sec_no(num):
    unq_num=list(set(num))
    unq_num.sort()
    return unq_num[1] if len(num)>1 else None
numbers= [124, 445, 325, 657, 465, 672, 996]
print(sec_no(numbers))

"""
#ex3

def word_frequency(sentence):
    words = sentence.split()  # split into words
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

sentence = "python is easy and python is powerful"
print(word_frequency(sentence))
# Output: {'python': 2, 'is': 2, 'easy': 1, 'and': 1, 'powerful': 1}




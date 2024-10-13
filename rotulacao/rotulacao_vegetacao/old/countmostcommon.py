from collections import Counter
 
def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]
   
List = [2, 1, 2, 2, 1, 3, 3, 3, 3]
print(most_frequent(List))
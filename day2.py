import numpy as np
marks = np.array([[70, 80, 90],
[60, 75, 85],
[88, 92, 79],
[55, 65, 70]])

# print(marks.shape)
# print(marks.dtype)
# print(marks.size)


# print(marks[:2,-1])

# student_average =marks.mean(axis=1)  
# subject_average =marks.mean(axis=0)  
# print(student_average)

# grace_marks = marks + 5
# print(grace_marks)


weights = np.array([0.3, 0.3, 0.4])
print(np.dot(marks, weights))
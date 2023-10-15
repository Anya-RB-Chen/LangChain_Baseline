YESORNO = """Given the following information about PolyU's courses and academic staff:
"
{info}
"

The following Yes/No questions (with answers) are according to the information above:

Did PolyU offer a course on "Computer Vision" with course code of COMP4423?
Answer: Yes

Is Prof. Wong Wing-tak insterested in "Linear Algebra"?
Answer: No

{question}
Answer:"""

# ================================================================================
# ================================================================================


PHRASE = """Given the following information about PolyU's courses and academic staff:
"
{info}
"

The following questions (with answers) are according to the information above:

What is the course code of the course "Computer Vision"?
Answer: COMP4423

Who is the chair professor of department of applied mathematics?
Answer: Prof. Chen Xiaojun

{question}
Answer:"""

# ================================================================================
# ================================================================================


SENTENCE = """Given the following information about PolyU's courses:
"
{info}
"

The following questions (with answers) are according to the information above:

What can I learn from the course "Computer Vision"?
Answer: This course is designed for the students interested in learning fundamental principles and important applications of computer vision using digital imaging. These images can be acquired using digital cameras in smartphones, infrared cameras, radars, or specialised sensors such as those employed for the medical imaging. This course will introduce a number of fundamental concepts in computer vision. During this course, the students will gain hands-on experience on a number of computer vision algorithms for the real-world applications.

What's the difference between COMP4423 and COMP4431?
Answer: The difference between COMP4423 and COMP4431 is that they are two different courses offered by the Department of Computing at PolyU. COMP4423 is a course on Computer Vision, which focuses on the fundamental principles and important applications of computer vision using digital imaging. COMP4431 is a course on Artificial Intelligence, which covers the basic concepts and techniques of artificial intelligence, such as search, knowledge representation, reasoning, planning, machine learning, natural language processing, and computer vision. Both courses have a credit value of 3 and are at level 4, but they have different objectives and contents.

{question}
Answer:"""

# ================================================================================
# ================================================================================


LIST = """Given the following information about PolyU's courses and academic staff:
"
{info}
"
The following questions (with list of elements as answers) are according to the information above:

What courses sould I take if I want to learn about "Computer Vision" and "Artificial Intelligence"?
Answer: comp4423, comp4431

Who are the professors that are interested in "cancer therapy" and work in Department of Applied Biology and Chemical Technology?
Answer: Prof. Chow Ming-cheung, Prof. Wong Wing-tak, Wong Ka-Leung, Tai Chi-shing

{question}
Answer:"""

# ================================================================================
# ================================================================================

MC = """Given the following information about PolyU's courses and academic staff:
"
{info}
"

The following multiple choice questions (with answers) are according to the information above:

Which of the following courses are offered by dept of APSS?
A. aae3003
B. apss3301
C. comp4431
D. apss5119
Answer: B

Who has research interest in "cancer therapy"?
A. Prof. Chow Ming-cheung
B. Prof. Wong Wing-tak
C. Qing Li
D. Cao Jiannong
Answer: A,B

{question}
Answer:"""

# ================================================================================
# ================================================================================


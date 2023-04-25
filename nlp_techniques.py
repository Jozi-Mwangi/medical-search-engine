# import required module
from sklearn.feature_extraction.text import TfidfVectorizer

with open("Disease_results.txt", "r") as f:
    lines=f.readlines()

vectorizer = TfidfVectorizer()

X=vectorizer.fit_transform(lines)

# analyze = vectorizer.build_analyzer()

# print("Document Disease NLP: ", analyze(lines))
# print("Document 2: ", analyze(Document2))
# print("Document 3: ", analyze(Document3))
print("Document Transform: ", X.toarray())

print(vectorizer.get_feature_names_out())
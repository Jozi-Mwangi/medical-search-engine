from sklearn.feature_extraction.text import TfidfVectorizer



with open("Disease_results.txt", "r") as f:
    lines=f.readlines()

vectorizer = TfidfVectorizer()
X=vectorizer.fit_transform(lines)

print("Document Transform: ", X.toarray())
print("Feature Names: ", vectorizer.get_feature_names_out())
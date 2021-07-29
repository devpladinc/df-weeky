# force match query for summary
force_match = {
    'power bi' : 'Power BI',
    'sql' : 'SQL',
    'Sql' : 'SQL'
}

exclude_sections = [
    'See also',
    'External links',
    'References',
    'Further reading'
]

topics = {
    'python' : 'Python_(programming_language)',
    'microsoft azure' : 'microsoft azure',
    'azure' : 'microsoft azure',
    'kotlin' : 'Kotlin (programming language)',
    'java' : 'Java (programming language)',
    'javascript' : 'Javascript (programming language)',
    'c++' : 'C++ (programming language)',
    'Logistics regression' : 'Logistic regression',
    'power bi' : 'Microsoft Power BI',
    'deep learning' : 'Deep learning',
    'machine learning' : 'Machine learning',
    'programming' : 'Programming language',
    'k-means clustering' : 'K-means_clustering'
}

main_chips = {
    "Data science" : "ds-landing",
    "Machine Learning" : "ml-landing",
    "Programming" : "pl-landing"
}


dynamic_chips_1 = {
    "Linear regression" : "lr-landing",
    "Deep Learning" : "dl-learning",
    "Logistics regression" : "logr-landing",
}

dynamic_chips_2 = {
    "Python" : 'python-landing',
    "Java" : "java-landing",
    "Power BI" : "pb-landing"
}

dynamic_chips_3 = {
    "Python" : 'python-landing',
    "Deep Learning" : "dl-learning",
    "Power BI" : "pb-landing"
}

dynamic_chips_4 = {
    "Logistics regression" : "logr-landing",
    "Deep Learning" : "dl-learning",
    "Azure" : "az-landing"
}

# always update if adding dynamic chip dict above
dynamic_chips = [
    dynamic_chips_1,
    dynamic_chips_2,
    dynamic_chips_3,
    dynamic_chips_4
]
# Tesis Captura de atributos discriminativos

## Aquí se encuentra el desarrollo del trabajo de tesis captura de atributos discriminativos desarrollado en Python y algunas de sus librerías, así como algunos archivos que se utilizaran durante el proceso.

## Herramientas

Se muestra una lista con las Herramientas que son necesarias para este proyecto

* ## Python
    * Python
    * Spyder (opcional) is the Scientific PYthon Development EnviRonment

* ## Natural Language Toolkit (NLTK) 
    * Is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum.
    * [install](https://www.nltk.org/)
    * [Data and corpus](https://www.nltk.org/data.html)
      ```
      import nltk
      nltk.download()
      ```

* ## WordNet
    * Is a large lexical database of English. Nouns, verbs, adjectives and adverbs are grouped into sets of cognitive synonyms (synsets), each expressing a distinct concept. Synsets are interlinked by means of conceptual-semantic and lexical relations.
    * [WordNet Interface](http://www.nltk.org/howto/wordnet.html)

* ## TextBlob
    * Is a Python (2 and 3) library for processing textual data. It provides a simple API for diving into common natural language processing (NLP) tasks such as part-of-speech tagging, noun phrase extraction, sentiment analysis, classification, translation, and more.
    * [install](http://textblob.readthedocs.io/en/dev/install.html)
      ```
      pip install -U textblob
      python -m textblob.download_corpora
      ```


* ## SpaCy
    * [install SpaCy](https://spacy.io/usage/#section-quickstart)
    * [install Models](https://spacy.io/usage/models)
    * Nota: con pip tiene problemas de instalacion, (utilizar sudo para instalar modelos) utilizar conda o bien el comando de abajo (solo python 3)
    * ```pip3 install spacy && python3 -m spacy download en```
    * [Documentación](https://spacy.io/usage/linguistic-features)

* ## Wikipedia API
    * Is easy to use Python wrapper for Wikipedias’ API. It supports extracting texts, sections, links, categories, translations, etc from Wikipedia. 
    * [Documentación](http://wikipedia-api.readthedocs.io/en/latest/README.html)
    * (only for python3)
    * ```pip3 install wikipedia-api```

* ## [Requests](http://docs.python-requests.org/en/master/user/quickstart/)
    * ``` pip3 install requests ```
    * HTTP GET

* ## [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
    * Is a Python library for pulling data out of HTML and XML files.
      ```
      pip2 install bs4
      pip3 install bs4
      ```
    * Parsing BeautifulSoup


### Objetivos
#### Objetivo General
Proponer un modelo de atributos discriminativos entre pares de palabras y un atributo extrayendo las diferencias semánticas de cada una.

#### Objetivos Específicos
1. Estudiar los artículos asociados a este problema que fue planteado por primera vez en el marco de SemEval 2016
2. Determinar el algoritmo de expansión de cada palabra que componen cada sentencia
3. Proponer un modelo que use el algoritmo anterior
4. Probar el modelo desarrollado
5. Participar en la conferencia SemEval 2018

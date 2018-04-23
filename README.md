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
      ```
      pip3 install requests
      ```
    * HTTP GET

* ## [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
    * Is a Python library for pulling data out of HTML and XML files.
      ```
      pip2 install bs4
      pip3 install bs4
      ```
    * Parsing BeautifulSoup



### Resumen

En la actualidad se han visto grandes avances tecnológicos, los cuales han motivado a mejorar la comunicación humano computadora es decir, que la máquina necesita procesar el lenguaje humano para tareas específicas, algunos ejemplos serian traductores de idioma, correctores de documentos, extracción de información relevante, búsquedas en internet con criterios específicos (buscar por idioma, fecha, relevancia, etc.) por mencionar algunos, se tiene una disciplina de Procesamiento del Lenguaje Natural (PLN) que combina la rama de la lingüística y la informática con el objetivo de modelar el lenguaje humano desde el punto de vista computacional.
Dentro de la rama de la lingüística se encuentra la disciplina de la semántica que estudia los significados de las palabras y de las expresiones más complejas. Hoy en día los modelos semánticos hacen un excelente trabajo para la detección de similitud semántica dentro del PLN. Sin embargo, muestran algunos errores ya que los modelos no pueden predecir las diferencias semánticas entre pares de palabras, para el caso de cappuccino, espresso y americano tienen un uso limitado los modelos semánticos, puesto que pueden decir que son similares entre si. Una posible solución a este problema es expresar las diferencias semánticas entre las palabras, al referirse a sus atributos que componen a cada palabra, por lo que una diferencia se puede expresar como la presencia o ausencia de un atributo en específico. Por ejemplo, una de las diferencias entre un narwhal (narval) y un dolphin (delfín) es la presencia del atributo horn (cuerno). Cabe mencionar que las palabras con las que se trabajará se tomarán en cuenta con su significado denotativo o denotación, es decir, el significado de la expresión tal cual se encuentra en el diccionario, no contextual. El no incluir las palabras con varios significados. Un ejemplo de lo anterior es para la palabra bow (weapon = arma), bow (curva, inclinación) and bow (ribbon = cinta, lazo, listón).
**Entonces para cada par de palabras se verifica que la primera tenga relación con el atributo proporcionado, pero la segunda no tenga relación alguna con el atributo para agregarlo a __lista de ejemplos candidatos positivos.__** Un ejemplo de lo anterior seria **palabra1 airplane (avión), palabra2 helicopter (helicóptero) y atributo wings (alas), donde la palabra1 tiene relación con el atributo wings, pero no la palabra2,** ya que un helicóptero no tiene alas; en el caso de palabra1 helicopter, palabra2 airplane, atributo wings se tomará en otra lista, ya que la palabra1 no tiene relación con el atributo. **Para la __lista de ejemplos negativos__ se tomarán en cuenta los casos donde ambas palabras tengan relación con el atributo y donde las dos palabras no tienen relación alguna con el atributo,** para este último caso la cantidad de ejemplos es muy grande.


### Objetivos
#### Objetivo General
Proponer un modelo de atributos discriminativos entre pares de palabras y un atributo extrayendo las diferencias semánticas de cada una.

#### Objetivos Específicos
1. Estudiar los artículos asociados a este problema que fue planteado por primera vez en el marco de SemEval 2016
2. Determinar el algoritmo de expansión de cada palabra que componen cada sentencia
3. Proponer un modelo que use el algoritmo anterior
4. Probar el modelo desarrollado
5. Participar en la conferencia SemEval 2018

# Tesis Captura de atributos discriminativos

## Aquí se encuentra el desarrollo del trabajo de tesis captura de atributos discriminativos desarrollado en Python y algunas de sus librerías, así como algunos archivos que se utilizaran durante el proceso.

### Resumen

En la actualidad se han visto grandes avances tecnológicos, los cuales han motivado a mejorar la comunicación humano computadora es decir, que la máquina necesita procesar el lenguaje humano para tareas específicas, algunos ejemplos serian traductores de idioma, correctores de documentos, extracción de información relevante, búsquedas en internet con criterios específicos (buscar por idioma, fecha, relevancia, etc.) por mencionar algunos, se tiene una disciplina de Procesamiento del Lenguaje Natural (PLN) que combina la rama de la lingüística y la informática con el objetivo de modelar el lenguaje humano desde el punto de vista computacional.
Dentro de la rama de la lingüística se encuentra la disciplina de la semántica que estudia los significados de las palabras y de las expresiones más complejas. Hoy en día los modelos semánticos hacen un excelente trabajo para la detección de similitud semántica dentro del PLN. Sin embargo, muestran algunos errores ya que los modelos no pueden predecir las diferencias semánticas entre pares de palabras, para el caso de cappuccino, espresso y americano tienen un uso limitado los modelos semánticos, puesto que pueden decir que son similares entre si. Una posible solución a este problema es expresar las diferencias semánticas entre las palabras, al referirse a sus atributos que componen a cada palabra, por lo que una diferencia se puede expresar como la presencia o ausencia de un atributo en específico. Por ejemplo, una de las diferencias entre un narwhal (narval) y un dolphin (delfín) es la presencia del atributo horn (cuerno). Cabe mencionar que las palabras con las que se trabajará se tomarán en cuenta con su significado denotativo o denotación, es decir, el significado de la expresión tal cual se encuentra en el diccionario, no contextual. El no incluir las palabras con varios significados. Un ejemplo de lo anterior es para la palabra bow (weapon = arma), bow (curva, inclinación) and bow (ribbon = cinta, lazo, listón).
Entonces para cada par de palabras se verifica que la primera tenga relación con el atributo proporcionado, pero la segunda no tenga relación alguna con el atributo para agregarlo a lista de ejemplos candidatos positivos. Un ejemplo de lo anterior seria palabra1 airplane (avión), palabra2 helicopter (helicóptero) y atributo wings (alas), donde la palabra1 tiene relación con el atributo wings, pero no la palabra2, ya que un helicóptero no tiene alas; en el caso de palabra1 helicopter, palabra2 airplane, atributo wings se tomará en otra lista, ya que la palabra1 no tiene relación con el atributo. Para la lista de ejemplos negativos se tomarán en cuenta los casos donde ambas palabras tengan relación con el atributo y donde las dos palabras no tienen relación alguna con el atributo, para este último caso la cantidad de ejemplos es muy grande.
Finalmente, el objetivo de este proyecto es a partir de dos sentencias y un atributo, en base a éste atributo decir si la sentencia 1 es similar a la 2


### Objetivos
#### Objetivo General
Proponer un modelo de atributos discriminativos entre pares de palabras y un atributo extrayendo las diferencias semánticas de cada una.

#### Objetivos Específicos
1. Estudiar los artículos asociados a este problema que fue planteado por primera vez en el marco de SemEval 2016
2. Determinar el algoritmo de expansión de cada palabra que componen cada sentencia
3. Proponer un modelo que use el algoritmo anterior
4. Probar el modelo desarrollado
5. Participar en la conferencia SemEval 2018

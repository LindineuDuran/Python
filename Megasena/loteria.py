#/usr/bin/env python
#coding: utf-8
#Programa gerador de numeros para Mega Sena
#Construido por 
#Luís Eduardo Boiko Ferreira
#Você pode modificar e distribuir o código desde que
#não retire o nome do autor.
import random
linha='-'*75
text0='por Luis Eduardo Boiko Ferreira'
text1='Mega-Sena Generator'
sequencia=random.sample(range(100),6)
print (linha)
print(text1.center(75,'*'))
print (linha)
print ('\n\n')
print ('Se você deu sorte os numeros serão: ', sequencia,'.')
print ('\n\n')
print(text0.center(75,'-'))



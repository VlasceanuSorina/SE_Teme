def decaler(caractere, decalage) :
    if caractere.islower():
      return chr(((ord(caractere)-97+decalage) % 26)+97)
    elif caractere.isupper():
      return chr(((ord(caractere)-65+decalage) % 26 )+65)
    else:
      return caractere # non alphabétique
      
def cesar(phrase, shift):
     message = ""
     for caractere in phrase:
      message += decaler(caractere, shift)
      return message
      
texte_clair = "Alea jacta est!"
texte_code = cesar(texte_clair, 3)
print texte_clair, "devient", texte_code

import numpy as np
import sys

#Lê as linhas do arquivo e as transforma em uma matriz do tamanho descrito no arquivo
def getArr(name):
    with open(name, "r") as f:
        lines = f.readlines()
        cords = lines[2].split(' ')
        x,y=int(cords[1]),int(cords[0])

        arr = np.zeros((x,y),dtype=int)
        contx=0
        conty=0
        for i,line in enumerate(lines[3:]):
            for j,num in enumerate(line):
                if(num !='\n'):
                    arr[contx][conty]=num
                    conty=conty+1
                if(conty==y):
                    contx=contx+1
                    conty=0
    return np.array(arr, dtype=np.uint8)

#Percorre a imagem observando os pontos em que a imagem é 1(objeto) e seus elementos vizinhos já percorridos
#Caso nenhum vizinho seja um objeto já encontrado atribui uma nova marcação ao elemento atual
#Caso algum vizinho seja um objeto já encontrado atribui a menor marcação dentre eles ao elemento atual
def countObjects(image):
    padded_image = np.pad(image, 1, mode='constant', constant_values=0)  
    count_matri = padded_image.copy()

    max_value=1
    for line in range(count_matri.shape[0]):
        for col in range(count_matri.shape[1]):
            
            if(count_matri[line][col]==1):
                if(count_matri[line-1][col] > 1 or count_matri[line-1][col-1] > 1 or count_matri[line][col-1] > 1 or count_matri[line-1][col+1] > 1):
                    lista_vizinhos = np.array([count_matri[line-1][col],count_matri[line-1][col-1],count_matri[line][col-1],count_matri[line-1][col+1]])
                    lista_vizinhos = lista_vizinhos[lista_vizinhos > 1]

                    count_matri[line][col] = min(lista_vizinhos)
                    menor = min(lista_vizinhos)
                    maior = max(lista_vizinhos)
                    if(menor != maior):
                        for i in range(count_matri.shape[0]):
                            for j in range(count_matri.shape[1]):
                                if(count_matri[i][j] == maior):
                                    count_matri[i][j] = menor

                else:
                    max_value = max_value + 1
                    count_matri[line][col] = max_value

    return count_matri

#Inverte a imagem, caso seja 0 vira 1 e vice-versa
#É utilizada na verificação dos furos
def inverse(image):
    inverse_arr = image.copy()
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if(inverse_arr[i][j] == 0):
                inverse_arr[i][j] = 1
            else:
                inverse_arr[i][j] = 0
    return inverse_arr

#Percorre a imagem, levando em consideração a matriz de furos e preenchendo todos os furos encontrados
def fillHoles(image,matrizFuros):
    copia = image.copy()
    for i in range(matrizFuros.shape[0]):
        for j in range(matrizFuros.shape[1]):
            if(matrizFuros[i][j] > 2):
                copia[i-1][j-1] = 1
    return copia

arr = getArr(sys.argv[1]) #Lê o arquivo e transforma em uma matriz
matrizObjetos = countObjects(arr) #Chama a função de contagem de objetos, armazenando a matriz de objetos

print('Num de Objetos:',len(np.unique(matrizObjetos))-1) # O número de objetos será o número de labels diferentes na matriz de objetos, exceto o proprio fundo

matrizFuros = countObjects(inverse(arr)) #Realiza a contagem na matriz inversa, mapeando de tal modo os furos em vez dos objetos

copia = fillHoles(arr,matrizFuros) #Cria uma cópia da imagem original e preenche os furos utilizando a matriz de furos

matrizObjetos2 = countObjects(copia) #Chama novamente a função de contagem de objetos, armazenando a matriz de objetos

verificacao = []

#Se o tamanho do objeto mudou entre a imagem original e a imagem preenchida era um objeto com furos
for i in range(1,len(np.unique(matrizObjetos))):
    if(np.count_nonzero(matrizObjetos == np.unique(matrizObjetos)[i]) != np.count_nonzero(matrizObjetos2 == np.unique(matrizObjetos2)[i])):
        verificacao.append(1)

numeroObjetosFurados = sum(verificacao) #Conta quantos objetos com furos foram identificados e então exibe
print('Num de Objetos com Furos:',numeroObjetosFurados)




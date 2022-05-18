import numpy as np

import sys


def morfoOperation(image, kernel, padding=1, operation=None):
    if operation:
        img_operated = image.copy()

        padding_value = 0          
        if operation == "erosao":  
            padding_value = 1      
        image_padded = np.pad(image, padding, mode='constant', constant_values=padding_value)  

        janela_vertical = image_padded.shape[0] - kernel.shape[0] #posição dinal vertical
        janela_horizontal = image_padded.shape[1] - kernel.shape[1] #posição final horizontal

        #começa a vertical em zero
        vertical_pos = 0

        #percorrendo vertivalmente
        while vertical_pos <= janela_vertical:
            horizontal_pos = 0

            #percorrendo horizontalmente
            while horizontal_pos <= janela_horizontal:
                dilation_flag = False
                erosion_flag = False
                
                for i in range(kernel.shape[0]):      
                    for j in range(kernel.shape[1]):  
                        if kernel[i][j] == 1:       
                            #Caso de erosão
                            if operation == "erosao":
                                #se achar 0 quebra o segundo loop
                                if image_padded[vertical_pos+i][horizontal_pos+j] == 0:  
                                    erosion_flag = True                            
                                    break
                            #caso dilatação
                            elif operation == "dilatacao":
                                #se achar 1 quebra o segundo loop
                                if image_padded[vertical_pos+i][horizontal_pos+j] == 1:  
                                    dilation_flag = True
                                    break
                    #quebra o primeiro loop do for se não tiver correspondência, apenas no caso de erosão
                    if operation == "erosao" and erosion_flag:         
                        img_operated[vertical_pos, horizontal_pos] = 0  
                        break
                    #quebra o primeiro loop do for se tem correspondência na flag horizontal e é dilatação
                    if operation == "dilatacao" and dilation_flag:      
                        img_operated[vertical_pos, horizontal_pos] = 1
                        break

                horizontal_pos += 1
            vertical_pos += 1

        return img_operated

    return "Adicione a Operacao"


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


def inverse(image):
    inverse_arr = image.copy()
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if(inverse_arr[i][j] == 0):
                inverse_arr[i][j] = 1
            else:
                inverse_arr[i][j] = 0
    return inverse_arr

kernel = np.array ([[0, 1, 0],
                    [1, 1, 1],
                    [0, 1, 0]], dtype = np.uint8)

arr = getArr(sys.argv[1])

copy_arr = arr.copy()
        
matrizObjetos = countObjects(arr)#Lê o arquivo e transforma em uma matriz
print('Num de Objetos:',len(np.unique(matrizObjetos))-1) # O número de objetos será o número de labels diferentes na matriz de objetos, exceto o proprio fundo


count = 0
while(1):
    
    inverse_arr = inverse(copy_arr)
    
    numeroFuros = len(np.unique(countObjects(inverse_arr)))-1# contagem da quantidade de furos que conta o número necessário de dilatação para preencher todos os furos
    if(numeroFuros > 1):
        copy_arr = morfoOperation(copy_arr, kernel, 1, "dilatacao")
        count = count + 1
    else:
        break

for i in range(count):
    copy_arr = morfoOperation(copy_arr, kernel, 1, "erosao")

matrizObjetos2 = countObjects(copy_arr)

verificacao = []

#Se o tamanho do objeto mudou entre a imagem original e a imagem preenchida era um objeto com furos
for i in range(1,len(np.unique(matrizObjetos))):
    if(np.count_nonzero(matrizObjetos2 == np.unique(matrizObjetos2)[i]) - np.count_nonzero(matrizObjetos == np.unique(matrizObjetos)[i]) > 5):
        verificacao.append(1)

numeroObjetosFurados = sum(verificacao) #Conta quantos objetos com furos foram identificados e então exibe
print('Num de Objetos com Furos:',numeroObjetosFurados)





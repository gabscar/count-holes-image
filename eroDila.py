import numpy as np
import matplotlib.pyplot as plt




def operation(image, kernel, padding=1, operation=None):
    if operation:
        img_operated = image.copy() #this will be the image

        padding_value = 0          
        if operation == "erosion":  
            padding_value = 1      
        padded = np.pad(image, padding, mode='constant', constant_values=padding_value)  

        vertical_window = padded.shape[0] - kernel.shape[0] #final vertical window position
        horizontal_window = padded.shape[1] - kernel.shape[1] #final horizontal window position

        #start with vertical window at 0 position
        vertical_pos = 0

        #sliding the window vertically
        while vertical_pos <= vertical_window:
            horizontal_pos = 0

            #sliding the window horizontally
            while horizontal_pos <= horizontal_window:
                dilation_flag = False
                erosion_flag = False

                #gives the index position of the box
                for i in range(kernel.shape[0]):      # <<< MODIFIED
                    for j in range(kernel.shape[1]):  # <<< MODIFIED
                        if kernel[i][j] == 1:         # <<< ADDED
                            #First Case
                            if operation == "erosion":
                                #if we find 0, then break the second loop
                                if padded[vertical_pos+i][horizontal_pos+j] == 0:  # <<< MODIFIED
                                    erosion_flag = True                            # <<< MODIFIED
                                    break
                            #Second Case
                            elif operation == "dilation":
                                #if we find 1, then break the second loop
                                if padded[vertical_pos+i][horizontal_pos+j] == 1:  # <<< MODIFIED
                                    dilation_flag = True
                                    break
                            else:
                                return  "Operation not understood!"

                    #if opertion is erosion and there is no match found, break the first 'for' loop
                    if operation == "erosion" and erosion_flag:         # <<< MODIFIED
                        img_operated[vertical_pos, horizontal_pos] = 0  # <<< ADDED
                        break

                    #if operation is dilation and we find a match, then break the first 'for' loop 
                    if operation == "dilation" and dilation_flag:       # <<< FIXED
                        img_operated[vertical_pos, horizontal_pos] = 1
                        break

                # !!! Removed unnecessary checks here

                #increase the horizontal window position
                horizontal_pos += 1

            #increase the vertical window position
            vertical_pos += 1

        return img_operated

    return "Operation Required!"


def convol(image, kernel, padding=1):
    # Reflexão do kernel
    kernel = np.flipud(np.fliplr(kernel))

    # Montando o array que vai receber a imagem após a convolução
    xOutput = int(((image.shape[0] - kernel.shape[0] + 2 * padding) ) + 1)
    yOutput = int(((image.shape[1] - kernel.shape[1] + 2 * padding) ) + 1)
    output = np.zeros((xOutput, yOutput))

    if padding != 0:
        imagePadded = np.zeros((image.shape[0] + padding*2, image.shape[1] + padding*2))
        imagePadded[int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = image
    else:
        imagePadded = image


    for y in range(image.shape[1]):
        for x in range(image.shape[0]):
            output[x, y] = (kernel * imagePadded[x: x + kernel.shape[0], y: y + kernel.shape[1]]).sum()

    return output



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

def countHoles(image):
    padded_image = np.pad(image, 1, mode='constant', constant_values=0)  
    count_matri = padded_image.copy()

    max_value=1
    ultimoObjeto = 0
    arrayObjetos= []
    for line in range(count_matri.shape[0]):
        for col in range(count_matri.shape[1]):
            
            if(count_matri[line][col] > 1):
                ultimoObjeto = count_matri[line][col]
            else:
                
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




array = np.array([[0,0,0,1,1,1],
               [0,0,0,1,0,1],
               [1,1,0,1,0,1],
               [1,1,0,1,1,1],
               [0,0,0,0,0,0],
               [1,1,1,1,0,0]], dtype=np.uint8)

kernel = np.array ([[0, 1, 0],
                    [1, 1, 1],
                    [0, 1, 0]], dtype = np.uint8)

arr = getArr("ImagemPI.pbm")
#plt.imshow(arr,cmap='gray')
#plt.show()
copy_arr = arr.copy()
        
matrizObjetos = countObjects(arr)
print('Num de Objetos:',len(np.unique(matrizObjetos))-1) # O número de objetos será o número de labels diferentes na matriz de objetos, exceto o proprio fundo


count = 0
while(1):
    
    inverse_arr = copy_arr.copy()
    for i in range(copy_arr.shape[0]):
        for j in range(copy_arr.shape[1]):
            if(inverse_arr[i][j] == 0):
                inverse_arr[i][j] = 1
            else:
                inverse_arr[i][j] = 0
    
    numeroFuros = len(np.unique(countObjects(inverse_arr)))-1
    if(numeroFuros > 1):
        copy_arr = operation(copy_arr, kernel, 1, "dilation")
        count = count + 1
    else:
        break

for i in range(count):
    copy_arr = operation(copy_arr, kernel, 1, "erosion")

matrizObjetos2 = countObjects(copy_arr)

verificacao = []

#Se o tamanho do objeto mudou entre a imagem original e a imagem preenchida era um objeto com furos
for i in range(1,len(np.unique(matrizObjetos))):
    if(np.count_nonzero(matrizObjetos2 == np.unique(matrizObjetos2)[i]) - np.count_nonzero(matrizObjetos == np.unique(matrizObjetos)[i]) > 5):
        verificacao.append(1)

numeroObjetosFurados = sum(verificacao) #Conta quantos objetos com furos foram identificados e então exibe
print('Num de Objetos com Furos:',numeroObjetosFurados)





class ExamException(Exception):

    pass


class CSVTimeSeriesFile():
    
    def __init__(self, name):
        
        self.name = name

    def get_data(self):         
        #Provo ad aprire il file
        try:                   
            my_file = open(self.name, 'r')
            
        #Se non lo può aprire restituisce un errore
        except ExamException as e:
            print('Errore in apertura del file: "{}"'.format(e))

        #Assegno a prova il file
        prova = open(self.name, 'r')

        #Provo a leggere il file
        try:
            content=prova.read()
            
        except:
            raise ExamException('Il file è illeggibile')

        #Controllo se il file è vuoto
        if content == '': 
            raise ExamException('Il file è vuoto')

        #Controllo se il nome del file non è una stringa
        if not type(self.name) == str: 
            raise ExamException('Errore: Il nome del file non è una stringa')

        #Per questo specifico caso controllo che il nome del file sia esattamente data.csv
        if self.name != 'data.csv':
            raise ExamException('Nome del file errato')
            
        #Creo la lista che riempirò con i dati splittati di ogni riga nel file data.csv
        time_series = []
        
        #Creo una lista di controllo da utilizzare per eventuali righe anomale
        controllo = []
        
        
        #Leggo il file riga per riga e ne splitto gli oggetti dove c'è una virgola  
        for line in my_file:
            
            #Salto eventuali righe vuote
            if line == '\n':
                pass
            
            #Salto eventuali righe dove epoch e temperatura non sono divise da una ','
            elif ',' not in line: 
                pass
                
            else:
                elements = line.split(',')
                elements[-1] = elements[-1].strip()
                
                #Inizializzo un counter che mi servirà per contare gli elementi di ogni lista nella lista
                counter = 0

                #Se 
                if elements[0] in controllo:
                    raise ExamException('Errore: Doppia epoch uguale nel file') 
                               
                #Scorro tra gli elementi della lista   
                for i in elements:
                    
                    counter = counter + 1
 
                    if counter >= 2:
                        
                        
                        try:
                            converti=int(elements[0])
                            if not isinstance(converti, int):
                                pass
      
                            if elements[0] in controllo:
                                raise ExamException('Ci sono due epoche uguali') 
        
                            else:
                                controllo.append(elements[0])
                                    
                            try:
                                temp=float(elements[1])
                                    
                                time_series.append([int(elements[0]), temp])
                    
                            except:
                                pass
                              
            
                        except:
                            pass
                            
                    else:
                        pass
                else:
                    pass

        my_file.close()
        return time_series

        
def compute_daily_max_difference(time_series): 
    
    lista_temp_giorno = []
    lista_escursione_termica = []

    giorno_corrente=0

    #Controllo se le epoch della time_series sono in ordine
    if not all(time_series[current][0] <= time_series[current+1][0] for current in range(len(time_series)-1)):
        raise ExamException('Errore: ci sono almeno due epoch non in ordine')

    
    for i, string_row in enumerate(time_series):
            
        massimo = 0.0
        minimo = 0.0

        epoch = int(string_row[0])
       
        temp = float(string_row[1])

        
        if i == 0 and isinstance(epoch, int):
            giorno_corrente = int(epoch/86400)
            if isinstance(temp, float):
                lista_temp_giorno.append(float(temp))

        else:
            giorno=int(epoch/86400)
            
            if giorno == giorno_corrente:
                lista_temp_giorno.append(float(temp))
                
            else:
                #Controllo se la lista non è vuota, quindi se il primo elemento del giorno non è compromesso
                if lista_temp_giorno:

                    #Trovo massimo e minimo della lista_temp_giorno che ho creato
                    massimo = max(lista_temp_giorno)
                    minimo = min(lista_temp_giorno)

                #Se ho solo un valore inserisco 'None' nella lista senza interromperla
                    if len(lista_temp_giorno)==1:
                        lista_escursione_termica.append(None)
                    else:
                        lista_escursione_termica.append(massimo-minimo)  
                
                lista_temp_giorno = []
                
                lista_temp_giorno.append(float(temp))
                
                giorno_corrente = giorno

    if lista_temp_giorno:
        massimo = max(lista_temp_giorno)
        minimo = min(lista_temp_giorno)
        
        #Se ho solo un valore
        if len(lista_temp_giorno)==1:
            lista_escursione_termica.append(None)
        else:
            lista_escursione_termica.append(massimo-minimo)
    
    return lista_escursione_termica
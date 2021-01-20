from threading import *

soma = 0


class LeitorTXT(Thread):
    def __init__(self, arqv, ident, mutex):
        self.arq = arqv
        self.id = ident
        self.locker = mutex
        self.soma = 0

        Thread.__init__(self)

    def run(self):
        global Resultados
        for valor in self.arq:
            with self.locker:
                self.soma += int(valor.strip())

        Resultados.append(self.soma)


Resultados = []
TodasThreads = []
arq = open('num.txt')
dados = arq.readlines()

# num == Numero de threads
# linhas == Quantidade de linhas do txt
# locker == Ao locker que bloqueia e desbloqueia as threads

num = 4
linhas = 10**6
locker = Lock()
for id in range(num):
    thread = LeitorTXT(dados[linhas // num * id:linhas // num * (id + 1)], id, locker)
    # A fórmula é simples
    # linhas do txt dividido pelo número de threads → Mesma quantidade pra cada uma.
    # Multiplicadas pelo o id, pq como é número:
    # A 1 (id == 0) thread lê as primeiras 250k linhas
    # A 2 (id == 1) thread lê as seguintes 250k (250k anterior)
    # A 3 (id == 2) thread lê as seguintes 250 (250k + 250k das anteriores)
    # e daí em diante

    thread.start()
    TodasThreads.append(thread)

for thread in TodasThreads:
    thread.join()

print('Resultado final:', sum(Resultados))

from resultados.resultado import CachedResultadosClient

if __name__ == "__main__":
    client = CachedResultadosClient("lotofacil")
    ultimo_resultado = client.get_resultado()
    print(f"{ultimo_resultado.concurso} -> {ultimo_resultado}")
    maior_numero = 25
    status = {}
    for i in range(1, maior_numero + 1):
        status[i] = 0
    
    for i in range(1, ultimo_resultado.concurso):
        resultado = client.get_resultado(i)
        to_sum = set(set([i for i in range(1, maior_numero + 1)])).difference(set(resultado))
        for num in resultado:
            status[num] = 0
        
        for num in to_sum:
            status[num] += 1
        
        for key in status.keys():
            print(f"{key:02d} -> {status[key]}", end=" ")
        print()

    sorted_footballers_by_goals = sorted(status.items(), key=lambda x:-x[1])
    print(sorted_footballers_by_goals)

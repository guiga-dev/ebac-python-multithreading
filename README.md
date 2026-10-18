# Catálogo de filmes com multithreading

Aluno: Guilherme Rodrigues — GitHub: guiga-dev.

Atividade Python Avançado da EBAC. O repositório de referência da aula foi atualizado para a versão 2: substitui o IMDb por um catálogo educacional estático, devido a alterações no HTML e bloqueios de scraping do IMDb.

Fonte dos dados: https://havokkmorands.github.io/movie-catalog/
Referência: https://github.com/havokkmorands/multithreading

Os registros são os filmes do catálogo educacional, e não representam um ranking atual do IMDb. Nenhum dado de filme é inventado pelo script.

```sh
python -m pip install -r requirements.txt
python scraper.py --threads 1 --output movies_1thread.csv
python scraper.py --threads 5 --output movies.csv
```

O programa coleta os links e visita os detalhes com `ThreadPoolExecutor`, extrai título, lançamento, nota e sinopse com BeautifulSoup e grava o CSV apenas na thread principal. Falhas HTTP ou campos ausentes interrompem a execução. Os tempos medidos aparecem no console, dependem da rede e não garantem aceleração em todas as execuções.

Na execução local de 16/10/2026 foram coletados 30 filmes: 7,7708 s com uma thread e 2,2228 s com cinco threads. Os dois CSVs foram comparados e têm o mesmo conteúdo. Esses tempos são medições desta execução, e não promessa geral de desempenho.

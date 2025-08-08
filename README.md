# Azure Text 2 Speach

Este projeto tem como objetivo um gerador de falas das vozes da Azure.

## Instalação

1. Clonar o repositório:

    ```bash
    git clone https://github.com/BernardoCastello/Text2Speach.git
    ```

2. Keys Necessárias:

    Para executar esse projeto se faz necessário criar um arquivo .env na raiz com o dados de Azure_Key e Azure_Region. Esses dados deveram ser pessoais e gerados na Azure.

3. Execução

    Para o backend: uvicorn app.main:app --reload

    Para o frontend: npm run dev


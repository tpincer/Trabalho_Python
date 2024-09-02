# Projeto de Análise de Dados de Voos

Este projeto é uma pipeline de processamento de dados de voos, que inclui etapas de saneamento, engenharia de features, e armazenamento em banco de dados. O objetivo principal é limpar e transformar dados de voos para análise posterior, armazenando-os em um banco de dados SQLite para consultas e relatórios.

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:


## Objetivo

O objetivo deste projeto é processar e transformar dados de voos para torná-los prontos para análise. O pipeline realiza as seguintes etapas:

1. **Saneamento dos Dados**:
   - Criação da coluna `data_voo` a partir das colunas `year`, `month`, e `day`.
   - Exclusão de observações nulas com base nas chaves definidas.
   - Conversão dos tipos de dados conforme especificado nos metadados.
   - Renomeação de colunas para atender aos requisitos do projeto.
   - Padronização de strings para consistência.

2. **Engenharia de Features**:
   - Criação de novas features, como a duração do voo, a partir das colunas existentes.

3. **Armazenamento em Banco de Dados**:
   - Salvamento dos dados transformados em um banco de dados SQLite.
   - Consulta e exibição dos dados armazenados.

## Arquivos e Pastas

- **`data/`**: Contém arquivos de dados brutos e o banco de dados SQLite. O arquivo `NyflightsDB.db` é o banco de dados onde os dados tratados são armazenados.

- **`assets/`**: Contém o módulo `utils.py`, que inclui funções auxiliares para o processamento e validação de dados.

- **`app.py`**: Script principal que orquestra o pipeline de dados. Este script carrega os dados, aplica saneamento e engenharia de features, e salva os dados em um banco de dados SQLite.

- **`requirements.txt`**: Lista as dependências do projeto, que podem ser instaladas usando `pip`.

- **`.env`**: Arquivo de variáveis de ambiente. Deve conter os caminhos para os arquivos de dados e metadados, por exemplo:


- **`README.md`**: Documento que fornece uma visão geral do projeto e instruções sobre a estrutura e uso.

## Instalação e Execução

1. **Instalação das Dependências**:
 - Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv env-impacta
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```
 - Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuração do Ambiente**:
 - Crie um arquivo `.env` na raiz do projeto e adicione os caminhos para os arquivos de dados e metadados.

3. **Execução do Pipeline**:
 - Execute o script principal:
   ```bash
   python app.py
   ```

## Contribuição

Sinta-se à vontade para contribuir para este projeto. Por favor, siga as melhores práticas para enviar pull requests e reporte quaisquer problemas encontrados.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

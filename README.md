[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Hppw7Zh2)

# 🔧 Otimizações em Interpretador da Linguagem Lox

## 👥 Integrantes

| Nome                          | Matrícula | Turma   |
| ----------------------------- | --------- | ------- |
| David William Lemos Ferreira  | 232001649 | 18h     |
| Yasmin Dayrell Albuquerque    | 232014226 | 16h     |

> Orientador: [Fabio M. Mendes](https://github.com/fabiommendes)

## 📌 Introdução

## Linguagem Lox

Este é o código fonte de um interpretetador da linguagem de programação [Lox](https://craftinginterpreters.com/the-lox-language.html) desenvolvido durante o curso de `Compiladores 1` da Universidade de Brasilia.

Ele estende um interpretador já desenvolvido ao longo do curso com **otimizações de código-fonte baseadas em análise da AST (Abstract Syntax Tree)**.

## Otimizações

As otimzações realizadas no interpretador incluem:

- 🔁 **Constant Propagation**: substituição de variáveis constantes diretamente por seus valores.
- 🔢 **Constant Folding**: avaliação de expressões constantes em tempo de compilação.
- 🗑️ **Dead Code Elimination**:
  - **Unused Variables**: remoção de variáveis nunca utilizadas.
  - ~~**Unreachable Code**~~: ainda não implementado.

Outras otimizações planejadas (não implementadas):

- ⏳ **Loop Unrolling**
- ⏳ **Inline Expansion**

As otimizações são aplicadas diretamente sobre a AST utilizando classes específicas localizadas no arquivo `lox/optimizations.py`.

### Exemplo de uso

```python
from optimizations import ConstantPropagation

ast = ...  # AST original

ConstantPropagation().propagate(ast)

print(ast.pretty())  # AST otimizada
```


## 🛠️ Instalação

O projeto utiliza o gerenciador [uv](https://docs.astral.sh/uv), então o primeiro passo é ter ele instalado.

**1. Clonar o repositório:**
```bash
git clone https://github.com/fcte-compiladores/trabalho-final-trabalho_final_loxotimizacoes.git

cd trabalho-final-trabalho_final_loxotimizacoes
```


**2. Instalar os pacotes**

Inicie o ambiente uv e intale os pacotes:

``` bash
uv venv
uv run
```

**3. Rodar os testes**

Na pasta `tests` existem alguns arquivos, o principal deles é o `tests/optimization.py`, ele roda o intepretador com os códigos na pasta `exemplos/optimization`, mostrando as otimizações realizadas e um benchmark comparativo. Para executar arquivo siga as instruções abaixo:

Execute o arquivo:
```
uv run tests/optimization.py
```

O script irá criar um arquivo `tests/results.txt`, que contém o resultado dos testes.

Para visualizar os resultados execute:
```
less -R tests/results.txt
# ou
cat tests/results.txt
```

> *⚠️ Importante: O arquivo `results.txt` usa caracteres ANSI (cores), recomenda-se a leitura com programas adequados*
> 

## 💡 Exemplos

A pasta [`exemplos/optimization`](./exemplos/optimization) contém os exemplos utilizados para testes das otimizações. Subpastas:

- `propagation/`: testes de propagação de constantes.
- `unsed_vars/`: testes de variáveis não utilizadas.
- `all/`: testes com múltiplas otimizações aplicadas.

Cada exemplo serve como benchmark incremental, com dificuldades crescentes.



## 📁 Estrutura do Código

```
.
├── exemplos
│   └── optimization
│       ├── all
│       ├── propagation
│       └── unsed_vars
├── lox
│   ├── __init__.py
│   ├── __main__.py
│   ├── ast.py
│   ├── cli.py
│   ├── ctx.py
│   ├── errors.py
│   ├── grammar.lark
│   ├── node.py
│   ├── optimizations.py
│   ├── parser.py
│   ├── runtime.py
│   ├── testing.py
│   └── transformer.py
├── pyproject.toml
├── pytest.ini
├── README.md
├── tests
│   ├── configs.py
│   ├── optimization.py
│   └── results.txt
└── uv.lock
```


## 📚 Referências
- [**IBM - Otimization Techniques**](https://www.ibm.com/docs/en/aix/7.2.0?topic=tuning-compiler-optimization-techniques) - Usado como exploratório para descobrir tecnicas de otimizções
- [**Geek for Geeks**](https://www.geeksforgeeks.org/compiler-design/code-optimization-in-compiler-design/) - Principal base para aplicação das otimizações
- [**Medium - Guannan Shen**](https://medium.com/@guannan.shen.ai/compiler-optimizations-46db19221947) - Explica algumas tecnicas de otimização que o GCC utiliza
- [**Crafting Interpreters**](https://craftinginterpreters.com/) – Bob Nystrom: principal base teórica e prática para o interpretador da linguagem Lox.
- [**Repositório da disciplina**](https://github.com/fabiommendes/lox-base): usado como base do interpretador.
- **[Implementações próprias](https://github.com/sluucke/lox-compiler)**: as otimizações foram inteiramente desenvolvidas pela equipe como extensão do interpretador.

## 🐞 Bugs / Limitações / Problemas Conhecidos

- ❌ Otimizações não incluem ainda análise de código inatingível
- 🔜 Outras otimizações (unroll, inline) ainda estão em planejamento
- 🛠️ Melhorias futuras podem incluir mais padrões da linguagem
# Trabalho Compiladores 1


## Linguagem Lox

Este é o código fonte de um interpretetador da linguagem de programação [Lox](https://craftinginterpreters.com/the-lox-language.html) desenvolvido durante o curso de `Compiladores 1` da Universidade de Brasilia.


Boa parte da implementação atual do projeto foi realizada durante o semestre, este repositório é o mesmo dos exercícios realizados na disciplina.

Este trabalho implementa o algumas otimizações, conteúdo sobre compiladores que não é abordado na disciplina

## Como executar?

Primeiro passo é ter o [uv](https://docs.astral.sh/uv) instalado em seu computador.

**Instalar os pacotes**
  - Execute o comando `uv run` para instalar os pacotes do projeto

**Rodar os testes**

Na pasta `tests` existem alguns arquivos de teste, o principal deles é o `tests/optimization.py`, ele roda o intepretador com os códigos na pasta `exemplos/optimization`, mostrando as otimizações realizadas e um benchmark comparativo. Para executar arquivo siga as instruções abaixo:


Execute o arquivo:
```
uv run tests/optimization.py
# ou python3 tests/optimization.py
```

O script irá criar um arquivo `tests/results.txt`, que contém o resultado dos testes, abra com `less -R tests/results.txt` ou `cat tests/results.txt`.

*Importante: O arquivo results.txt tem caracteres de cor ANSII, portanto devem ser abertos com algum programa compativel para leitura*

Exemplo:

```py
from optimizations import ConstantPropagation

ast = ...

ConstantPropagation().propagate(ast)

print(ast.pretty()) // ast otimizada com constant propagation + folding
```

### Otimizações

Esse trabalho aplica as seguintes otimizações no interpretador original:

- Constant Propagation

- Constant Folding

- Dead code
  - Unsed variables
  - ~~Unreach code~~

- ~~For-loops unroll~~
  - Soon...
  
- ~~Inline Expansion~~
  - Soon...

## Participantes

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/fabiommendes.png" width="60" style="border-radius: 50%;" /><br/>
      <a href="https://github.com/fabiommendes" target="_blank">Fabio M Mendes</a><br/>
      <sub>Orientador</sub>
    </td>
    <td align="center">
      <img src="https://github.com/sluucke.png" width="60" style="border-radius: 50%;" /><br/>
      <a href="https://github.com/sluucke" target="_blank">David William</a><br/>
      <sub>Discente</sub>
    </td>
    <td align="center">
      <img src="https://github.com/yasmindayrell.png" width="60" style="border-radius: 50%;" /><br/>
      <a href="https://github.com/yasmindayrell" target="_blank">Yasmin Dayrell</a><br/>
      <sub>Discente</sub>
    </td>
  </tr>
</table>


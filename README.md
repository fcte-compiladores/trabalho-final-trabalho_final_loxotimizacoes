# Trabalho Compiladores 1


## Linguagem Lox

Este é o código fonte de um interpretetador da linguagem de programação [Lox](https://craftinginterpreters.com/the-lox-language.html) desenvolvido durante o curso de `Compiladores 1` na Universidade de Brasilia.


Boa parte da implementação atual do projeto foi realizada durante o semestre, este repositório é o mesmo dos exercícios realizados na disciplina.

Este trabalho implementa o algumas otimizações, conteúdo sobre compiladores que não é abordado na disciplina

## Como executar?

Primeiro passo é ter o [uv](https://docs.astral.sh/uv) instalado em seu computador, depois é só rodar `uv run` para instalar os pacotes.

Na pasta `tests` existem alguns arquivos de teste que roda o interpretador com e sem as otimizações mostrando um benchmark com as difereças e as AST's correspondentes.

As otimizações estão concentradas no final do arquivo `lox/optimizations.py`, funcionam como um 'plugin' para a AST.


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

- Dead Code
  - Unreach code elimination

- For-loops unroll

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


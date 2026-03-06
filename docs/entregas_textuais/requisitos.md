# PROJETO – FASE DE ANÁLISE

## Descrição do Problema Organizacional

A organização em questão necessita disponibilizar seus dados gerenciais de produtos por meio de uma solução de Business Intelligence (BI) acessível via web. Atualmente, apesar de possuir um banco de dados de produtos estabelecido, a análise dessas informações é descentralizada e carece de uma visão consolidada.

Observa-se a inexistência de um mecanismo estruturado e visual de acesso remoto, o que aumenta o tempo necessário para a tomada de decisão e dificulta a extração de insights estratégicos (como giro de estoque, produtos mais rentáveis, etc.). 

Diante desse contexto, faz-se necessária a implementação de uma solução web conectada ao banco de dados atual, que permita a visualização dinâmica de indicadores, garantindo segurança, escalabilidade e agilidade no suporte à gestão.

---

## Requisitos Funcionais

* **RF01.** O sistema deve conectar-se ao banco de dados de produtos existente para extração e consolidação das informações em uma única interface.
* **RF02.** O sistema deve possibilitar a rotina de atualização (carga) diária dos dados exibidos nos relatórios, garantindo uma defasagem máxima de 24 horas (D-1).
* **RF03.** O sistema deve exigir a autenticação de usuários para acesso seguro às informações.
* **RF04.** O sistema deve permitir a visualização de indicadores gerenciais de produtos por meio de dashboards acessíveis via ambiente web.
* **RF05.** O sistema deve permitir a geração e exportação de relatórios em formatos digitais padrão (ex: PDF e XLSX) para consulta externa.

---

## Requisitos Não Funcionais

* **RNF01 – Segurança:** O sistema deve implementar controle de acesso baseado em perfis de usuário, garantindo restrição adequada às informações sensíveis.
* **RNF02 – Desempenho:** O tempo máximo de carregamento dos dashboards não deve exceder 5 segundos em condições normais de operação.
* **RNF03 – Disponibilidade:** O sistema deve apresentar disponibilidade mínima de 99% durante o horário comercial.
* **RNF04 – Escalabilidade:** O sistema deve suportar o crescimento do volume do banco de dados (ex: até 50GB iniciais) e picos de acesso de até 100 usuários simultâneos sem degradação significativa do desempenho.
* **RNF05 – Usabilidade:** O sistema deve apresentar interface intuitiva, permitindo sua utilização por gestores sem necessidade de treinamento técnico especializado.

---

## Delimitação de Escopo

Não fazem parte do escopo deste projeto, nesta fase:
* O desenvolvimento de um novo sistema de ERP ou banco de dados a partir do zero;
* A implementação de aplicativo móvel dedicado (app nativo);
* A aplicação de técnicas avançadas de análise preditiva ou inteligência artificial;
* Customizações específicas e aprofundadas por departamento que fujam da visão geral de produtos.

---

## Justificativa de Requisitos

### Justificativa do RF01 e RF04 – Conexão e Visualização
A conexão direta com o banco de dados existente e a visualização em dashboards web eliminam a dependência de extrações manuais, garantindo que os gestores tomem decisões com base em uma "única fonte de verdade", atualizada e confiável.

### Justificativa do RNF01 – Segurança
Os dados de produtos, custos e vendas possuem caráter estratégico e sensível. A implementação de controle de acesso baseado em perfis reduz riscos de vazamento de informações para a concorrência e garante a integridade da estratégia corporativa.
Author= ofelippm
Update_Date = 2022-05-10

# Projeto - PV Load Forecast

## Objetivo

O projeto visa o forecasting, de médio a longo prazo (1 mês a frente), com 
resolução diária de um sistema fotovoltaico (PV). Isso é necessário para ter
a possibilidade de planejamento de despacho melhor da Distribuidora além
de possibilidade de equalizar o Fator de potência da aplicação, evitando
multas e reduzindo os impactos na rede.

    " Nesta pesquisa se desenvolverá um novo modelo de previsão de irradiância
    solar para microrredes. Este modelo utiliza uma reduzida base de dados para
    prever a irradiação solar com um dia de antecedência. O modelo considera 
    dados passados de irradiância solar, irradiância de céu claro e 
    complementações de informações para três regimes ou estados: regimes de 
    alta, média e baixa energia para dias correspondentes a dias ensolarados, 
    levemente nublados e extremamente nublados, respectivamente." TRUJILLO, Joel.

## Proposta

A proposta inicial concentra-se na previsão de demanda de irradiância solar
que incide sobre um dado sistema PV em uma dada região e com dados extras do
ambiente, seja possível realizar o cálculo da potência ativa gerada pelo 
sistema.

Portanto será necessário a construçao da solução a partir dos chamados modelos
físicos, da qual a partir de dados de irradiância, tempo, clima e outros 
fatores, pode-se calcular a potência gerada pelo sistema.

Além disso, pode-se simular cenários onde considera-se os erros de previsão
a fim de ter-se os limites mínimos e máximos de geração e possibilidade de 
alguma ação para minimizar os impactos na rede.

## Perguntas

1. Qual é a média de geração diária do sistema escolhido para o trabalho? 
(Importante para entender se as métricas de erro estão dentro dos limites
esperados.)


## Dificuldades

* Curto período de histórico (2 meses)

## Metodologia
### Fonte de Dados
### Modelo Escolhido



---

# Artigos

## Resumo dos Artigos

Essa seção se destina a escrita das perguntas abaixo, para cada um dos temas 
lidos:

* Qual o tema tratado?
* Qual a proposta de solução?
* Quais os resultados obtidos?
* Existe algo que pode ser reaproveitado?

---

# Irradiância Solar

A seção abaixo indica os artigos que utilizam técnicas de Machine Learning e
Deep Learning para a previsão de irradiância solar em uma dada região e 
posteriormente se calcula a carga gerada em um sistema PV.


## [01] Solar Irradiance Forecasting in Remote Microgrids Using Markov Switching Model

[doi] 10.1109/TSTE.2016.2629974  
[Estudante] Ayush Shakya  
[Professor] Reinaldo Tonkoski  

### Qual o tema tratado?

Forecasting de Irradiância Solar para três categorias de 'disposição' do dia: 
alto (sem nuvens), médio (nuvens parciais), baixo (muitas nuvens). Cada um dos
níveis representa um modelo de regressão linear que indica o nível de 
irradiância que pode ser obtido por um sistema de geração híbrido (diesel e 
painel photovoltaico) remoto, ou seja, que se desloca entre regiões geográficas.


### Qual a proposta de solução?

Criar modelos de regressão linear para forecasting de irradiância solar em um 
dado ponto geográfico, baseado em dados de irradiâncias passadas e expansão de 
Fourier (para identificação do nível de irradiância dependendo do dia).

Com esses tipos de modelos lineares é possível a previsão de um dia a frente
por muitos anos, antes da necessidade de 'fit' dos modelos novamente, o que 
configura uma boa estratégia para sistemas remotos como o objeto de estudo.

[?] Os dados dos dias que se passam, são coletados diariamente por sensores e 
seus valores também calculados em modelos que consideram a rotaçao da terra e
as variações da geografia existentes no local (direções percorridas).


### Quais os resultados obtidos?

O sistema foi implantado em Brooklin, USA, e teve um MAPE (Mean Absolute 
Percentage Error) de aproximadamente 31,8% na média. Utilizou-se um período
inicial de dados de 2001 a 2005.

Os maiores erros foram contabilizados nas estações de verão por conta da maior
disponibilidade de recurso solar em dias maiores, quando comparados aos de 
estação do inverno.

### Existe algo que pode ser reaproveitado?

Talvez a variável de intensidade de radiação (alto, médio, baixo) pode ser uma 
variável do modelo causal de forecasting de geração de energia elétrica PV.

---

## [10][Applied_Energy]Novel_ML_Approach_PV_Forecast_Extra_Terrestrial_Solar_Irradiance

[doi] https://doi.org/10.1016/j.apenergy.2021.118152 
[Estudante] Zuansi Cai
[Professor] Cornelia A. Fjelkestam Frederiksen

### Qual o tema tratado?

Forecasting de níveis de irradiância extra-terrestre utilizando métodos de 
Machine Learning e acoplando variáveis de clima, realizar o calculo da potência
gerada pelo sistema PV para 7 dias a frente com resolução de 30 minutos.


### Qual a proposta de solução?

A proposta reside num modelo de ML que teria como objetivo fazer o forecasting
de níveis de irradiância solar fora da terra, ou seja, capturando a totalidade
da irradiância e eliminando a correlação direta com o clima do local.

O modelo de irradiância pura, chama-se ERAD (Slopped Extra-terrestrial 
Irradiance) que será posteriormente acoplado a variáveis de condições 
climáticas da região, podendo chegar nos níveis de irradiação locais.

Os diferenciais são:
* ERAD independe do tempo
* Pode ser calculada para qualquer parte do globo  

### Quais os resultados obtidos?

Os resultados do ERAD são comparados a um modelo de irradiância utilizando as 
mesmas variáveis que, porém com a diferença de que o modelo 'Irrad' é uma 
irradiância modelada.

O ERAD se comporta abaixo do modelo Irrad na maioria das estações, ficando até
3 p.p. abaixo, utilizando a métrica nRMSE. Os resultados variam de acordo com 
as estações do ano, o que é esperado.

### Existe algo que pode ser reaproveitado?

É interessante a abordagem do autor na previsão de irradiância excluindo os 
efeitos climáticos, tipicamente regionais, e passando a caracterizar a queda de
irradiância acoplando as variáveis de clima somente depois.

* Criação de modelo de forecasting de irradiância solar
* Acoplamento de variáveis climáticas
* Modelo de forecasting de potência gerada

### Informações Complementares

Pontos de atenção:

* Período previsto ainda não é o suficiente para o projeto (que seria de 30 
dias)
* Talvez seja interessante o estudo das variáveis que mais impactam nos 
resultados do forecasting a fim de identificar as variáveis que podem ser 
suprimidas ou substituídas por algumas de fácil acesso.

---

## [13][Renewable_Energy]Solar_irradiance_forecasting_without_onsite_training_measurements

[doi] https://doi.org/10.1016/j.renene.2020.01.092  
[Estudante] Andres Felipe Zambrano  
[Professor] Luis Felipe Giraldo  

### Qual o tema tratado?

Previsão de uma região (*site*) que não possui dados suficientes de irradiância
solar ou de outras variáveis climáticas, através de regiões vizinhas e que 
podem ser consideradas como próximas.

### Qual a proposta de solução?

Ordena-se os sites mais 'próximos' tanto em distância, quanto em fatores 
externos que possam ser mais similares ao site estudado sem dados.

Variáveis externas selecionadas das regiões que possuem dados:
1. Elevação
2. latitude/longitude,
3. Modelos de céu limpo
4. Medidas de satellite da região de forecast
5. Medidas de satelite das regiões vizinhas
6. Irradiância Solar das regiões vizinhas

* ANN para prever a Radiância solar de 1h a 48h nos sites próximos

* Criação de Vetor 2D de irradiância usando GHI (Global horizontal irradiance),
medidas de Satelite e CSM (Clear Sky Model), com configuração matricial sendo
as coordenadas as datas e os horários -> feito para feature selection

* Criação de métodos para a escolha dos sites mais próximos: 
    * Principal Component Analysis (PCA)
    * Learning to Rank
    * Kernel Machines

* Aplicação da distância de Mahalanobis ponderada


### Quais os resultados obtidos?

Olhando os gráficos da figura 2, os melhores resultados foram obtidos em 
intervalos menores, como 1h e 2h, distanciando-se cada vez mais com o aumento
do horizonte de tempo do forecast.

Além disso, perde-se as variações intradiárias, ficando na média depois de um 
período. O MAE passa de 44,5 W/m² (1h) até 63 W/m² (48h).

A tabela 2 também é muito interessante por conta da importância de cada uma das
features para o modelo de forecast.

A métrica escolhida para a seleçao de qual site se aproxima mais do site sem dados
é escolhida pelo MAE. 

### Existe algo que pode ser reaproveitado?

É interessante a possibilidade de se utilizar dados de lugares próximos,
não necessariamente fisicamente, mas que tenham mais a dizer sobre a semelhança
local. Pode ser um ponto de partida.

### Informações Complementares

---

## [14][Renewable_Energy]AddedValue_ensemble_prediction_system_quality_solar_irradiance_probabilistic_forecasts

[doi] https://doi.org/10.1016/j.renene.2020.07.042  
[Estudante] Josselin Le Gal La Salle  
[Professor] Jordi Badosa, Mathieu David, Pierre Pinson, Philippe Lauret  

### Qual o tema tratado?

Forecasting probabilístico de GHI (Global Horizontal Irradiance) considerando 
variáveis climáticas calculadas por modelos NWP (Numerical Weather Prediction)


### Qual a proposta de solução?

Para 6 regiões diferentes (*sites*) que possuem condições de céu diferentes, 
são realizados 3 modelos probabilisticos:

1. Utilizando apenas dados inferidos do membro de controle do sistema EPS;
2. Utilizando os dados do conjunto inteiro de membros do EPS, considerando
apenas a média dos cenários.
3. Utilizando os dados da maior parte do conjunto de membros do EPS, 
considerando a média e a variância dos cenários.

Além disso, seguem com duas linhas de resolução:

1. Utilização de dados de output de modelos de NWP (determinísticos) acoplados
a métodos estatísticos (Linear Quantile Regression e Analog Ensemble);

2. Forecast baseado na calibração de um sistema EPS (Ensemble Prediction 
System), onde podem ser aplicadas técnicas de tratamento do dado bruto, como a
Regressão Não Homogênea, além da utilizaçao de métodos estatísticos para a 
formação das probabilidades.


### Quais os resultados obtidos?

[Necessidade_Mais_Entendimento]

A tabela 4 do autor, indica o RMSE de cada uma das etapas de criação dos 
modelos. A calibração do EPS pela média de todos os membros é uma das métricas
com menor erro RMSE associado, perdendo apenas para a utilização de apenas o 
membro controle no site SP (o que configura uma exceção).

### Existe algo que pode ser reaproveitado?

Os EPS são sistemas bem complexos e computacionalmente custosos. Embora alguns
dos dados estejam disponíveis para o uso, não sabemos se todos eles, ou se 
todos os membros compartilham sua totalidade.

### Informações Complementares

EPS (Ensemble Prediction System) - Parece ser um modelo de cenários diferentes
por variáveis associadas. Por exemplo, qual seria a sensibilidade da previsão
quando uma das variáveis se altera? Esses são os tipos de cenário que podem ser
criados e mensurados.

CRPS (Continuous Ranked Probability Scores) - Sistema de rankeamento de 
forecasts probabilísticos 


---


## [16][Renewable_Energy]ShortTerm_global_horizontal_irradiance_forecasting_CNN_LSTM_model_spatiotemporal_correlations

[doi] https://doi.org/10.1016/j.renene.2020.05.150  
[Estudante] Haixiang Zang  
[Professor] Ling Liu, Li Sun, Lilin Cheng, Zhinong Wei e Guoqiang Sun  

### Qual o tema tratado?

Combinação de técnicas de Deep Learning, CNN (Convulutional Neural Networking)
e LSTM (Long Short-Term Memory), criando-se um modelo Híbrido para o forecast
de irradiância horizontal global num dado *site*.

### Qual a proposta de solução?

CNN extrai as variáveis espaciais mais relevantes da *site* (região a ser 
estudada) comparadas aos outros *sites* mais próximos ('vizinhos').

LSTM tenta extrair a relação entre a irradiância solar e a série temporal do
*site* estudado. 

Posteriormente as features selecionadas na CNN são acopladas ao modelo de LSTM
para que se possa realizar a previsão de irradiância horizontal global para uma
hora a frente.

Os dados inputados nos modelos, tem 1 ano de histórico, para 34 sites presentes
em diversas localidades apresentando diferentes zonas climáticas, em diferentes
estações e com diversidade de disposição de nuvens.

### Quais os resultados obtidos?

Os resultados do modelo híbrido CNN-LSTM são comparados com os modelos sozinhos
CNN, LSTM e com alguns benchmarks.

Os resultados anuais, nas diversas bases escolhidas, indicam que o modelo é o 
melhor dentre os benchmarks de comparação, em todas as métricas, com exceção do
*site* de Dallas que o modelo ANN-LSTM é ligeiramente melhor.

Quando comparados os resultados por estação, os resultados variam 
consideravelmente:
* Outono é a estação com menor erro MAE e RMSE para todos os modelos
* O modelo híbrido proposto é o melhor do *site* de San Jacinto
* Dentre os modelos, os que melhor apresentam métricas, são os híbridos que se
utilizam de Deep Learning.


### Existe algo que pode ser reaproveitado?

A utilização de DL (Deep Learning) para a extração de features (variáveis)
metereológicas representativas, pode ser uma idea boa se comparada com as 
outras regiões. Talvez um agrupamento seja necessário para saber quais são os
sites mais 'próximos' entre si, quando se trata de variáveis meteorológicas.

A maioria dos estudos indicam que a utilização de modelos híbridos se 
sobressaem às técnicas convencionais de previsão. O único problema é a 
quantidade e disponibilidade dos dados.

Outra coisa que pode ser reaproveitada é como é feita a *hybridização* do 
modelo proposto CNN-LSTM. [Procurar_Referências]


Obs.: 

* Existem dados suficientes no *site* estudado para se extrair a correlação com
*sites* vizinhos e irradiância ao longo do tempo.

* Autor diz que SVM (Support Vector Machine) tem boa performance para histórico
com poucos dados.

* Autor indica os softwares e máquina utilizada nos resultados do projeto.

### Informações Complementares

---

## [XX] 

[doi]
[Estudante]  
[Professor]

### Qual o tema tratado?

### Qual a proposta de solução?

### Quais os resultados obtidos?

### Existe algo que pode ser reaproveitado?

### Informações Complementares

---

# Forecasts variados

A seção abaixo indica os artigos que utilizam técnicas de Machine Learning e
Deep Learning para a previsão de demanda de carga gerada em um sistema PV 
dispondo de dados históricos suficientes e/ou imagens de satélites.


## [02][Energies]Deep Neural Network Model Short Term Load Forecast

10.3390/en11123493 [doi]
Chujie Tian [Estudante]  
[Professor]

### Qual o tema tratado?

Direcionamento geral focado principalmente em reduzir os erros de previsão
que podem ocasionar custos gigantescos ao sistema de produação de energia de
um dado local do mundo.

Realiza um detalhamento dos diferentes tipos de modelos existentes para a
previsão de demanda de carga em sistemas como um todo, explicitando o nível
de acurácia das CNN (Convulutional Neural Network) quando comparados aos 
métodos anteriores a ela, passando pelos métodos estatísticos e posteriormente
aos métodos de inteligência artificial.


### Qual a proposta de solução?

Criação de um modelo híbrido de redes neurais convulucionais (CNN) com um 
método de previsão chamado de termo de memória de longo a curto prazo 
(LSTM-Long-Short Term Memory) que é indicado como um método de redes neurais
recorrentes (RNN). O primeiro possibilita entender as variáveis ocultas do
período analisado e juntar com as informações de clima e ambiente enquanto 
o LSTM indica uma melhor captura das informações de longo período.

O modelo proposto utiliza os dados de 21 dias antes, com um tempo de 
intervalo de 1h, caracterizando uma curva detalhada. Esse input entra nos dois 
modelos ao mesmo tempo, e as respectivas últimas camadas de ambas as redes são 
'fundida' num processo chamado de 'feature-fusion' criando assim, a predição 
final do LTLF.

### Quais os resultados obtidos?

O sistema foi implantado no norte da Itália, com um período de Jan/2015 a 
Dec/2017, com intervalos de medição de 1h. Os dados foram obtidos pelo portal
de Transparência da região.

O período de treino: 2015 e 2016
O período de teste: 2017

O período de teste foi dividido em 8 seções, das quais foram comparados com 
diversos outros métodos de previsão, por sua vez mais simples, que o proposto.
Teve-se a comparação com Arvores de Decisão (DT), Random Forest (RF), DeepEnergy (DE) e as camadas simples de CNN e LSTM utilizadas previamente para a criação do modelo híbrido.

Em níveis de erros, o modelo híbrido se destacou como o melhor na média e 
melhor na maior parte dos períodos de teste destacados, com um MAPE médio de 4%
(Variando de 2,35% a 5,9%).

### Existe algo que pode ser reaproveitado?

**TODO**: Verificar Referência [29] nesse artigo

Os pontos de utilizar um modelo híbrido são bem interessantes, principalmente
o 'feature-fusion' proposto.

Pelo identificado, a previsão ocorre de 24h em 24h. Pode ser um bom ponto de 
começo para a previsão.


### Informações Complementares

Sistemas de Gerenciamento de Energia (EMS):
* VSTLF (Very Short Term Load Forecast) - Poucos minutos a frente
* STLF (Short Term Load Forecast)       - 24h a uma semana a frente
* MTLF (Medium Short Term Load Forecast)- + de uma semana a meses a frente
* LTLF (Long Short Term Load Forecast)  - + de um ano a frente


Explicando um pouco as redes neurais destacadas:

* RNN: são boas em capturar as dependencias não estacionárias do período bem 
como as dependencias de longo termo (+ de um ano por exemplo);

* CNN: são amplamente usadas nos campos de previsão (predict), devido a sua 
capacidade de capturar tendências locais e características que estão 
correlacionadas entre si;
---

## [03][Energy]Deep_Learning_Meteorological_params_Forecast_Intra_Hour_Power_PV_Gen

[*****] EXCELENTE

https://doi.org/10.1016/j.energy.2021.122116 [doi]

[Estudante]  
[Professor]

### Qual o tema tratado?

Definições acerca dos tipos de previsões estudadas e criadas, primeiramente
por conta dos período a frente previsto:
* intra-horario - até 1h após,
* intra-diario  - até 24h após,
* diario        - de 24h a 72h,
* semanal       - + 72h

Além disso contextualiza todo o problema acerca da disponibilidade de energia
por fonte renovável que depende de variáveis físicas para seu desempenho, 
impactando os níveis de geração e podendo comprometer a disponibilidade e a
segurança da rede, quando o gerador é interligado ao sistema.

### Qual a proposta de solução?

Forecast intra-horário, num intervalo de 10 min a frente, qual é a potência/
energia gerada por um sistema PV, utilizando métodos de Deep Learning. Utiliza
também modelos matemáticos e funções de densidade de probabilidade (PDF's) para
estipular o nível de confiabilidade do sistema.

É classificado como uma previsão 'paramétrica indireta' (PI) pois utiliza para
as suas previsões, dados de Irradiância prevista que não são inerentes ao 
modelo preditivo.

Utiliza também intervalos de 95% de confiança para três tipos de estado do 
clima: ensolarado, com poucas nuvens e nubaldo. Então existem qual o nível de 
probabilidade para cada uma das situações.

** Modelo Tecnico **
    DL = Deep Learning feedforward spatiotemporal neural network model

### Quais os resultados obtidos?

Os resultados atingem níveis melhores de precisão, utilizando intervalos de 
confiança mais restritos, o que garante um nível de acurácia melhor além de
identificar os possíveis valores de máximo e mínimo para cada tipo de dia em
questão.


### Existe algo que pode ser reaproveitado?

É necessário primeiramente entender como funcionam as funções de probabilidade
para posteriormente entender a relevância dos resultados obtidos.

Mas, o interessante é que ao invés de somente prever um valor, prever os
limites de cada curva é bom para nivelar quais são os possíveis máximos e 
mínimos de operação para o PV ou conjunto de PV'S. Isso pode significar uma
possível mudança no sistema, ou indicar qual o nível de potência reativa a ser
regulada ou até mesmo o quanto de multa a ser gerado.


### Informações Complementares

Principais características que influenciam a geração de um sistema PV são:
* Irradiância Solar
* Temperatura ambiente
* Velocidade do Vento

Distinção entre tipos de pesquisas em forecast:
* Physical - prevê uma condição climática ou algo que é puramente físico, sem
    a preocupação de se preocupar com a geração de energia elétrica. Também 
    ocorre que as previsões são feitas com modelos físico-matemáticos além da 
    utilização do reconhecimento de imagens de satélite para aperfeiçoar as 
    técnicas já desenvolvidas na teoria.
* Statistical - com base em dados históricos e algoritmos de ML, são previsões
    da parte final (geração de energia), utilizando as características já 
    mensuradas do ambiente,aplicando apenas métodos estatísticos pra isso.


---

## [04][Applied_Energy]Extensive_Comparison_Physical_Models_PV_Power_Forecast

https://doi.org/10.1016/j.apenergy.2020.116239 [doi]
[Estudante]  
[Professor]

### Qual o tema tratado?

Direcionamento geral e amplo estudo sobre os diferentes tipos de forecasting
de sistemas PV, cada qual com suas caracterísiticas, usabilidades e limitações,
separando-os em 3 tipos: 
* físicos - quando não se dispõe de dados suficientes e/ou não tem uma
    confiabilidade inerente ao processo, esses modelos se destacam por
    apresentar a previsão baseada em fatores físico-climáticos (como 
    irradiância solar, ou imagens de satélite)
* estatísticos - *data-drive*, ou seja, necessidade de um histórico relevante
    para se obter melhores resultados.
* híbridos - a combinação dos últimos dois e o que possui melhor performance.
    utiliza os dados disponíveis dos sistemas PVs ao mesmo tempo que baliza 
    suas decisões em fatores físico, incorporando-os.

### Qual a proposta de solução?

Identificar e comparar uma grande parcela dos sistemas físicos de calculo de
potência elétrica gerado por sistemas PV, identificando os melhores modelos,
bem como quais são os passos principais (etapas de cálculos necessários) que 
correspondem a esses modelos.

Os modelos analisados correspondem a forecastings intra-day e day-ahead com
resolução de 15 min.

### Quais os resultados obtidos? 

[POLEMICO] O modelo tido como o melhor dentre os da literatura não foi 
considerado como o melhor, pelo estudo.

O que mais impactou os erros associados a geração de um dado PV foi a
irradiância solar obtida.

MAE e RMSE são métricas antagonistas, ou seja, não corroboram ao mesmo
resultado. Caminham em direções opostas e o autor não soube definir qual seria
a melhor a ser seguida.

Os modelos mais complexos tendem a reduzir mais o MAE, enquanto os mais simples
diminuem o RMSE.


A escolha dos procedimentos são dadas pelo autor:

    "The model chains with lowest MAE consist of the STARKE separation model, 
    MUNEER transposition model, MARTIN-RUIZ or PHYSICAL reflection model, 
    FAIMAN or MATTEI cell temperature model, EVANS PV perfor­mance model, 
    beam shading calculation, and CONSTANT or QUADRATIC inverter efficiency models.

    The model chains with the lowest RMSE induce the BLR separation model, 
    LIU-JORDAN transposition model, PHYSICAL reflection calculation, NOCT cell 
    temperature model, EVANS PV model, beam shading calculation, and CONSTANT 
    inverter efficiency."

Resumindo:

|         Cálculo / Métrica        	|           MAE           	|    RMSE    	|
|:--------------------------------:	|:-----------------------:	|:----------:	|
| Modelo de Separação              	|          STARKE         	|     BLR    	|
| Modelo de Transposição           	|          MUNEER         	| LIU-JORDAN 	|
| Modelo de Reflexão               	| MARTIN-RUIZ ou PHYSICAL 	|  PHYSICAL  	|
| Modelo de Temperatura da Célula  	|     FAIMAN ou MATTEI    	|    NOCT    	|
| Modelo de Performance da PV      	|          EVANS          	|    EVANS   	|
| Modelo de Cálculo de Sombra      	|           BEAM          	|    BEAM    	|
| Modelo de Eficiência do Inversor 	|  CONSTANT ou QUADRATIC  	|  QUADRATIC 	|


### Existe algo que pode ser reaproveitado?

O conhecimento dos melhores modelos físicos, proporcionam uma possibilidade de
forecasting para casos onde não se tem dados disponíveis para essa geração. 
Portanto pode ser considerado como um método inicial.

Importante também para o forecasting de irradiancia solar e acoplamento num 
modelo de otimização da qual se estima as potências ao longo de um período 
maior.

### Informações Complementares

---


## [05][Applied_Energy]PV_Power_Forecast_Satellite_Imgs_Solar_Position

https://doi.org/10.1016/j.apenergy.2021.117514 [doi]
[Estudante]  
[Professor]

### Qual o tema tratado?

Dada a dificuldade de forecast de potência de sistemas PV, o artigo trata da
possibilidade de se prever a potência desses sistemas considerando a passagem
das nuvens e a localização do sol em um dado momento.

Isso faz com que a previsão pudesse ser mais correta, visto que as oscilações
presentes nos métodos de forecasting são relacionadas a partes onde o clima se
apresenta com nuvens, completa ou parcialmente.

### Qual a proposta de solução?

A proposta se divide em 4 principais etapas:

1. Utilização de CNN, Conv-LSTM (Convulutional Long-Short Term Memory) para
    identificação do vetor de direção das nuvens, utilizando imagens de 
    satélites, considerando a mudança de espessura e formato.
2. Predição da área afetada pela nuvem utilizando um modelo chamado ACSR 
    (Active Cloud Region Selection), e portanto identificando qual é a 
    proporção de impacto na previsão de potência do sistema.
3. Predição das áreas de nuvens que afetam os sistemas PVs em um intervalo de
    tempo curtíssimo, da ordem de 15 minutos. Modelo chamado de SCRS 
    (Sequential Cloud Region Selection)
4. Usando as variáveis calculadas anteriormente, utiliza-se o algoritmo XGBoost
    para calculo da potência elétrica prevista para o sistema PV nos próximos 
    15 min.


### Quais os resultados obtidos?

É feito uma comparação entre modelos com algumas variáveis a menos, a fim de
constatar a eficácia do método escolhido e o porquê de todos os passos 
executados, garantindo que as nuvens e sua localização impactam de maneira
direta e significativa na previsão de demanda da potência de sistemas PV.

O modelo proposto é tido como o melhor dentre 3 modelos com quantidades de 
variáveis diferentes, assim como melhor também quando comparados a LSTM e CNN
originais (mesmo que pouco para esses últimos), para todos as resoluções de 
previsão selecionadas (15, 30 e 60 min).

As métricas variam de 3,4 a 3,6% para os modelos M1 a M3, enquanto que o
proposto atinge 3% de erro NMSE (normalized Mean Square Error) para uma 
resolução de 15 min.


### Existe algo que pode ser reaproveitado?

É interessante como o autor aplicou as previsões de imagens de satélite em 
intervalos posteriores, para saber onde estarão as nuves. Além de identificar
onde as nuvens terão mais impacto em uma dada região por conta da posição do
sol.

Mesmo assim, os dados de potência elétrica do sistema PV ainda é necessário
dado que a ultima parte de previsão é colocada no algoritmo de XGBoost.


### Informações Complementares

NWP- Numerical Weather Prediction

---

## [06][Applied_Energy]Probabilistic_Forecast_PV_Power_Supply

https://doi.org/10.1016/j.apenergy.2021.117599 [doi]
[Estudante]  
[Professor]

### Qual o tema tratado?

Forecasting probabilístico da potência de saída de um sistema PV e suas
comparações com os modelos determinísticos de previsão de demanda, das quais 
podem não agregar a dados setores de mercado e/ou energia no planejamento de
suas operações diárias.

O autor relata a diferença entre os modelos determinísticos em físicos e 
estatísticos e indica que os estudos na área de forecasting probabilístico tem
crescido ultimamente, dado as diferentes possibilidades de usos.

### Qual a proposta de solução?

A proposta de solução é a aplicação de métodos de pré e pós-processamento dos 
dados de input em um modelo 'convencional' e uma tentativa de melhora do 
forecasing probabilistico usando 'copulas'.

A ideia geral pode ser separada em 3 principais passos:

1. **Modelo Físico** - Utilização de um modelo para previsão de características
    físicas para input de um modelo estatístico.
2. **Modelo Estatítico (*Data-Driven*)** - Da qual teremos o resultado do 
    forecasting de potência utilizando o modelo físico anterior para
    composição de algumas das variáveis além de criação de um método de pré e
    pós processamento desses mesmos dados ao entrar e sair do modelo.
3. **Modelo Probabilistico** - utilização de técnicas de 'copulas' para medir a 
    probabilidade de ocorrência de um evento em cada um dos nós de uma rede. 
    Isso ajuda na criação de cenários e sua dada probabilidade de ocorrência.

### Quais os resultados obtidos?

[Necessidade]: Estudar mais sobre os métodos probabilisticos e como funcionam.

### Existe algo que pode ser reaproveitado?

[Necessidade]: Estudar mais sobre os métodos probabilisticos e como funcionam.
[REFERENCIA][15]

A aplicação do método probabilistico no final do processo, é utilizado para um 
conjunto de PVs organizados em uma rede e utiliza os erros associados de 
previsão, ditos correlacionados entre si.

Ainda acredito que a definição de um intervalo de confiança numa dada previsão
determinística ainda possui mais valor para o caso atual do que a presente 
situaçao.

### Informações Complementares



---



## [07][Applied_Energy]Comparison_Day_Ahead_PV_Power_Forecasting_Deep_Learning_Neural_Networks 

https://doi.org/10.1016/j.apenergy.2019.113315 [doi]
[Estudante]  
[Professor]

### Qual o tema tratado?

Comparação entre 3 modelos de forecasting utilzando CNN (Convulutional Neural
Network), LSTM (Long-Short Term Memory) e um modelo híbrido com os dois na 
previsão de carga num sistema PV. 

### Qual a proposta de solução?

Realizar a predição com os três tipos de modelos mencionados acima e comparar
suas efetividades. Além disso, conta com uma iteração na quantidade de dados de
input são inseridos no melhor dos modelos e compara-se os resultados, ou seja
indica quanto de efetividade se perde ao se inserir mais ou menos dados na 
entrada.

A ultima coisa mencionada é o período de treinamento necessário para que o 
modelo esteja pronto para realizar o forecasting.

Os principais dados utilizados:

* Corrente de fase (A)
* Potência Ativa (kW)
* Velocidade do vento (m/s)
* Temperatura (°C)
* Umidade relativa (%)
* Radiação Horizontal Global (w/ m 2 × sr)
* Radiação Horizontal Difusa (w/ m 2 × sr)
* Direção do vento (Â°)
* Entre outras.

### Quais os resultados obtidos?

Os melhores resultados foram obtidos pelo modelo híbrido, que ficou pouco a
frente do modelo puro CNN, enquanto que o LSTM ficou em último nas comparações.

Os mínimos MAPEs entre todos os períodos testados, é de 2,2% (CLSTM), 2,5% 
(CNN) e 3,2% (LSTM).

O interessante é que com a quantidade de dados de entrada, houve uma variação
muito brusca dos resultados, tendo uma tendência de queda de 6 meses a 3 anos,
atingindo seu valor mínimo, e posteriormente elevando as métricas de erro após
esse período, que se estende até 4 anos.

### Existe algo que pode ser reaproveitado?

Dois artigos mostraram bons efeitos de se utilizar os modelos híbridos de CNN
com um LSTM, além de demonstrarem que o período de histórico é importante, 
mas em demasia, pode significar uma piora na performance. 

### Informações Complementares

---

## [08][Energy]PV_Power_Forecast_LSTM_Convulutional_Network

[Estudante]  
[Professor]

### Qual o tema tratado?

### Qual a proposta de solução?

### Quais os resultados obtidos?

### Existe algo que pode ser reaproveitado?

### Informações Complementares

---

## [09][Applied_Energy]SolarNet_Hybrid_Reliable_Model_CNN_hourly_Forecast_PV_Power

https://doi.org/10.1016/j.apenergy.2021.117410 [doi]
Deniz Korkmaz [Estudante]  
[Professor] 

### Qual o tema tratado?

Previsão de potência ativa produzida por um sistema PV utilizando os dados
climáticos e de relevância física do sistema de forma que eles passem a uma 
composição de uma imagem, que posteriormente é utilizada no modelo de CNN,
denonimado SolarNET.

### Qual a proposta de solução?


    'The proposed framework includes four main stages as decom­
    position with the VMD, reconstruction of the historical time-series in­
    puts into the hue-saturation-value (HSV) color space and concatenation
    into a single red–greenblue (RGB) image, training of the designed CNN
    model, and testing phase of the trained network.'

    'The input parameters of the network are the measured historical global
    horizontal radiation, diffuse horizontal radiation, temperature, humid­
    ity, and active power of the technology demonstration facility in
    Australia'

### Quais os resultados obtidos?

As curvas da projeção são bem aderentes a curva real do sistema, com MAE de
aproximadamente 0,2 a 0,4 para 1h de previsão a frente, podendo chegar a 0,64
para previsões de 3h.

As estações do ano influenciam, como era de se esperar, nos resultados do 
modelo onde níveis mais ensolarados (meses do meio do ano) possuem erros 
menores quando comparados aos meses com mais nuves e chuvas.

### Existe algo que pode ser reaproveitado?

Talvez o método de decomposição das variáveis possa ser estudado com mais 
calma para poder identificar o que pode ser aplicado em um exemplo pático de
long-term prediction.


### Informações Complementares

Primeira introdução dos 'soft' models, da qual um popular é o SVR (Support 
Vector Regression), métodos de otimização que indicam os melhores 
hiperparâmetros de um modelo 

---



## [XX] 

[Estudante]  
[Professor]

### Qual o tema tratado?

### Qual a proposta de solução?

### Quais os resultados obtidos?

### Existe algo que pode ser reaproveitado?

### Informações Complementares

---

# Fontes de Dados

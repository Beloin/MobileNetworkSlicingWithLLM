# Roteiro de Apresentação — Bloco 3 · Seção IX (versão condensada, alinhada ao deck)
Artigo: *6G: The Intelligent Network of Everything* (H. Pennanen et al., IEEE Access, vol. 13, 2025, DOI: 10.1109/ACCESS.2024.3521579)
Deck: `6G-Lit-Review-Proposta-v2-37-slides.pptx` — slides 20 a 28 (Bloco 3: "Arquitetura, core e virtual slicing")
Duração alvo: ~8–10 minutos (~1.100–1.300 palavras em ritmo normal)

---

## Plano de tempo

| Tempo | Slide | Conteúdo                                             |
|-------|-------|------------------------------------------------------|
| 0:00  | 20    | Abertura do Bloco 3                                  |
| 0:30  | 21    | Panorama da Seção IX (A–J) e nosso recorte           |
| 1:30  | 22    | D · INTN / SAGIN — as três camadas                   |
| 3:00   | 23    | D · UDN, IAB e cell-free massive MIMO                |
| 4:30  | 24    | E · Evolução do core, geração a geração              |
| 5:30  | 25    | E · O que o 5G já trouxe: SBA, SDN, NFV, slicing     |
| 6:15  | 26    | E.1 · Intelligent core e AI-native slicing           |
| 7:15  | 27    | E.2–E.3 · Edge inteligente e interface aérea          |
| 8:30  | 28    | RQ3 · Quatro lacunas do slicing autônomo              |
| 9:15  | —     | Fechamento e transição para o Bloco 4                |

---

## SLIDE 20 — ABERTURA DO BLOCO 3 (0:00 – 0:30)

Chegamos ao **Bloco 3** — o recorte técnico central da nossa revisão de literatura.

Aqui, aprofundamos a **Seção IX do artigo-base**, que cataloga vinte e sete tecnologias 6G em dez famílias. Mas o nosso foco não é percorrer as dez — é detalhar as duas que mais interessam à nossa revisão: **arquitetura de rede e inteligência de rede**. São elas que sustentam o tema do nosso trabalho: o **slicing** no 6G.

---

## SLIDE 21 — PANORAMA DA SEÇÃO IX (0:30 – 1:30)

A Seção IX organiza as tecnologias 6G em dez famílias, de A a J:

**A** — espectro (THz e comunicação óptica sem fio);
**B** — sistemas de antena (ultra-massive MIMO, RIS, holographic MIMO);
**C** — esquemas de transmissão (multi-waveform, modulação/codificação, NOMA, grant-free);
**D** — **arquitetura de rede** — redes não-terrestres integradas, UDN, IAB e cell-free massive MIMO;
**E** — **inteligência de rede** — core, edge e interface aérea inteligentes;
**F** — além-comunicação (computação, sensoriamento e energia integrados);
**G** — energia (redes verdes, harvesting, backscatter);
**H** — dispositivos finais (D2D, V2X, UAVs);
**I** — serviços (redes privadas);
**J** — segurança.

[pausa]

De todas essas, o nosso recorte é: **D e E**. Por quê? Porque respondem diretamente às nossas questões de pesquisa — RQ1, sobre o core 6G nativo em IA, e RQ2, sobre as arquiteturas que suportam o slicing fim a fim. As demais famílias entram na Lit Review como contexto.

---

## SLIDE 22 — D · INTN / SAGIN (1:30 – 3:00)

Começando pela arquitetura. O primeiro elemento é a rede integrada terrestre e não-terrestre — o que a literatura chama de **SAGIN**: space-air-ground integrated network. O artigo descreve três camadas operando como uma só rede.

**Camada terrestre** — as redes móveis convencionais e as estações terrenas: é onde está o grosso da capacidade, nas áreas urbanas e suburbanas.

**Camada aérea** — HAPS, as plataformas de alta altitude, e UAVs. Elas adicionam cobertura intermediária, preenchendo lacunas entre o solo e o espaço — do denso urbano ao rural.

**Camada espacial** — satélites em órbita baixa, média e geossíncrona — LEO, MEO e GEO — entregando cobertura verdadeiramente global.

A mensagem-chave: no 6G, o limite da rede não é mais o horizonte. O slicing atravessa as três camadas — e é justamente a orquestração de fatias nesse cenário 3D e heterogêneo que conecta com a nossa **RQ2**.

---

## SLIDE 23 — D · UDN, IAB E CELL-FREE (3:00 – 4:30)

A segunda metade da arquitetura de rede responde a três perguntas práticas.

**Primeira: como entregar capacidade extrema?** Com **redes ultra-densas — UDN**. Lembrem que as frequências THz, apontadas para o 6G, têm alcance muito curto. Para que elas cubram algo, as células precisam ser pequenas e numerosíssimas. A UDN é o outro lado da moeda do THz: densificação extrema.

**Segunda: como conectar milhares de células pequenas sem cavar ruas para passar fibra?** Com **IAB — integrated access and backhaul**. A célula atende o usuário e, ao mesmo tempo, serve de backhaul sem fio para as células vizinhas. A implantação fica flexível e barata — a célula se instala onde há demanda, não onde há fibra.

**Terceira: como garantir QoS estável em toda a área?** Com **cell-free massive MIMO** — o fim da célula fixa. Vários pontos de acesso distribuídos cooperam e atendem cada usuário de forma conjunta. Sem bordas de célula, sem "cantos" onde o sinal cai — qualidade uniforme onde o usuário estiver.

Essas três tecnologias, junto com a SAGIN, são a resposta arquitetural da literatura para a nossa **RQ2**: que estruturas suportam slicing fim a fim no 6G.

---

## SLIDE 24 — E · EVOLUÇÃO DO CORE (4:30 – 5:30)

Da arquitetura para a inteligência. O artigo conta a história do núcleo de rede geração a geração — e essa linha do tempo é o cerne da nossa **RQ1**.

No **2G**, o core era de **comutação de circuitos** — dedicado à voz.

No **3G e 4G**, chegou o **packet core** — a internet no celular, comutação por pacotes.

No **5G**, o core se torna **cloud-native**: SBA, SDN, NFV e network slicing — funções de rede que viram software, rodando em nuvem.

E o **6G** propõe o próximo passo: o **cloud intelligence** — IA pervasiva no núcleo. O core deixa de ser apenas virtualizado e passa a ser **inteligente**: gerenciado, otimizado e fatiado pela própria IA.

É dessa transição — cloud-native para AI-native — que trata a nossa RQ1.

---

## SLIDE 25 — E · O QUE O 5G JÁ TROUXE (5:30 – 6:15)

Antes de olhar o 6G, vamos fixar o que o 5G estabeleceu, porque o 6G herda e amplia tudo isso.

**SBA — service-based architecture**: o core é um conjunto de funções de rede interconectadas, cada uma oferecendo serviços reutilizáveis por outras funções. Isso permite agregar novas funcionalidades com agilidade.

**SDN — software-defined networking**: a gestão da rede se descola do hardware e se torna flexível, nativa em nuvem.

**NFV + network slicing**: os recursos físicos são divididos em **fatias virtuais**, cada uma dedicada a um serviço — uma fatia para URLLC, outra para eMBB, outra para mMTC. É o slicing que conhecemos — e é o ponto de partida da nossa revisão.

---

## SLIDE 26 — E.1 · INTELLIGENT CORE (6:15 – 7:15)

O primeiro nível da inteligência 6G é o **core inteligente**.

O artigo propõe IA/ML pervasiva otimizando operação, gestão e **segurança** do núcleo de forma **autônoma**. O core cloud-native do 5G virtualizou as funções; o core 6G as torna inteligentes — a rede passa a se autoconfigurar e se autocurar.

E aqui está o conceito central para a nossa revisão: o **AI-native slicing**. No 5G, a fatia é definida e orquestrada por regras humanas. No 6G, **a própria IA decide como fatiar a rede** — dinamicamente, conforme a demanda, o tráfego e o contexto. É essa autonomia que abre as lacunas que veremos no slide 28.

---

## SLIDE 27 — E.2–E.3 · EDGE E INTERFACE AÉREA (7:15 – 8:30)

A inteligência não fica só no core. Dois desdobramentos completam o quadro:

**Intelligent edge** — a combinação de edge computing com IA. O artigo classifica **seis níveis de inteligência de borda**: no nível 1, o treino e a inferência ficam na nuvem; no outro extremo, tudo roda on-device. Entre eles, um espectro de trade-offs: **latência, energia e privacidade** — quanto mais perto do dispositivo, mais rápido e privado; quanto mais na nuvem, mais poder de processamento.

**Intelligent air interface** — a IA chega à camada física. O artigo descreve **três fases** de evolução: primeiro, a IA **substitui blocos individuais** do processamento — estimação de canal, demapeamento de símbolos. Depois, **projeta vários blocos em conjunto** — estimação, equalização e demapeamento como um só modelo. Por fim, **desenha a interface aérea inteira** com aprendizado fim a fim — uma ruptura no projeto e na padronização de redes móveis.

Com isso, a inteligência cobre o core, a borda e o rádio — ponta a ponta.

---

## SLIDE 28 — RQ3 · LACUNAS DO SLICING AUTÔNOMO (8:30 – 9:15)

Fechamos com a pergunta que motiva a nossa revisão: **onde a literatura ainda não fechou a conta?** No slicing autônomo, quatro lacunas:

**Explicabilidade** — se a IA decide as fatias, as decisões precisam ser **auditáveis**. Como justificar — e corrigir — uma decisão do modelo?

**Garantia de SLA** — como assegurar isolamento e estabilidade entre fatias quando a rede se **reconfigura continuamente**?

**Segurança do modelo** — envenenamento de dados e ataques adversariais: a IA que controla a fatia vira ela mesma alvo.

**Orquestração fim a fim** — fatias atravessando RAN, transporte, core **e SAGIN** — incluindo a camada não-terrestre do slide 22. Ninguém ainda orquestrou isso de ponta a ponta.

Essas quatro lacunas são a contribuição original que a nossa Lit Review se propõe a mapear.

---

## FECHAMENTO (9:15 – 9:45)

Em resumo: o 6G arquitetonicamente é uma rede **híbrida e tridimensional** — SAGIN, UDN, IAB e cell-free; e funcionalmente é uma rede **nativa em inteligência** — core, edge e rádio aperfeiçoados por IA, com slicing autônomo como caso extremo.

Onde a literatura ainda não convergiu — explicabilidade, SLA, segurança e orquestração fim a fim — é exatamente onde a nossa revisão vai se debruçar.

Na sequência, o Bloco 4 mostra o **para quê**: as aplicações e casos de uso que justificam toda essa estrutura. [transição para o slide 29]

---

## Fatos de apoio (para o Q&A)

- 27 tecnologias / 10 categorias (A–J) na Seção IX; cada uma revisada no modelo visão → introdução → passado/presente → oportunidades/desafios → literatura
- Core (paper, IX-E.1): "evolved from the circuit-switched network of 2G through the packet cores of 3G and 4G to the latest software/service-based architecture of 5G" (Rel-15); 6G = "from cloud to cloud intelligence"
- 5G Core: SBA, SDN, NFV, network slicing (3GPP Release 15)
- Edge intelligence: 6 níveis (Figura 31 do paper) — trade-off latência × energia × privacidade
- Air interface: 3 fases rumo à AI-native (Figura 32 do paper) — bloco individual → projeto conjunto → end-to-end
- SAGIN: ground (redes móveis/estações terrenas) · airborne (HAPS, UAVs) · spaceborne (LEO/MEO/GEO)
- UDN como contrapartida do THz de curto alcance; IAB já presente no 5G; cell-free massive MIMO para QoS estável sem bordas de célula
- IA/ML nos padrões: 3GPP Release 18 (5G-Advanced)
- Lacunas RQ3 do deck: explicabilidade, SLA, segurança do modelo, orquestração fim a fim (RAN + transporte + core + SAGIN)
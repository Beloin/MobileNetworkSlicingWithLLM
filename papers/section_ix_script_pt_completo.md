# Roteiro de Apresentação — Seção IX: "Potential Technologies for 6G" (versão completa, A–J)
Artigo: *6G: The Intelligent Network of Everything* (H. Pennanen et al., IEEE Access, vol. 13, 2025, DOI: 10.1109/ACCESS.2024.3521579)
Duração alvo: ~15 minutos (~2.000 palavras em ritmo normal de fala)
Referências de slides: `6G-Lit-Review-Proposta-v2-37-slides.pptx`

---

## Plano de tempo

| Tempo | Parte                                               | Slides (deck) |
|-------|-----------------------------------------------------|---------------|
| 0:00  | Abertura e roteiro da seção                          | —             |
| 1:00  | A. Espectro: THz + OWC                              | —             |
| 2:30  | B. Sistemas de antena: UM-MIMO, RIS, HMIMO          | —             |
| 4:00  | C. Esquemas de transmissão                           | —             |
| 5:00  | D. Arquitetura de rede: INTN, UDN, IAB, cell-free    | 22–23         |
| 6:30  | E. Inteligência de rede: core, edge, interface aérea | 24–27         |
| 8:00  | F. Além-comunicação: i3C, ISAC, WET                  | —             |
| 9:30  | G. Tecnologias de energia                             | —             |
| 10:30 | H. Dispositivos: D2D, V2X, UAV                       | —             |
| 11:30 | I. Serviços: redes privadas                          | —             |
| 12:00 | J. Segurança                                         | —             |
| 13:00  | Fechamento                                           | —             |

> Observação: as categorias A–C e F–J não têm slides dedicados no deck. Use o roteiro abaixo como **backup** (ex.: se perguntas da banca/toada abordarem essas famílias) ou para a redação da Lit Review.

---

## ABERTURA (0:00 – 1:00)

Bom dia / boa tarde a todos.

Nesta parte, vou percorrer a Seção IX do artigo, "Potential Technologies for 6G". Este é o núcleo técnico do survey: os autores identificam e revisam **vinte e sete tecnologias candidatas, organizadas em dez categorias**.

Duas observações antes de começar:

Primeira: cada tecnologia da seção segue o **mesmo modelo de apresentação** — visão, introdução, passado e presente, oportunidades e desafios, literatura e direções futuras. A estrutura se repete, o que facilita o acompanhamento.

Segunda: a mensagem central da seção é esta — o 6G **não será construído sobre uma única disrupção**. Será um sistema **grande e heterogêneo**, e cada uma das dez categorias resolve uma parte diferente do quebra-cabeça: espectro, antenas, transmissão, arquitetura, inteligência, e assim por diante.

[Se estiver usando o deck: este é o contexto do slide 21, que abre o Bloco 3 — "Panorama da Seção IX".]

Vamos lá, categoria por categoria.

---

## A. TECNOLOGIAS DE NÍVEL DE ESPECTRO (1:00 – 2:30)

A primeira categoria é o **espectro**. Duas tecnologias.

**Número um: comunicação Terahertz.**

[desacelerar — é a tecnologia-carro-chefe]

A banda THz vai de 0,1 a 10 terahertz. Pela **enorme quantidade de espectro disponível**, o THz é visto como *o* habilitador-chave para as metas de capacidade extrema do 6G — incluindo o objetivo de **um terabit por segundo de taxa de pico**.

O contrapeso é a propagação dura: alta perda de trajeto, absorção molecular e bloqueio fácil. Logo, THz significa **curto alcance** — o que funciona para hotspots, enlaces de proximidade e aplicações sedentas por dados, como telepresença holográfica e XR sem fio.

Onde estamos hoje? As demonstrações da indústria já impressionam: a Samsung atingiu 6,2 gigabits por segundo a 140 gigahertz; a Nokia com a NTT alcançou 25 gigabits por segundo a 144 gigahertz; e a Keysight passou de 100 gigabits por segundo a 300 gigahertz. No plano regulatório, a WRC-2023 identificou **cinco faixas acima de 100 gigahertz** para potencial uso IMT-2030, com decisão esperada na WRC-2031. Ou seja: o 6G será a **primeira geração a ultrapassar os 100 gigahertz** — assim como o 5G foi a primeira acima de 6 gigahertz.

Principais desafios: perdas de propagação, desalinhamento de feixe no ultra-massive MIMO, impairments de hardware como ruído de fase e consumo de energia. O artigo aponta RIS e beamforming híbrido como caminhos de mitigação.

**Número dois: comunicação óptica sem fio — OWC.**

A OWC complementa o rádio em **cenários especiais**: visible light communication para acesso interno de curto alcance, e free-space optics — FSO — para enlaces ponto a ponto externos de longo alcance, como backhaul. Experimentos modernos de FSO já demonstraram **multi-terabits por segundo** sobre quilômetros, e até classe petabit em distâncias curtas. O porém: turbulência atmosférica, divergência do feixe e necessidade de linha de visada, o que limita a confiabilidade na prática.

**Transição:** Esse é o espectro. A pergunta seguinte — como explorá-lo no nível de antenas?

---

## B. TECNOLOGIAS DE SISTEMAS DE ANTENA (2:30 – 4:00)

Três tecnologias, todas empurrando as antenas ao limite.

**Primeira: ultra-massive MIMO.** Evolução natural do massive MIMO, com **centenas a milhares de elementos de antena**, possivelmente embutidos em superfícies ao redor do dispositivo. O papel no 6G: viabilizar o THz em ambiente celular — os altos ganhos de beamforming compensam as enormes perdas de trajeto. Feixes muito estreitos trazem também **benefícios além da comunicação**: sensoriamento e localização de alta precisão.

**Segunda — e a mais revolucionária — Reconfigurable Intelligent Surfaces, RIS.** [pausa]

A ideia é simples e poderosa: em vez de nos adaptarmos ao ambiente sem fio, nós **programamos o próprio ambiente**. Um RIS é um painel com muitos elementos passivos, de baixo custo, controlados eletronicamente, que refletem o sinal incidente com fase ajustável — criando "beamforming passivo" na direção do receptor. Benefícios: melhor qualidade de sinal, extensão de cobertura e — muito relevante para THz — **contornar bloqueios**. Como o RIS passivo quase não consome energia, é barato e eficiente. Por isso o artigo o chama de potencial game-changer: transformar o canal sem fio imprevisível em uma **entidade programável e controlável**.

**Terceira: holographic MIMO.** Pense no limite teórico dessa tendência: uma superfície com um número de elementos virtualmente contínuo — quase infinito. Superfícies holográficas ativas atuam como transceptores; as passivas se aproximam do RIS. A promessa são **ganhos de multiplexação espacial muito altos**, aproximando os limites fundamentais da teoria MIMO.

**Transição:** As antenas são os "encanamentos" — mas o que transmitimos por eles?

---

## C. TECNOLOGIAS DE ESQUEMA DE TRANSMISSÃO (4:00 – 5:00)

Quatro elementos, que vou agrupar.

**Esquema multi-waveform.** O 6G precisa operar de sub-6 gigahertz até THz — as condições mudam drasticamente ao longo dessa faixa. Em vez de "tamanho único", espera-se que o 6G suporte uma interface aérea **multi-waveform flexível e ajustável**: o formato de onda se adapta à banda e ao cenário.

**Modulação e codificação avançadas.** Trabalho clássico de camada física, agora adaptado para grandes larguras de banda, impairments de hardware e integração com sensoriamento — por exemplo, modulações que também funcionam bem para funções tipo radar.

**NOMA — non-orthogonal multiple access.** Atender múltiplos usuários no mesmo recurso tempo-frequência melhora a eficiência espectral. O artigo destaca um caso de uso bem "6G": **IoT massivo** em combinação com acesso grant-free.

**E a quarta: acesso grant-free.** Hoje, um dispositivo precisa solicitar uma concessão ("grant") antes de transmitir. Em IoT ultra-massivo, essa sinalização colapsaria. O grant-free permite que os dispositivos **transmitam instantaneamente, sem agendamento** — economizando latência, sinalização e energia.

**Transição:** Agora — como organizar tudo isso no nível de rede?

[Se estiver usando o deck: a partir daqui, você chega ao slide 22.]

---

## D. TECNOLOGIAS DE ARQUITETURA DE REDE (5:00 – 6:30)

A rede se torna um **sistema tridimensional e híbrido**. Quatro tecnologias.

**Redes não-terrestres e terrestres integradas — INTNs.** [slide 22 do deck: camadas SAGIN]

Esta é a arquitetura espaço–ar–terra: **terrestre** (redes móveis e estações terrenas), **aérea** (HAPS e UAVs, cobertura do urbano ao rural) e **espacial** (satélites LEO, MEO e GEO) operando como uma só rede. O objetivo é **cobertura verdadeiramente global** — terra, mar e ar — mais aplicações como conectividade em áreas remotas e monitoramento global de IoT.

**Redes ultra-densas — UDN.** Lembrem: THz tem alcance curto — então, para entregar capacidade extrema, as células precisam ficar muito menores e muito mais densas. A UDN é, essencialmente, o outro lado da moeda do THz.

**Acesso e backhaul integrados — IAB.** Com milhares de células pequenas, não dá para levar fibra até cada uma. O IAB permite que as células **atendam usuários e sirvam de backhaul umas às outras no mesmo enlace sem fio**. Já existe no 5G, mas o papel cresce conforme a densificação continua.

**Cell-free massive MIMO.** Uma ruptura com o paradigma celular: muitos pontos de acesso distribuídos atendem cada usuário **de forma conjunta e cooperativa** — sem bordas de célula. A motivação é **QoS estável e uniforme** em toda a área de cobertura.

**Transição:** Até aqui, tudo é engenharia convencional. A próxima categoria é a grande mudança de paradigma: tornar a própria rede inteligente.

---

## E. TECNOLOGIAS DE INTELIGÊNCIA DE REDE (6:30 – 8:00)

É aqui que IA e aprendizado de máquina deixam de ser um acessório e passam a ser **nativas** da rede. O artigo posiciona a inteligência em três níveis. [slides 24–27 do deck]

**Core inteligente.** [slides 24–26]

O core do 5G foi sobre softwarização — funções de rede virtualizadas, SBA, SDN, NFV e network slicing. O 6G vai além: IA/ML pervasiva torna o core **autogerenciável, automatizado e proativo**. Os autores enquadram isso como uma evolução do "cloud" para o "**cloud intelligence**". Um conceito importante para o nosso trabalho: o **AI-native slicing** — a própria IA decide, de forma autônoma, como fatiar a rede. [conecta com RQ1 do grupo: a transição do core 5G cloud-native para o core 6G nativo em IA]

**Edge inteligente.** [slide 27]

Edge intelligence é a combinação de **edge computing + IA**. O artigo define **seis níveis de inteligência de borda**, do treino/inferência totalmente na nuvem até o totalmente on-device — um trade-off contínuo entre latência, energia, custo de comunicação e privacidade.

**Interface aérea inteligente.** [slide 27]

Até a camada física é aperfeiçoada por IA/ML. O artigo descreve **três fases evolutivas** rumo a uma interface aérea AI-native: primeiro, a IA substitui **blocos individuais** (estimação de canal, demapeamento de símbolos); depois, **projeta blocos em conjunto** (estimação + equalização + demapeamento); por fim, **desenha a interface aérea fim a fim** via aprendizado end-to-end — uma ruptura completa no projeto e na padronização de redes móveis.

Contexto relevante: IA/ML entrou nos padrões 3GPP a partir do Release 18 (5G-Advanced). O 6G tende a torná-la pervasiva.

**Transição:** Com inteligência por toda parte, a rede pode assumir tarefas que vão além da comunicação.

---

## F. TECNOLOGIAS ALÉM-COMUNICAÇÃO (8:00 – 9:30)

Esta categoria é o destaque conceitual da seção — a verdadeira mudança de paradigma.

**Primeira: integração de comunicação, computação e caching — "i3C".** Projeto conjunto das três capacidades na borda, explorando sinergias. Computação e armazenamento viram **recursos de rede**, agendados como o espectro.

**Segunda — a estrela do grupo — integrated sensing and communication, ISAC.** [pausa]

Com o 6G, a rede **sente o ambiente enquanto comunica**. Antenas massivas, largas faixas de banda e implantações densas fazem da rede um gigante sensor distribuído. Aplicações: monitoramento ambiental, reconhecimento de gestos, monitoramento de saúde, e até "visão no escuro" — enxergar através de obstáculos em frequências THz. O artigo chama o ISAC de **tecnologia revolucionária**: a rede móvel deixa de ser só comunicação e passa a oferecer sensoriamento onipresente.

**Terceira: transferência de energia sem fio — WET.** Irradiar energia para alimentar dispositivos IoT leves — sensores sem bateria que coletam energia pelo ar.

**Transição:** Falando em energia — é exatamente a próxima categoria.

---

## G. TECNOLOGIAS CONSCIENTES DE ENERGIA (9:30 – 10:30)

Eficiência energética não é opcional no 6G — com redes mais densas e as demandas de potência do THz, é uma questão de vida ou morte. Três tecnologias:

**Redes verdes**: projeto eficiente em energia em todos os níveis — componentes, adaptação de enlace, gerenciamento de recursos, operação da rede — por razões ecológicas e econômicas.

**Energy harvesting**: dispositivos IoT de baixa potência coletando energia de fontes ambientes — solar, RF, movimento — viabilizando redes de sensores sustentáveis e autossuficientes.

**Backscatter communications**: a jogada extrema de baixo consumo. O dispositivo comunica **refletindo um sinal portador existente**, em vez de gerar o próprio. Combinada com a WET, permite tags e sensores que comunicam com **micro-watts** de consumo.

**Transição:** Esses dispositivos leves fazem parte de uma tendência maior — a explosão de dispositivos finais.

---

## H. COMUNICAÇÃO ORIENTADA A DISPOSITIVOS FINAIS (10:30 – 11:30)

Três tecnologias centradas em dispositivos:

**D2D — device-to-device.** Dispositivos próximos conversam **diretamente**, sem passar pela estação base. Descarrega a rede, reduz latência e suporta cenários do celular ao industrial e aéreo.

**V2X — vehicle-to-everything.** Habilitador-chave do transporte inteligente: veículo-para-veículo, para infraestrutura, para pedestres, para rede. Na era 6G, é a espinha dorsal dos **veículos autônomos conectados**.

**UAVs conectados à rede celular.** Drones atendidos pela — e voando dentro da — rede celular. Viabiliza aplicações aéreas, e a rede precisa também **lidar** com esses usuários aéreos, cuja mobilidade é genuinamente tridimensional.

**Transição:** Quando a rede toca todas essas indústrias, surge um novo modelo de serviço.

---

## I. TECNOLOGIAS ORIENTADAS A SERVIÇOS (11:30 – 12:00)

Uma tecnologia aqui: **redes privadas**.

Redes públicas atendem consumidores; redes privadas são sob medida para um **cliente vertical** — uma fábrica, um hospital, um porto. O 5G introduziu as non-public networks no Release 16, mas espera-se que o 6G as leve ao próximo nível com **desempenho extremo, IA pervasiva e sensoriamento integrado**. O artigo as posiciona como habilitador central da Indústria 4.0 e da penetração das redes móveis em todos os níveis da sociedade — além de uma grande **nova oportunidade de negócio** para operadoras.

---

## J. TECNOLOGIAS DE SEGURANÇA (12:00 – 13:00)

Última categoria — e não por acaso: se a sociedade depende do 6G, o 6G precisa ser **confiável**.

A tecnologia aqui é a **arquitetura holística de segurança de rede**. Os autores propõem uma abordagem em três fases:

Um — identificar o **cenário completo de ameaças**, em todas as camadas da rede, e mantê-lo atualizado.
Dois — desenvolver **soluções tecnológicas** para cada ameaça identificada.
Três — integrar tudo em uma **arquitetura abrangente** cobrindo segurança, privacidade e confiança.

Detalhe importante: o cenário de ameaças cresce com o próprio 6G — novas tecnologias como IA, redes não-terrestres e V2X criam **novas superfícies de ataque**. E o artigo faz uma observação interessante: IA/ML é uma **espada de dois gumes** — ferramenta poderosa de defesa, mas também novo alvo de ataques.

---

## FECHAMENTO (13:00 – 14:30)

Três conclusões da seção:

**Um — heterogeneidade é a filosofia de projeto.** Nenhuma tecnologia única define o 6G. Vinte e sete tecnologias em dez categorias — espectro do sub-6 ao THz e óptico, antenas que programam o ambiente, transmissão flexível, arquiteturas híbridas 3D, inteligência nativa, integração de sensoriamento e energia, projeto eficiente em energia, ecossistemas massivos de dispositivos, serviços privados e segurança.

**Dois — a maioria das peças já existe em forma inicial.** IAB, redes privadas, IA/ML na RAN — começaram no 5G-Advanced. O papel do 6G é torná-las pervasivas, integradas e extremas.

**Três — as maiores rupturas são conceituais.** O RIS transforma o ambiente em software. O ISAC transforma a rede em sensor. A IA pervasiva a torna um sistema autogerenciável. Por isso o artigo chama o 6G de *the intelligent network of everything*.

Obrigado — posso responder perguntas.

---

## Fatos de apoio (para o Q&A)

- Banda THz: 0,1–10 THz; janelas de transmissão acima do limite de absorção de ~800 GHz
- IEEE 802.15.3d-2017: primeiro padrão THz, ponto a ponto fixo em 252–321 GHz
- Faixas candidatas da WRC-2023 (>100 GHz): 102–109,5 · 151,5–164 · 167–174,8 · 209–226 · 252–275 GHz
- 5G FR2-1: 24,5–52,6 GHz (Rel-15); FR2-2: 52,7–71 GHz (Rel-17)
- Samsung 2021: 6,2 Gbit/s @ 140 GHz, 50 ft; LG 2022: enlace THz externo de 320 m @ 155–175 GHz; Nokia/NTT/Docomo 2023: 25 Gbit/s @ 144 GHz; Keysight 2023: >100 Gbit/s @ 300 GHz
- OWC: fotofone de Bell, 1880; FSO moderno: 13,16 Tbit/s em 10,45 km (2018)
- Evolução do core (paper, Seção IX-E.1): 2G circuit-switched → 3G/4G packet core → 5G cloud-native SBA/SDN/NFV/slicing (Rel-15) → 6G "cloud intelligence"
- Edge intelligence: 6 níveis (Figura 31 do paper)
- Interface aérea: 3 fases rumo à AI-native (Figura 32 do paper)
- Redes privadas no 5G: public-network-integrated e stand-alone NPN (Rel-16)
- Segurança 6G: 3 fases — identificação de ameaças → soluções por ameaça → arquitetura holística
- 27 tecnologias / 10 categorias — mesmo modelo de revisão para cada uma (visão, introdução, passado e presente, oportunidades e desafios, literatura e direções futuras)
# Documento de Estudo — Conteúdo e Cross-Referências por Slide
## Deck: `6G-Lit-Review-Proposta-v2-37-slides.pptx`
**Artigo-base:** H. Pennanen et al., *"6G: The Intelligent Network of Everything"*, IEEE Access, vol. 13, 2025, DOI: 10.1109/ACCESS.2024.3521579 (103 páginas, 600+ referências)

> Este documento não é um roteiro de fala — é o **material de leitura e preparação**. Para cada slide, explica o conteúdo em profundidade e traz **o texto real do artigo** (citações e paráfrases), não apenas a indicação de onde ele está.
>
> **Convenção de cross-referência:** `[§IX-E.1, p. 1373]` = Seção IX, subseção E.1, página impressa do artigo. Quando houver aspas, é **citação direta** do artigo (traduzida). `[Fig. 11]`/`[Tab. 4]` = figura/tabela do artigo.
>
> **Sobre as siglas:** toda sigla é explicada por extenso no próprio texto, na primeira vez em que aparece.

---

## MAPA DO ARTIGO → SLIDES

| Bloco do deck | Slides | Seção do artigo | Conteúdo |
|---|---|---|---|
| Abertura | 1–7 | §II (methodology), Capa | Artigo, proposta, RQs, método |
| Bloco 1 — Histórico | 8–13 | §I (Introduction) | 1G→6G + padronização |
| Bloco 2 — Fundamentos | 14–19 | §III, §IV, §X, §XI | Visão, elementos, 12 features, números |
| Bloco 3 — Arquitetura & core | 20–28 | §IX (D e E) | SAGIN, UDN, IAB, cell-free, inteligência |
| Bloco 4 — Aplicações | 29–32 | §V, §VI | 12 aplicações, 8 casos de uso |
| Proposta & encerramento | 33–37 | — | Grupo: cronograma, entregáveis |

### Estrutura completa do artigo (para navegação)
§I Introdução (histórico 1G→6G) · §II Artigo em detalhes · §III Visão 6G · §IV Elementos fundamentais · §V Aplicações disruptivas · §VI Casos de uso · §VII Requisitos de desempenho · §VIII IA/ML (Inteligência Artificial / aprendizado de máquina) para 6G · **§IX Tecnologias potenciais (27/10)** · §X Características definidoras · §XI 6G em resumo · §XII Visão 7G · §XIII Conclusão

---

# ABERTURA — SLIDES 1–7

---

## SLIDE 1 — Proposta de Lit Review

**O que dizer/conteúdo:** Apresentação da proposta de revisão de literatura para a disciplina RMSF (Redes Móveis Sem Fio, UFC), baseada no artigo de Pennanen et al.

**Cross-referência:** O artigo completo está em `6G_The_Intelligent_Network_of_Everything (1).pdf`. Os autores o descrevem como um documento que combina três funções: **"visão, survey e tutorial"** [§II, p. 1330]. Em outras palavras: ele apresenta uma visão de futuro (6G e até 7G), faz um levantamento (*survey*) da literatura (600+ referências) e ensina (*tutorial*) cada tecnologia passo a passo.

**Contexto importante:** Publicado na **IEEE Access** (IEEE = Institute of Electrical and Electronics Engineers, a maior sociedade profissional de engenharia elétrica/eletrônica do mundo), vol. 13 (2025). O **DOI** (Digital Object Identifier, o identificador permanente do documento) é 10.1109/ACCESS.2024.3521579. A época é o "auge da padronização": a Fase 2 do **IMT-2030** (International Mobile Telecommunications para 2030 — a "geração" 6G formal da ITU-R) começou em 2024 [§I-C, p. 1324].

---

## SLIDE 2 — Sumário: quatro blocos

**O que dizer/conteúdo:** A trilha da apresentação em quatro blocos temáticos, do histórico ao núcleo técnico.

**Cross-referência:** Os quatro blocos seguem a própria arquitetura do artigo: §I (histórico), §III/IV/X/XI (fundamentos), §IX (tecnologias), §V/VI (aplicações). O artigo é explicitamente estruturado para ser lido assim — a §II ("O artigo em detalhes") apresenta o conteúdo de cada seção, funcionando como um "mapa de leitura" interno.

**Nota para o apresentador:** O Bloco 3 (§IX) recebe ênfase deliberada: é o recorte técnico da revisão do grupo, conforme as **RQs** (Research Questions, questões de pesquisa) do slide 5.

---

## SLIDE 3 — Sobre o artigo-base

**O que dizer/conteúdo:** 103 páginas · vol. 13, IEEE Access 2025 · 600+ referências · 3 gêneros (visão, survey, tutorial).

**Cross-referência:** O "3 gêneros" vem de [§II-B, "Contributions of the article", linhas ~1168-1251]. Os autores declaram textualmente:
> **Visão** — "apresentamos uma visão 6G e, para situá-la num contexto mais amplo, esboçamos uma visão de 7G."
> **Survey** — "identificamos e revisamos 27 tecnologias 6G potenciais em 10 categorias tecnológicas... a nosso conhecimento, este é o conjunto mais abrangente de tecnologias 6G revisado em um único artigo."
> **Tutorial** — cada tecnologia é explicada no mesmo modelo: visão → introdução → passado/presente → oportunidades/desafios → literatura/direções futuras.

**Dado útil (Q&A):** Os autores também alegam que a visão de 7G é *"a primeira visão estruturada de 7G na literatura"* [§XII, p. 1401].

---

## SLIDE 4 — Objetivo desta proposta

**O que dizer/conteúdo:** O que o artigo entrega vs. o que o grupo propõe (4 blocos + busca estruturada guiada por 3 RQs).

**Cross-referência:** O resumo do slide é literalmente a estrutura do documento (§I→§XII). O trecho "esboço especulativo do 7G" está em [§XII, p. 1401-1402]: os autores escrevem que *"embora o 6G esteja em desenvolvimento e a anos da implantação, já podemos ver grandes tendências que evoluem além do 6G"* — e esboçam o que chamam de **"Deeply Intelligent Network of Hyperverses"** (a "Rede Profundamente Inteligente de Hiperversos").

---

## SLIDE 5 — Questões de pesquisa (RQ1, RQ2, RQ3)

**O que dizer/conteúdo:** As três **RQs** (Research Questions) que guiam a revisão.

**Cross-referência das bases (com o conteúdo real do artigo):**

- **RQ1 (core):** [§IX-E.1, p. 1373]. O artigo diz, textualmente: *"os core networks evoluíram da rede de comutação de circuitos do 2G, passando pelos packet cores de 3G e 4G, até a mais recente arquitetura baseada em software/serviços do 5G"* — e projeta o 6G como a passagem *"do cloud para cloud intelligence"*. É essa transição que a RQ1 investiga.
- **RQ2 (arquitetura):** [§IX-D, linhas 4690-5284]. As quatro arquiteturas estão lá: **INTN** (Integrated Non-Terrestrial and Terrestrial Networks) [4716], **UDN** (Ultra-Dense Networks) [4921], **IAB** (Integrated Access and Backhaul) [5034], **cell-free massive MIMO** [5132].
- **RQ3 (lacunas):** consolidação do grupo a partir dos surveys citados pelo artigo — segurança/privacidade [497], [645]–[658] e redes privadas/slicing [638]–[644]. A matriz de lacunas é **contribuição do grupo**, não está pronta no artigo.

---

## SLIDE 6 — Protocolo de busca e seleção

**O que dizer/conteúdo:** Kitchenham & Charters + **PRISMA 2020** · bases IEEE Xplore/Scopus/ACM DL · *snowballing* · período 2019–2026 · string "6G AND (core OR slicing) AND IA" · critérios de inclusão/exclusão · checklist de 5 critérios.

**Cross-referência (o que cada sigla significa):**

- **PRISMA** (Preferred Reporting Items for Systematic Reviews and Meta-Analyses): um padrão de relato para revisões sistemáticas, com um fluxograma de seleção de estudos (Page et al., 2021, BMJ 372:n71).
- **Kitchenham & Charters (2007)**: o guia clássico de revisão sistemática em Engenharia de Software (EBSE = Evidence-Based Software Engineering, Technical Report).
- ***Snowballing***: técnica de expandir a busca seguindo as referências dos artigos já selecionados (neste caso, as 600+ do artigo-base).

**Nota:** O período 2019–2026 vem da linha do tempo do artigo [§I-C]: 2019 = lançamento comercial do 5G (Rel-15); 2026 = final previsto do **Release 20** e da Fase 2 do IMT-2030 [p. 1324].

---

## SLIDE 7 — Fluxo PRISMA

**O que dizer/conteúdo:** As quatro etapas (identificação → triagem → elegibilidade → inclusão) e o registro dos números (n) no fluxograma final.

**Cross-referência:** Estrutura padrão do PRISMA 2020 (Page et al., 2021). O fluxo funciona assim: **identificação** (resultados brutos da busca), **triagem** (leitura de título/resumo), **elegibilidade** (leitura completa contra os critérios), **inclusão** (corpus final). Nenhuma seção do artigo cobre isso — é método do grupo.

---

# BLOCO 1 — HISTÓRICO (SLIDES 8–13) — Seção I do artigo

---

## SLIDE 8 — Divisória Bloco 1

**Conteúdo:** Panorama histórico das redes sem fio, de 1G a 6G, e o caminho até a padronização — a Seção I (p. 1320-1325).

**Contexto do artigo:** A §I tem uma tese central que vale guardar — a **"regra dos ciclos de duas gerações"**: *"as disrupções principais ocorrem em ciclos de duas gerações, isto é, 1G/2G, 3G/4G e 5G/6G. Nesse ciclo, a primeira geração introduz a nova disrupção, enquanto a segunda a faz explodir"* [§XII, p. 1401]. Exemplos do próprio artigo: *"1G introduziu a telefonia móvel, enquanto 2G libertou seu potencial. A internet móvel foi primeiramente habilitada pelo 3G e se tornou mainstream na era 4G. Atualmente, o 5G está introduzindo a mobile intelligence e espera-se que o 6G a leve ao próximo nível."*

---

## SLIDE 9 — 1G e 2G (anos 80–90)

**O que dizer/conteúdo:**

**1G (anos 80):** analógico, caro, limitado. O artigo diz: *"1G começou a revolução das comunicações pessoais sem fio, mas permaneceu limitado — analógico, apenas voz, caro e restrito."* Os sistemas eram regionais e incompatíveis entre si:
- **AMPS** (Advanced Mobile Phone System) — América do Norte
- **NMT** (Nordic Mobile Telephone) — países nórdicos
- **TACS** (Total Access Communication System) — Reino Unido

**2G (anos 90):** a digitalização. *"A disrupção real ocorreu nos anos 1990, quando as redes 2G foram introduzidas"* [linha 85]. O sistema dominante foi o **GSM** (Global System for Mobile Communications — o padrão europeu que se tornou mundial); alternativos: D-AMPS (AMPS digital) e **cdmaOne** na América do Norte, **PDC** (Personal Digital Cellular) no Japão.

**Por que foi a primeira grande disrupção:** *"o game changer foi a evolução do analógico para o digital, tornando os telefones acessíveis, pequenos e fáceis de carregar. As pessoas puderam ligar e enviar mensagens para qualquer pessoa em qualquer lugar."* [§I, ~90-95]

**Cross-referência:** [§I, subseções "1) 1G" e "2) 2G", p. 1320-1321].

---

## SLIDE 10 — 3G e 4G (anos 2000–2009)

**O que dizer/conteúdo:**

**3G (anos 2000):** acesso por **CDMA** (Code-Division Multiple Access — acesso múltiplo por divisão de código, que "permite uso mais eficiente do espectro"). O **turbo coding** "permitiu aos enlaces 3G se aproximarem do limite de capacidade de Shannon na prática". Sistemas: **CDMA2000** (América) e **UMTS** (Universal Mobile Telecommunications System, dominante no resto do mundo).

O ponto que o artigo destaca — e o slide ecoa — é que **a tecnologia sozinha não bastou**: *"a internet móvel não explodiu na fase inicial do 3G porque os telefones não tinham telas de toque, seus sistemas operacionais não eram otimizados para o uso móvel, e a maioria do conteúdo da internet não era otimizada para o telefone... tudo começou a mudar após o **iPhone** (2007-08)."* [§I, ~125-135]

**4G (2009):** troca de CDMA por **OFDM** (Orthogonal Frequency-Division Multiplexing — multiplexação por divisão de frequência ortogonal), escolhido "por sua robustez, flexibilidade e suporte direto a **MIMO** e receptores de menor complexidade". O sistema dominante foi o **LTE** (Long-Term Evolution — Evolução de Longo Prazo) do 3GPP, Release 8. O 4G foi *"o primeiro sistema em larga escala a explorar canais MIMO full-dimension"*. Evoluções: LTE-A (Rel-10) e LTE-A Pro (Rel-13), com *carrier aggregation*, **CoMP** (Coordinated Multipoint — transmissão/recepção coordenada entre múltiplas células) e *dual connectivity*.

**Sementes do futuro:** *"A evolução do LTE também introduziu suporte a comunicações **V2X** (Vehicle-to-Everything — veículo para tudo) e **MTC** (Machine-Type Communications — comunicação do tipo máquina)."* [§I, ~168]

**Cross-referência:** [§I, subseções "3) 3G" e "4) 4G", p. 1321].

---

## SLIDE 11 — 5G (2019 em diante)

**O que dizer/conteúdo:**

**5G Core:** **SBA** (Service-Based Architecture — arquitetura baseada em serviços), **SDN** (Software-Defined Networking — redes definidas por software), **NFV** (Network Function Virtualization — virtualização de funções de rede) e *network slicing* (fatiamento de rede) [§I, ~180]. Todos explicados em detalhe no slide 25.

**5G RAN** (Radio Access Network — rede de acesso por rádio): *mmWave* (ondas milimétricas), *massive MIMO* (MIMO massivo), *small cells* (células pequenas) [§I, ~180-185].

**Alcance vertical:** o artigo lista que o 5G *"também introduziu suporte a **NTNs** (Non-Terrestrial Networks — redes não-terrestres), **IAB** (Integrated Access and Backhaul — acesso e backhaul integrados), NR positioning, NR não-licenciado, UAS (sistemas aéreos não-tripulados) e NR V2X"* [§I, ~185-190].

**Ponto de virada — Release 18 (5G-Advanced):** *"o recurso mais disruptivo do Release 18 foi a introdução de inteligência artificial e aprendizado de máquina"* [§I, ~213]. Primeira vez que **IA/ML** entra formalmente nos padrões **3GPP** (3rd Generation Partnership Project — o consórcio que padroniza as redes móveis desde o 3G).

**Timeline dos releases 5G [§I-C, p. 1322]:** Rel-15 (2018) · Rel-16 (meados de 2020) · Rel-17 (Q1 2022) · Rel-18 (final de 2023) · Rel-19 (~meados de 2025).

**Cross-referência:** [§I, "5) 5G", p. 1321-1322].

---

## SLIDE 12 — 6G (~2029–2030)

**O que dizer/conteúdo:**

**Tecnologias-chave:** **THz** (terahertz — 0,1–10 THz), ultra-massive MIMO, **RIS** (Reconfigurable Intelligent Surface — superfície inteligente reconfigurável), **UDN** (Ultra-Dense Network — rede ultra-densa), **ISAC** (Integrated Sensing and Communication — sensoriamento e comunicação integrados) [§IX].

**Visão central:** 6G como *"the Intelligent Network of Everything"*. O artigo define a próxima disrupção como **mobile intelligence** (inteligência móvel): *"a fusão de tecnologias wireless, IA e IoE em todos os níveis da sociedade... tem o potencial de tornar qualquer coisa conectada, inteligente e consciente do ambiente ao redor."* [§III, "Big Picture", p. 1335]

**A fórmula do slide ("desempenho extremo + IA pervasiva + IoE + além-comunicação")** é a decomposição dos três elementos fundamentais da §IV:
- **Wireless** = comunicação + sensoriamento + posicionamento + energia
- **AI** = uso extensivo de IA em todos os níveis do ecossistema
- **IoE** (Internet of Everything — Internet de Tudo) = sensores, máquinas, veículos, drones, robôs

**Nota 7G (bônus):** [§XII, p. 1401]: *"prevemos que a próxima grande disrupção na era pós-6G será o hiperverso móvel habilitado por 7G/8G"*, sobre três pilares — **unlimited wireless** (wireless ilimitado), **DI** (Deep Intelligence — inteligência profunda) e **IoI** (Internet of Intelligence — Internet da Inteligência).

**Cross-referência:** [§III, p. 1335] + [§XII, p. 1401-1402].

---

## SLIDE 13 — Caminho até a padronização

**O que dizer/conteúdo:**

**ITU-R** (International Telecommunication Union — Radiocommunication Sector, a agência da ONU para radiocomunicações) e o **IMT-2030** [§I-C, p. 1323-1324]:

- **Fase 1 (2020–2023, concluída):** visão → culminou na **Rec. ITU-R M.2160-0** ("IMT-2030 Framework", nov/2023), que define tendências, cenários de uso e capacidades. O ITU-R define **15 capacidades de desempenho** nessa recomendação.
- **Fase 2 (2024–2026):** requisitos técnicos + metodologia de avaliação (relatórios "Technical Performance Requirements", "Evaluation Methodology", "Submission Template").
- **Fase 3 (2027–2030):** avaliação e seleção das **RITs** (Radio Interface Technologies — as interfaces de rádio candidatas, que o 3GPP e outros submetem).

**3GPP [§I-C, p. 1322-1324]:**

- **Release 20 (7/2025–12/2026):** *"o último release dominado pelo 5G, junto com os primeiros estudos sobre 6G"* — o artigo cita: *"está planejado que o Release 20 inicie o processo de padronização 6G, sendo o primeiro release a estudar features 6G."*
- **Release 21 (~2028):** *"esperado como o primeiro release a definir tecnologias 6G — assim, o primeiro padrão oficial 6G."* Preparação começa no início de 2027; submissão ao ITU-R como candidata IMT-2030.
- **Comercialização:** *"se o Release 21 for concluído em meados de 2028, as primeiras redes 6G comerciais podem ser lançadas já no final de 2028 a início de 2029."*

**Cross-referência:** [§I-C "Standardization activities", p. 1322-1324]. Slide factualmente denso — todos os números vêm dessa subseção.

---

# BLOCO 2 — FUNDAMENTOS (SLIDES 14–19) — Seções III, IV, X, XI

---

## SLIDE 14 — Divisória Bloco 2

**Conteúdo:** Fundamentos: três elementos (§IV), 12 características (§X), síntese (§XI).

**Contexto do artigo:** A §III ("6G Vision") é o mapa conceitual. O artigo se autodeclara "bem alinhado à visão do ITU-R, embora mais abrangente" [§III, p. 1335].

---

## SLIDE 15 — Elemento fundamental 1: Wireless

**O que dizer/conteúdo:**

**Wireless além da comunicação:** *"no contexto do 6G, wireless refere-se a uma variedade de tecnologias incluindo comunicação, sensoriamento, posicionamento e energia"* [§IV, p. 1336].

**As seis dimensões de desempenho:** *"capacity, latency, reliability, density, coverage, mobility"* (capacidade, latência, confiabilidade, densidade, cobertura, mobilidade) [§IV, ~1642] — *"seis dimensões principais de desempenho que precisam ser empurradas a níveis extremos"*. São as mesmas dimensões que o ITU-R lista como capacidades do IMT-2030.

**Dimensões adicionais:** eficiência energética e precisão de posicionamento [§X, ~7764].

**Consequência:** com as seis no extremo, o 6G suporta cenários hoje contraditórios na mesma rede — internet ultra-rápida, conectividade tempo-sensível, **IoT** (Internet of Things — Internet das Coisas) ultra-denso, cobertura global e hiper-mobilidade [§VI-A].

**Cross-referência:** [§IV "Wireless", p. 1336] + [§X, p. 1400].

---

## SLIDE 16 — Elementos 2 e 3: IA e Internet of Everything

**O que dizer/conteúdo:**

**IA pervasiva:** *"AI refere-se ao uso extensivo de IA em todos os níveis do ecossistema 6G — core da rede, bordas da rede, interface aérea, dispositivos, serviços e aplicações"* [§IV, p. 1336]. Não é um recurso adicional — é **elemento estrutural**.

**IoE:** *"um número massivo de objetos conectados à rede: sensores, dispositivos, máquinas, veículos, drones, robôs, etc."* [§III]. O foco muda **de humano para máquina/aplicação**.

**Por que os três juntos:** *"para prover uma grande disrupção, o 6G precisa se basear em três elementos profundos: wireless, AI e IoE"* [§III]. Wireless extremo conecta, IoE dá a escala de objetos, AI dá a inteligência.

**Aprofundamento:** a §VIII dedica uma seção inteira às técnicas de ML para 6G — **DL** (Deep Learning — aprendizado profundo, redes neurais), **FL** (Federated Learning — aprendizado federado, treino distribuído sem centralizar dados), **TL** (Transfer Learning — aprendizado por transferência, reuso de modelos).

**Cross-referência:** [§IV, p. 1336] + [§III, p. 1335] + [§VIII, p. 1345-1352].

---

## SLIDE 17 — O "101" do 6G · Parte 1 (pares 1–3)

**O que dizer/conteúdo:**

A §X identifica **12 características em 6 pares** [Fig. 50, p. 1400]. O artigo: *"nesta seção, identificamos 12 features principais que definem a essência do 6G."*

**Par 1 — Extreme Capacity and Performance** (capacidade e desempenho extremos): *"capacidade e desempenho extremos serão os pilares do 6G. Há seis dimensões de desempenho principais que precisam ser empurradas aos níveis extremos... outras dimensões importantes são eficiência energética e precisão de posicionamento."*

**Par 2 — Ultra-Flexible and Agile** (ultra-flexível e ágil): *"para se adaptar a uma ampla gama de ambientes sem fio e cenários de aplicação, o 6G será projetado para ser ultra-flexível e ágil. Flexibilidade e agilidade precisam ser otimizadas em todos os níveis da rede, do dispositivo e da comunicação aos níveis de rede e serviço."*

**Par 3 — Highly Intelligent and Aware** (altamente inteligente e consciente): *"o uso extensivo de IA/ML tornará o 6G altamente inteligente... além disso, espera-se que o 6G se torne consciente do ambiente ao redor através de network sensing (sensoriamento de rede)."* As tecnologias mais promissoras: **DL, FL, TL**.

**Cross-referência:** [§X, p. 1400, Fig. 50].

---

## SLIDE 18 — O "101" do 6G · Parte 2 (pares 4–6)

**O que dizer/conteúdo:**

**Par 4 — Ubiquitously Available and Reliable** (ubiquamente disponível e confiável): *"a chave para a disponibilidade ubíqua é a cobertura ampla, habilitada pela integração de redes terrestres e não-terrestres."* — a ponte direta para a **SAGIN** do Bloco 3. *"Confiabilidade deve ser maximizada em diferentes níveis de rede, de esquemas PHY robustos a mecanismos de nível de rede."*

**Par 5 — Truly Green and Sustainable** (verdadeiramente verde e sustentável): *"o 6G será projetado para greenness e sustentabilidade, aprimorando a eficiência energética em todos os níveis da rede, do core e das bordas aos protocolos MAC e PHY."*

**Par 6 — Thoroughly Secure and Trustworthy** (totalmente seguro e confiável): *"uma arquitetura de segurança de rede holística precisa ser desenvolvida para o 6G, levando em conta também privacidade e confiança."*

**Siglas usadas aqui:** **PHY** (Physical layer — camada física) e **MAC** (Medium Access Control — controle de acesso ao meio) são as duas camadas de rádio da interface aérea.

**Leitura dos pares:** pares 1–2 = *o que a rede faz*; pares 3–6 = *como a rede é*. Juntas, síntese qualitativa; o slide 19 é a síntese quantitativa.

**Cross-referência:** [§X, p. 1400-1401, Fig. 50].

---

## SLIDE 19 — 6G em números (síntese da visão)

**O que dizer/conteúdo:**

Os alvos numéricos vêm da **Rec. ITU-R M.2160-0** e são consolidados no artigo [Tab. 4, p. 1343; §VII, p. 1343-1345]. O ITU-R definiu **15 capacidades**, com alvos numéricos para **9**:

| Requisito | IMT-2030 (6G) | IMT-2020 (5G) | Literatura 6G |
|---|---|---|---|
| Taxa de pico | 50 / 100 / 200 Gbit/s | 20 Gbit/s | 1 Tbit/s |
| Taxa experimentada | 300 / 500 Mbit/s | 100 Mbit/s | — |
| Eficiência espectral de pico | 1,5× / 3× | — | — |
| Capacidade de área | 30 / 50 Mbit/s/m² | 10 Mbit/s/m² | — |
| Latência do plano de usuário | 0,1–1 ms | 1 ms | — |
| Confiabilidade | 10⁻⁵–10⁻⁷ | 10⁻⁵ | — |
| Densidade de conexões | 10⁶–10⁸/km² | 10⁶/km² | — |
| Mobilidade máxima | 500–1000 km/h | 500 km/h | — |
| Precisão de posicionamento | 1–10 cm | — | — |

**O que o artigo diz sobre cada (detalhe fino):**
- **Taxa de pico:** *"em IMT-2020, o pico-alvo é 20 Gbit/s. Os alvos do ITU-R para IMT-2030 são 50, 100 e 200 Gbit/s, dependendo do cenário de uso. Na literatura, a taxa-alvo mais comum para 6G é 1 Tbit/s."*
- **Taxa experimentada:** *"a taxa obtida por 95% dos usuários na área de cobertura... o ITU-R sugere 300 e 500 Mbit/s para IMT-2030."*
- **Confiabilidade:** o artigo nota que os valores "dependem do cenário", de 10⁻⁵ a 10⁻⁷ (de "cinco noves" a "sete noves").
- **Capacidades sem alvo:** o ITU-R não define alvos para 6 das 15 capacidades (energia, cobertura, resiliência etc.) por serem "difíceis de medir numericamente" [§VII, ~2444].

**Cross-referência:** [§XI, p. 1400] + [§VII + Tab. 4, p. 1343-1345].

---

# BLOCO 3 — ARQUITETURA, CORE E SLICING (SLIDES 20–28) — Seção IX (D e E)

---

## SLIDE 20 — Divisória Bloco 3

**Conteúdo:** Foco técnico principal: **Seção IX**, recorte nas famílias **D** (arquitetura) e **E** (inteligência), fio condutor do **slicing**.

**Contexto do artigo:** A §IX é a maior seção: **27 tecnologias em 10 categorias (A–J)**, cada uma no template *vision → introduction → past and present → opportunities and challenges → literature and future directions* [§IX, intro, ~2869-2908; Fig. 11].

**As 10 famílias (mapa completo, com cada tecnologia explicada):**

- **A — Espectro:** **THz** (comunicação em terahertz, de 0,1 a 10 THz — o espectro extremo para capacidade) e **OWC** (comunicação óptica sem fio, que usa luz visível e laser).
- **B — Antenas:** **ultra-massive MIMO** (centenas a milhares de antenas), **RIS** (superfície inteligente reconfigurável, que "programa" o ambiente de rádio refletindo sinais) e **holographic MIMO** (superfície com número quase contínuo de elementos).
- **C — Transmissão:** **multi-waveform** (formas de onda múltiplas e flexíveis), **modulação/codificação avançadas**, **NOMA** (acesso múltiplo não-ortogonal, que sobrepõe usuários no mesmo recurso) e **grant-free** (acesso sem concessão, em que o dispositivo transmite sem pedir autorização).
- **D — Arquitetura:** **INTN** (redes não-terrestres e terrestres integradas), **UDN** (redes ultra-densas), **IAB** (acesso e backhaul integrados) e **cell-free massive MIMO** (MIMO massivo sem célula fixa).
- **E — Inteligência:** **core inteligente**, **edge inteligente** e **interface aérea inteligente**.
- **F — Além-comunicação:** **i3C** (comunicação, computação e cache integrados), **ISAC** (sensoriamento e comunicação integrados) e **WET** (transferência de energia sem fio).
- **G — Energia:** **green networks** (redes verdes), **energy harvesting** (coleta de energia do ambiente) e **backscatter** (comunicação por reflexão de um sinal existente).
- **H — Dispositivos:** **D2D** (dispositivo-a-dispositivo), **V2X** (veículo-para-tudo) e **UAV celular** (drones conectados à rede).
- **I — Serviços:** **redes privadas**.
- **J — Segurança:** **arquitetura de segurança holística**.

---

## SLIDE 21 — Panorama da Seção IX

**O que dizer/conteúdo:** As 10 famílias A–J e o recorte do grupo (D + E).

**Justificativa do recorte (ligação com RQs):** D e E respondem diretamente RQ1 (core nativo em IA) e RQ2 (arquiteturas para slicing fim a fim). As demais entram como contexto: A/B sustentam a capacidade (THz/antenas), F sustenta os casos de uso além-comunicação (slide 32), G sustenta a feature "verde" (slide 18), J sustenta a feature "seguro" (slide 18).

**Figura-chave:** [Fig. 11, "Potential technologies for 6G", p. 1349] — o mapa visual das 27 tecnologias.

---

## SLIDE 22 — D · INTN / SAGIN

**O que dizer/conteúdo:**

**INTN** (Integrated Non-Terrestrial and Terrestrial Networks — redes não-terrestres e terrestres integradas) [§IX-D.1, linha 4716]: a integração espaço-ar-terra como uma só rede — a literatura chama de **SAGIN** (Space-Air-Ground Integrated Network — rede integrada espaço-ar-terra).

**As três camadas:**
- **Ground** (solo): redes móveis terrestres e estações terrenas — o grosso da capacidade.
- **Airborne** (aéreo): **HAPS** (High-Altitude Platform Stations — plataformas de alta altitude, tipo balões/dirigíveis na estratosfera) e **UAVs** (Unmanned Aerial Vehicles — veículos aéreos não-tripulados, drones).
- **Spaceborne** (espacial): satélites **LEO** (Low Earth Orbit — órbita baixa), **MEO** (Medium Earth Orbit — órbita média), **GEO** (Geostationary Earth Orbit — órbita geoestacionária).

**Visão do artigo [~4719]:** *"INTNs devem desempenhar um papel-chave no 6G, potencialmente fornecendo cobertura global e habilitando uma miríade de aplicações — de conectividade de alta velocidade em áreas remotas a IoT global e monitoramento ambiental/industrial em escala mundial."*

**Por que importa para o slicing (RQ2):** uma fatia fim a fim precisa atravessar as três camadas — e a orquestração nesse cenário 3D heterogêneo é uma das lacunas mapeadas (slide 28).

**Cross-referência:** [§IX-D.1, p. 1367-1369; Fig. 23 "Integrated space-air-ground network"; Tab. 9].

---

## SLIDE 23 — D · UDN, IAB e Cell-free

**O que dizer/conteúdo:**

**UDN** (Ultra-Dense Network — rede ultra-densa) [§IX-D.2, 4921]: densificação extrema de células. O artigo: *"UDNs são consideradas elemento-chave para atender às necessidades de capacidade extrema do 6G, especialmente via implantações densas de células THz."* Lógica: THz tem alcance curto (perdas de propagação altas) → células pequenas em quantidade massiva.

**IAB** (Integrated Access and Backhaul — acesso e backhaul integrados) [§IX-D.3, 5034]: a célula atende usuários **e** faz *backhaul* (o enlace que conecta a célula ao core) sem fio para as vizinhas. O artigo: *"enquanto o IAB já faz parte dos padrões 5G, seu papel no 6G crescerá devido à contínua densificação de células."* Elimina a fibra até cada célula.

**Cell-free massive MIMO** (MIMO massivo sem célula) [§IX-D.4, 5132]: o "fim da célula fixa". Muitos pontos de acesso (APs) distribuídos atendem cada usuário **de forma conjunta e cooperativa**, sem bordas de célula. *"Aplicável a cenários que exigem níveis estáveis de **QoS** (Quality of Service — qualidade de serviço) em toda a área de cobertura."*

**Síntese:** UDN = "onde está a capacidade"; IAB = "como conectar as células"; cell-free = "como garantir QoS uniforme". Juntas com a SAGIN, respondem à RQ2.

**Cross-referência:** [§IX-D.2/D.3/D.4, p. 1370-1372; Tab. 9].

---

## SLIDE 24 — E · Evolução do core, geração a geração

**O que dizer/conteúdo:**

A linha do tempo dos núcleos de rede [§IX-E.1, "Past and Present", ~5325-5345]:

- **2G:** core de **comutação de circuitos** (*circuit-switched*) — dedicado à voz; uma conexão dedicada por chamada.
- **3G/4G:** **packet core** (núcleo de pacotes) — dados em pacotes, a internet no celular.
- **5G:** core **cloud-native** (nativo em nuvem), *service-oriented*, definido pelo 3GPP no **Release 15**: *"as características principais do 5G Core incluem SBA, SDN, NFV e network slicing."*
- **6G:** *"evolução do cloud para **cloud intelligence**"* [~5304] — IA pervasiva no núcleo.

**Citação-chave (use na fala):** *"os core networks evoluíram da rede de comutação de circuitos do 2G, passando pelos packet cores de 3G e 4G, até a mais recente arquitetura baseada em software/serviços do 5G."* [~5333]

**Conexão RQ1:** é exatamente a transição 5G-cloud-native → 6G-AI-native que a revisão investiga.

**Cross-referência:** [§IX-E.1, p. 1373-1374].

---

## SLIDE 25 — E · O que o 5G já trouxe (SBA, SDN, NFV, slicing)

**O que dizer/conteúdo (agora com cada conceito explicado):**

**SBA — Service-Based Architecture (arquitetura baseada em serviços):** *"conta com uma vasta variedade de funções de rede interconectadas, cada uma provendo um ou mais serviços acessíveis por outras funções. Essa arquitetura permite a adição ágil de novas funcionalidades."* Na prática: em vez de um core monolítico, o 5G é um conjunto de funções especializadas que conversam entre si via APIs (interfaces de programação). Exemplos: a **AMF** (Access and Mobility Management Function — gerencia o acesso e a mobilidade do dispositivo), a **SMF** (Session Management Function — gerencia as sessões/serviços de dados), a **UPF** (User Plane Function — encaminha os pacotes de dados do usuário) e a **NSSF** (Network Slice Selection Function — seleciona a fatia de rede do usuário). Cada uma oferece um "serviço" que as outras consomem.

**SDN — Software-Defined Networking (redes definidas por software):** *"habilita gestão de rede flexível."* O princípio é **separar o plano de controle (o "cérebro", que decide as rotas) do plano de dados (que apenas encaminha os pacotes)**. Isso permite programar e reconfigurar a rede por software, sem mexer no hardware.

**NFV — Network Function Virtualization (virtualização de funções de rede):** transforma funções que antes exigiam aparelhos dedicados (firewall, roteador, gateway) em **software que roda em servidores comuns (commodity)**. Sem NFV não haveria slicing, porque as funções de cada fatia são instanciadas como software.

**Network Slicing (fatiamento de rede):** *"NFV e network slicing permitem a divisão dos recursos da rede em fatias virtuais independentes, cada uma podendo ser dedicada a um serviço específico. O slicing virtual facilita a introdução de novos serviços e soluções sob medida para o cliente."* Uma fatia **URLLC**, uma **eMBB**, uma **mMTC** (siglas no próximo parágrafo).

**Siglas das fatias (os 3 pilares do 5G):**
- **eMBB** = enhanced Mobile Broadband (banda larga móvel aprimorada)
- **URLLC** = Ultra-Reliable Low-Latency Communications (comunicações ultraconfiáveis de baixa latência)
- **mMTC** = massive Machine-Type Communications (comunicação massiva do tipo máquina)

**Ponto-chave:** no 5G, o slicing é **definido e orquestrado por regras humanas** (configuração estática/semi-estática). O salto 6G é torná-lo **dinâmico e autônomo** — daí nascem as lacunas da RQ3.

**Cross-referência:** [§IX-E.1, p. 1373] + [§I, "5G", p. 1321-1322].

---

## SLIDE 26 — E.1 · Intelligent Core

**O que dizer/conteúdo:**

**Visão [§IX-E.1, ~5301]:** *"no core network, o 6G irá além da softwarização do 5G adotando inteligência via IA/ML pervasiva — uma evolução do cloud para o cloud intelligence."*

**O que muda na prática:** IA/ML otimizando **operação, gestão e segurança** do núcleo de forma **autônoma** — autoconfiguração, autocura, otimização contínua. O core cloud-native *virtualizou* as funções; o core 6G as torna *inteligentes*.

**AI-native slicing:** a IA decide, dinamicamente, **como fatiar a rede** — conforme demanda, tráfego e contexto. É a síntese de RQ1 + RQ3: a autonomia é o objetivo (RQ1) e a origem das lacunas (RQ3 — explicabilidade, SLA, segurança, orquestração).

**Desafios listados pelo artigo [§IX-E.1, "Opportunities and Challenges"]:** aquisição de dados (datasets grandes e representativos), custo de treino/inferência, escalabilidade da IA/ML no núcleo, segurança do próprio modelo.

**Referência-chave citada pelo artigo:** [480] W. Zhuang, *"AI-native network slicing for 6G networks"* — explora "IA para slicing" (a IA otimiza as fatias) **e** "slicing para IA" (as fatias como veículo para oferecer IA como serviço).

**Cross-referência:** [§IX-E.1, p. 1373-1375; Tab. 10].

---

## SLIDE 27 — E.2–E.3 · Intelligent Edge e Intelligent Air Interface

**O que dizer/conteúdo:**

**Intelligent Edge [§IX-E.2, 5442]:** **EI** (Edge Intelligence — inteligência de borda) = *edge computing* (computação na borda, perto do usuário) **+ IA/ML**. O artigo define **seis níveis de EI** [Fig. 31, p. 1375]: do nível 1 (treino e inferência na nuvem — poder alto, custo de comunicação alto) ao nível 6 (tudo on-device — latência mínima, privacidade máxima, poder limitado). Os níveis intermediários distribuem partes do *pipeline* entre nuvem/borda/dispositivo.

**O trade-off central:** *latência × energia × privacidade × poder computacional*. Mover para a borda reduz latência e exposição de dados, mas limita o modelo; mover para a nuvem amplia capacidades, mas adiciona latência e tráfego.

**Intelligent Air Interface [§IX-E.3, 5613]:** a IA chega ao **PHY/MAC** (camada física/controle de acesso ao meio) em **três fases** [Fig. 32, p. 1377]:

1. **Fase 1:** IA/ML substitui **blocos individuais** — ex.: estimação de canal, demapeamento de símbolos.
2. **Fase 2:** IA/ML substitui **vários blocos projetados em conjunto** — ex.: estimação de canal + equalização + demapeamento como um único modelo.
3. **Fase 3:** IA/ML **desenha a interface aérea fim a fim** via aprendizado end-to-end — *"uma mudança de paradigma revolucionária no projeto de redes móveis, trazendo benefícios substanciais de desempenho e redução significativa da padronização."* [~5631]

**Por que é profundo:** hoje o PHY é um *pipeline* de blocos projetados separadamente com modelos matemáticos — o conjunto é subótimo, mas a otimização conjunta é *"matematicamente extremamente complexa"* para ferramentas convencionais [~5640]. O aprendizado fim a fim contorna essa barreira.

**Cross-referência:** [§IX-E.2, p. 1375-1377, Fig. 31] + [§IX-E.3, p. 1377-1378, Fig. 32] + [§VIII sobre DL/FL/TL].

---

## SLIDE 28 — RQ3 · Lacunas do slicing autônomo

**O que dizer/conteúdo:**

As quatro lacunas (consolidação do grupo):

1. **Explicabilidade (explainability):** se a IA decide as fatias, as decisões precisam ser **auditáveis** — por que o modelo realocou recursos? Como corrigir erros? Sem explicabilidade, não há confiança regulatória nem operacional.
2. **Garantia de SLA** (Service Level Agreement — acordo de nível de serviço): isolamento e estabilidade entre fatias sob **reconfiguração contínua** — a fatia A pode degradar a fatia B?
3. **Segurança do modelo:** envenenamento de dados (*data poisoning*), ataques adversariais — a IA que controla a fatia vira **alvo**. O artigo nota: *"IA/ML pode ser vista como uma espada de dois gumes"* [§IX-J, ~7730] — ferramenta de defesa e vetor de ataque.
4. **Orquestração fim a fim:** fatias atravessando **RAN, transporte, core e SAGIN** — nenhum trabalho ainda orquestrou fatias de ponta a ponta nesse cenário 3D heterogêneo.

**Base no artigo:** as lacunas não estão prontas no artigo — emergem da leitura cruzada de [§IX-E.1 (desafios da IA no core)] + [§IX-J (segurança)] + [§IX-D (complexidade SAGIN)] + surveys [497], [645]-[658], [638]-[644]. **A matriz de lacunas é a contribuição original do grupo** — deixe isso claro.

**Cross-referência:** [§IX-E.1 + §IX-J + §IX-D; refs. 497, 638-658].

---

# BLOCO 4 — APLICAÇÕES E CASOS DE USO (SLIDES 29–32) — Seções V e VI

---

## SLIDE 29 — Divisória Bloco 4

**Conteúdo:** O "para quê" do 6G: Seções V (aplicações disruptivas) e VI (casos de uso). Cada aplicação empurra ao extremo uma dimensão diferente — justificando os requisitos do slide 19 e as tecnologias do Bloco 3.

---

## SLIDE 30 — Aplicações disruptivas (12 em 3 categorias)

**O que dizer/conteúdo:**

[§V, p. 1338-1342; Fig. 8] — **12 aplicações em 3 categorias**:

**1. Interações humano-máquina [§V-A]:**
- **Metaverso** [V-A.1]: *"espaço virtual compartilhado gerado por computador... um ecossistema virtual totalmente imersivo, interoperável e hiper-espaço-temporal, fundindo os mundos físico, humano e digital."* Evolução em 3 fases: *digital twins → digital natives → surreality*. Estado atual: *"ainda em sua infância."*
- **XR** (Extended Reality — realidade estendida) [V-A.2]: guarda-chuva de **VR** (Virtual Reality — tudo virtual), **AR** (Augmented Reality — virtual sobre o real) e **MR** (Mixed Reality — mistura dos dois).
- **Comunicação holográfica** [V-A.3]: telepresença 3D volumétrica — demanda taxas enormes (liga ao THz e ao alvo de 1 Tbit/s).
- **Gêmeos digitais** (*Digital Twins*) [V-A.4]: réplica virtual sincronizada de objetos/sistemas físicos.
- **Internet tátil** (*Tactile Internet*) [V-A.5]: comunicação de toque/força remota — latência ~sub-ms, confiabilidade extrema.

**2. Ambientes inteligentes [§V-B]:** *"entidade em que tecnologias avançadas (5G/6G, AI/ML, IoT/IoE, cloud/edge) são exploradas para produzir maior valor."*
- **Smart society** (sociedade inteligente) [V-B.1] · **Smart city** (cidade) [V-B.2] · **Smart factory** (fábrica — conecta com redes privadas §IX-I) [V-B.3] · **Smart home** (casa) [V-B.4].

**3. Sistemas autônomos conectados [§V-C]:** *"tais sistemas estabelecem requisitos de desempenho rigorosos para o 6G, particularmente em confiabilidade, disponibilidade, latência e mobilidade."*
- **CAVs** (Connected Autonomous Vehicles — veículos autônomos conectados) [V-C.1] · **UAVs** autônomos [V-C.2] · **sistemas robóticos autônomos** [V-C.3].

**Cross-referência:** [§V, p. 1338-1342; Fig. 6 e Fig. 8].

---

## SLIDE 31 — Casos de uso orientados à comunicação (5)

**O que dizer/conteúdo:**

[§VI-A, p. 1342-1343; Fig. 9; Tab. 3] — cinco casos cobrindo as seis dimensões:

1. **Ultra-Broadband Multimedia Communications:** extensão do **eMBB** — conteúdo imersivo multissensorial (XR, holografia, *information showers*) "de hotspots densos a áreas rurais esparsas". O artigo alerta: os requisitos **conflitam** entre si — *"atingir esses requisitos simultaneamente é um trade-off específico de aplicação."*
2. **Extreme Time-Sensitive and Mission-Critical Communications:** extensão do **URLLC** — fábricas, hospitais, veículos autônomos. Habilitadores: diversidade de rede/enlace, altas taxas de codificação, modulações robustas, retransmissão avançada.
3. **Ultra-Massive Communications:** extensão do **mMTC** — até 10⁸ conexões/km².
4. **Global-Scale Communications:** terrestre + não-terrestre — a **SAGIN** como caso de uso.
5. **Hyper-Mobility Communications:** até 500–1000 km/h — trens-bala, aeronaves.

**Ponto estruturante:** cada caso empurra ao extremo **uma ou duas das seis dimensões** do slide 15 — juntos, cobrem todas.

**Cross-referência:** [§VI-A, p. 1342-1343; Fig. 9; Tab. 3].

---

## SLIDE 32 — Casos de uso além-comunicação (3)

**O que dizer/conteúdo:**

[§VI-B, p. 1343-1344; Tab. 3] — três casos **sem equivalente no 5G**:

1. **Network Intelligence (inteligência de rede):** *"fornecer serviços e aplicações inteligentes assistidos por IA/ML — intelligence as a service, sistemas inteligentes assistidos por rede (indústria, transporte, saúde), offloading de computação e edge caching."* Habilitador: a infraestrutura **i3C** (Integrated Communication, Computation, and Caching — comunicação, computação e cache integrados) da §IX-F.
2. **Network Sensing (sensoriamento de rede):** *"expandir as capacidades das redes celulares para sensoriamento e posicionamento."* Exemplos do artigo: detectar vazamento de gás numa fábrica; detectar queda de idoso com chamada automática. Habilitador: **ISAC** (§IX-F.2).
3. **Network Energy (energia de rede):** *"suportar serviços de transferência de energia sem fio (**WET** — Wireless Energy Transfer) para alimentar nós de rede — sensores IoT e dispositivos de baixa potência."* Habilitador: **energy beamforming** (direcionamento do feixe de energia); desafios: eficiência e alcance.

**Mensagem-síntese:** a rede deixa de ser um "tubo de bits" e vira **plataforma de capacidades** — computar, sentir, energizar.

**Cross-referência:** [§VI-B, p. 1343-1344] + [§IX-F (i3C, ISAC, WET), p. 1379-1384].

---

# PROPOSTA E ENCERRAMENTO (SLIDES 33–37)

---

## SLIDE 33 — Como conduziremos a Lit Review

**Conteúdo (do grupo):** síntese temática por bloco guiada pelas RQs · corpus = artigo-base + estudos do protocolo · matriz de lacunas em slicing autônomo (RQ3) · entregável: artigo de revisão, estrutura RMSF, ênfase em arquitetura e core (Bloco 3) · PRISMA documentado · conexão fundamentos → arquitetura → aplicações.

**Q&A provável:** "Por que ênfase em arquitetura e core?" — porque é onde a transição 5G→6G é mais profunda (softwarização → inteligência nativa) e onde as lacunas do slicing autônomo estão concentradas.

---

## SLIDE 34 — Cronograma (11 semanas)

**Conteúdo (do grupo):** Semanas 1–2 protocolo/busca · 3–4 triagem/elegibilidade · 5–6 extração/síntese · 7–8 redação Blocos 1, 2 e 4 · 9–10 Bloco 3 + lacunas · 11 revisão cruzada, PRISMA e entrega.

**Q&A provável:** "Por que o Bloco 3 no fim?" — porque é o núcleo técnico: depende do contexto dos blocos anteriores e concentra as respostas às RQs.

---

## SLIDE 35 — Divisão de responsabilidades

**Conteúdo (do grupo):** Anderson → Bloco 1 (histórico/padronização) · Beloin → Bloco 2 (fundamentos/features/requisitos) · Emanuel → Bloco 3 (core/slicing/lacunas RQ3) · Hywre → Bloco 4 (aplicações/casos de uso/revisão final). Busca e triagem em pares.

---

## SLIDE 36 — Literatura complementar

**Conteúdo:** cinco referências de partida:

**Método:**
- Kitchenham & Charters (2007) — guia de revisão sistemática em Eng. de Software.
- Page et al. (2021) — o PRISMA 2020 (padrão de relato).

**Visão 6G:**
- **ITU-R M.2160-0 (2023)** — o framework oficial do IMT-2030 [ref. 20 do artigo].
- Saad, Bennis & Chen (2020) — *A Vision of 6G Wireless Systems*, IEEE Network 34(3).
- Letaief et al. (2019) — *The Roadmap to 6G: AI Empowered Wireless Networks*, IEEE Commun. Mag. 57(8).

**Q&A provável:** "Por que essas cinco?" — duas sustentam o método; três sustentam a visão (o framework oficial + os dois artigos seminais que o artigo-base cita extensivamente).

---

## SLIDE 37 — Encerramento

**Conteúdo:** referência completa (Pennanen et al., IEEE Access vol. 13, 2025, DOI: 10.1109/ACCESS.2024.3521579) · agradecimento · abertura para perguntas.

---

# APÊNDICE — FATOS DE APOIO CONSOLIDADOS (Q&A)

## A. Linha do tempo (datas exatas do artigo)

| Evento | Data | Ref. |
|---|---|---|
| Rel-15 (primeiro padrão 5G) | final de 2018 / comercial 1º sem. 2019 | §I-C |
| Rel-16 | meados de 2020 | §I-C |
| Rel-17 | Q1 2022 | §I-C |
| Rel-18 (5G-Advanced, IA/ML) | final de 2023 | §I-C |
| Rel-19 | ~meados de 2025 | §I-C |
| Rel-20 (primeiros estudos 6G) | 7/2025–12/2026 | §I-C |
| Rel-21 (primeiro padrão 6G) | prep. início 2027, conclusão ~meados 2028 | §I-C |
| Redes 6G comerciais | ~final 2028–2030 | §I-C |
| ITU-R Fase 1 (visão IMT-2030) | 2020–2023 (Rec. M.2160-0, nov/2023) | §I-C |
| ITU-R Fase 2 (requisitos + metodologia) | 2024–2026 | §I-C |
| ITU-R Fase 3 (avaliação/seleção) | 2027–2030 | §I-C |

## B. Alvos IMT-2030 (detalhado — §VII + Tab. 4)

Pico 50/100/200 Gbit/s (5G: 20) · experimentada 300/500 Mbit/s (5G: 100) · eficiência espectral pico 1,5×/3× · área 30/50 Mbit/s/m² (5G: 10) · latência do plano de usuário (UP = *user plane*, a via de dados de fato usada pelo usuário) 0,1–1 ms (5G: 1 ms) · confiabilidade 10⁻⁵–10⁻⁷ · densidade 10⁶–10⁸/km² (5G: 10⁶) · mobilidade 500–1000 km/h · posicionamento 1–10 cm. O ITU-R definiu **15 capacidades**, com alvos para 9; a literatura 6G fala em **1 Tbit/s** de pico.

## C. Seção IX completa (27 tecnologias, explicadas)

**A — Espectro.** A comunicação em **terahertz (THz)** opera de 0,1 a 10 THz, com espectro imenso para capacidade extrema — demos da indústria: Samsung 6,2 Gbit/s @140 GHz em 50 ft, LG 320 m @155–175 GHz, Nokia/NTT 25 Gbit/s @144 GHz, Keysight >100 Gbit/s @300 GHz; a WRC-2023 reservou cinco faixas acima de 100 GHz; o IEEE 802.15.3d-2017 é o primeiro padrão THz. A **comunicação óptica sem fio (OWC)** usa luz — **VLC** (luz visível) em ambientes internos e **FSO** (laser em espaço livre) em enlaces longos (13,16 Tbit/s @10,45 km, 2018).

**B — Antenas.** O **ultra-massive MIMO** usa centenas/milhares de antenas para compensar as perdas do THz. A **superfície inteligente reconfigurável (RIS)** reflete e redireciona sinais com elementos passivos, "programando" o ambiente. O **holographic MIMO (HMIMO)** leva isso ao limite, com superfícies quase contínuas (4 modos de operação).

**C — Transmissão.** O **multi-waveform** adapta a forma de onda à banda. As **modulação e codificação avançadas** otimizam a camada física. O **NOMA** (acesso múltiplo não-ortogonal) sobrepõe usuários no mesmo recurso para ganhar eficiência espectral. O **grant-free** permite transmitir sem solicitar concessão — essencial no IoT massivo.

**D — Arquitetura.** **INTN/SAGIN** integra espaço-ar-terra. A **UDN** densifica células. O **IAB** faz acesso e backhaul no mesmo enlace. O **cell-free massive MIMO** elimina as bordas de célula com pontos de acesso cooperativos.

**E — Inteligência.** O **core inteligente** põe IA no núcleo. A **edge inteligente** combina computação de borda com IA (6 níveis). A **interface aérea inteligente** aplica IA ao PHY/MAC (3 fases).

**F — Além-comunicação.** O **i3C** integra comunicação, computação e cache. O **ISAC** funde sensoriamento e comunicação. A **WET** transfere energia sem fio.

**G — Energia.** **Green networks** buscam eficiência; **energy harvesting** coleta energia do ambiente; **backscatter** comunica refletindo um sinal existente (consumo de micro-watts).

**H — Dispositivos.** **D2D** é comunicação direta entre dispositivos; **V2X** é veículo-para-tudo; **UAV celular** conecta drones à rede.

**I — Serviços.** **Redes privadas** (no 3GPP Rel-16: PNI-NPN, integrada à pública, e SNPN, autônoma) servem verticais como a indústria 4.0.

**J — Segurança.** A **arquitetura de segurança holística** (3 fases: mapear ameaças → criar soluções → integrar tudo), com a IA como "espada de dois gumes".

## D. Metodologia AI/ML (§VIII)

O artigo dedica a §VIII às três técnicas de aprendizado de máquina mais promissoras para o 6G. **DL** (Deep Learning — aprendizado profundo) usa redes neurais com muitas camadas, sendo a técnica dominante para a camada física e otimização de rede. **FL** (Federated Learning — aprendizado federado) treina modelos distribuídos sem centralizar os dados dos usuários, preservando a privacidade. **TL** (Transfer Learning — aprendizado por transferência) reaproveita o conhecimento de um domínio em outro, reduzindo o custo de treino. [Tab. 5, Fig. 10]

## E. Visão 7G (§XII — bônus)

**Ciclos de duas gerações:** 1G introduz telefonia móvel / 2G a explodiu; 3G habilita internet móvel / 4G a popularizou; 5G introduz mobile intelligence / 6G a tornará pervasiva. Próxima disrupção: **7G/8G mobile hyperverse** — pilares **unlimited wireless + DI + IoI**. Visão: *"Deeply Intelligent Network of Hyperverses"* — *"a primeira visão estruturada de 7G na literatura."* [§XII, p. 1401-1402; Tab. 16]

---

*Documento de estudo gerado a partir da leitura integral do artigo (103 p., via extração de texto) e do deck de 37 slides. As citações entre aspas são traduções diretas do artigo Pennanen et al. 2025.*

---

# APÊNDICE G — PRIMER: O QUE É NETWORK SLICING (leia antes do Bloco 3)

O slicing é o fio condutor do trabalho — aqui está a base conceitual completa, com fontes da sua própria pasta.

### G.1 Definição formal

> *"Network Slicing (NS) pode ser simplificado à ideia de dividir uma única rede física em múltiplas redes lógicas autocontidas"* — 5G Network Slice: A URLLC Resource Allocation Perspective (PDF local, §I).

> *"Uma fatia de rede (network slice) é uma rede lógica fim a fim, implantada com recursos virtuais isolados sobre a infraestrutura física compartilhada"* — Sensors 2022, 22, 6724 (PDF local, §1).

**Em uma frase:** o operador pega a mesma infraestrutura física (antenas, fibra, servidores, espectro) e cria, por software, várias **redes virtuais fim a fim**, cada uma sob medida para um serviço.

### G.2 Analogias

Com a **computação em nuvem**: assim como o IaaS compartilha servidores entre inquilinos (*tenants*), o slicing compartilha infraestrutura entre serviços. Modelos cunhados: Network-as-a-Service (NaaS) e **Slice-as-a-Service (SlaaS)** [URLLC PDF]. Outra analogia: um prédio (infraestrutura) com apartamentos independentes (fatias) — paredes próprias (isolamento), mesmo terreno.

### G.3 Por que existe (o problema do "one-size-fits-all")

Os três pilares do 5G têm requisitos **conflitantes** [§VI-A]:

| Serviço | Requisito dominante |
|---|---|
| eMBB (banda larga) | capacidade altíssima |
| URLLC (crítico) | latência ~ms, confiabilidade extrema |
| mMTC (IoT massivo) | densidade 10⁶/km², dispositivos baratos |

Não há uma rede ótima para os três ao mesmo tempo; antes do slicing, eram redes físicas paralelas (caras). O slicing resolve: **uma infraestrutura, fatias especializadas**.

### G.4 Como funciona (a tríade SBA/SDN/NFV)

O slicing só é possível porque o core 5G foi softwarizado [§IX-E.1]:
- **SDN** separa controle e dados — o "cérebro" programável.
- **NFV** transforma funções de rede em **software** em servidor comum — cada fatia instancia as suas.
- **SBA** organiza o core como funções de serviço interconectadas.

**Componentes 3GPP:** a **NSSF** (Network Slice Selection Function — a função que escolhe em qual fatia o usuário será atendido), a **NSSS** (o procedimento de seleção de fatia executado no registro do dispositivo) e o ciclo de vida da fatia — preparação → ativação → desativação — gerenciado pelo operador através do **OSS** (Operations Support System — o sistema de suporte à operação da rede).

### G.5 Propriedades essenciais

1. **Isolamento:** o que acontece numa fatia (carga, falha, ataque) não pode degradar as outras — a mais crítica e difícil.
2. **Fim a fim:** a fatia atravessa dispositivo → RAN → transporte → core → nuvem.
3. **Customização:** cada fatia tem seus KPIs/SLA contratados.
4. **Elasticidade:** recursos alocados dinamicamente conforme a demanda.

### G.6 Evolução 5G → 6G

| Aspecto | Slicing 5G (hoje) | AI-native slicing 6G (proposto) |
|---|---|---|
| Decisão | Regras humanas, estática/semi-estática | **A própria IA decide**, dinamicamente [§IX-E.1; ref. 480] |
| Ciclo de vida | Provisionamento lento (horas/dias) | Autoprovisionamento em tempo real |
| Garantia de SLA | Contratos estáticos | Monitoramento preditivo + autoajuste |
| Orquestração | RAN + core terrestre | **Fim a fim via SAGIN** |
| Limitação | Escala e rigidez | Explicabilidade, segurança do modelo (RQ3) |

Referência-chave: **[480] "AI-native network slicing for 6G networks"** (W. Zhuang) — "IA para slicing" e "slicing para IA".

### G.7 Onde o slicing aparece

| Onde | Papel |
|---|---|
| Slides 5, 28, 33 | RQ2, RQ3, matriz de lacunas |
| Slide 25 [§IX-E.1] | Origem: NFV + slicing (Rel-15) |
| Slide 26 [§IX-E.1, ref. 480] | Salto: AI-native slicing |
| Slide 22 [§IX-D.1] | Desafio: fatias via SAGIN |
| Slide 32 [§VI-B] | Fatias servindo "Network Intelligence" |
| PDFs locais | Definições formais de fatia URLLC |

### G.8 Perguntas prováveis de banca

- **"Fatia vs VLAN/VPN?"** — VLAN/VPN segmentam um único domínio (L2/L3); a fatia é **fim a fim**, multi-domínio, com SLA e recursos orquestrados por software.
- **"Slicing é 4G?"** — virtualização existia, mas o slicing fim a fim **nasce no 5G** (Rel-15, SBA/NFV) [§IX-E.1].
- **"Estado no 6G?"** — propostas de AI-native slicing [480, 481]; sem solução: explicabilidade, SLA, segurança do modelo, orquestração E2E com SAGIN (as 4 lacunas da RQ3).
- **"Onde está no artigo-base?"** — §IX-E.1 (visão/desafios), §I (5G Core), §VI-B (inteligência como serviço); refs. [480]/[481].

# Roteiro de Apresentação — 6G: The Intelligent Network of Everything
## Deck completo: `6G-Lit-Review-Proposta-v2-37-slides.pptx` (37 slides)
Artigo-base: H. Pennanen et al., *6G: The Intelligent Network of Everything*, IEEE Access, vol. 13, 2025, DOI: 10.1109/ACCESS.2024.3521579

Duração alvo: **~25 minutos** · Locutores marcados conforme o slide 35 (divisão por blocos)
Estimativa por slide: ~35–40 s em média; abertura, Bloco 3 e lacunas (RQ3) respiram mais.

---

## Plano de tempo e locutores

| Tempo    | Slides | Parte                          | Locutor           |
|----------|--------|--------------------------------|-------------------|
| 0:00–2:00| 1–7    | Abertura, método e RQs          | Definido pelo grupo |
| 2:00–7:30| 8–13   | Bloco 1 · Histórico (Seção I)   | ANDERSON          |
| 7:30–12:00| 14–19 | Bloco 2 · Fundamentos (IV, X, XI)| BELOIN          |
| 12:00–19:30| 20–28 | Bloco 3 · Arquitetura & core (IX)| EMANUEL        |
| 19:30–23:30| 29–32 | Bloco 4 · Aplicações (V, VI)   | HYWRE            |
| 23:30–25:00| 33–37 | Proposta e encerramento         | Definido pelo grupo |

---

# ABERTURA (0:00 – 2:00) — slides 1 a 7

---

## SLIDE 1 — TÍTULO (0:00 – 0:20)

Bom dia / boa tarde. Nós somos o grupo da disciplina **Redes Móveis Sem Fio**, da UFC, e apresentamos hoje a nossa **proposta de revisão de literatura**.

O ponto de partida é o artigo de **Pennanen e colegas**, publicado na IEEE Access em 2025, com o título *"6G: The Intelligent Network of Everything"* — a Rede Inteligente de Tudo. É um survey-tutorial abrangente, escrito no auge da fase de padronização do 6G, e é a partir dele que construímos toda a estrutura do nosso trabalho.

---

## SLIDE 2 — SUMÁRIO (0:20 – 0:40)

A apresentação segue **quatro blocos**:

**Bloco 1** — o panorama histórico, da Seção I do artigo: de 1G a 6G.
**Bloco 2** — os fundamentos do 6G: Seções IV, X e XI — os elementos básicos, as características definidoras e os requisitos-alvo.
**Bloco 3** — arquitetura e core: a Seção IX, que é o **foco técnico principal** da nossa revisão.
**Bloco 4** — aplicações e casos de uso: Seções V e VI.

A trilha vai do histórico ao núcleo técnico, e cada bloco vira uma seção do nosso artigo de revisão.

---

## SLIDE 3 — SOBRE O ARTIGO-BASE (0:40 – 1:00)

Por que este artigo? Três números explicam a escolha:

**103 páginas** — é praticamente um livro sobre 6G.
**Mais de 600 referências** citadas — cobertura amplíssima da literatura.
E **3 gêneros em um só texto** — o artigo combina visão, survey e tutorial ao mesmo tempo.

Ou seja: não é apenas um artigo que lista tecnologias — é um documento de referência que combina visão de futuro, mapeamento do estado da arte e tutorial técnico.

---

## SLIDE 4 — OBJETIVO DESTA PROPOSTA (1:00 – 1:20)

O que o artigo entrega: ele reconstrói a evolução 1G até 6G, define os elementos fundamentais, as aplicações, os casos de uso, os requisitos — e um catálogo tutorial de tecnologias, encerrando com um esboço especulativo do 7G.

O que **nós propomos**: extrair quatro blocos temáticos das seções do artigo, com ênfase em **arquitetura e núcleo de rede** — e ampliá-los com uma **busca estruturada na literatura complementar**, guiada por três questões de pesquisa.

---

## SLIDE 5 — QUESTÕES DE PESQUISA (1:20 – 1:45)

Essas são as três perguntas que guiam a busca, a seleção e a síntese do nosso trabalho:

**RQ1 — Estado da arte do core**: como a literatura descreve a transição do core 5G cloud-native — SBA, SDN, NFV — para um core 6G **nativo em IA**?

**RQ2 — Arquitetura integrada**: quais arquiteturas — SAGIN, UDN, IAB, cell-free — são propostas para suportar **slicing fim a fim** no 6G?

**RQ3 — Lacunas em aberto**: quais desafios seguem sem solução no **slicing autônomo** — explicabilidade, SLA, segurança e orquestração?

Guardem essas três siglas — elas voltam no Bloco 3.

---

## SLIDE 6 — PROTOCOLO DE BUSCA E SELEÇÃO (1:45 – 2:00)

Nosso método segue o protocolo de **Kitchenham & Charters**, com o fluxo do **PRISMA 2020**.

Na **busca**: bases IEEE Xplore, Scopus e ACM DL, mais *snowballing* sobre as mais de 600 referências do artigo-base. Período 2019 a 2026, inglês e português — do lançamento do 5G à fase 2 do IMT-2030. A string resume-se a: **6G E (core OU slicing) E IA**.

Na **seleção**: inclusão de estudos revisados por pares sobre arquitetura, core ou slicing no contexto 6G; exclusão do que é só PHY/antenas, duplicatas e textos sem revisão; e um checklist de qualidade de 5 critérios — método claro, avaliação, reprodutibilidade e aderência às RQs.

---

## SLIDE 7 — FLUXO PRISMA (transição rápida)

O fluxo tem quatro etapas: **identificação** — busca mais snowballing; **triagem** — título e resumo, com dois revisores por artigo; **elegibilidade** — texto completo contra os critérios e o checklist; e **inclusão** no corpus final. Os números de cada etapa serão registrados no fluxograma PRISMA do artigo final.

Com o método definido, vamos ao conteúdo. **Anderson, o histórico.**

---

# BLOCO 1 · PANORAMA HISTÓRICO (2:00 – 7:30) — slides 8 a 13 — ANDERSON

---

## SLIDE 8 — DIVISÓRIA DO BLOCO 1 (2:00 – 2:15)

Obrigado. O Bloco 1 cobre a **Seção I** do artigo: a evolução das redes sem fio de 1G a 6G — e o caminho até a padronização. É a história de quatro disrupções, uma por geração de onda tecnológica.

---

## SLIDE 9 — 1G E 2G (2:15 – 3:15)

Anos 80: nasce o **1G** — analógico, caro e limitado. Eram sistemas regionais — o **AMPS** na América do Norte, o **NMT** nórdico, o **TACS** britânico. Disrupção modesta: a telefonia móvel existia, mas era de poucos.

Anos 90: o **2G** digitaliza tudo com o **GSM** — dominante na Europa e depois no mundo; na América, D-AMPS e cdmaOne; no Japão, PDC. O game-changer foi a evolução **do analógico para o digital**: transceptores menores, mais eficientes e baratos — o celular coube no bolso.

E aqui ocorre a **primeira grande disrupção real de mercado**: com SMS e alta penetração, as pessoas passam a **ligar e enviar mensagens para qualquer lugar**. A telefonia móvel vira parte do cotidiano.

---

## SLIDE 10 — 3G E 4G (3:15 – 4:15)

Anos 2000: o **3G** leva a internet ao celular — **CDMA** e **UMTS**, turbo coding aproximando o limite de Shannon. Mas reparem no detalhe que o artigo destaca: a base técnica estava pronta, **mas o boom só veio com o iPhone, em 2007–08** — tela sensível ao toque, sistema operacional pensado para o celular, conteúdo otimizado. Antes disso, o ecossistema era imaturo, e a experiência, ruim.

2009: o **4G** troca CDMA por **OFDM/LTE** — o Release 8 do 3GPP, depois LTE-Advanced e LTE-A Pro. O suporte a MIMO em larga escala e a reutilização de espectro fazem a internet móvel **explodir** — e ela se torna essencial no cotidiano. Essa é a segunda disrupção: **a internet móvel**.

Vale registrar: a evolução do LTE-Advanced já introduz **V2X e MTC** — comunicação veicular e comunicação de máquinas — sementes do que vem depois.

---

## SLIDE 11 — 5G (4:15 – 5:15)

2019 em diante: o **5G** — quando **a rede encontra a inteligência**.

Do lado do core: o **5G Core** com **SBA, SDN, NFV e network slicing** — a rede vira software em nuvem. Do lado do rádio: **mmWave e massive MIMO** na RAN, células pequenas, edge computing.

O alcance vertical: o 5G já traz suporte a **NTN** — redes não-terrestres —, **IAB**, redes privadas.

E o ponto de virada: o **Release 18, o 5G-Advanced**, introduz **IA/ML nos padrões 3GPP**. É a primeira vez que a inteligência entra formalmente na especificação — e é daí que o 6G herda o DNA. Terceira disrupção: a **inteligência móvel**.

---

## SLIDE 12 — 6G (5:15 – 6:15)

E chegamos ao horizonte do 6G — comercialização estimada para **~2029–2030**: a visão do 6G como **a Rede Inteligente de Tudo** — *"the Intelligent Network of Everything"*.

O que sustenta essa visão? **THz, ultra-massive MIMO, RIS, UDN e ISAC** como tecnologias-chave em desenvolvimento — que veremos em detalhe no Bloco 3.

E a fórmula central do artigo, que resume o 6G: **desempenho extremo + IA pervasiva + Internet of Everything + capacidades além da comunicação**. O foco da rede muda: de conectar humanos para conectar tudo — máquinas, veículos, sensores — e para fazer coisas além de comunicar.

---

## SLIDE 13 — CAMINHO ATÉ A PADRONIZAÇÃO (6:15 – 7:15)

Essa transição do 5G pro 6G não é espontânea — ela tem calendário. Dois relógios correndo em paralelo:

**Na ITU-R**, o rumo ao IMT-2030 em três fases: a **Fase 1**, de 2020 a 2023, já concluída — construiu a visão do IMT-2030, consolidada na Recomendação **M.2160**. A **Fase 2**, de 2024 a 2026 — requisitos de desempenho e metodologia de avaliação. E a **Fase 3**, de 2027 a 2030 — avaliação e seleção das interfaces candidatas.

**No 3GPP**: o **Release 20**, ~2025–2026, traz os primeiros estudos formais de tecnologias 6G; o **Release 21**, ~2028, deve ser o **primeiro padrão oficial**; e a previsão é de redes comerciais em **2029–2030**.

A mensagem: estamos exatamente na janela em que a pesquisa vira padrão — e é por isso que uma revisão de literatura agora é oportuna. **Beloin, os fundamentos.**

---

# BLOCO 2 · FUNDAMENTOS DO 6G (7:30 – 12:00) — slides 14 a 19 — BELOIN

---

## SLIDE 14 — DIVISÓRIA DO BLOCO 2 (7:30 – 7:45)

Obrigado. O Bloco 2 cobre as Seções IV, X e XI — o "101" do 6G: os **três elementos fundamentais**, as **12 características definidoras** e a síntese da visão em números.

---

## SLIDE 15 — ELEMENTO FUNDAMENTAL 1: WIRELESS (7:45 – 8:45)

O artigo define **três elementos fundamentais** do 6G. O primeiro é o próprio **wireless — muito além da comunicação tradicional**.

Aqui a palavra-chave é **extremo**: comunicação, **sensoriamento, posicionamento e energia**, todos levados ao limite.

E o artigo define **seis dimensões de desempenho** que o 6G precisa empurrar ao extremo — e que reaparecem nos requisitos do IMT-2030: **capacidade, latência, confiabilidade, densidade, cobertura e mobilidade**. Duas outras dimensões importantes: eficiência energética e precisão de posicionamento.

Guardem essas seis — elas são a régua com que o 6G será medido.

---

## SLIDE 16 — ELEMENTOS 2 E 3: IA E IoE (8:45 – 9:45)

Os outros dois elementos fundamentais:

**Inteligência Artificial — pervasiva em toda a rede.** O artigo prevê IA presente no **núcleo, na borda e na interface aérea** — motor da automação e otimização ponta a ponta. No Bloco 3 veremos o que isso significa na prática.

**Internet of Everything — além do IoT.** A rede não conecta só dispositivos IoT convencionais: conecta **sensores, máquinas, veículos, drones e robôs**. O foco muda do **humano para a máquina e a aplicação** — o tráfego do futuro majoritariamente não é mais pessoas navegando.

Esses três elementos — wireless extremo, IA pervasiva e IoE — são a base sobre a qual o artigo define as características do 6G.

---

## SLIDE 17 — O "101" DO 6G · PARTE 1 (9:45 – 10:30)

A Seção X identifica **12 características definidoras**, organizadas em **6 pares**. Três primeiros pares:

**Par 1 — Capacidade e Desempenho Extremos.** O *cornerstone* do 6G: as seis dimensões de performance levadas ao limite. É a base de tudo — sem performance extrema, as aplicações do Bloco 4 não existem.

**Par 2 — Ultra-Flexível e Ágil.** Adaptação em **todos os níveis** — dispositivo, comunicação, rede e serviço. O 6G precisa servir de um sensor de miliwatts a um trem de 1000 km/h, na mesma rede.

**Par 3 — Altamente Inteligente e Consciente.** IA pervasiva **somada à consciência do ambiente** via sensoriamento — a rede não só decide, como percebe.

---

## SLIDE 18 — O "101" DO 6G · PARTE 2 (10:30 – 11:10)

Os três pares que completam as 12 características:

**Par 4 — Ubiquamente Disponível e Confiável.** A chave da disponibilidade é **cobertura ampla** — viabilizada pela integração de redes terrestres e não-terrestres, a que chamamos SAGIN no Bloco 3.

**Par 5 — Verdadeiramente Verde e Sustentável.** Eficiência energética do **core ao PHY/MAC** — por benefício ecológico e econômico.

**Par 6 — Totalmente Seguro e Confiável.** Arquitetura de segurança **holística**, com privacidade e confiança.

Vale notar o desenho dos pares: performance e flexibilidade são "o que a rede faz"; inteligência, disponibilidade, sustentabilidade e segurança são "como a rede é". Juntos, definem a essência do 6G.

---

## SLIDE 19 — 6G EM NÚMEROS (11:10 – 12:00)

E aqui a visão resumida **em números** — os alvos do IMT-2030, consolidados na Seção XI do artigo e na Recomendação ITU-R M.2160:

**50 a 200 Gbit/s** de taxa de pico — 10 a 100 vezes o 5G.
**0,1 a 1 milissegundo** de latência de plano de usuário.
**Confiabilidade-alvo de 10⁻⁵ a 10⁻⁷** — cinco a sete noves, conforme o cenário.
**10⁶ a 10⁸ conexões por km²** — de um milhão a cem milhões.
**Mobilidade de até 500–1000 km/h** — trens de alta velocidade, aeronaves.
**Precisão de posicionamento de 1 a 10 cm** — da régua de obra ao sensor de fábrica.
**30 a 50 Mbit/s/m²** de capacidade de área — e **300 a 500 Mbit/s** de taxa experimentada.

O contraste com o 5G é ordem de grandeza em quase tudo. Esses números são o "para quê" das tecnologias do Bloco 3. **Emanuel, arquitetura e core.**

---

# BLOCO 3 · ARQUITETURA, CORE E VIRTUAL SLICING (12:00 – 19:30) — slides 20 a 28 — EMANUEL

> Nota: o roteiro detalhado desta seção está em `section_ix_script_pt_deck.md`. Aqui está a versão integrada, no tempo deste roteiro completo.

---

## SLIDE 20 — DIVISÓRIA DO BLOCO 3 (12:00 – 12:15)

Obrigado. Chegamos ao **Bloco 3** — o recorte técnico central da nossa revisão: a **Seção IX** do artigo, com foco em **arquitetura de rede** e **inteligência de rede** — e o fio condutor do nosso trabalho: o **slicing**.

---

## SLIDE 21 — PANORAMA DA SEÇÃO IX (12:15 – 13:15)

A Seção IX organiza **27 tecnologias 6G em 10 famílias, de A a J**: espectro, antenas, transmissão, arquitetura — o D —, inteligência de rede — o E —, além-comunicação, energia, dispositivos, serviços e segurança.

[pausa]

O nosso recorte é **D e E** — porque respondem diretamente às nossas questões: **RQ1**, sobre o core 6G nativo em IA, e **RQ2**, sobre as arquiteturas que suportam o slicing fim a fim. As demais famílias entram como contexto na revisão.

---

## SLIDE 22 — D · INTN / SAGIN (13:15 – 14:15)

O primeiro elemento da arquitetura: a rede integrada terrestre e não-terrestre — a **SAGIN**, de *space-air-ground integrated network*. Três camadas, uma só rede:

**Terrestre** — as redes móveis convencionais e estações terrenas: o grosso da capacidade.
**Aérea** — HAPS e UAVs: cobertura intermediária, do urbano ao rural.
**Espacial** — satélites **LEO, MEO e GEO**: cobertura verdadeiramente global.

No 6G, o limite da rede não é mais o horizonte — e o slicing atravessa as três camadas. Essa é a primeira resposta arquitetural à nossa **RQ2**.

---

## SLIDE 23 — D · UDN, IAB E CELL-FREE (14:15 – 15:15)

A segunda metade da arquitetura responde três perguntas práticas:

**Capacidade extrema?** **UDN** — redes ultra-densas. O THz tem alcance curto; logo, células pequenas e numerosíssimas. A UDN é o outro lado da moeda do THz.

**Conectar milhares de células sem fibra?** **IAB** — a célula atende o usuário e serve de backhaul sem fio para as vizinhas. Instala-se onde há demanda, não onde há fibra.

**QoS estável em toda a área?** **Cell-free massive MIMO** — o fim da célula fixa: pontos de acesso distribuídos cooperam e atendem cada usuário em conjunto. Sem bordas de célula, qualidade uniforme onde o usuário estiver.

Juntas com a SAGIN, são as estruturas da **RQ2** para o slicing fim a fim.

---

## SLIDE 24 — E · EVOLUÇÃO DO CORE (15:15 – 16:00)

Da arquitetura para a inteligência — a linha do tempo do core, que é o cerne da nossa **RQ1**:

**2G**: core de **comutação de circuitos** — dedicado à voz.
**3G/4G**: **packet core** — a internet no celular.
**5G**: core **cloud-native** — SBA, SDN, NFV e network slicing: funções de rede que viram software em nuvem.
**6G**: o próximo passo — **cloud intelligence**: IA pervasiva no núcleo. O core deixa de ser virtualizado e passa a ser **inteligente** — gerenciado, otimizado e fatiado pela própria IA.

É dessa transição — cloud-native para AI-native — que trata a RQ1.

---

## SLIDE 25 — E · O QUE O 5G JÁ TROUXE (16:00 – 16:45)

Fixando o que o 5G estabeleceu — porque o 6G herda e amplia tudo isso:

**SBA**: o core como funções de rede interconectadas, cada uma oferecendo serviços reutilizáveis — agilidade para agregar funcionalidades.
**SDN**: gestão da rede descolada do hardware — flexível e nativa em nuvem.
**NFV + network slicing**: recursos físicos divididos em **fatias virtuais**, cada uma dedicada a um serviço — uma fatia URLLC, uma eMBB, uma mMTC.

É esse slicing — hoje definido e orquestrado por regras humanas — o ponto de partida da nossa revisão.

---

## SLIDE 26 — E.1 · INTELLIGENT CORE (16:45 – 17:30)

O primeiro nível da inteligência 6G: o **core inteligente**. IA/ML pervasiva otimizando operação, gestão e **segurança** do núcleo de forma **autônoma**. O core cloud-native virtualizou as funções; o core 6G as torna inteligentes — a rede se autoconfigura e se autocura.

E o conceito central para nós: o **AI-native slicing**. No 5G, a fatia é definida por regras humanas. No 6G, **a própria IA decide como fatiar a rede** — dinamicamente, conforme demanda, tráfego e contexto. É essa autonomia que abre as lacunas do slide 28.

---

## SLIDE 27 — E.2–E.3 · EDGE E INTERFACE AÉREA (17:30 – 18:30)

A inteligência não fica só no core. Dois desdobramentos:

**Intelligent edge** — edge computing **+** IA. O artigo classifica **seis níveis de inteligência de borda**: num extremo, treino e inferência na nuvem; no outro, tudo on-device. Entre eles, trade-offs de **latência, energia e privacidade** — quanto mais perto do dispositivo, mais rápido e privado; quanto mais na nuvem, mais poder de processamento.

**Intelligent air interface** — a IA chega à camada física, em **três fases**: primeiro, substitui **blocos individuais** (estimação de canal, demapeamento); depois, **projeta blocos em conjunto** (estimação + equalização + demapeamento num só modelo); por fim, **desenha a interface aérea inteira** com aprendizado fim a fim — ruptura no projeto e na padronização.

Core, borda e rádio: inteligência ponta a ponta.

---

## SLIDE 28 — RQ3 · LACUNAS DO SLICING AUTÔNOMO (18:30 – 19:15)

Fechamos com a pergunta que motiva a revisão: **onde a literatura ainda não fechou a conta?** Quatro lacunas no slicing autônomo:

**Explicabilidade** — se a IA decide as fatias, as decisões precisam ser **auditáveis**.
**Garantia de SLA** — isolamento e estabilidade entre fatias sob **reconfiguração contínua**.
**Segurança do modelo** — envenenamento de dados, ataques adversariais: a IA que controla a fatia vira alvo.
**Orquestração fim a fim** — fatias atravessando RAN, transporte, core **e SAGIN** — ninguém ainda orquestrou isso de ponta a ponta.

Essas quatro lacunas são a contribuição original que a nossa Lit Review se propõe a mapear. **Hywre, as aplicações.**

---

# BLOCO 4 · APLICAÇÕES E CASOS DE USO (19:30 – 23:30) — slides 29 a 32 — HYWRE

---

## SLIDE 29 — DIVISÓRIA DO BLOCO 4 (19:30 – 19:45)

Obrigado. O Bloco 4 responde o "para quê": Seções V e VI — as aplicações que justificam toda a estrutura técnica que o Emanuel apresentou.

---

## SLIDE 30 — APLICAÇÕES DISRUPTIVAS (19:45 – 20:45)

O artigo define **12 aplicações disruptivas em 3 categorias**:

**Interações humano-máquina** — metaverso, **realidade estendida**, **comunicação holográfica**, **gêmeos digitais** e **internet tátil**. O fio condutor: a experiência com o digital vira imersiva e sensorial — ver, tocar e manipular conteúdo remoto como se estivesse ali.

**Ambientes inteligentes** — sociedade, cidade, fábrica e casa inteligentes. O ambiente percebe, decide e age — a cidade que se otimiza em tempo real, a fábrica que se reconfigura sozinha.

**Sistemas autônomos conectados** — **CAVs**, veículos autônomos; **UAVs** autônomos; e **sistemas robóticos** autônomos. São as aplicações mais exigentes: exigem do 6G o extremo das dimensões — confiabilidade, latência, mobilidade — que o Beloin mostrou no slide 19.

---

## SLIDE 31 — CASOS DE USO ORIENTADOS À COMUNICAÇÃO (20:45 – 21:45)

Na Seção VI, o artigo define **cinco casos de uso orientados à comunicação** — todos extensões diretas dos três pilares do 5G:

**Banda ultra-larga multimídia** — a extensão do **eMBB**: 50–200 Gbit/s de pico servindo XR e holografia.
**Tempo-sensível e crítico à missão** — a extensão do **URLLC**: 0,1–1 ms, confiabilidade 10⁻⁵–10⁻⁷ — controle industrial, cirurgia remota.
**Comunicações ultra-massivas** — a extensão do **mMTC**: 10⁶–10⁸ conexões por km².
**Escala global** — cobertura terrestre **+ não-terrestre**: a SAGIN em ação.
**Hiper-mobilidade** — até **500–1000 km/h**: o 6G mantém a conexão no trem-bala e na aeronave.

Percebam: cada caso de uso empurra ao extremo uma dimensão do slide 15.

---

## SLIDE 32 — CASOS DE USO ALÉM-COMUNICAÇÃO (21:45 – 23:15)

E aqui o novum do 6G: **três casos de uso além da comunicação — sem equivalente no 5G**:

**Inteligência de rede** — IA/ML como **serviço da própria rede**: o dispositivo não precisa de processamento local pesado — a rede treina e infere por ele, como serviço.

**Sensoriamento de rede** — a rede detecta **objetos e eventos via ISAC**: o mesmo sinal que comunica mapeia o ambiente — o "olho" do 6G, aplicado à fábrica, à cidade, à saúde.

**Energia de rede** — **transferência de energia sem fio**: a rede não só conecta dispositivos, ela os **alimenta** — sensores sem bateria que colhem energia do ar.

[pausa]

Esses três casos definem a fronteira do 6G: a rede deixa de ser um **tubo de bits** e vira uma **plataforma de capacidades** — computar, sentir, energizar. É a concretização do *"além da comunicação"* que atravessa o artigo inteiro — e é o que separa o 6G de todas as gerações anteriores.

---

# PROPOSTA DO GRUPO (23:30 – 25:00) — slides 33 a 37

---

## SLIDE 33 — COMO CONDUZIREMOS A LIT REVIEW (23:30 – 23:50)

Fechando: como conduzimos a revisão a partir de tudo isso.

**Metodologia**: síntese temática por bloco, guiada pelas RQs — corpus formado pelo artigo-base mais os estudos do protocolo; extração registrada em matriz, culminando na **matriz de lacunas em slicing autônomo**, a RQ3.

**Entregável**: um artigo de revisão na estrutura da RMSF, com **ênfase em arquitetura e core** — o Bloco 3 —, protocolo e fluxograma PRISMA documentados, e a conexão fundamentos → arquitetura → aplicações.

---

## SLIDE 34 — CRONOGRAMA (23:50 – 24:05)

Plano de **11 semanas**: semanas 1–2, protocolo e busca; 3–4, triagem e elegibilidade; 5–6, extração e síntese — matriz por bloco e por RQ, mapa de lacunas; 7–8, redação dos Blocos 1, 2 e 4; 9–10, Bloco 3 e as lacunas — o núcleo técnico; semana 11, revisão cruzada, PRISMA e entrega.

---

## SLIDE 35 — DIVISÃO DE RESPONSABILIDADES (24:05 – 24:20)

Divisão por bloco, com busca e triagem sempre em pares:

**Anderson** — histórico e padronização. **Beloin** — fundamentos, 12 características, requisitos-alvo. **Emanuel** — core, slicing e a matriz de lacunas da RQ3. **Hywre** — aplicações, casos de uso e a revisão final do texto.

---

## SLIDE 36 — LITERATURA COMPLEMENTAR (24:20 – 24:35)

Nossa base de partida em duas frentes — **método**: Kitchenham & Charters, para o protocolo; Page et al., o PRISMA 2020. E **visão 6G**: a Recomendação ITU-R M.2160, o framework do IMT-2030; Saad, Bennis & Chen; e Letaief e colegas — dois artigos seminais da visão 6G e da IA nas redes sem fio.

---

## SLIDE 37 — ENCERRAMENTO (24:35 – 25:00)

Referência principal: H. Pennanen et al., "6G: The Intelligent Network of Everything", IEEE Access, vol. 13, 2025 — DOI na tela.

Em resumo: apresentamos a estrutura de quatro blocos, três questões de pesquisa, um protocolo PRISMA e um cronograma de 11 semanas — com foco na transição do core cloud-native para o nativo em IA, as arquiteturas do slicing fim a fim e as lacunas do slicing autônomo.

**Obrigado.** Perguntas e sugestões são bem-vindas antes de avançarmos para a redação.

---

## Q&A — Backup de fatos (por bloco)

### Bloco 1 (histórico)
- 1G analógico: AMPS (América do Norte), NMT (Nórdico), TACS (Reino Unido)
- 2G digital: GSM dominante; D-AMPS/cdmaOne (América), PDC (Japão); primeira disrupção real de mercado (voz + SMS)
- 3G: CDMA/UMTS; turbo coding aproximando Shannon; boom só com iPhone (2007–08) — ecossistema imaturo antes disso
- 4G: OFDM/LTE (3GPP Rel-8, 2009); LTE-A (Rel-10), LTE-A Pro (Rel-13); MIMO full-dimension; V2X e MTC na evolução LTE-A
- 5G (Rel-15, 2019): 5G Core (SBA/SDN/NFV/slicing) + 5G NR (mmWave, massive MIMO); NTN, IAB, redes privadas; Rel-16/17/18; **Rel-18 (5G-Advanced) = IA/ML nos padrões**
- IMT-2030 (ITU-R): Fase 1 2020–23 (visão, Rec. M.2160); Fase 2 2024–26 (requisitos); Fase 3 2027–30 (avaliação). 3GPP: Rel-20 ~2025–26 estudos 6G; Rel-21 ~2028 primeiro padrão; comercial 2029–30

### Bloco 2 (fundamentos)
- Três elementos fundamentais: wireless extremo, IA pervasiva, Internet of Everything
- Seis dimensões: capacidade, latência, confiabilidade, densidade, cobertura, mobilidade (+ eficiência energética e precisão de posicionamento como dimensões importantes)
- 12 características / 6 pares (Seção X): extremo, ultra-flexível, inteligente/consciente, ubiquamente disponível, verdadeiramente verde, totalmente seguro
- Alvos IMT-2030 (Seção XI): pico 50/100/200 Gbit/s · experimentada 300/500 Mbit/s · eficiência espectral 1,5X/3X · capacidade de área 30/50 Mbit/s/m² · latência UP 0,1–1 ms · confiabilidade 10⁻⁵–10⁻⁷ · densidade 10⁶–10⁸/km² · mobilidade 500–1000 km/h · posicionamento 1–10 cm

### Bloco 3 (arquitetura e core)
- Seção IX: 27 tecnologias / 10 famílias A–J; recorte do grupo: D (arquitetura) + E (inteligência)
- Core (IX-E.1): "evolved from the circuit-switched network of 2G through the packet cores of 3G and 4G to the latest software/service-based architecture of 5G" (Rel-15); 6G = "from cloud to cloud intelligence"
- SAGIN: ground (redes móveis/estações terrenas) · airborne (HAPS, UAVs) · spaceborne (LEO/MEO/GEO)
- UDN contrapartida do THz (curto alcance); IAB já no 5G (Rel-16); cell-free massive MIMO = QoS estável sem bordas de célula
- Edge intelligence: 6 níveis (Figura 31 do paper) — trade-off latência × energia × privacidade
- Air interface: 3 fases rumo à AI-native (Figura 32) — bloco individual → projeto conjunto → end-to-end
- IA/ML nos padrões: 3GPP Release 18 (5G-Advanced)
- Lacunas RQ3: explicabilidade, SLA, segurança do modelo, orquestração fim a fim (RAN + transporte + core + SAGIN)

### Bloco 4 (aplicações)
- 12 aplicações / 3 categorias (Seção V): humano-máquina (metaverso, XR, holográfica, gêmeos digitais, internet tátil), ambientes inteligentes (sociedade, cidade, fábrica, casa), autônomos (CAV, UAV, robóticos)
- 5 casos orientados à comunicação (Seção VI): ultra-banda larga (eMBB++), tempo-sensível/crítico (URLLC++), ultra-massivo (mMTC++), escala global (terrestre+NTN), hiper-mobilidade (500–1000 km/h)
- 3 casos além-comunicação: inteligência de rede, sensoriamento de rede (ISAC), energia de rede (WET)

### Referências de método (slide 36)
- Kitchenham & Charters (2007), EBSE TR
- Page et al. (2021), PRISMA 2020, BMJ 372:n71
- ITU-R M.2160-0 (2023)
- Saad, Bennis & Chen (2020), IEEE Network 34(3)
- Letaief et al. (2019), IEEE Commun. Mag. 57(8)

### Bônus (se perguntarem sobre o 7G)
- O artigo encerra com a primeira visão estruturada de 7G na literatura: "Deeply Intelligent Network of Hyperverses" — e a evolução 1G→7G em ciclos de duas gerações
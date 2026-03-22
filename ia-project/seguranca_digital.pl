% ============================================================
% SISTEMA ESPECIALISTA: SEGURANÇA DIGITAL
% Base de Conhecimento em Prolog - AEMS / TADS
% ============================================================
% Baseado no Questionário de Segurança Digital do site AEMS
% Perguntas: 10 questões sim/não sobre hábitos digitais
% ============================================================

% ============================================================
% SEÇÃO 1: FATOS - PERGUNTAS E CATEGORIAS
% ============================================================

% pergunta(ID, Categoria, RiscoAssociado)
% Mapeia cada pergunta à sua categoria de segurança e ao risco associado
pergunta(q1,  reutilizacao_senha,       invasao_conta).
pergunta(q2,  autenticacao_dois_fatores, invasao_conta).
pergunta(q3,  armazenamento_senha,      roubo_senha).
pergunta(q4,  phishing,                 engenharia_social).
pergunta(q5,  atualizacao_sistema,      malware).
pergunta(q6,  backup_dados,             perda_dados).
pergunta(q7,  wifi_publico,             interceptacao_dados).
pergunta(q8,  permissoes_app,           malware).
pergunta(q9,  bloqueio_tela,            acesso_fisico).
pergunta(q10, downloads_seguros,        malware).

% enunciado(ID, Texto)
% Texto completo de cada pergunta do questionário
enunciado(q1,  'Você usa a mesma senha (ou senhas muito parecidas) em mais de um lugar?').
enunciado(q2,  'O site pede um código por SMS/app ao entrar no e-mail ou redes sociais?').
enunciado(q3,  'Você anota suas senhas em papéis, cadernos ou WhatsApp/Bloco de Notas?').
enunciado(q4,  'Se receber mensagem urgente sobre prêmio ou bloqueio, você clica no link?').
enunciado(q5,  'Quando aparece aviso de atualização, você atualiza o sistema na hora?').
enunciado(q6,  'Se seu celular sumisse hoje, seus arquivos estariam salvos em outro lugar?').
enunciado(q7,  'Você usa Wi-Fi aberto de praças/shoppings/aeroportos sem proteção extra?').
enunciado(q8,  'Antes de instalar um app, você verifica se pede permissões desnecessárias?').
enunciado(q9,  'Seu celular e computador bloqueiam a tela e pedem senha/digital para abrir?').
enunciado(q10, 'Você evita baixar filmes/jogos de sites desconhecidos ou "piratas"?').

% ============================================================
% SEÇÃO 2: FATOS - RESPOSTAS SEGURAS E DICAS
% ============================================================

% resposta_segura(ID, Resposta)
% A resposta que indica boa prática de segurança para cada pergunta
resposta_segura(q1,  nao). % não reutilizar senhas é seguro
resposta_segura(q2,  sim). % ter 2FA ativo é seguro
resposta_segura(q3,  nao). % não anotar senhas é seguro
resposta_segura(q4,  nao). % não clicar em links suspeitos é seguro
resposta_segura(q5,  sim). % atualizar sistema é seguro
resposta_segura(q6,  sim). % ter backup é seguro
resposta_segura(q7,  nao). % não usar Wi-Fi aberto sem VPN é seguro
resposta_segura(q8,  sim). % verificar permissões é seguro
resposta_segura(q9,  sim). % ter bloqueio de tela é seguro
resposta_segura(q10, sim). % evitar downloads piratas é seguro

% dica(ID, Texto)
% Orientação de segurança para cada área de risco
dica(q1,  'Use senhas únicas para cada conta. Considere usar um gerenciador de senhas.').
dica(q2,  'Ative a autenticação de dois fatores (2FA) no e-mail e redes sociais agora.').
dica(q3,  'Nunca anote senhas em locais acessíveis. Use um gerenciador de senhas seguro.').
dica(q4,  'Mensagens urgentes sobre prêmios ou bloqueios quase sempre são golpes. Acesse o site oficial diretamente.').
dica(q5,  'Atualize seus dispositivos assim que possível. As atualizações corrigem vulnerabilidades.').
dica(q6,  'Configure backup automático na nuvem (Google Fotos, iCloud) para proteger seus arquivos.').
dica(q7,  'Evite usar Wi-Fi público sem proteção. Use uma VPN ou aguarde uma rede confiável.').
dica(q8,  'Sempre revise permissões antes de instalar apps. Desconfie de acesso desnecessário.').
dica(q9,  'Configure bloqueio de tela com senha, PIN ou biometria em todos os dispositivos.').
dica(q10, 'Baixe programas e mídia apenas de lojas e sites oficiais para evitar vírus.').

% ============================================================
% SEÇÃO 3: FATOS - TIPOS DE GOLPES
% ============================================================

% tipo_golpe(Nome, Descricao)
tipo_golpe(phishing,          'Golpistas se passam por instituições para roubar dados via links falsos.').
tipo_golpe(malware,           'Programas maliciosos que espionam, roubam senhas ou sequestram dados.').
tipo_golpe(whatsapp_clonado,  'Criminosos clonam o WhatsApp para pedir dinheiro a amigos e familiares.').
tipo_golpe(ligacao_maliciosa, 'Golpistas fingem ser banco ou suporte técnico para obter dados confidenciais.').
tipo_golpe(engenharia_social, 'Manipulação psicológica para induzir vítimas a revelar informações sigilosas.').
tipo_golpe(ransomware,        'Sequestro de dados com exigência de pagamento (geralmente em criptomoeda).').

% prevencao_golpe(Nome, Orientacao)
prevencao_golpe(phishing,          'Nunca clique em links de mensagens suspeitas. Acesse o site oficial diretamente.').
prevencao_golpe(malware,           'Use antivírus, mantenha o sistema atualizado e baixe apenas de fontes confiáveis.').
prevencao_golpe(whatsapp_clonado,  'Ative a verificação em duas etapas no WhatsApp via Configurações > Conta.').
prevencao_golpe(ligacao_maliciosa, 'Bancos jamais pedem senhas por telefone. Desligue e ligue para o número oficial.').
prevencao_golpe(engenharia_social, 'Desconfie de urgência e pressão. Sempre verifique por canais oficiais antes de agir.').
prevencao_golpe(ransomware,        'Faça backups regulares e nunca abra anexos de remetentes desconhecidos.').

% golpe_relacionado(Categoria, TipoGolpe)
% Liga categorias de vulnerabilidade aos golpes que exploram essa fraqueza
golpe_relacionado(reutilizacao_senha,       phishing).
golpe_relacionado(autenticacao_dois_fatores, phishing).
golpe_relacionado(armazenamento_senha,      engenharia_social).
golpe_relacionado(phishing,                 engenharia_social).
golpe_relacionado(atualizacao_sistema,      malware).
golpe_relacionado(wifi_publico,             phishing).
golpe_relacionado(permissoes_app,           malware).
golpe_relacionado(bloqueio_tela,            engenharia_social).
golpe_relacionado(downloads_seguros,        malware).
golpe_relacionado(downloads_seguros,        ransomware).

% nivel_risco_categoria(Categoria, Nivel)
nivel_risco_categoria(reutilizacao_senha,       alto).
nivel_risco_categoria(autenticacao_dois_fatores, alto).
nivel_risco_categoria(armazenamento_senha,      alto).
nivel_risco_categoria(phishing,                 alto).
nivel_risco_categoria(wifi_publico,             alto).
nivel_risco_categoria(downloads_seguros,        alto).
nivel_risco_categoria(atualizacao_sistema,      medio).
nivel_risco_categoria(backup_dados,             medio).
nivel_risco_categoria(permissoes_app,           medio).
nivel_risco_categoria(bloqueio_tela,            medio).

% ============================================================
% SEÇÃO 4: REGRAS - ANÁLISE DE RESPOSTAS INDIVIDUAIS
% ============================================================

% resposta_correta(+Pergunta, +Resposta)
% Verdadeiro se a resposta fornecida é a resposta segura
resposta_correta(Pergunta, Resposta) :-
    resposta_segura(Pergunta, Resposta).

% resposta_incorreta(+Pergunta, +Resposta)
% Verdadeiro se a resposta fornecida indica hábito inseguro
resposta_incorreta(Pergunta, Resposta) :-
    resposta_segura(Pergunta, RespostaSegura),
    Resposta \= RespostaSegura.

% vulneravel_em(+Pergunta, +Resposta)
% Verdadeiro se o usuário está vulnerável na área coberta por Pergunta
vulneravel_em(Pergunta, Resposta) :-
    resposta_incorreta(Pergunta, Resposta),
    pergunta(Pergunta, _, _).

% risco_alto_em(+Pergunta, +Resposta)
% Verdadeiro se a vulnerabilidade encontrada é de risco alto
risco_alto_em(Pergunta, Resposta) :-
    vulneravel_em(Pergunta, Resposta),
    pergunta(Pergunta, Categoria, _),
    nivel_risco_categoria(Categoria, alto).

% ============================================================
% SEÇÃO 5: REGRAS - PONTUAÇÃO
% ============================================================

% pontuacao_pergunta(+Pergunta, +Resposta, -Ponto)
% Retorna 1 se a resposta é segura, 0 caso contrário
pontuacao_pergunta(Pergunta, Resposta, 1) :-
    resposta_correta(Pergunta, Resposta).
pontuacao_pergunta(Pergunta, Resposta, 0) :-
    resposta_incorreta(Pergunta, Resposta).

% calcular_pontuacao(+ListaRespostas, -Pontuacao)
% ListaRespostas deve ter o formato: [resp(q1, sim), resp(q2, nao), ...]
calcular_pontuacao([], 0).
calcular_pontuacao([resp(Q, R) | Resto], Total) :-
    pontuacao_pergunta(Q, R, Ponto),
    calcular_pontuacao(Resto, SubTotal),
    Total is SubTotal + Ponto.

% ============================================================
% SEÇÃO 6: REGRAS - NÍVEL DE SEGURANÇA
% ============================================================

% nivel_seguranca(+Pontuacao, -Nivel)
% Classifica o nível de segurança do usuário conforme pontuação
nivel_seguranca(Pontuacao, alto)  :- Pontuacao >= 8.
nivel_seguranca(Pontuacao, medio) :- Pontuacao >= 5, Pontuacao < 8.
nivel_seguranca(Pontuacao, baixo) :- Pontuacao < 5.

% mensagem_nivel(+Nivel, -Mensagem)
mensagem_nivel(alto,  'Parabéns! Você tem ótimos hábitos de segurança digital. Continue se mantendo atualizado.').
mensagem_nivel(medio, 'Você já tem boas práticas, mas ainda há pontos a melhorar. Veja as dicas abaixo.').
mensagem_nivel(baixo, 'Atenção! Seus hábitos digitais precisam de ajustes importantes para sua proteção.').

% cor_nivel(+Nivel, -Cor)
% Representação visual do nível (compatível com o site)
cor_nivel(alto,  verde).
cor_nivel(medio, amarelo).
cor_nivel(baixo, vermelho).

% ============================================================
% SEÇÃO 7: REGRAS - DIAGNÓSTICO
% ============================================================

% areas_vulneraveis(+ListaRespostas, -ListaVulneraveis)
% Extrai as IDs das perguntas em que o usuário respondeu de forma insegura
areas_vulneraveis([], []).
areas_vulneraveis([resp(Q, R) | Resto], [Q | Vulneraveis]) :-
    resposta_incorreta(Q, R), !,
    areas_vulneraveis(Resto, Vulneraveis).
areas_vulneraveis([_ | Resto], Vulneraveis) :-
    areas_vulneraveis(Resto, Vulneraveis).

% obter_dicas(+ListaPerguntas, -ListaDicas)
% Retorna lista de dicas para cada área vulnerável identificada
obter_dicas([], []).
obter_dicas([Q | Resto], [dica(Q, D) | Dicas]) :-
    dica(Q, D),
    obter_dicas(Resto, Dicas).

% avaliar_usuario(+ListaRespostas, -Pontuacao, -Nivel, -Mensagem)
% Avalia completamente o perfil do usuário com base nas respostas
avaliar_usuario(ListaRespostas, Pontuacao, Nivel, Mensagem) :-
    calcular_pontuacao(ListaRespostas, Pontuacao),
    nivel_seguranca(Pontuacao, Nivel),
    mensagem_nivel(Nivel, Mensagem).

% diagnostico_completo(+ListaRespostas, -Pontuacao, -Nivel, -Mensagem, -Dicas)
% Diagnóstico completo: pontuação, nível, mensagem e lista de dicas personalizadas
diagnostico_completo(ListaRespostas, Pontuacao, Nivel, Mensagem, Dicas) :-
    avaliar_usuario(ListaRespostas, Pontuacao, Nivel, Mensagem),
    areas_vulneraveis(ListaRespostas, Vulneraveis),
    obter_dicas(Vulneraveis, Dicas).

% ============================================================
% SEÇÃO 8: REGRAS - CONSULTAS TEMÁTICAS
% ============================================================

% protegido_contra(+ListaRespostas, +TipoRisco)
% Verdadeiro se o usuário respondeu corretamente à pergunta que cobre esse risco
protegido_contra(ListaRespostas, TipoRisco) :-
    pergunta(Q, _, TipoRisco),
    resposta_segura(Q, RespostaSegura),
    member(resp(Q, RespostaSegura), ListaRespostas).

% tem_risco_alto(+ListaRespostas)
% Verdadeiro se o usuário possui ao menos uma vulnerabilidade de risco alto
tem_risco_alto(ListaRespostas) :-
    member(resp(Q, R), ListaRespostas),
    risco_alto_em(Q, R).

% contar_vulnerabilidades_altas(+ListaRespostas, -Quantidade)
contar_vulnerabilidades_altas(ListaRespostas, Quantidade) :-
    findall(Q, (
        member(resp(Q, R), ListaRespostas),
        risco_alto_em(Q, R)
    ), Lista),
    length(Lista, Quantidade).

% golpes_a_que_esta_exposto(+ListaRespostas, -ListaGolpes)
% Lista os tipos de golpe aos quais o usuário está exposto com base nas vulnerabilidades
golpes_a_que_esta_exposto(ListaRespostas, ListaGolpes) :-
    findall(Golpe, (
        member(resp(Q, R), ListaRespostas),
        resposta_incorreta(Q, R),
        pergunta(Q, Categoria, _),
        golpe_relacionado(Categoria, Golpe)
    ), Repetidos),
    list_to_set(Repetidos, ListaGolpes).

% ============================================================
% EXEMPLOS DE CONSULTAS
% ============================================================
%
% --- Consulta 1: Usuário com todos os hábitos seguros (pontuação 10) ---
%
% ?- avaliar_usuario([
%      resp(q1,nao), resp(q2,sim), resp(q3,nao), resp(q4,nao), resp(q5,sim),
%      resp(q6,sim), resp(q7,nao), resp(q8,sim), resp(q9,sim), resp(q10,sim)
%    ], Pontuacao, Nivel, Mensagem).
%
% Resultado esperado:
%   Pontuacao = 10
%   Nivel = alto
%   Mensagem = 'Parabéns! Você tem ótimos hábitos de segurança digital...'
%
% ─────────────────────────────────────────────────────────────────────
%
% --- Consulta 2: Diagnóstico completo de usuário com hábitos inseguros ---
%
% ?- diagnostico_completo([
%      resp(q1,sim), resp(q2,nao), resp(q3,sim), resp(q4,sim), resp(q5,nao),
%      resp(q6,nao), resp(q7,sim), resp(q8,nao), resp(q9,nao), resp(q10,nao)
%    ], Pontuacao, Nivel, Mensagem, Dicas).
%
% Resultado esperado:
%   Pontuacao = 0, Nivel = baixo
%   Mensagem = 'Atenção! Seus hábitos digitais precisam de ajustes...'
%   Dicas = [dica(q1,'...'), dica(q2,'...'), ...]
%
% ─────────────────────────────────────────────────────────────────────
%
% --- Consulta 3: Verificar se usuário está protegido contra phishing ---
%
% ?- protegido_contra([resp(q4,nao), resp(q2,sim)], engenharia_social).
% Resultado esperado: true
%
% ─────────────────────────────────────────────────────────────────────
%
% --- Consulta 4: Listar golpes aos quais o usuário está exposto ---
%
% ?- golpes_a_que_esta_exposto([
%      resp(q1,sim), resp(q2,nao), resp(q3,nao), resp(q4,sim),
%      resp(q5,sim), resp(q6,sim), resp(q7,nao), resp(q8,sim),
%      resp(q9,sim), resp(q10,sim)
%    ], Golpes).
% Resultado esperado:
%   Golpes = [phishing, engenharia_social]
%
% ─────────────────────────────────────────────────────────────────────
%
% --- Consulta 5: Verificar vulnerabilidade em senha reutilizada ---
%
% ?- vulneravel_em(q1, sim).
% Resultado esperado: true
%
% ?- risco_alto_em(q1, sim).
% Resultado esperado: true
%
% ─────────────────────────────────────────────────────────────────────
%
% --- Consulta 6: Obter prevenção contra um tipo de golpe ---
%
% ?- prevencao_golpe(phishing, Prevencao).
% Resultado esperado:
%   Prevencao = 'Nunca clique em links de mensagens suspeitas...'
%
% ─────────────────────────────────────────────────────────────────────
%
% --- Consulta 7: Contar vulnerabilidades de alto risco ---
%
% ?- contar_vulnerabilidades_altas([
%      resp(q1,sim), resp(q2,nao), resp(q3,nao), resp(q4,sim),
%      resp(q5,sim), resp(q6,sim), resp(q7,sim), resp(q8,sim),
%      resp(q9,sim), resp(q10,sim)
%    ], Quantidade).
% Resultado esperado: Quantidade = 3

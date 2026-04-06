-- Migração 001 — Tabela de diagnósticos
-- Execute no SQL Editor do painel Supabase (https://supabase.com/dashboard)

create table if not exists public.diagnosticos (
  id                  uuid          primary key default gen_random_uuid(),
  nome                text,
  respostas           jsonb         not null,
  pontuacao           integer       not null,
  nivel_risco         text          not null check (nivel_risco in ('baixo', 'medio', 'alto')),
  regras_disparadas   text[]        not null default '{}',
  conclusoes_derivadas text[]       not null default '{}',
  recomendacoes       text[]        not null default '{}',
  falhas_detectadas   text[]        not null default '{}',
  criado_em           timestamptz   not null default now()
);

-- Índice para filtro e ordenação mais rápidos
create index if not exists idx_diagnosticos_nivel_risco
  on public.diagnosticos (nivel_risco);

create index if not exists idx_diagnosticos_criado_em
  on public.diagnosticos (criado_em desc);

-- RPC para estatísticas agregadas (usada pelo endpoint /api/estatisticas)
create or replace function public.stats_diagnosticos()
returns table (
  nivel_risco     text,
  quantidade      bigint,
  soma_pontuacao  bigint
)
language sql
stable
as $$
  select
    nivel_risco,
    count(*)        as quantidade,
    sum(pontuacao)  as soma_pontuacao
  from public.diagnosticos
  group by nivel_risco;
$$;

-- RLS: desabilita para acesso via service role key (backend)
-- Se quiser expor ao frontend com anon key, habilite RLS e crie policies.
alter table public.diagnosticos disable row level security;

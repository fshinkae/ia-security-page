# AEMS Segurança Digital — Documento de Projeto

## Visão Geral

Refatoração do site educacional de cibersegurança da AEMS de HTML/CSS/JS puro para **React + Vite**, modernizando a stack e elevando o nível visual mantendo a identidade cyberpunk/hacker existente.

---

## Stack Técnica

| Tecnologia | Uso |
|---|---|
| React 18 + Vite | Framework principal, build tool |
| Tailwind CSS v4 | Estilização utility-first |
| Framer Motion | Animações (scroll, tilt, typewriter) |
| gh-pages | Deploy no GitHub Pages |

> React Router **não é necessário** — site single-page com scroll.

---

## Identidade Visual

### Paleta de Cores

| Token | Valor | Uso |
|---|---|---|
| `bg-primary` | `#080B0F` | Fundo principal |
| `bg-surface` | `#0D1117` | Superfície de cards |
| `accent-red` | `#E53E3E` | Alertas, CTAs, destaques |
| `accent-cyan` | `#00FFFF` | Hover, ícones tech, secundário |
| `text-primary` | `#FFFFFF` | Texto principal |
| `text-muted` | `#A0AEC0` | Texto secundário |
| `glow-red` | `rgba(229, 62, 62, 0.3)` | Sombras e bordas vermelhas |
| `glow-cyan` | `rgba(0, 255, 255, 0.2)` | Sombras e bordas cyan |

### Tipografia

| Fonte | Aplicação |
|---|---|
| **Pixelify Sans** | Títulos de seção (identidade pixel/hacker) |
| **Inter** | Corpo de texto, parágrafos |
| **JetBrains Mono** | Números, badges, labels técnicos |

### Efeitos Visuais

- Grid de pontos no fundo com opacidade 4% (estilo circuit board)
- Glow vermelho/cyan em elementos interativos
- Scanlines horizontais sutis sobre o hero
- Noise texture no background
- Cards com borda gradiente animada `vermelho → cyan`

---

## Estrutura de Componentes

```
src/
├── components/
│   ├── layout/
│   │   ├── Header.jsx
│   │   └── Footer.jsx
│   ├── sections/
│   │   ├── HeroPopup.jsx
│   │   ├── Intro.jsx
│   │   ├── CasosReais.jsx
│   │   ├── TiposGolpes.jsx
│   │   ├── DicasPreveção.jsx
│   │   ├── ComoDenunciar.jsx
│   │   ├── Equipe.jsx
│   │   └── Questionario.jsx
│   └── ui/
│       ├── Button.jsx
│       ├── Card.jsx
│       ├── Modal.jsx
│       ├── StarRating.jsx
│       └── TypewriterText.jsx
├── data/
│   ├── team.js
│   ├── newsCards.js
│   ├── golpes.js
│   ├── dicas.js
│   └── quizQuestions.js
├── App.jsx
└── main.jsx
```

---

## Melhorias por Seção

### Header
- Logo com glow sutil ao carregar
- Navbar com links âncora e indicador de seção ativa no scroll
- Sticky com `backdrop-filter: blur(12px)` ao rolar

### Hero Popup
- Efeito typewriter via `TypewriterText` com Framer Motion
- Estatística animada de golpes (mockada, contador em tempo real)
- Ícone de alerta com animação pulse cyan

### Intro
- Layout 2 colunas com entrada staggered (Framer Motion)
- Número "1,2 milhão" animado de 0 ao valor ao entrar na viewport
- GIF com border glow ou substituído por Lottie

### Casos Reais
- Cards com borda gradiente animada no hover + elevação
- Lazy loading nas imagens
- Badge de categoria: `[ HACKING ]`, `[ ENGENHARIA SOCIAL ]`

### Tipos de Golpes
- Accordion/tabs em mobile
- Badge de severidade: `[ ALTO ]`, `[ MÉDIO ]`
- Entrada alternada: slide-in esquerda/direita

### Dicas de Prevenção
- Grid 2×2 com flip 3D no hover
- Frente: ícone + título
- Verso: descrição detalhada em fundo cyan escuro

### Como Denunciar
- Timeline vertical com linha conectora que "desenha" conforme scroll
- Cada passo com fade-in sequencial

### Equipe
- Cards com foto circular e borda gradiente
- Hover revela ícones de redes sociais

### Questionário
- Progress bar animada no topo
- Uma pergunta por vez com transição de slide
- Resultado com gauge circular + badge de nível + dicas personalizadas

---

## Padrões de Animação (Framer Motion)

```js
// Entrada padrão de seções
const sectionVariants = {
  hidden: { opacity: 0, y: 40 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: 'easeOut' }
  }
}

// Stagger em grids de cards
const containerVariants = {
  visible: {
    transition: { staggerChildren: 0.15 }
  }
}
```

---

## Restrições — O que NÃO alterar

- [ ] Conteúdo textual em português
- [ ] Identidade visual cyberpunk/hacker
- [ ] Integração com Google Forms (`entry.971847553`)
- [ ] Deploy via GitHub Pages
- [ ] Nenhuma seção removida

---

> Cada seção do Figma mapeia 1:1 para um componente em `sections/`.

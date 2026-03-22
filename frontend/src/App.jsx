import { useState } from 'react'
import Header from './components/layout/Header'
import Footer from './components/layout/Footer'
import HeroPopup from './components/sections/HeroPopup'
import Intro from './components/sections/Intro'
import CasosReais from './components/sections/CasosReais'
import TiposGolpes from './components/sections/TiposGolpes'
import DicasPrevencao from './components/sections/DicasPrevencao'
import ComoDenunciar from './components/sections/ComoDenunciar'
import Equipe from './components/sections/Equipe'
import Questionario from './components/sections/Questionario'

export default function App() {
  const [heroVisible, setHeroVisible] = useState(true)

  return (
    <div className="min-h-screen bg-[#080B0F] text-white font-inter relative overflow-x-hidden">
      {/* Dot grid background */}
      <div
        className="fixed inset-0 pointer-events-none z-0"
        style={{
          backgroundImage: 'radial-gradient(circle, rgba(255,255,255,0.04) 1px, transparent 1px)',
          backgroundSize: '28px 28px',
        }}
      />

      {heroVisible && <HeroPopup onClose={() => setHeroVisible(false)} />}

      <div className="relative z-10">
        <Header />
        <main>
          <Intro />
          <CasosReais />
          <TiposGolpes />
          <DicasPrevencao />
          <ComoDenunciar />
          <Equipe />
          <Questionario />
        </main>
        <Footer />
      </div>
    </div>
  )
}

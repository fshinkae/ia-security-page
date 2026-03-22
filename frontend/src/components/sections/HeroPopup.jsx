import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import TypewriterText from '../ui/TypewriterText'

export default function HeroPopup({ onClose }) {
  const [typed, setTyped] = useState(false)
  const [count, setCount] = useState(0)

  // Animated counter for scam stats
  useEffect(() => {
    const target = 1200000
    const duration = 2000
    const step = target / (duration / 16)
    let current = 0
    const timer = setInterval(() => {
      current = Math.min(current + step, target)
      setCount(Math.floor(current))
      if (current >= target) clearInterval(timer)
    }, 16)
    return () => clearInterval(timer)
  }, [])

  useEffect(() => {
    document.body.classList.add('no-scroll')
    return () => document.body.classList.remove('no-scroll')
  }, [])

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.4 }}
        className="fixed inset-0 z-50 flex items-center justify-center bg-[#080B0F]/95 scanlines"
        style={{ backdropFilter: 'blur(4px)' }}
      >
        {/* Scanlines overlay */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.04) 2px, rgba(0,0,0,0.04) 4px)',
          }}
        />

        <div className="relative z-10 text-center px-6 max-w-lg mx-auto">
          {/* Pulse icon */}
          <motion.div
            animate={{ scale: [1, 1.08, 1] }}
            transition={{ repeat: Infinity, duration: 2, ease: 'easeInOut' }}
            className="mb-8 inline-block"
          >
            <img
              src="/images/warning.png"
              alt="Alerta"
              className="w-24 h-24 mx-auto"
              style={{ filter: 'drop-shadow(0 0 16px rgba(0,255,255,0.6))' }}
            />
          </motion.div>

          <h1 className="font-pixel text-lg md:text-2xl text-white mb-4 leading-relaxed min-h-[3.5rem]">
            <TypewriterText
              text="SOFREU UM CYBERATAQUE? EVITE PREJUÍZOS, ATUE RAPIDAMENTE!"
              speed={40}
              onComplete={() => setTyped(true)}
            />
          </h1>

          {/* Stats counter */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: typed ? 1 : 0 }}
            transition={{ duration: 0.5 }}
            className="font-mono text-sm text-[#A0AEC0] mb-8"
          >
            Em 2024 o Brasil registrou{' '}
            <span className="text-[#E53E3E] font-bold text-base">
              {count.toLocaleString('pt-BR')}
            </span>{' '}
            golpes virtuais
          </motion.p>

          <motion.button
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: typed ? 1 : 0, y: typed ? 0 : 10 }}
            transition={{ duration: 0.4 }}
            onClick={() => {
              document.body.classList.remove('no-scroll')
              onClose()
            }}
            whileHover={{ scale: 1.05, boxShadow: '0 0 20px rgba(229,62,62,0.5)' }}
            whileTap={{ scale: 0.97 }}
            className="px-8 py-3 bg-[#E53E3E] text-white font-pixel text-sm rounded-sm tracking-widest uppercase cursor-pointer transition-all"
          >
            ENTRAR NO SITE
          </motion.button>
        </div>
      </motion.div>
    </AnimatePresence>
  )
}

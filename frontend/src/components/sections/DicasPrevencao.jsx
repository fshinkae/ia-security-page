import { useRef, useState } from 'react'
import { motion, useInView } from 'framer-motion'
import { dicas } from '../../data/dicas'

const cardVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: (i) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: 'easeOut', delay: i * 0.12 },
  }),
}

function FlipCard({ dica, index }) {
  const [flipped, setFlipped] = useState(false)

  return (
    <motion.div
      custom={index}
      variants={cardVariants}
      className="flip-card h-56"
      onClick={() => setFlipped((f) => !f)}
    >
      <div className={`flip-card-inner rounded-lg${flipped ? ' is-flipped' : ''}`}>
        {/* Front */}
        <div className="flip-card-front gradient-border rounded-lg bg-[#0D1117] flex flex-col items-center justify-center gap-4 p-6 text-center">
          <img src={dica.img} alt={dica.alt} className="w-16 h-16 object-cover rounded" loading="lazy" />
          <p className="font-pixel text-sm text-white leading-snug">{dica.frente}</p>
          <span className="font-mono text-[10px] text-[#00FFFF]/60 hidden md:block">Passe o mouse para saber mais</span>
          <span className="font-mono text-[10px] text-[#00FFFF]/60 md:hidden">Toque para saber mais</span>
        </div>

        {/* Back */}
        <div
          className="flip-card-back rounded-lg flex items-center justify-center p-6 text-center"
          style={{ background: 'linear-gradient(135deg, #0a1a2e, #0D1117)', border: '1px solid rgba(0,255,255,0.3)' }}
        >
          <p className="text-sm text-white leading-relaxed">{dica.verso}</p>
        </div>
      </div>
    </motion.div>
  )
}

export default function DicasPrevencao() {
  const ref = useRef(null)
  const inView = useInView(ref, { once: true, margin: '-60px' })

  return (
    <section id="prevencao" className="py-20 px-6">
      <div className="max-w-6xl mx-auto">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.5 }}
          className="font-pixel text-2xl md:text-3xl text-white mb-12 text-center"
        >
          Dicas de Prevenção
        </motion.h2>

        <motion.div
          ref={ref}
          initial="hidden"
          animate={inView ? 'visible' : 'hidden'}
          className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6"
        >
          {dicas.map((dica, i) => (
            <FlipCard key={dica.id} dica={dica} index={i} />
          ))}
        </motion.div>
      </div>
    </section>
  )
}

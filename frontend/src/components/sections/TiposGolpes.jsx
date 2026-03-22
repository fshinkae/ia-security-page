import { useRef } from 'react'
import { motion, useInView } from 'framer-motion'
import { golpes } from '../../data/golpes'

const severidadeColors = {
  ALTO: 'border-[#E53E3E] text-[#E53E3E]',
  MÉDIO: 'border-yellow-400 text-yellow-400',
}

const itemVariants = {
  hidden: (i) => ({ opacity: 0, x: i % 2 === 0 ? -40 : 40 }),
  visible: { opacity: 1, x: 0, transition: { duration: 0.6, ease: 'easeOut' } },
}

export default function TiposGolpes() {
  const ref = useRef(null)
  const inView = useInView(ref, { once: true, margin: '-60px' })

  return (
    <section id="golpes" className="py-20 px-6 bg-[#0D1117]/50">
      <div className="max-w-6xl mx-auto">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.5 }}
          className="font-pixel text-2xl md:text-3xl text-white mb-12 text-center"
        >
          Tipos de Golpes na Internet
        </motion.h2>

        <motion.div
          ref={ref}
          initial="hidden"
          animate={inView ? 'visible' : 'hidden'}
          className="space-y-6"
        >
          {golpes.map((golpe, i) => (
            <motion.div
              key={golpe.id}
              custom={i}
              variants={itemVariants}
              className="gradient-border rounded-lg p-6 bg-[#0D1117] flex flex-col items-center sm:flex-row sm:items-start gap-6"
            >
              <div className="flex-shrink-0">
                <img
                  src={golpe.img}
                  alt={golpe.alt}
                  className="w-20 h-20 object-cover rounded"
                  loading="lazy"
                />
              </div>
              <div className="flex-1 w-full text-center sm:text-left">
                <div className="flex items-center justify-center sm:justify-start gap-3 mb-2 flex-wrap">
                  <h3 className="font-pixel text-lg text-white">{golpe.titulo}</h3>
                  <span
                    className={`font-mono text-[10px] border px-2 py-0.5 rounded flex-shrink-0 ${severidadeColors[golpe.severidade] || ''}`}
                  >
                    [ {golpe.severidade} ]
                  </span>
                </div>
                <p className="text-[#A0AEC0] text-sm leading-relaxed">{golpe.descricao}</p>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}

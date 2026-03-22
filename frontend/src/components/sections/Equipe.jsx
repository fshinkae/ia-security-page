import { useRef } from 'react'
import { motion, useInView } from 'framer-motion'
import { membros } from '../../data/team'
import StarRating from '../ui/StarRating'

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: (i) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: 'easeOut', delay: i * 0.06 },
  }),
}

function MembroCard({ membro, index }) {
  const githubUrl = membro.github ? `https://github.com/${membro.github}` : null

  return (
    <motion.div
      custom={index}
      variants={cardVariants}
      className="flex flex-col items-center gap-3 group w-24"
    >
      <a
        href={githubUrl || '#'}
        target={githubUrl ? '_blank' : undefined}
        rel="noopener noreferrer"
        className="block relative"
      >
        <div
          className="w-20 h-20 rounded-full overflow-hidden border-2 border-transparent transition-all duration-300"
          style={{
            background: 'linear-gradient(#0D1117, #0D1117) padding-box, linear-gradient(135deg, #E53E3E, #00FFFF) border-box',
          }}
        >
          <img
            src={membro.img}
            alt={membro.nome}
            loading="lazy"
            className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
            onError={(e) => {
              e.currentTarget.onerror = null
              if (membro.github) {
                e.currentTarget.src = `https://github.com/${membro.github}.png`
              } else {
                e.currentTarget.src = '/images/default.jpg'
              }
            }}
          />
        </div>

        {/* GitHub overlay */}
        {githubUrl && (
          <div className="absolute inset-0 rounded-full bg-black/60 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.44 9.8 8.2 11.38.6.11.82-.26.82-.58v-2.03c-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.34-1.76-1.34-1.76-1.09-.75.08-.74.08-.74 1.2.09 1.84 1.24 1.84 1.24 1.07 1.83 2.81 1.3 3.5 1 .11-.78.42-1.3.76-1.6-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.13-.3-.54-1.52.12-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 3-.4c1.02 0 2.04.14 3 .4 2.29-1.55 3.3-1.23 3.3-1.23.66 1.66.24 2.88.12 3.18.77.84 1.24 1.91 1.24 3.22 0 4.61-2.81 5.63-5.49 5.92.43.37.82 1.1.82 2.22v3.29c0 .32.22.7.83.58C20.56 21.8 24 17.3 24 12c0-6.63-5.37-12-12-12z" />
            </svg>
          </div>
        )}
      </a>

      <p className="text-xs text-[#A0AEC0] text-center font-mono">{membro.nome}</p>
    </motion.div>
  )
}

export default function Equipe() {
  const ref = useRef(null)
  const inView = useInView(ref, { once: true, margin: '-60px' })

  return (
    <section id="equipe" className="py-20 px-6">
      <div className="max-w-6xl mx-auto">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.5 }}
          className="font-pixel text-2xl md:text-3xl text-white mb-4 text-center"
        >
          TADS AEMS
        </motion.h2>

        <motion.div
          ref={ref}
          initial="hidden"
          animate={inView ? 'visible' : 'hidden'}
          className="flex flex-wrap justify-center gap-4 sm:gap-6 mb-6"
        >
          {membros.map((m, i) => (
            <MembroCard key={m.nome} membro={m} index={i} />
          ))}
        </motion.div>

        <motion.p
          initial={{ opacity: 0 }}
          animate={inView ? { opacity: 1 } : {}}
          transition={{ duration: 0.5, delay: 0.6 }}
          className="text-center text-[#A0AEC0] text-xs font-mono mb-10"
        >
          Clique nos ícones para acessar os perfis GitHub da equipe.
        </motion.p>

        <div className="flex justify-center">
          <StarRating />
        </div>
      </div>
    </section>
  )
}

import { useRef } from 'react'
import { motion, useInView } from 'framer-motion'
import { newsCards } from '../../data/newsCards'

const badgeColors = {
  'HACKING': 'border-[#E53E3E] text-[#E53E3E]',
  'SEGURANÇA': 'border-[#00FFFF] text-[#00FFFF]',
  'ENGENHARIA SOCIAL': 'border-yellow-400 text-yellow-400',
}

const cardVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: (i) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: 'easeOut', delay: i * 0.15 },
  }),
}

function NewsCard({ card, index }) {
  return (
    <motion.a
      href={card.href}
      target="_blank"
      rel="noopener noreferrer"
      custom={index}
      variants={cardVariants}
      whileHover={{
        y: -6,
        boxShadow: '0 0 30px rgba(229,62,62,0.2), 0 0 60px rgba(0,255,255,0.08)',
      }}
      className="block gradient-border rounded-lg overflow-hidden bg-[#0D1117] cursor-pointer"
    >
      <div className="relative overflow-hidden h-44">
        <img
          src={card.img}
          alt={card.alt}
          loading="lazy"
          className="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
        />
        <span
          className={`absolute top-3 left-3 font-mono text-[10px] border px-2 py-0.5 rounded ${badgeColors[card.badge] || 'border-white/30 text-white/60'}`}
        >
          [ {card.badge} ]
        </span>
      </div>
      <p className="p-4 text-sm text-[#A0AEC0] leading-relaxed hover:text-white transition-colors">
        {card.text}
      </p>
    </motion.a>
  )
}

export default function CasosReais() {
  const ref = useRef(null)
  const inView = useInView(ref, { once: true, margin: '-60px' })

  return (
    <section id="noticias" className="py-20 px-6">
      <div className="max-w-6xl mx-auto">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.5 }}
          className="font-pixel text-2xl md:text-3xl text-white mb-12 text-center"
        >
          Casos Reais
        </motion.h2>

        <motion.div
          ref={ref}
          initial="hidden"
          animate={inView ? 'visible' : 'hidden'}
          className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6"
        >
          {newsCards.map((card, i) => (
            <NewsCard key={card.id} card={card} index={i} />
          ))}
        </motion.div>
      </div>
    </section>
  )
}

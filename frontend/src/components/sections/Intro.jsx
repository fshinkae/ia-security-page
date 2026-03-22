import { useEffect, useRef, useState } from 'react'
import { motion, useInView } from 'framer-motion'

const sectionVariants = {
  hidden: { opacity: 0, y: 40 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: 'easeOut' } },
}

const staggerContainer = {
  visible: { transition: { staggerChildren: 0.15 } },
}

function AnimatedNumber({ target, duration = 2000 }) {
  const [value, setValue] = useState(0)
  const ref = useRef(null)
  const inView = useInView(ref, { once: true })

  useEffect(() => {
    if (!inView) return
    let current = 0
    const step = target / (duration / 16)
    const timer = setInterval(() => {
      current = Math.min(current + step, target)
      setValue(Math.floor(current))
      if (current >= target) clearInterval(timer)
    }, 16)
    return () => clearInterval(timer)
  }, [inView, target, duration])

  return (
    <span ref={ref} className="text-[#E53E3E] font-bold">
      {value.toLocaleString('pt-BR')}
    </span>
  )
}

export default function Intro() {
  const ref = useRef(null)
  const inView = useInView(ref, { once: true, margin: '-80px' })

  return (
    <section className="py-20 px-6">
      <div className="max-w-6xl mx-auto">
        <motion.div
          ref={ref}
          variants={staggerContainer}
          initial="hidden"
          animate={inView ? 'visible' : 'hidden'}
          className="grid md:grid-cols-2 gap-12 items-center"
        >
          {/* Text column */}
          <motion.div variants={sectionVariants} className="space-y-5 text-center md:text-left">
            <h1 className="font-pixel text-2xl md:text-3xl text-white leading-snug">
              A Sociedade e a Vulnerabilidade aos Ataques Virtuais
            </h1>
            <p className="text-[#A0AEC0] leading-relaxed">
              Em tempos cada vez mais conectados, a segurança digital se tornou uma necessidade
              básica. Em 2024, o Brasil registrou mais de{' '}
              <strong className="text-white">
                <AnimatedNumber target={1200000} />
              </strong>{' '}
              golpes virtuais, afetando diretamente pessoas físicas e jurídicas.
            </p>
            <p className="text-[#A0AEC0] leading-relaxed">
              Os vazamentos de dados comprometem não apenas contas bancárias, mas também
              reputações, identidades e até a segurança de famílias inteiras. Hackers e grupos
              criminosos utilizam desde engenharia social até ferramentas sofisticadas para invadir
              sistemas e manipular vítimas.
            </p>
            <p className="text-[#A0AEC0] leading-relaxed">
              Nós do <strong className="text-white">Curso de TADS</strong> temos o papel de oferecer
              informações atualizadas, orientações práticas e apoio à prevenção desses crimes.
              Quanto mais conhecemos os riscos, mais preparados estamos para agir.
            </p>
          </motion.div>

          {/* Image column */}
          <motion.div
            variants={sectionVariants}
            className="flex justify-center"
          >
            <div
              className="rounded-lg overflow-hidden w-full max-w-sm"
              style={{ boxShadow: '0 0 40px rgba(0,255,255,0.15)' }}
            >
              <img
                src="/images/security-image.gif"
                alt="Segurança Digital"
                className="w-full h-auto block rounded-lg"
              />
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  )
}

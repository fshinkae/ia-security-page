import { useRef } from 'react'
import { motion, useInView } from 'framer-motion'

const passos = [
  {
    id: 1,
    img: '/images/informacao.png',
    titulo: 'Reúna as informações',
    descricao: 'prints, e-mails, mensagens, etc.',
  },
  {
    id: 2,
    img: '/images/boletim.png',
    titulo: 'Registre um boletim de ocorrência',
    descricao: (
      <>
        Você pode fazer isso presencialmente ou online via{' '}
        <a
          href="https://delegaciavirtual.sinesp.gov.br/"
          target="_blank"
          rel="noopener noreferrer"
          className="text-[#00FFFF] underline hover:text-white transition-colors"
        >
          Delegacia Virtual
        </a>
        .
      </>
    ),
  },
  {
    id: 3,
    img: '/images/comunique.png',
    titulo: 'Comunique bancos e empresas envolvidas',
    descricao: 'Informe sobre o vazamento para que possam bloquear transações e evitar prejuízos.',
  },
  {
    id: 4,
    img: '/images/Denuncie.png',
    titulo: 'Denuncie em órgãos competentes',
    descricao: (
      <>
        <a
          href="https://www.consumidor.gov.br/"
          target="_blank"
          rel="noopener noreferrer"
          className="text-[#00FFFF] underline hover:text-white transition-colors"
        >
          Consumidor.gov.br
        </a>{' '}
        ou{' '}
        <a
          href="https://www.procon.sp.gov.br/"
          target="_blank"
          rel="noopener noreferrer"
          className="text-[#00FFFF] underline hover:text-white transition-colors"
        >
          Procon
        </a>{' '}
        ajudam na mediação e orientação de consumidores lesados.
      </>
    ),
  },
  {
    id: 5,
    img: '/images/repasse.png',
    titulo: 'Alerte outras pessoas',
    descricao: 'Compartilhe o ocorrido com amigos e familiares para que eles fiquem alertas.',
  },
]

export default function ComoDenunciar() {
  const ref = useRef(null)
  const inView = useInView(ref, { once: true, margin: '-60px' })

  return (
    <section id="denunciar" className="py-20 px-6 bg-[#0D1117]/50">
      <div className="max-w-3xl mx-auto">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.5 }}
          className="font-pixel text-2xl md:text-3xl text-white mb-4 text-center"
        >
          Como Denunciar um Golpe no Brasil
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={inView ? { opacity: 1 } : {}}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-center text-[#A0AEC0] mb-12"
        >
          Siga o passo a passo abaixo para denunciar um golpe ou vazamento de dados:
        </motion.p>

        {/* Timeline */}
        <div ref={ref} className="relative">
          {/* Vertical connector — starts at center of first node (top-8 = 32px = h-16/2) */}
          <div className="absolute left-8 top-8 bottom-8 w-px timeline-line" />

          <div className="space-y-8">
            {passos.map((passo, i) => (
              <motion.div
                key={passo.id}
                initial={{ opacity: 0, x: -30 }}
                animate={inView ? { opacity: 1, x: 0 } : {}}
                transition={{ duration: 0.5, delay: i * 0.15 }}
                className="flex items-start gap-6 relative"
              >
                {/* Node */}
                <div className="flex-shrink-0 w-16 h-16 rounded-full bg-[#0D1117] border-2 border-[#E53E3E] flex items-center justify-center z-10">
                  <img src={passo.img} alt={`Passo ${passo.id}`} className="w-8 h-8 object-contain" />
                </div>

                {/* Content */}
                <div className="gradient-border rounded-lg bg-[#0D1117] p-4 flex-1">
                  <strong className="text-white text-sm">{passo.titulo}:</strong>
                  <p className="text-[#A0AEC0] text-sm mt-1">{passo.descricao}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        <motion.p
          initial={{ opacity: 0 }}
          animate={inView ? { opacity: 1 } : {}}
          transition={{ duration: 0.5, delay: 0.9 }}
          className="text-center text-[#E53E3E] font-mono text-sm mt-10"
        >
          Em caso de emergência, procure a Polícia Civil ou Federal.
        </motion.p>
      </div>
    </section>
  )
}

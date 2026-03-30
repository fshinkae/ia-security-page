import { useState, useRef } from 'react'
import { motion, AnimatePresence, useInView } from 'framer-motion'
import { questions } from '../../data/quizQuestions'

const TOTAL = questions.length

function ResultGauge({ score }) {
  const pct = (score / TOTAL) * 100
  const circumference = 2 * Math.PI * 54
  const offset = circumference - (pct / 100) * circumference

  const level =
    score >= 8
      ? { label: 'Alto Nível de Segurança', color: '#00FFFF', cls: 'text-[#00FFFF]' }
      : score >= 5
      ? { label: 'Nível Médio de Segurança', color: '#FFD700', cls: 'text-yellow-400' }
      : { label: 'Baixo Nível de Segurança', color: '#E53E3E', cls: 'text-[#E53E3E]' }

  return (
    <div className="flex flex-col items-center gap-4">
      <svg width="128" height="128" viewBox="0 0 128 128">
        <circle cx="64" cy="64" r="54" fill="none" stroke="#1a1f2e" strokeWidth="12" />
        <motion.circle
          cx="64"
          cy="64"
          r="54"
          fill="none"
          stroke={level.color}
          strokeWidth="12"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.2, ease: 'easeOut' }}
          style={{ transform: 'rotate(-90deg)', transformOrigin: '64px 64px' }}
        />
        <text x="64" y="60" textAnchor="middle" fill="white" fontSize="28" fontFamily="JetBrains Mono" fontWeight="bold">
          {score}
        </text>
        <text x="64" y="80" textAnchor="middle" fill="#A0AEC0" fontSize="13" fontFamily="JetBrains Mono">
          /{TOTAL}
        </text>
      </svg>
      <span className={`font-mono text-sm font-bold ${level.cls}`}>{level.label}</span>
    </div>
  )
}

function QuizModal({ onClose }) {
  const [answers, setAnswers] = useState({})
  const [currentQ, setCurrentQ] = useState(0)
  const [result, setResult] = useState(null)
  const [direction, setDirection] = useState(1)

  const question = questions[currentQ]
  const progress = ((currentQ) / TOTAL) * 100

  const handleAnswer = (id, value) => {
    setAnswers((prev) => ({ ...prev, [id]: value }))
  }

  const goNext = () => {
    if (!answers[question.id]) {
      alert('Por favor, responda a pergunta antes de continuar.')
      return
    }
    if (currentQ < TOTAL - 1) {
      setDirection(1)
      setCurrentQ((q) => q + 1)
    }
  }

  const goPrev = () => {
    if (currentQ > 0) {
      setDirection(-1)
      setCurrentQ((q) => q - 1)
    }
  }

  const handleSubmit = () => {
    if (!answers[question.id]) {
      alert('Por favor, responda a pergunta antes de ver o resultado.')
      return
    }
    let score = 0
    const wrong = []
    questions.forEach((q) => {
      if (answers[q.id] === q.respostaSegura) score++
      else wrong.push(q)
    })
    setResult({ score, wrong })
  }

  const handleRetry = () => {
    setAnswers({})
    setCurrentQ(0)
    setResult(null)
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        onClick={(e) => e.stopPropagation()}
        className="bg-[#0D1117] border border-white/10 rounded-xl w-full max-w-xl max-h-[90vh] overflow-y-auto relative mx-2"
        style={{ boxShadow: '0 0 60px rgba(229,62,62,0.15)' }}
      >
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-white/40 hover:text-white text-2xl leading-none transition-colors z-10"
        >
          &times;
        </button>

        <div className="p-4 sm:p-8">
          <h2 className="font-pixel text-xl text-white mb-1 text-center">
            Questionário de Segurança Digital
          </h2>
          <p className="text-[#A0AEC0] text-sm text-center mb-6">
            Responda as perguntas e descubra o quanto você está protegido.
          </p>

          {!result ? (
            <>
              {/* Progress bar */}
              <div className="w-full h-1.5 bg-white/10 rounded-full mb-8">
                <motion.div
                  className="h-full bg-gradient-to-r from-[#E53E3E] to-[#00FFFF] rounded-full"
                  animate={{ width: `${progress}%` }}
                  transition={{ duration: 0.3 }}
                />
              </div>

              <AnimatePresence mode="wait" custom={direction}>
                <motion.div
                  key={currentQ}
                  custom={direction}
                  initial={{ opacity: 0, x: direction * 40 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -direction * 40 }}
                  transition={{ duration: 0.3 }}
                  className="gradient-border rounded-lg p-6 bg-[#080B0F]"
                >
                  <span className="font-mono text-[#E53E3E] text-xs mb-3 block">
                    {question.numero} / {String(TOTAL).padStart(2, '0')}
                  </span>
                  <p className="text-white text-sm leading-relaxed mb-6">{question.pergunta}</p>

                  <div className="flex gap-4">
                    {['sim', 'nao'].map((val) => (
                      <label
                        key={val}
                        className="flex-1 cursor-pointer"
                      >
                        <input
                          type="radio"
                          name={question.id}
                          value={val}
                          checked={answers[question.id] === val}
                          onChange={() => handleAnswer(question.id, val)}
                          className="sr-only"
                        />
                        <div
                          className="text-center py-3 rounded border transition-all duration-200 font-mono text-sm"
                          style={{
                            borderColor: answers[question.id] === val ? '#00FFFF' : 'rgba(255,255,255,0.1)',
                            color: answers[question.id] === val ? '#00FFFF' : '#A0AEC0',
                            background: answers[question.id] === val ? 'rgba(0,255,255,0.07)' : 'transparent',
                          }}
                        >
                          {val === 'sim' ? 'Sim' : 'Não'}
                        </div>
                      </label>
                    ))}
                  </div>
                </motion.div>
              </AnimatePresence>

              {/* Navigation */}
              <div className="flex justify-between items-center mt-6">
                <button
                  onClick={goPrev}
                  disabled={currentQ === 0}
                  className="font-mono text-xs text-[#A0AEC0] hover:text-white transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
                >
                  ← Anterior
                </button>

                {currentQ < TOTAL - 1 ? (
                  <button
                    onClick={goNext}
                    className="px-5 py-2 bg-[#E53E3E] text-white font-mono text-xs rounded hover:bg-[#C53030] transition-colors"
                  >
                    Próxima →
                  </button>
                ) : (
                  <button
                    onClick={handleSubmit}
                    className="px-5 py-2 bg-[#E53E3E] text-white font-mono text-xs rounded hover:bg-[#C53030] transition-colors"
                  >
                    Ver Resultado
                  </button>
                )}
              </div>
            </>
          ) : (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <ResultGauge score={result.score} />

              <div className="mt-6 text-center text-sm text-[#A0AEC0]">
                {result.score >= 8
                  ? 'Parabéns! Você tem ótimos hábitos de segurança digital. Continue assim e mantenha-se atualizado sobre novas ameaças.'
                  : result.score >= 5
                  ? 'Você já tem boas práticas, mas ainda há pontos a melhorar. Veja as dicas abaixo para se proteger ainda mais.'
                  : 'Atenção! Seus hábitos digitais precisam de ajustes importantes. Siga as dicas abaixo para se proteger contra golpes e ataques.'}
              </div>

              {result.wrong.length > 0 && (
                <div className="mt-6">
                  <h3 className="font-pixel text-sm text-white mb-3">Pontos para melhorar:</h3>
                  <div className="space-y-3">
                    {result.wrong.map((q) => (
                      <div
                        key={q.id}
                        className="flex gap-3 items-start bg-[#080B0F] rounded p-3 border border-[#E53E3E]/20"
                      >
                        <span className="text-[#E53E3E] font-mono text-lg leading-none mt-0.5">!</span>
                        <p className="text-[#A0AEC0] text-xs leading-relaxed">{q.dica}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {result.wrong.length === 0 && (
                <p className="mt-4 text-center text-[#00FFFF] font-mono text-sm">
                  Incrível! Você acertou tudo. Seus hábitos de segurança são exemplares!
                </p>
              )}

              <button
                onClick={handleRetry}
                className="mt-6 w-full py-3 border border-[#E53E3E] text-[#E53E3E] font-mono text-sm rounded hover:bg-[#E53E3E] hover:text-white transition-colors"
              >
                Tentar Novamente
              </button>
            </motion.div>
          )}
        </div>
      </motion.div>
    </motion.div>
  )
}

export default function Questionario() {
  const [open, setOpen] = useState(false)
  const ref = useRef(null)
  const inView = useInView(ref, { once: true, margin: '-60px' })

  return (
    <section id="quiz" className="py-20 px-6 bg-[#0D1117]/50">
      <div ref={ref} className="max-w-2xl mx-auto text-center">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.5 }}
          className="font-pixel text-2xl md:text-3xl text-white mb-4"
        >
          Teste Seu Nível de Segurança
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={inView ? { opacity: 1 } : {}}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-[#A0AEC0] mb-8"
        >
          Descubra o quanto você está protegido no mundo digital respondendo{' '}
          <span className="font-mono text-white">{TOTAL}</span> perguntas simples.
        </motion.p>

        <motion.button
          initial={{ opacity: 0, y: 10 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.5, delay: 0.2 }}
          onClick={() => setOpen(true)}
          whileHover={{ scale: 1.05, boxShadow: '0 0 20px rgba(229,62,62,0.4)' }}
          whileTap={{ scale: 0.97 }}
          className="px-8 py-3 bg-[#E53E3E] text-white font-pixel text-sm rounded-sm tracking-widest uppercase cursor-pointer"
        >
          Iniciar Questionário
        </motion.button>
      </div>

      <AnimatePresence>
        {open && <QuizModal onClose={() => setOpen(false)} />}
      </AnimatePresence>
    </section>
  )
}

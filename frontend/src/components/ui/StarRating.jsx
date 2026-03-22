import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const FORM_URL =
  'https://docs.google.com/forms/d/e/1FAIpQLSfI2NzkjYZ4WHdTw7-qTw-lERDfXlVpr7m7hIO1ChrxGneKMw/formResponse'
const ENTRY_ID = 'entry.971847553'

export default function StarRating() {
  const [open, setOpen] = useState(false)
  const [selected, setSelected] = useState(0)
  const [hovered, setHovered] = useState(0)
  const [sent, setSent] = useState(false)

  const handleSubmit = () => {
    if (!selected) {
      alert('Por favor, selecione uma avaliação antes de enviar.')
      return
    }
    const formData = new FormData()
    formData.append(ENTRY_ID, selected)
    fetch(FORM_URL, { method: 'POST', mode: 'no-cors', body: formData })
      .then(() => {
        setSent(true)
        setTimeout(() => {
          setOpen(false)
          setSent(false)
          setSelected(0)
        }, 1800)
      })
      .catch(() => alert('Erro ao enviar a avaliação.'))
  }

  return (
    <>
      <motion.button
        onClick={() => setOpen(true)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="px-6 py-2 border border-[#E53E3E] text-[#E53E3E] font-mono text-sm rounded hover:bg-[#E53E3E] hover:text-white transition-colors duration-200"
      >
        Avalie-nos
      </motion.button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
            onClick={() => setOpen(false)}
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-[#0D1117] border border-[#E53E3E]/30 rounded-lg p-8 w-full max-w-sm text-center"
              style={{ boxShadow: '0 0 40px rgba(229,62,62,0.15)' }}
            >
              <h2 className="font-pixel text-xl text-white mb-6">Avalie-nos</h2>

              {sent ? (
                <p className="text-[#00FFFF] font-mono">Avaliação enviada! Obrigado.</p>
              ) : (
                <>
                  <div className="flex justify-center gap-2 mb-6">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        key={star}
                        onClick={() => setSelected(star)}
                        onMouseEnter={() => setHovered(star)}
                        onMouseLeave={() => setHovered(0)}
                        className="text-3xl transition-transform hover:scale-125"
                        style={{
                          color: star <= (hovered || selected) ? '#FFD700' : '#374151',
                        }}
                      >
                        ★
                      </button>
                    ))}
                  </div>

                  <div className="flex gap-3 justify-center">
                    <button
                      onClick={handleSubmit}
                      className="px-5 py-2 bg-[#E53E3E] text-white font-mono text-sm rounded hover:bg-[#C53030] transition-colors"
                    >
                      Enviar
                    </button>
                    <button
                      onClick={() => setOpen(false)}
                      className="px-5 py-2 border border-white/20 text-white/60 font-mono text-sm rounded hover:border-white/40 transition-colors"
                    >
                      Fechar
                    </button>
                  </div>
                </>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}

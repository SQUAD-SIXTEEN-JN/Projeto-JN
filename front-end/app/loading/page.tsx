import { Sidebar } from "../_components/Sidebar"
import Image from "next/image"

export default function ChatbotPage() {
  return (
    <div className="flex min-h-screen">
      {/* Sidebar fixa */}
      <Sidebar />

      {/* Área principal */}
      <main className="flex-1 bg-[#FCF8ED] relative">
        
        {/* Logo Jotanunes no topo direito */}
        <div className="absolute top-6 right-6 z-10">
          <Image
            src="/logo-preta.svg"
            alt="Jotanunes Construtora"
            width={200}
            height={54}
            className="h-auto"
          />
        </div>

        {/* Fundo decorativo */}
        <div className="absolute inset-0 z-0">
          <Image
            src="/background-decorado.png"
            alt="Fundo decorado"
            layout="fill"
            objectFit="cover"
          />
        </div>

        {/* Conteúdo centralizado */}
        <div className="flex items-center justify-center min-h-screen z-10 relative">
          <div className="flex flex-col items-center space-y-4">
            
            {/* GIF de carregamento — tamanho aumentado */}
            <div className="w-40 h-40">
              <img
                src="/carregando.gif"
                alt="Carregando"
                className="w-full h-full object-contain"
              />
            </div>

            {/* Texto abaixo da animação */}
            <p className="text-black text-center text-lg font-medium">
              Estamos carregando, aguarde...
            </p>
          </div>
        </div>
      </main>
    </div>
  )
}

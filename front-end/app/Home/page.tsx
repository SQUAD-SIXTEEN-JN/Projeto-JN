import Image from "next/image";

import { Sidebar } from "../_components/Sidebar"
import { CourseCarousel } from "../_components/Course-carousel"

export default function Home() {
  return (
    <div className="flex h-screen bg-[#FCF8ED]">
      <Sidebar />
      <main className="flex-1 overflow-auto">
        <div className="flex justify-end p-2">
          <Image
            src="/logo-preta.svg"
            alt="Jotanunes Construtora"
            width={100}
            height={25}
            className="h-auto"
          />
        </div>

        <div className="px-4 py-3">
          <div className="flex flex-col lg:flex-row-reverse items-center mb-6 relative">
            {/* A imagem agora tem uma margem extra à direita */}
            <div className="relative w-full lg:w-2/5 lg:mr-24 lg:order-2">
              <Image
                src="/foto-objeto.svg"
                alt="Ilustração de pessoas estudando"
                width={400}
                height={240}
                className="w-full h-auto"
              />
            </div>

            {/* A frase agora tem uma margem extra à esquerda */}
            <div className="w-full lg:w-2/5 mt-3 lg:mt-0 lg:order-1 lg:ml-24">
              <h1 className="text-2xl lg:text-4xl font-bold text-center lg:text-left">
                <span className="text-black">Pequenos</span>
                <br />
                <span className="text-red-600">Passos</span>
                <span className="text-black">,</span>
                <br />
                <span className="text-black">Grandes</span>
                <br />
                <span className="text-red-600">Conquistas!</span>
              </h1>
            </div>
          </div>
<h2 className="text-2xl font-bold text-gray-900 pl-2">Novidades</h2>
          <div className="mt-4">
            <CourseCarousel />
          </div>
        </div>
      </main>
    </div>
  )
}
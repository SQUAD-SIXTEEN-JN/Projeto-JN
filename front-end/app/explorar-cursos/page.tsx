import Image from "next/image"
import { Sidebar } from "../_components/Sidebar"
import { CourseCarousel } from "../_components/Course-carousel"

interface CourseCardProps {
  title: string
  modules: number
  duration: string
  students: number
  image: string
  professor: string
  rating: number
}

export default function ExplorePage() {
  return (
    <div className="flex h-screen bg-[#FDF9ED]">
      <Sidebar />

      <main className="flex-1 px-6 py-6 overflow-y-auto">
        <div className="flex justify-between items-start mb-6 mt-8">
          <h1 className="text-4xl font-bold text-gray-900">Explorar Cursos</h1>
          <Image src="/logo-preta.svg" alt="Logo" width={140} height={50} />
        </div>

        <section className="mb-10">
          <h2 className="text-lg font-semibold mb-4 text-gray-900 ">Adicionados recentemente!</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <CourseCard
              title="Design de interiores – Para iniciantes."
              modules={6}
              duration="11h 20m"
              students={22}
              image="/course-image-1.svg"
              professor="Professor 1"
              rating={4.8}
            />
            <CourseCard
              title="Materiais e técnicas construtivas"
              modules={60}
              duration="70h 45m"
              students={202}
              image="/course-image-2.svg"
              professor="Professor 2"
              rating={4.5}
            />
            <CourseCard
              title="Desenho e representação"
              modules={8}
              duration="18h 20m"
              students={66}
              image="/course-image-3.svg"
              professor="Professor 3"
              rating={4.8}
            />
          </div>
        </section>

        <section>
          <h2 className="text-lg font-semibold mb-4 text-gray-900">Disponíveis para você!</h2>
          <CourseCarousel />
        </section>
      </main>
    </div>
  )
}

function CourseCard({ title, modules, duration, students, image, professor, rating }: CourseCardProps) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden flex flex-col">
      <div className="relative h-40 w-full">
        <Image src={image} alt={title} fill className="object-cover" />
      </div>

      <div className="p-4 flex flex-col gap-2 flex-1">
        <div className="flex gap-2 text-xs text-gray-500 font-medium">
          <span className="bg-gray-100 px-2 py-0.5 rounded-full">Arquitetura</span>
          <span className="text-gray-400 line-through">Com</span>
          <span className="text-black font-semibold">Certificado</span>
        </div>

        <h3 className="font-semibold text-sm text-gray-800">{title}</h3>

        <div className="flex items-center gap-2 text-xs text-gray-600">
          <div className="flex items-center gap-1">
            <Image src="/avatar-placeholder.png" alt={professor} width={20} height={20} className="rounded-full" />
            {professor}
          </div>
          <div className="flex items-center gap-1 text-yellow-500">
            ★ <span className="text-gray-600">{rating.toFixed(1)} Avaliações</span>
          </div>
        </div>

        <div className="flex justify-between text-xs text-gray-500 mt-auto pt-2 border-t border-gray-100">
          <span className="flex items-center gap-1">
            📘 {modules.toString().padStart(2, "0")}
          </span>
          <span className="flex items-center gap-1">
            ⏱ {duration}
          </span>
          <span className="flex items-center gap-1">
            🎓 {students}
          </span>
        </div>
      </div>
    </div>
  )
}

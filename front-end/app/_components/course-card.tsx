import Link from "next/link"
import Image from "next/image"

interface CourseCardProps {
  title: string
  modules: number
  duration: string
  image: string
}

export function CourseCard({ title, modules, duration, image }: CourseCardProps) {
  return (
    <Link href="/curso" className="block">
      <div className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-100 h-full hover:shadow-lg transition-shadow duration-200">
        <div className="h-40 relative">
          <Image src={image || "/placeholder.svg"} alt={title} fill className="object-cover" />
        </div>
        <div className="p-4">
          <h3 className="font-medium text-sm mb-3">{title}</h3>
          <div className="flex items-center justify-between text-sm text-gray-500">
            <div className="flex items-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="mr-1"
              >
                <path d="M18 3v17a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V3m12 0H6a2 2 0 0 0-2 2v17a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2Z" />
                <path d="M9 17h6" />
              </svg>
              {modules} Módulos ({duration})
            </div>
            <span className="text-red-600">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <circle cx="12" cy="12" r="10" />
                <path d="m12 8 4 4-4 4" />
                <path d="m8 12h8" />
              </svg>
            </span>
          </div>
        </div>
      </div>
    </Link>
  )
}

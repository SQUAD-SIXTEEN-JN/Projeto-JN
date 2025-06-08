"use client"

import { useState, useRef, useEffect } from "react"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { CourseCard } from "./course-card"

interface Course {
  id: number
  title: string
  modules: number
  duration: string
  image: string
}

export function CourseCarousel() {
  const [currentIndex, setCurrentIndex] = useState(0)
  const carouselRef = useRef<HTMLDivElement>(null)

  const courses: Course[] = [
    {
      id: 1,
      title: "Técnicas de Alvenaria Estrutural",
      modules: 12,
      duration: "18h 45m",
      image: "/course-image-1.svg",
    },
    {
      id: 2,
      title: "Instalações Hidráulicas Residenciais",
      modules: 8,
      duration: "14h 20m",
      image: "/course-image-2.svg",
    },
    {
      id: 3,
      title: "Fundações e Estruturas de Concreto",
      modules: 15,
      duration: "22h 30m",
      image: "/course-image-3.svg",
    },
    {
      id: 4,
      title: "Gestão de Obras e Projetos",
      modules: 10,
      duration: "16h 15m",
      image: "/course-image-1.svg",
    },
    {
      id: 5,
      title: "Técnicas de Acabamento e Revestimento",
      modules: 9,
      duration: "15h 40m",
      image: "/course-image-2.svg",
    },
    {
      id: 6,
      title: "Segurança no Trabalho na Construção Civil",
      modules: 7,
      duration: "12h 30m",
      image: "/course-image-2.svg",
    },
  ]

  const visibleCourses = 3
  const maxIndex = courses.length - visibleCourses

  const nextSlide = () => {
    if (currentIndex < maxIndex) {
      setCurrentIndex(currentIndex + 1)
    }
  }

  const prevSlide = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1)
    }
  }

  useEffect(() => {
    if (carouselRef.current) {
      const scrollAmount = currentIndex * (carouselRef.current.scrollWidth / courses.length)
      carouselRef.current.scrollTo({
        left: scrollAmount,
        behavior: "smooth",
      })
    }
  }, [currentIndex, courses.length])

  return (
    <div className="relative">
      <div className="flex justify-between items-center mb-4">
        
        <div className="flex space-x-2">
          <button
            onClick={prevSlide}
            disabled={currentIndex === 0}
            className={`p-2 rounded-full ${currentIndex === 0 ? "text-gray-300" : "text-gray-700 hover:bg-gray-100"}`}
            aria-label="Slide anterior"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <button
            onClick={nextSlide}
            disabled={currentIndex >= maxIndex}
            className={`p-2 rounded-full ${currentIndex >= maxIndex ? "text-gray-300" : "text-gray-700 hover:bg-gray-100"}`}
            aria-label="Próximo slide"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </div>

      <div className="relative overflow-hidden">
        <div
          ref={carouselRef}
          className="flex transition-transform duration-300 ease-in-out"
          style={{ transform: `translateX(-${currentIndex * (100 / courses.length)}%)` }}
        >
          {courses.map((course) => (
            <div key={course.id} className="min-w-[calc(100%/3-16px)] px-2">
              <CourseCard
                title={course.title}
                modules={course.modules}
                duration={course.duration}
                image={course.image}
              />
            </div>
          ))}
        </div>
      </div>

      <div className="flex justify-center mt-4">
        {Array.from({ length: maxIndex + 1 }).map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentIndex(index)}
            className={`w-2 h-2 mx-1 rounded-full ${currentIndex === index ? "bg-[#BC1F1B]" : "bg-gray-300"}`}
            aria-label={`Ir para slide ${index + 1}`}
          />
        ))}
      </div>
    </div>
  )
}
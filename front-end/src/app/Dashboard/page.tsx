"use client";
import { useEffect, useState } from "react";
import { isAuthenticated, getCurrentUser, logout } from "../../services/authService";
import { useRouter } from "next/navigation";

// Definir o tipo do usuário
type User = {
  id: number;
  matricula: string;
  nome: string;
  curso: string;
};

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/");
      return;
    }
    
    const currentUser = getCurrentUser();
    setUser(currentUser);
  }, [router]);

  const handleLogout = () => {
    logout();
    router.push("/");
  };

  if (!user) {
    return <div>Carregando...</div>;
  }

  // Neste ponto, o TypeScript sabe que user não é null
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div className="bg-white p-6 rounded shadow-md">
        <h2 className="text-xl mb-4">Bem-vindo, {user.nome}!</h2>
        <p>Matrícula: {user.matricula}</p>
        <p>Curso: {user.curso}</p>
        <button 
          onClick={handleLogout}
          className="mt-4 bg-red-500 text-white px-4 py-2 rounded"
        >
          Sair
        </button>
      </div>
    </div>
  );
}
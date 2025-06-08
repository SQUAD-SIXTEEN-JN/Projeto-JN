// src/app/login/page.jsx
"use client";
import { useState, useEffect } from "react";
import { HeaderLogin } from "./_components/HeaderLogin";
import Image from "next/image";
import { BadgeIcon, Lock, LogIn } from 'lucide-react'; // Certifique-se de que BadgeIcon está disponível
import Link from 'next/link';
import { login } from "@/services/authService";
import { useRouter } from "next/navigation";

export default function Login() {
  const [matricula, setMatricula] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [authStatus, setAuthStatus] = useState("checking");
  const router = useRouter();
  
  useEffect(() => {
    // Verificar se o usuário já está logado usando localStorage
    const storedUser = localStorage.getItem('user');
    const storedToken = localStorage.getItem('token');
    
    if (storedUser && storedToken) {
      setAuthStatus("logged-in");
      console.log("Usuário já está logado:", JSON.parse(storedUser));
      router.push("/Dashboard");
    } else {
      setAuthStatus("logged-out");
      console.log("Usuário não está logado");
    }
  }, [router]);
  
  const handleSignIn = async (e) => {
    e.preventDefault(); 
    setLoading(true);
    setError(null);
    
    console.log("Tentando login com:", matricula, password);
    
    try {
      const response = await login(matricula, password);
      
      if (response.success) {
        console.log("Usuário logado com sucesso:", response.user);
        router.push("/Dashboard");
      } else {
        // Tratamento de erro baseado na mensagem retornada
        let errorMessage = "Ocorreu um erro ao fazer login. Tente novamente.";
        
        if (response.message === "wrong_credentials") {
          errorMessage = "Matrícula ou senha incorreta. Tente novamente.";
        } else if (response.message === "user_not_found") {
          errorMessage = "Matrícula não encontrada. Verifique seus dados.";
        } else if (response.message === "service_error") {
          errorMessage = "Erro no serviço de autenticação. Tente novamente mais tarde.";
        }
        
        setError(errorMessage);
      }
    } catch (error) {
      console.error("Erro ao logar:", error);
      setError("Ocorreu um erro inesperado. Tente novamente mais tarde.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <HeaderLogin />
      <main className="grid grid-cols-1 md:grid-cols-2 justify-items-center p-4">
        <div className="justify-items-center text-[39px] md:text-4xl p-4">
          <Image
            src="/photocard.svg"
            alt="Foto do mascote em Card"
            width={470}
            height={318}
            priority
            className="mb-8 md:mb-12 w-full md:w-auto max-w-full"
          />
          <h1 className="text-center text-2xl md:text-3xl font-black text-[#010101]">
            Moldando Seu Futuro <br />
            Conosco.
          </h1>
        </div>

        <div className="mt-8 md:mt-[50px] text-xl md:text-2xl text-center p-6 md:mr-10">
          <h1 className="mb-6 md:mb-[42px] leading-[44px]">
            Faça login para entrar em sua <br />
            jornada de aprendizado
          </h1>

          <form onSubmit={handleSignIn}>
            <div className="relative">
              <input
                type="text"
                id="matricula"
                required
                placeholder="Matrícula"
                className="pl-10 pr-20 py-3 md:py-[24px] border w-full border-[#757575] mb-[18px]"
                value={matricula}
                onChange={(e) => setMatricula(e.target.value)}
              />
              <BadgeIcon className="w-5 h-5 text-gray-500 absolute left-3 top-[40px] transform -translate-y-1/2" />
            </div>
            <div className="relative">
              <input
                type="password"
                id="password"
                required
                placeholder="Senha"
                className="pl-10 pr-20 py-3 md:py-[24px] border w-full border-[#757575] mb-[18px]"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <Lock className="w-5 h-5 text-gray-500 absolute left-3 top-[40px] transform -translate-y-1/2" />
            </div>
            {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
            <div className="mb-[25px]">
              <button
                type="submit"
                disabled={loading}
                className="w-full md:w-[450px] max-w-full bg-[#D1484C] text-white cursor-pointer py-[22px] px-[35px] flex justify-between items-center font-medium"
              >
                <span>{loading ? "Entrando..." : "Entrar"}</span>
                {loading ? (
                  <span className="animate-spin">⟳</span>
                ) : (
                  <LogIn size={24} />
                )}
              </button>
            </div>
            <Link href="/esqueceusenha" className="text-[14px] text-[#424242] underline">
              Esqueceu a senha?
            </Link>
          </form>
          
          {/* Informação de debug */}
          { /* process.env.NODE_ENV === 'development' && (
            <div className="mt-8 p-3 bg-gray-100 text-xs text-left rounded">
              <p className="font-bold">Credenciais de teste:</p>
              <p>Matrícula: 12345</p>
              <p>Senha: senha123</p>
              <p className="mt-2">Status: {authStatus}</p>
            </div>
          ) */} 
        </div>
      </main>
    </div>
  );
}
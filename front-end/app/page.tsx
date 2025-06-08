"use client";
import React, { useState, FormEvent } from "react";
import { HeaderLogin } from "./_components/HeaderLogin";
import Image from "next/image";
import { BadgeIcon, Lock, LogIn } from "lucide-react";
import { useRouter } from "next/navigation";
import { login } from "@/services/auth";  // Importando a função login do auth.ts

interface LoginResponse {
  success: boolean;
  first_acess?: boolean;  // Presumo que isso é boolean e opcional
  message?: string;
  username?: string;
}

export default function Login() {
  const [matricula, setMatricula] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const router = useRouter();

  const handleSignIn = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    if (!matricula || !password) {
      setError("Preencha todos os campos.");
      setLoading(false);
      return;
    }

    try {
      const response: LoginResponse = await login(matricula, password);

      if (response.success) {
        setMatricula("");
        setPassword("");

        console.log("Nome recebido:", response.username);
        if (response.username) {
          localStorage.setItem('nomeUsuario', response.username);
        }

        // Redireciona de forma condicional
        router.push(response.first_acess ? "/Home" : "/Home");
      } else {
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
      <main className="grid grid-cols-1 md:grid-cols-2 justify-items-center p-4 bg-white text-black min-h-screen">
        <div className="justify-items-center text-[39px] md:text-4xl p-4">
          <Image
            src="/photocard.svg"
            alt="Foto do mascote em Card"
            width={470}
            height={318}
            priority
            className="mb-8 md:mb-12 w-full md:w-auto max-w-full"
          />
          <h1 className="text-center text-2xl md:text-3xl font-black text-black">
            Moldando Seu Futuro <br />
            Conosco.
          </h1>
        </div>

        <div className="mt-8 md:mt-[50px] text-xl md:text-2xl text-center p-6 md:mr-10">
          <h1 className="mb-6 md:mb-[42px] leading-[44px] text-black">
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
                className="pl-10 pr-20 py-3 md:py-[24px] border w-full border-[#757575] mb-[18px] bg-transparent text-black placeholder-gray-500"
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
                className="pl-10 pr-20 py-3 md:py-[24px] border w-full border-[#757575] mb-[18px] bg-transparent text-black placeholder-gray-500"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <Lock className="w-5 h-5 text-gray-500 absolute left-3 top-[40px] transform -translate-y-1/2" />
            </div>
            {error && <p className="text-red-500 text-sm mb-4" aria-live="assertive">{error}</p>}
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
          </form>
        </div>
      </main>
    </div>
  );
}

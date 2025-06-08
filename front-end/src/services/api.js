// src/services/api.js
export const loginApi = async (matricula, password) => {
    // Versão mock
    return new Promise((resolve) => {
      setTimeout(() => {
        if (matricula === "12345" && password === "senha123") {
          resolve({
            success: true,
            user: { id: 1, matricula, nome: "Aluno Exemplo", curso: "Engenharia Civil" },
            token: "mock-token-123"
          });
        } else {
          resolve({ success: false, message: "wrong_credentials" });
        }
      }, 800);
    });
  };
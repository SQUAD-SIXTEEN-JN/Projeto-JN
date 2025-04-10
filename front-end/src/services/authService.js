// src/services/authService.js
import { loginApi } from './api';

export const login = async (matricula, password) => {
  try {
    const response = await loginApi(matricula, password);
    
    if (response.success) {
      // Armazenar dados do usuário e token
      localStorage.setItem('user', JSON.stringify(response.user));
      localStorage.setItem('token', response.token);
    }
    
    return response;
  } catch (error) {
    console.error("Erro no serviço de autenticação:", error);
    return { success: false, message: "service_error" };
  }
};

// Função para verificar se o usuário está logado
export const isAuthenticated = () => {
  if (typeof window === 'undefined') return false;
  return localStorage.getItem('token') !== null;
};

// Função para obter o usuário atual
export const getCurrentUser = () => {
  if (typeof window === 'undefined') return null;
  const user = localStorage.getItem('user');
  return user ? JSON.parse(user) : null;
};

// Função para logout
export const logout = () => {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('user');
  localStorage.removeItem('token');
};
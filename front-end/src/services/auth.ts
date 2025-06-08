

export async function login(matricula: string, senha: string) {
  try {
    const response = await fetch('http://ec2-3-94-61-97.compute-1.amazonaws.com:8000/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        matricula: parseInt(matricula),
        senha: senha,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      return {
        success: false,
        message: error.detail || 'Erro desconhecido',
      };
    }

    const data = await response.json();
    return {
      success: true,
      token: data.token,
      first_acess: data.primeiro_acesso,
      username: data.username,
    };
  } catch (error) {
    console.error("Erro no login:", error);
    return {
      success: false,
      message: "service_error",
    };
  }
}

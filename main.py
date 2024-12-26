import os
import venv
import subprocess

class AmbienteVirtual:
    """
    Classe para gerenciar a criação e configuração de ambientes virtuais Python, incluindo a instalação de dependências.
    
    A classe fornece métodos para:
    - Criar um ambiente virtual.
    - Instalar dependências a partir de um arquivo de requisitos.
    - Salvar dependências instaladas em um arquivo de requisitos.
    - Exibir instruções sobre como ativar e usar o ambiente virtual.
    
    Attributes:
        nome_env (str): O nome do ambiente virtual. O valor padrão é 'venv'.
        requirements_txt (str): O nome do arquivo que contém os requisitos do pip. O valor padrão é 'req.txt'.
    """
    
    def __init__(self, nome_env="venv", requirements_txt="req.txt"):    
        """
        Inicializa o objeto AmbienteVirtual com o nome do ambiente e o arquivo de requisitos.

        :param nome_env: Nome do ambiente virtual (default "venv").
        :param requirements_txt: Nome do arquivo de requisitos pip (default "req.txt").
        """
        self.nome_env = nome_env
        self.requirements_txt = requirements_txt

    def ambiente_existe(self):
        """
        Verifica se o ambiente virtual já existe.

        :return: True se o ambiente virtual existir, caso contrário False.
        """
        return os.path.exists(self.nome_env)

    def cria_ambiente_virtual(self, instrucoes=True):
        """
        Cria um novo ambiente virtual e instala as dependências.

        :param instrucoes: Se True, exibe instruções após a criação do ambiente virtual. Default é True.
        """
        if self.ambiente_existe():
            print(f"O ambiente virtual '{self.nome_env}' já existe.")
        else:
            self._criar_ambiente()

        self._instalar_dependencias()
        if instrucoes:
            self.exibir_instrucoes()

    def salvar_requirements(self):
        """
        Salva as dependências instaladas no ambiente virtual em um arquivo 'requirements.txt'.
        """
        with open(self.requirements_txt, 'w') as req_file:
            subprocess.run(['pip', 'freeze'], stdout=req_file)
            print(f"Dependências salvas em '{self.requirements_txt}'.")

    def _criar_ambiente(self):
        """
        Cria o ambiente virtual com o pip integrado.
        """
        try:
            venv.create(self.nome_env, with_pip=True)
            print(f"Ambiente virtual '{self.nome_env}' criado com sucesso!")
        except Exception as e:
            print(f"Erro ao criar o ambiente virtual: {e}")

    def _instalar_dependencias(self):
        """
        Instala as dependências a partir do arquivo 'requirements.txt'.
        """
        req_txt_path = os.path.join(os.getcwd(), self.requirements_txt)
        
        if not os.path.isfile(req_txt_path):
            print(f"Arquivo '{self.requirements_txt}' não encontrado.")
            return

        pip_executable = self._get_pip_executable()
        if not pip_executable:
            print("Erro ao localizar o executável do pip.")
            return

        try:
            subprocess.check_call([pip_executable, "install", "-r", self.requirements_txt])
            print("Dependências instaladas com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao instalar dependências: {e}")

    def _get_pip_executable(self):
        """
        Retorna o caminho do executável pip dependendo do sistema operacional.

        :return: Caminho do executável do pip ou None se não encontrado.
        """
        if os.name == "nt":  # Windows
            return os.path.join(self.nome_env, "Scripts", "pip")
        elif os.name == "posix":  # macOS/Linux
            return os.path.join(self.nome_env, "bin", "pip")
        return None

    def exibir_instrucoes(self):
        """
        Exibe instruções para ativar o ambiente virtual e acessar o diretório do projeto.
        """
        comando_ativacao = self._get_comando_ativacao()
        print(f"Para ativar o ambiente virtual, execute: {comando_ativacao}")
        print(f"Para acessar o diretório do projeto, execute: cd {os.getcwd()}")
        print("Para iniciar o shell Python, execute: python -m idlelib.idle")

    def _get_comando_ativacao(self):
        """
        Retorna o comando para ativar o ambiente virtual, dependendo do sistema operacional.

        :return: Comando para ativar o ambiente virtual.
        """
        if os.name == "nt":  # Windows
            return f"{self.nome_env}\\Scripts\\activate"
        elif os.name == "posix":  # macOS/Linux
            return f"source {self.nome_env}/bin/activate"
        return ""

if __name__ == "__main__":
    # Exemplo de uso da classe AmbienteVirtual
    ambiente = AmbienteVirtual()
    ambiente.cria_ambiente_virtual()

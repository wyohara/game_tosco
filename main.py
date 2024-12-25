import os
import venv
import subprocess

class AmbienteVirtual:

    def __init__(self, nome_env="venv", requirements_txt="req.txt"):    
        """
        Cria o ambiente virtual e carrega as dependências de um txt de requerimentos

        Parameters:
        nome_env (string, opcional): o nome do ambiente virtual. O padrão é 'venv'
        requirements_txt (string, opcional): o nome do arquivo de requerimentos do pip a ser usado. O padrão é 'req.txt'

        Methods:
        ambiente_existe: Verifica se já existe um ambiente virtual.
        cria_ambiente_virtual: Cria o ambiente virtual.
        salvar_requirements: Salva o  requeriments do arquivo pip
        exibir_instrucoes: Exibe as instruções sobre o uso do ambiente virtual
        """
        self.nome_env = nome_env
        self.requirements_txt = requirements_txt

    def ambiente_existe(self):
        """
        Verifica se o ambiente virtual já existe.

        Return: 
        Boolean: True se existir um ambiente virtual e False se não existir.

        """
        return os.path.exists(self.nome_env)

    def cria_ambiente_virtual(self, instrucoes=True):
        """
        Cria um ambiente virtual e instala as dependências especificadas.

        Parameters:
        instrucoes (boolean, opcional): caso True mostra a instrução. Padrão é True
        """
        if self.ambiente_existe():
            print(f"O ambiente virtual '{self.nome_env}' já existe.")
        else:
            self._criar_ambiente()
        
        self._instalar_dependencias()
        if instrucoes: self.exibir_instrucoes()

    def salvar_requirements(self):
        """
        Executa o comando pip freeze e salva as dependências no arquivo requirements.txt.
        """
        with open(self.requirements_txt, 'w') as req_file:
            subprocess.run(['pip', 'freeze'], stdout=req_file)
            print(f"Dependências salvas em '{self.requirements_txt}'.")


    def _criar_ambiente(self):
        """Cria o ambiente virtual com pip integrado."""
        try:
            venv.create(self.nome_env, with_pip=True)
            print(f"Ambiente virtual '{self.nome_env}' criado com sucesso!")
        except Exception as e:
            print(f"Erro ao criar o ambiente virtual: {e}")

    def _instalar_dependencias(self):
        """Instala as dependências especificadas no arquivo requirements.txt."""
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
        
        """
        if os.name == "nt":  # Windows
            return os.path.join(self.nome_env, "Scripts", "pip")
        elif os.name == "posix":  # macOS/Linux
            return os.path.join(self.nome_env, "bin", "pip")
        return None


    def exibir_instrucoes(self):
        """Exibe instruções para ativar o ambiente virtual."""
        comando_ativacao = self._get_comando_ativacao()
        print(f"Para ativar o ambiente virtual, execute: {comando_ativacao}")
        print(f"Para acessar o diretório do arquivo, execute: cd {os.getcwd()}")
        print("Para iniciar o shell, execute: python -m idlelib.idle")

    def _get_comando_ativacao(self):
        """Retorna o comando para ativar o ambiente virtual dependendo do sistema operacional."""
        if os.name == "nt":  # Windows
            return f"{self.nome_env}\\Scripts\\activate"
        elif os.name == "posix":  # macOS/Linux
            return f"source {self.nome_env}/bin/activate"
        return ""

if __name__ == "__main__":
    ambiente = AmbienteVirtual()
    ambiente.cria_ambiente_virtual()

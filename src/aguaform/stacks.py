from cdktf import TerraformStack
from constructs import Construct
from cdktf_cdktf_provider_docker.provider import DockerProvider
from cdktf_cdktf_provider_docker.container import Container
from cdktf_cdktf_provider_docker.image import Image


class BaseTerraformStack(TerraformStack):
    """Classe base para todos os stacks do Terraform"""
    
    def __init__(self, scope: Construct, id: str, name: str, provider: str, 
                 nginx_image: str, internal_port: int, external_port: int):
        super().__init__(scope, id)
        
        self.name = name
        self.provider = provider
        self.nginx_image = nginx_image
        self.internal_port = internal_port
        self.external_port = external_port
        
        self._setup_provider()
        self._create_resources()
    
    def _setup_provider(self):
        """Configura o provider baseado na seleção"""
        if self.provider == "docker":
            self.docker_provider = DockerProvider(self, "docker")
        elif self.provider == "aws":
            # Placeholder para AWS provider - pode ser implementado futuramente
            pass
    
    def _create_resources(self):
        """Cria os recursos base do Terraform"""
        if self.provider == "docker":
            # Criar imagem Docker
            self.docker_image = Image(self, f"{self.name}_image",
                name=self.nginx_image,
                keep_locally=False
            )
            
            # Criar container Docker
            self.docker_container = Container(self, f"{self.name}_container",
                name=f"{self.name}_container",
                image=self.docker_image.image_id,
                ports=[{
                    "internal": self.internal_port,
                    "external": self.external_port
                }]
            )


class Api(BaseTerraformStack):
    """Stack para aplicação do tipo API"""
    
    def __init__(self, scope: Construct, id: str, name: str, provider: str, 
                 nginx_image: str, internal_port: int, external_port: int):
        super().__init__(scope, id, name, provider, nginx_image, internal_port, external_port)
        self._configure_api_specific()
    
    def _configure_api_specific(self):
        """Configurações específicas para API"""
        if hasattr(self, 'docker_container'):
            # Adicionar configurações específicas para API
            self.docker_container.env = ["API_MODE=true"]


class Worker(BaseTerraformStack):
    """Stack para aplicação do tipo Worker"""
    
    def __init__(self, scope: Construct, id: str, name: str, provider: str, 
                 nginx_image: str, internal_port: int, external_port: int):
        super().__init__(scope, id, name, provider, nginx_image, internal_port, external_port)
        self._configure_worker_specific()
    
    def _configure_worker_specific(self):
        """Configurações específicas para Worker"""
        if hasattr(self, 'docker_container'):
            # Adicionar configurações específicas para Worker
            self.docker_container.env = ["WORKER_MODE=true"]


class Service(BaseTerraformStack):
    """Stack para aplicação do tipo Service"""
    
    def __init__(self, scope: Construct, id: str, name: str, provider: str, 
                 nginx_image: str, internal_port: int, external_port: int):
        super().__init__(scope, id, name, provider, nginx_image, internal_port, external_port)
        self._configure_service_specific()
    
    def _configure_service_specific(self):
        """Configurações específicas para Service"""
        if hasattr(self, 'docker_container'):
            # Adicionar configurações específicas para Service
            self.docker_container.env = ["SERVICE_MODE=true"]


# Mapeamento das classes por tipo de aplicação
STACK_CLASSES = {
    "api": Api,
    "worker": Worker,
    "service": Service
} 
import sys
import os
import tempfile
import subprocess
import gradio as gr
from cdktf import App

from .stacks import STACK_CLASSES


def deploy_terraform_stack(name: str, provider: str, nginx_image: str, 
                          internal_port: int, external_port: int, 
                          application: str) -> str:
    """
    Executa o deploy do stack Terraform baseado nos parâmetros do formulário
    """
    try:
        # Validar parâmetros
        if not name.strip():
            return "❌ Erro: Nome não pode estar vazio"
        
        if application not in STACK_CLASSES:
            return f"❌ Erro: Tipo de aplicação '{application}' não suportado"
        
        # Criar diretório temporário para o deploy
        with tempfile.TemporaryDirectory() as temp_dir:
        
            # Criar aplicação CDKTF
            app = App(outdir=temp_dir)
            
            # Selecionar e instanciar a classe do stack apropriada
            stack_class = STACK_CLASSES[application]
            stack = stack_class(
                app, 
                f"{name}_{application}_stack",
                name=name,
                provider=provider,
                nginx_image=nginx_image,
                internal_port=internal_port,
                external_port=external_port
            )
        
            # Gerar o código Terraform
            app.synth()
            
            # Executar terraform init e apply
            terraform_dir = os.path.join(temp_dir, "stacks", f"{name}_{application}_stack")
            
            if os.path.exists(terraform_dir):
                # Inicializar Terraform
                init_result = subprocess.run(
                    ["terraform", "init"],
                    cwd=terraform_dir,
                    capture_output=True,
                    text=True
                )
                
                if init_result.returncode != 0:
                    return f"❌ Erro no terraform init:\n{init_result.stderr}"
                
                # Aplicar configuração
                apply_result = subprocess.run(
                    ["terraform", "apply", "-auto-approve"],
                    cwd=terraform_dir,
                    capture_output=True,
                    text=True
                )
                
                if apply_result.returncode != 0:
                    return f"❌ Erro no terraform apply:\n{apply_result.stderr}"
                
                return f"✅ Deploy realizado com sucesso!\n\n" \
                       f"📋 Detalhes:\n" \
                       f"• Nome: {name}\n" \
                       f"• Provider: {provider}\n" \
                       f"• Imagem: {nginx_image}\n" \
                       f"• Porta interna: {internal_port}\n" \
                       f"• Porta externa: {external_port}\n" \
                       f"• Tipo: {application}\n\n" \
                       f"🔧 Saída do Terraform:\n{apply_result.stdout}"
            else:
                return f"❌ Erro: Diretório do Terraform não encontrado em {terraform_dir}"
                
    except Exception as e:
        return f"❌ Erro durante o deploy: {str(e)}"


def create_gradio_interface():
    """
    Cria a interface Gradio para o formulário de deploy
    """
    with gr.Blocks(
        title="AguaForm - Terraform Stack Deploy",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 800px !important;
            margin: 0 auto !important;
        }
        """
    ) as demo:
        gr.HTML("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1>🌊 AguaForm</h1>
            <h2>Terraform Stack Deploy</h2>
            <p>Configure e execute o deploy dos seus containers com facilidade</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column():
                name_input = gr.Textbox(
                    label="Nome",
                    placeholder="Digite o nome do seu projeto",
                    value=""
                )
                
                provider_select = gr.Dropdown(
                    label="Provider",
                    choices=["docker", "aws"],
                    value="docker"
                )
                
                nginx_image_input = gr.Textbox(
                    label="Nginx Image",
                    value="nginx:latest",
                    placeholder="nginx:latest"
                )
                
            with gr.Column():
                internal_port_input = gr.Number(
                    label="Porta Interna",
                    value=80,
                    precision=0
                )
                
                external_port_input = gr.Number(
                    label="Porta Externa",
                    value=8080,
                    precision=0
                )
                
                application_select = gr.Dropdown(
                    label="Aplicação",
                    choices=["api", "worker", "service"],
                    value="api"
                )
        
        with gr.Row():
            run_button = gr.Button(
                "🚀 Executar Deploy",
                variant="primary",
                size="lg",
                scale=2
            )
        
        with gr.Row():
            output_text = gr.Textbox(
                label="Resultado do Deploy",
                lines=15,
                max_lines=20,
                interactive=False,
                show_copy_button=True
            )
        
        # Conectar o botão à função de deploy
        run_button.click(
            fn=deploy_terraform_stack,
            inputs=[
                name_input,
                provider_select,
                nginx_image_input,
                internal_port_input,
                external_port_input,
                application_select
            ],
            outputs=output_text,
            show_progress=True
        )
        
        gr.HTML("""
        <div style="text-align: center; margin-top: 30px; color: #666;">
            <p>Desenvolvido com ❤️ usando Gradio e CDKTF</p>
        </div>
        """)
    
    return demo


def main() -> None:
    """
    Função principal que inicia a aplicação
    """
    # Verificar argumentos da linha de comando
    if len(sys.argv) != 3:
        print("❌ Uso: aguaform <host> <porta>")
        print("   Exemplo: aguaform 0.0.0.0 8080")
        sys.exit(1)
    
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
    except ValueError:
        print("❌ Erro: A porta deve ser um número inteiro")
        sys.exit(1)
    
    # Verificar se o Terraform está instalado
    try:
        subprocess.run(["terraform", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Aviso: Terraform não encontrado. Certifique-se de que está instalado e no PATH")
        print("   Visite: https://www.terraform.io/downloads.html")
    
    print(f"🌊 Iniciando AguaForm em http://{host}:{port}")
    print("🚀 Acesse o endereço acima no seu navegador para usar a interface")
    
    # Criar e iniciar a interface Gradio
    demo = create_gradio_interface()
    demo.launch(
        server_name=host,
        server_port=port,
        share=False,
        show_error=True,
        quiet=False
    )

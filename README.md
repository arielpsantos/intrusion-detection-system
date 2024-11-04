# intrusion-detection-system

# Simple Intrusion Detection System (IDS) - SYN Flood Detection

Este projeto implementa um sistema básico de detecção de intrusão (IDS) para identificar e bloquear ataques de SYN flood. Ele utiliza `iptables` para bloquear IPs que excedem um limite de pacotes SYN, caracterizando um possível ataque.

## Objetivo

Detectar ataques de SYN flood e bloquear automaticamente o IP de origem do ataque em um ambiente de sandbox.

## Pré-requisitos

- **Python 3.x**
- **Permissões de root** (para manipulação de `iptables` e captura de pacotes raw)
- **Bibliotecas Python**: `socket`, `os`, `struct`, `time`
- **Ambiente de Teste**: Dois computadores ou máquinas virtuais Linux:
  - **Máquina Alvo**: Ubuntu Server
  - **Máquina Atacante**: Ubuntu Desktop (usada para gerar pacotes SYN com `nmap`)

## Estrutura do Projeto

- `ids.py`: Script Python principal que detecta o ataque e executa o bloqueio de IP.
- `syn_flood_log.txt`: Arquivo de log onde são registrados os IPs bloqueados e o horário de cada ataque detectado.

## Funcionalidades

1. **Captura de Pacotes**: O script escuta por pacotes IPv4 usando um socket raw, verifica pacotes TCP e identifica aqueles com o flag SYN ativo.
2. **Detecção de SYN Flood**: Monitora a frequência de pacotes SYN de um mesmo IP. Quando um IP ultrapassa o limite de pacotes (`SYN_THRESHOLD`), é considerado um ataque.
3. **Bloqueio de IP**: Adiciona uma regra no `iptables` para bloquear o IP atacante.
4. **Log**: Registra a detecção e o bloqueio do IP em um arquivo de log (`syn_flood_log.txt`).

## Configuração e Execução

### 1. Preparação do Ambiente

- Certifique-se de que o Python 3.x está instalado na máquina alvo.
- Dê permissão de root para o script:
  ```bash
  sudo chmod +x ids.py
### 3. Na máquina alvo, execute o script:
sudo python3 ids.py

### 4. sudo python3 ids.py
Na máquina atacante, use o Nmap para simular um ataque SYN flood:

sudo nmap -p 80 --syn <IP_da_máquina_alvo>

## Testes e Validação
O script detectará o ataque, registrará o evento no log (syn_flood_log.txt) e bloqueará o IP atacante automaticamente.
